"""Offline tests for the read-only mint provenance walker (no network)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mint_provenance as mp


def creation_tx(sig, payer, mint, init=True, funder=None):
    inner = [{"program": "system", "parsed": {"type": "createAccount",
              "info": {"source": funder or payer, "newAccount": mint}}}]
    if init:
        inner.append({"program": "spl-token-2022", "parsed": {"type": "initializeMint2",
                      "info": {"mint": mint, "mintAuthority": "auth"}}})
    return {"transaction": {"message": {"accountKeys": [{"pubkey": payer, "signer": True}],
                                         "instructions": [{"programId": "pump"}]}},
            "meta": {"innerInstructions": [{"index": 0, "instructions": inner}]}}


mint_of = [None]


def fake_rpc(pages, payer, mint=None, tx=None):
    calls = {"sig": 0}
    mint_of[0] = mint

    def call(method, params):
        if method == "getSignaturesForAddress":
            i = calls["sig"]
            calls["sig"] += 1
            return pages[i] if i < len(pages) else []
        if method == "getTransaction":
            return tx if tx is not None else creation_tx(params[0], payer, mint_of[0])
        raise AssertionError(method)
    return call


class ProvenanceTests(unittest.TestCase):
    def test_short_history_reads_creation_payer(self):
        page = [{"signature": "new", "blockTime": 1780000000},
                {"signature": "old", "blockTime": 1775308301}]
        m = mp.MINTS["pumpfun_creator_linked_primary"]
        call = fake_rpc([page], "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD", m)
        out = mp.inspect(call, "pumpfun_creator_linked_primary", m)
        self.assertEqual(out["first_signature"], "old")
        self.assertTrue(out["history_complete"])
        self.assertTrue(out["creator_matches_expected"])
        self.assertTrue(out["creator_linked_to_owner_wallets"])
        self.assertTrue(out["first_seen_utc"].startswith("2026-04-04"))
        self.assertTrue(out["creation_instruction_verified"])
        self.assertEqual(out["token_program"], "spl-token-2022")
        self.assertTrue(out["funder_equals_fee_payer"])

    def test_first_tx_without_initialize_mint_is_not_accepted(self):
        m = mp.MINTS["pumpfun_creator_linked_primary"]
        page = [{"signature": "only", "blockTime": 1775308301}]
        tx = creation_tx("only", "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD", m, init=False)
        out = mp.inspect(fake_rpc([page], "x", m, tx), "pumpfun_creator_linked_primary", m)
        self.assertFalse(out["creation_instruction_verified"])
        self.assertFalse(out["creator_matches_expected"])

    def test_creator_is_the_mint_account_funder(self):
        m = mp.MINTS["owner_reported"]
        page = [{"signature": "only", "blockTime": 1750673132}]
        tx = creation_tx("only", "RelayerPayer111111111111111111111111111111", m,
                         funder="28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4")
        out = mp.inspect(fake_rpc([page], "x", m, tx), "owner_reported", m)
        self.assertEqual(out["creator"], "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4")
        self.assertFalse(out["funder_equals_fee_payer"])
        self.assertTrue(out["creator_matches_expected"])

    def test_mismatch_is_flagged(self):
        page = [{"signature": "only", "blockTime": 1730000000}]
        m = mp.MINTS["owner_reported"]
        call = fake_rpc([page], "SomeOtherWallet1111111111111111111111111111", m)
        out = mp.inspect(call, "owner_reported", m)
        self.assertFalse(out["creator_matches_expected"])
        self.assertFalse(out["creator_linked_to_owner_wallets"])

    def test_unlinked_historical_has_no_expectation(self):
        page = [{"signature": "only", "blockTime": 1730000000}]
        m = mp.MINTS["historical_document"]
        call = fake_rpc([page], "SomeOtherWallet1111111111111111111111111111", m)
        out = mp.inspect(call, "historical_document", m)
        self.assertIsNone(out["creator_matches_expected"])

    def test_capped_history_does_not_guess_creator(self):
        full = [{"signature": f"s{i}", "blockTime": 1780000000 - i} for i in range(mp.PAGE)]
        call = fake_rpc([full] * (mp.MAX_PAGES + 1), "x")
        out = mp.inspect(call, "historical_document", mp.MINTS["historical_document"])
        self.assertFalse(out["history_complete"])
        self.assertNotIn("creator_fee_payer", out)

    def test_four_mints_and_no_signing_code(self):
        self.assertEqual(len(mp.MINTS), 4)
        src = Path(mp.__file__).read_text(encoding="utf-8")
        for forbidden in ("sendTransaction", "signTransaction", "secretKey", "private_key"):
            self.assertNotIn(forbidden, src)


if __name__ == "__main__":
    unittest.main()
