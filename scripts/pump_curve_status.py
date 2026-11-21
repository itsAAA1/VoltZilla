#!/usr/bin/env python3
"""Read-only: state of the Pump.fun bonding curve for the GDY mint.

Finds the curve account (owner of the largest GDY token account, owned by
the Pump.fun program), decodes its reserves and computes how much SOL of
net buys is still needed for the curve to complete (graduate to PumpSwap).
No wallet, no signing, no transactions.
"""
import argparse, base64, json, struct, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

MINT = "GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump"
PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
LAMPORTS = 10**9
TOKEN_DECIMALS = 6


def rpc(url, method, params, retries=4):
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
            time.sleep(2 ** attempt)


def decode_curve(raw: bytes):
    """Anchor BondingCurve: 8-byte discriminator, 5 x u64, bool complete."""
    if len(raw) < 49:
        raise ValueError(f"curve account too short: {len(raw)} bytes")
    vt, vs, rt, rs, supply = struct.unpack_from("<5Q", raw, 8)
    return {"virtual_token_reserves": vt, "virtual_sol_reserves": vs,
            "real_token_reserves": rt, "real_sol_reserves": rs,
            "token_total_supply": supply, "complete": bool(raw[48])}


def sol_to_complete(curve):
    """Net SOL (lamports) that buys every remaining real token on the constant-product curve, before fees."""
    vt, vs, rt = curve["virtual_token_reserves"], curve["virtual_sol_reserves"], curve["real_token_reserves"]
    if curve["complete"] or rt == 0:
        return 0
    if rt >= vt:
        raise ValueError("real token reserves must be below virtual token reserves")
    return -(-vs * rt // (vt - rt))  # ceil division


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
        "spot_price_sol_per_token": price_lamports_per_token * 10**TOKEN_DECIMALS / LAMPORTS,
        "raw": curve,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rpc", default=DEFAULT_RPC)
    args = ap.parse_args()
    call = lambda m, p: rpc(args.rpc, m, p)
    largest = call("getTokenLargestAccounts", [MINT, {"commitment": "finalized"}])["value"][0]["address"]
    acct = call("getAccountInfo", [largest, {"encoding": "jsonParsed"}])["value"]
    curve_address = acct["data"]["parsed"]["info"]["owner"]
    info = call("getAccountInfo", [curve_address, {"encoding": "base64"}])["value"]
    if info is None or info["owner"] != PUMP_PROGRAM:
        sys.exit(f"curve account {curve_address} is not owned by the Pump.fun program")
    out = summarize(decode_curve(base64.b64decode(info["data"][0])), curve_address)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
