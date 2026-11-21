#!/usr/bin/env python3
"""Read-only: state of the Pump.fun bonding curve for the GDY mint.

Derives the curve account (PDA ["bonding-curve", mint] of the Pump.fun
program, checked on-chain to be owned by that program), decodes its reserves and computes how much SOL of
net buys is still needed for the curve to complete (graduate to PumpSwap).
No wallet, no signing, no transactions.
"""
import argparse, base64, hashlib, json, struct, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

MINT = "GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump"
PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
LAMPORTS = 10**9
TOKEN_DECIMALS = 6


B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode(text):
    n = 0
    for ch in text:
        n = n * 58 + B58.index(ch)
    return n.to_bytes(32, "big")


def b58encode(raw):
    n, out = int.from_bytes(raw, "big"), ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(raw) - len(raw.lstrip(b"\0"))) + out


_P = 2**255 - 19
_D = (-121665 * pow(121666, _P - 2, _P)) % _P


def on_ed25519_curve(point):
    """True if 32 bytes decode to a point on edwards25519 (PDAs must be off-curve)."""
    y = int.from_bytes(point, "little") & ((1 << 255) - 1)
    sign = point[31] >> 7
    if y >= _P:
        return False
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return sign == 0
    x = pow(x2, (_P + 3) // 8, _P)
    if x * x % _P != x2:
        x = x * pow(2, (_P - 1) // 4, _P) % _P
    return x * x % _P == x2


def find_program_address(seeds, program_id):
    program = b58decode(program_id)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + program + b"ProgramDerivedAddress").digest()
        if not on_ed25519_curve(h):
            return b58encode(h), bump
    raise ValueError("no PDA found")


def rpc(url, method, params, retries=6):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, body, {"Content-Type": "application/json", "User-Agent": "voltzilla-curve/1"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            if "error" in data:
                raise RuntimeError(data["error"])
            return data["result"]
        except (urllib.error.URLError, ValueError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(min(2 ** (attempt + 1), 30))


def decode_curve(raw: bytes):
    """Anchor BondingCurve: 8-byte discriminator, 5 x u64, bool complete."""
    if len(raw) < 49:
        raise ValueError(f"curve account too short: {len(raw)} bytes")
    vt, vs, rt, rs, supply = struct.unpack_from("<5Q", raw, 8)
    out = {"virtual_token_reserves": vt, "virtual_sol_reserves": vs,
           "real_token_reserves": rt, "real_sol_reserves": rs,
           "token_total_supply": supply, "complete": bool(raw[48]),
           "account_len": len(raw)}
    if len(raw) >= 81:
        out["creator"] = b58encode(raw[49:81])
    if len(raw) >= 82:
        out["is_mayhem_mode"] = bool(raw[81])
    if len(raw) >= 83:
        # Official IDL (pump-fun/pump-public-docs): on a cashback coin the 0.30% creator fee
        # is credited to the buyer when the interface uses the cashback instructions.
        out["is_cashback_coin"] = bool(raw[82])
    return out


def sol_to_complete(curve):
    """Net SOL (lamports) that buys every remaining real token on the constant-product curve, before fees."""
    vt, vs, rt = curve["virtual_token_reserves"], curve["virtual_sol_reserves"], curve["real_token_reserves"]
    if curve["complete"] or rt == 0:
        return 0
    if rt >= vt:
        raise ValueError("real token reserves must be below virtual token reserves")
    return -(-vs * rt // (vt - rt))  # ceil division


CURVE_FEE_BPS = 125       # 0.95% protocol + 0.30% creator, charged on top of the SOL entering the curve
APP_FEE_BPS = 45          # pump.fun web/mobile Platform Fee since 17 Oct 2026, deducted from the amount spent
APP_FEE_REFERRAL_BPS = 40


def gross_spend(net_lamports, app_fee_bps=0):
    """SOL a buyer spends so that `net_lamports` enter the curve."""
    with_curve_fee = net_lamports * (10_000 + CURVE_FEE_BPS) / 10_000
    return with_curve_fee / (1 - app_fee_bps / 10_000)


def summarize(curve, curve_address):
    need = sol_to_complete(curve)
    price_lamports_per_token = curve["virtual_sol_reserves"] / curve["virtual_token_reserves"]
    return {
        "checked_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mint": MINT,
        "curve_account": curve_address,
        "complete": curve["complete"],
        "real_sol_in_curve": curve["real_sol_reserves"] / LAMPORTS,
        "real_tokens_left_on_curve": curve["real_token_reserves"] / 10**TOKEN_DECIMALS,
        "net_sol_to_complete_before_fees": need / LAMPORTS,
        "total_real_sol_at_completion": (curve["real_sol_reserves"] + need) / LAMPORTS,
        "spend_with_curve_fee": gross_spend(need) / LAMPORTS,
        "spend_via_pumpfun_app": gross_spend(need, APP_FEE_BPS) / LAMPORTS,
        "spend_via_pumpfun_app_with_referral": gross_spend(need, APP_FEE_REFERRAL_BPS) / LAMPORTS,
        "spot_price_sol_per_token": price_lamports_per_token * 10**TOKEN_DECIMALS / LAMPORTS,
        "raw": curve,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rpc", default=DEFAULT_RPC)
    args = ap.parse_args()
    call = lambda m, p: rpc(args.rpc, m, p)
    curve_address, _ = find_program_address([b"bonding-curve", b58decode(MINT)], PUMP_PROGRAM)
    info = call("getAccountInfo", [curve_address, {"encoding": "base64"}])["value"]
    if info is None or info["owner"] != PUMP_PROGRAM:
        sys.exit(f"curve account {curve_address} is not owned by the Pump.fun program")
    out = summarize(decode_curve(base64.b64decode(info["data"][0])), curve_address)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
