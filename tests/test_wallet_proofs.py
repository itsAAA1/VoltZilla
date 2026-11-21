"""Signed wallet-control proofs must verify offline and must not carry secrets."""
import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_wallet_proof as v  # noqa: E402

PROOF = ROOT / "proofs" / "2026-11-21_28fU8_wallet-control.json"


class WalletProofs(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(PROOF.read_text(encoding="utf-8"))

    def test_28fu8_proof_verifies(self):
        self.assertEqual(v.check(self.record), [])
        self.assertEqual(self.record["wallet"], "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4")
        self.assertIn("Matches expected wallet: true", self.record["message_lines"])
        self.assertIn("Proof of wallet control only; NOT a transaction or spending authorization",
                      " ".join(self.record["message_lines"]))

    def test_tampered_message_fails(self):
        bad = copy.deepcopy(self.record)
        bad["message_lines"][3] = bad["message_lines"][3].replace("DHx", "GDY")
        bad["message_sha256"] = __import__("hashlib").sha256("\n".join(bad["message_lines"]).encode()).hexdigest()
        self.assertTrue(any("does NOT verify" in p for p in v.check(bad)))

    def test_other_wallet_fails(self):
        bad = copy.deepcopy(self.record)
        bad["wallet"] = "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD"
        self.assertTrue(v.check(bad))

    def test_no_secret_fields(self):
        text = PROOF.read_text(encoding="utf-8").lower()
        for word in ("private_key", "secret_key", "seed", "mnemonic", "recovery_phrase"):
            self.assertNotIn(word, text)

    def test_all_proof_files_valid(self):
        self.assertEqual(v.main([]), 0)


if __name__ == "__main__":
    unittest.main()
