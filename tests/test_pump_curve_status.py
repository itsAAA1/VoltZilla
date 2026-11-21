import struct, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pump_curve_status as pc


def raw(vt, vs, rt, rs, supply, complete=0):
    return b"\x17" * 8 + struct.pack("<5Q", vt, vs, rt, rs, supply) + bytes([complete]) + b"\0" * 32


class PumpCurveTests(unittest.TestCase):
    def test_fresh_curve_needs_about_85_sol(self):
        # Standard Pump.fun start: 1,073,000,000 virtual tokens, 30 virtual SOL, 793,100,000 real tokens.
        c = pc.decode_curve(raw(1_073_000_000 * 10**6, 30 * 10**9, 793_100_000 * 10**6, 0, 10**15))
        need = pc.sol_to_complete(c) / 10**9
        self.assertAlmostEqual(need, 85.0, delta=0.1)

    def test_complete_curve_needs_nothing(self):
        c = pc.decode_curve(raw(279_900_000 * 10**6, 115 * 10**9, 0, 85 * 10**9, 10**15, 1))
        self.assertEqual(pc.sol_to_complete(c), 0)

    def test_creator_and_mayhem_flag_decoded(self):
        creator = pc.b58decode("GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD")
        data = b"\x17" * 8 + struct.pack("<5Q", 1, 1, 0, 0, 1) + b"\0" + creator + b"\x01\x01"
        c = pc.decode_curve(data)
        self.assertEqual(c["creator"], "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD")
        self.assertTrue(c["is_mayhem_mode"])
        self.assertTrue(c["is_cashback_coin"])

    def test_fee_gross_up(self):
        net = 10**9
        self.assertAlmostEqual(pc.gross_spend(net) / 10**9, 1.0125)
        self.assertAlmostEqual(pc.gross_spend(net, 45) / 10**9, 1.0125 / 0.9955)

    def test_short_account_rejected(self):
        with self.assertRaises(ValueError):
            pc.decode_curve(b"\0" * 20)

    def test_pda_is_off_curve_and_deterministic(self):
        addr, bump = pc.find_program_address([b"bonding-curve", pc.b58decode(pc.MINT)], pc.PUMP_PROGRAM)
        self.assertEqual(addr, pc.find_program_address([b"bonding-curve", pc.b58decode(pc.MINT)], pc.PUMP_PROGRAM)[0])
        self.assertFalse(pc.on_ed25519_curve(pc.b58decode(addr)))
        # A real wallet public key is on the curve.
        self.assertTrue(pc.on_ed25519_curve(pc.b58decode("GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD")))

    def test_no_signing_code(self):
        src = (Path(pc.__file__)).read_text()
        for word in ("sign(", "Keypair", "private", "sendTransaction"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
