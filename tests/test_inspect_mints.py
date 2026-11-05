"""Offline tests for the read-only standard SPL Token mint parser."""
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from inspect_mints import b58encode, parse_mint, MINTS, EXPECTED


class InspectMintTests(unittest.TestCase):
    def build_mint(self, supply, decimals, has_mint=True, has_freeze=False):
        raw = bytearray(82)
        struct.pack_into("<I", raw, 0, 1 if has_mint else 0)
        if has_mint:
            raw[4:36] = bytes([4] * 32)
        struct.pack_into("<Q", raw, 36, supply)
        raw[44] = decimals
        raw[45] = 1
        struct.pack_into("<I", raw, 46, 1 if has_freeze else 0)
        if has_freeze:
            raw[50:82] = bytes([7] * 32)
        return bytes(raw)

    def test_decodes_supply_and_authorities(self):
        parsed = parse_mint(self.build_mint(1_000_000_000_000_000, 9))
        self.assertEqual(parsed["supply_ui"], "1000000")
        self.assertEqual(parsed["decimals"], 9)
        self.assertIsNotNone(parsed["mint_authority"])
        self.assertIsNone(parsed["freeze_authority"])

    def test_revoked_authorities(self):
        parsed = parse_mint(self.build_mint(1_234_567, 6, False, False))
        self.assertEqual(parsed["supply_ui"], "1.234567")
        self.assertIsNone(parsed["mint_authority"])
        self.assertIsNone(parsed["freeze_authority"])

    def test_b58_leading_zeros(self):
        self.assertEqual(b58encode(bytes(32)), "1" * 32)

    def test_invalid_data_rejected(self):
        with self.assertRaises(ValueError):
            parse_mint(b"too short")
        raw = bytearray(self.build_mint(0, 6))
        raw[45] = 0
        with self.assertRaises(ValueError):
            parse_mint(raw)
        raw[45] = 1
        struct.pack_into("<I", raw, 0, 2)
        with self.assertRaises(ValueError):
            parse_mint(raw)

    def test_candidate_addresses_are_distinct(self):
        self.assertNotEqual(MINTS["owner_reported"], MINTS["historical_document"])
        self.assertNotEqual(EXPECTED["owner_reported"]["decimals"],
                            EXPECTED["historical_document"]["decimals"])


if __name__ == "__main__":
    unittest.main()
