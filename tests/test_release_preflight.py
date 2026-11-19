"""Offline release preflight tests; never requires wallet access/network."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preflight", ROOT / "scripts" / "release_preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class ReleasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "project-manifest.json").read_text(encoding="utf-8"))

    def test_manifest_is_valid_but_release_is_blocked(self):
        self.assertEqual(preflight.validate(self.data), [])
        status = preflight.readiness(self.data)
        self.assertFalse(status["ready_for_public_release"])
        self.assertIn("owner_identity_not_verified", status["missing"])

    def test_candidate_address_is_not_a_seed(self):
        for candidate in self.data["candidates"]:
            self.assertEqual(len(preflight.decode_pubkey(candidate["mint"])), 32)

    def test_different_mints_cannot_be_merged(self):
        mints = [c["mint"] for c in self.data["candidates"]]
        self.assertEqual(len(set(mints)), 3)
        self.assertEqual({c["decimals"] for c in self.data["candidates"]}, {6, 9})

    def test_creator_linked_pumpfun_mint_kept_separate(self):
        primary = next(c for c in self.data["candidates"] if c["id"] == "pumpfun_creator_linked_primary")
        self.assertEqual(primary["mint"], self.data["preferred_mint_candidate"])
        self.assertEqual(primary["creator_wallet"], "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD")
        self.assertEqual(primary["token_program"], "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb")
        self.assertFalse(primary["pumpfun_curve_complete"])
        self.assertIsNone(self.data["official_mint"])

    def test_unknown_preferred_mint_is_rejected(self):
        self.data["preferred_mint_candidate"] = "11111111111111111111111111111111"
        self.assertTrue(any("Preferred mint" in e for e in preflight.validate(self.data)))

    def test_fake_mint_is_rejected(self):
        self.data["official_mint"] = "not-a-solana-address"
        self.assertTrue(any("Official mint" in msg for msg in preflight.validate(self.data)))

    def test_unknown_official_mint_is_rejected(self):
        self.data["official_mint"] = "11111111111111111111111111111111"
        self.assertTrue(any("Official mint" in msg for msg in preflight.validate(self.data)))

    def test_duplicate_candidate_is_rejected(self):
        self.data["candidates"][1]["mint"] = self.data["candidates"][0]["mint"]
        self.assertIn("Duplicate candidate mint", preflight.validate(self.data))

    def test_secret_field_is_rejected(self):
        self.data["private_key"] = "dummy"
        self.assertTrue(any("secret-bearing" in e for e in preflight.validate(self.data)))


if __name__ == "__main__":
    unittest.main()
