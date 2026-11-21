"""Offline tests for the read-only mint provenance walker (no network)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mint_provenance as mp


def fake_rpc(pages, payer):
    calls = {"sig": 0}

    def call(method, params):
        if method == "getSignaturesForAddress":
            i = calls["sig"]
            calls["sig"] += 1
            return pages[i] if i < len(pages) else []
        if method == "getTransaction":
            return {"transaction": {"message": {"accountKeys": [{"pubkey": payer}, {"pubkey": "x"}]}}}
        raise AssertionError(method)
    return call


class ProvenanceTests(unittest.TestCase):
    def test_short_history_reads_creation_payer(self):
        page = [{"signature": "new", "blockTime": 1780000000},
                {"signature": "old", "blockTime": 1775308301}]
        call = fake_rpc([page], "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD")
        out = mp.inspect(call, "pumpfun_creator_linked_primary", mp.MINTS["pumpfun_creator_linked_primary"])
        self.assertEqual(out["first_signature"], "old")
        self.assertTrue(out["history_complete"])
        self.assertTrue(out["creator_matches_expected"])
        self.assertTrue(out["creator_linked_to_owner_wallets"])
        self.assertTrue(out["first_seen_utc"].startswith("2026-04-04"))

    def test_mismatch_is_flagged(self):
        page = [{"signature": "only", "blockTime": 1730000000}]
        call = fake_rpc([page], "SomeOtherWallet1111111111111111111111111111")
        out = mp.inspect(call, "owner_reported", mp.MINTS["owner_reported"])
        self.assertFalse(out["creator_matches_expected"])
        self.assertFalse(out["creator_linked_to_owner_wallets"])

    def test_unlinked_historical_has_no_expectation(self):
        page = [{"signature": "only", "blockTime": 1730000000}]
        call = fake_rpc([page], "SomeOtherWallet1111111111111111111111111111")
        out = mp.inspect(call, "historical_document", mp.MINTS["historical_document"])
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
