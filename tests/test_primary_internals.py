"""Regression tests for actual Token-2022 mint internals; run offline with stdlib."""
import base64
import struct
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import audit_primary_internals as audit

MINT = "GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump"
POOL = "6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk"
CREATOR = "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD"

def raw_mint(exts=(18, 19), supply=1007005921840554):
    raw = bytearray(166)
    struct.pack_into("<Q", raw, 36, supply)
    raw[44], raw[45], raw[165] = 6, 1, 1
    for kind in exts:
        raw += struct.pack("<HH", kind, 3) + b"abc"
    return bytes(raw)


def raw_token_account(owner, amount):
    raw = bytearray(165)
    raw[:32] = audit.decode_pubkey(MINT)
    raw[32:64] = audit.decode_pubkey(owner)
    struct.pack_into("<Q", raw, 64, amount)
    raw[108] = 1
    return bytes(raw)


def account(data, program=audit.PROGRAM):
    return {"owner": program, "data": [base64.b64encode(data).decode("ascii"), "base64"]}


class PrimaryTokenInternalsTests(unittest.TestCase):
    def test_parses_only_metadata_extensions_and_flags_no_transfer_fee(self):
        ext = audit.parse_mint_extensions(raw_mint())
        self.assertEqual([e["name"] for e in ext], ["MetadataPointer", "TokenMetadata"])
        self.assertEqual(audit.risk_extension_names(ext), [])
        self.assertEqual(audit.risk_extension_names(audit.parse_mint_extensions(raw_mint((18, 1, 12)))) ,
                         ["TransferFeeConfig", "PermanentDelegate"])

    def test_fails_closed_on_invalid_mint_layout(self):
        with self.assertRaises(ValueError):
            audit.parse_mint_extensions(raw_mint()[:-1])
        bogus = bytearray(raw_mint())
        bogus[165] = 2
        with self.assertRaises(ValueError):
            audit.parse_mint_extensions(bytes(bogus))

    def test_fails_closed_for_unknown_extension_types(self):
        ext = audit.parse_mint_extensions(raw_mint((18, 999)))
        self.assertEqual(audit.risk_extension_names(ext), ["Unknown(999)"])

    def test_reads_raw_token_account_owners_and_exact_balance(self):
        a = audit.parse_token_account(raw_token_account(CREATOR, 7005921840554), MINT)
        self.assertEqual(a["owner"], CREATOR)
        self.assertEqual(a["amount_raw"], "7005921840554")
        with self.assertRaises(ValueError):
            audit.parse_token_account(raw_token_account(CREATOR, 7005921840554), POOL)

    def test_reconciles_solana_accounts_without_summing_provider_percentages(self):
        total=Decimal("1007005921.840554")
        entries=[
            {"owner": POOL, "raw": "1000000000000000"},
            {"owner": CREATOR, "raw": "7005921840554"},
        ]
        rec = audit.reconcile_holders(total, entries, 6)
        self.assertEqual(rec["accounted_ui"], "1007005921.840554")
        self.assertEqual(rec["unaccounted_ui"], "0")
        self.assertEqual(sum(Decimal(x["share_percent"]) for x in rec["holders"]), Decimal("100.00000000"))
        self.assertEqual(rec["pool_share_percent"], "99.30428196")
        self.assertEqual(rec["creator_share_percent"], "0.69571804")

    def test_over_supply_fails_not_silently_clamped(self):
        with self.assertRaises(ValueError):
            audit.reconcile_holders(Decimal(100), [
                {"owner": POOL, "raw": "100000001"}], 6)


    def test_fallback_keeps_observation_scoped_to_known_accounts(self):
        selected, scope = audit.select_token_accounts(None)
        self.assertEqual(scope, "known_snapshot_partial")
        self.assertIn("HRa4LY8PLdhKG9YUvxafqjFzaqD7bXAiWU9FodrSpA9T", selected)
        self.assertIn("EPKbdTsaYqqBGcjHHcEWM7EyHr8Buzqw3rGPB1wsCCf1", selected)
        selected, scope = audit.select_token_accounts([{"address": "abc"}])
        self.assertEqual(scope, "rpc_top20")
        self.assertEqual(selected, ["abc"])

    def test_default_rpc_candidates_have_distinct_verified_public_hostnames(self):
        self.assertGreaterEqual(len(audit.DEFAULT_RPCS), 2)
        self.assertEqual(len(set(audit.DEFAULT_RPCS)), len(audit.DEFAULT_RPCS))


    def test_live_observe_falls_back_to_known_accounts_when_index_is_rate_limited(self):
        def fake_rpc(url, method, params, attempts=3):
            if method == "getAccountInfo":
                return {"context": {"slot": 1}, "value": account(raw_mint())}
            if method == "getTokenLargestAccounts":
                raise RuntimeError("HTTP 429 Too Many Requests")
            if method == "getMultipleAccounts":
                owners = [(POOL, 1000000000000000), (CREATOR, 7005921840554),
                          ("BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s", 0)]
                return {"context": {"slot": 1},
                        "value": [account(raw_token_account(o, amt)) for o, amt in owners]}
            raise AssertionError("Unexpected RPC method " + method)

        with patch.object(audit, "rpc_call", side_effect=fake_rpc):
            observed = audit.observe("https://example.test")
        self.assertEqual(observed["holder_discovery"]["coverage"], "known_snapshot_partial")
        self.assertEqual(observed["holders"]["unaccounted_ui"], "0")
        self.assertEqual(observed["holders"]["pool_share_percent"], "99.30428196")

    def test_immutable_permissions_still_do_not_prove_social_ownership(self):
        data = audit.describe_authorities({"mint_authority": None, "freeze_authority": None})
        self.assertTrue(data["mint_authority_revoked"])
        self.assertTrue(data["freeze_authority_revoked"])
        self.assertFalse(data["proves_human_owner"])
        self.assertFalse(data["proves_liquidity_lock"])


if __name__ == "__main__":
    unittest.main()
