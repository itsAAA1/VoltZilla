#!/usr/bin/env python3
"""Read-only SPL Token mint inspector for two documented VoltZilla candidates.

This tool reads on-chain account data; it never signs a transaction or claims
that either candidate belongs to the project owner.

Usage:
  python3 scripts/inspect_mints.py
  python3 scripts/inspect_mints.py --check
  python3 scripts/inspect_mints.py --rpc https://your-public-rpc.example
"""
import argparse
import base64
import json
import struct
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal

TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
MINTS = {
    "owner_reported": "DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9",
    "historical_document": "JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump",
}
EXPECTED = {
    "owner_reported": {
        "decimals": 9,
        "mint_authority": "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4",
        "freeze_authority": None,
    },
    "historical_document": {
        "decimals": 6,
        "mint_authority": None,
        "freeze_authority": None,
    },
}


def b58encode(raw: bytes) -> str:
    value = int.from_bytes(raw, "big")
    output = ""
    while value:
        value, idx = divmod(value, 58)
        output = ALPHABET[idx] + output
    prefix = len(raw) - len(raw.lstrip(bytes([0])))
    return "1" * prefix + output


def decode_coption_pubkey(data: bytes, offset: int):
    present = struct.unpack_from("<I", data, offset)[0]
    if present not in (0, 1):
        raise ValueError("invalid Solana COption pubkey tag")
    return b58encode(data[offset + 4:offset + 36]) if present else None


def parse_mint(raw: bytes) -> dict:
    if len(raw) != 82:
        raise ValueError(f"expected 82-byte standard SPL mint; got {len(raw)}")
    if raw[45] != 1:
        raise ValueError("mint account is not initialized")
    supply_raw = struct.unpack_from("<Q", raw, 36)[0]
    decimals = raw[44]
    return {
        "supply_raw": str(supply_raw),
        "supply_ui": str(Decimal(supply_raw) / Decimal(10 ** decimals)),
        "decimals": decimals,
        "mint_authority": decode_coption_pubkey(raw, 0),
        "freeze_authority": decode_coption_pubkey(raw, 46),
    }


def get_account(rpc_url: str, mint: str) -> dict:
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "getAccountInfo",
        "params": [mint, {"encoding": "base64", "commitment": "finalized"}],
    }).encode("utf-8")
    req = urllib.request.Request(
        rpc_url, payload,
        {"Content-Type": "application/json", "User-Agent": "VoltZilla-readonly-inspector/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        info = json.load(response)
    if "error" in info:
        raise ValueError(f"RPC error: {info['error']}")
    data = info.get("result") or {}
    account = data.get("value")
    if not account:
        raise ValueError(f"mint not found: {mint}")
    if account.get("owner") != TOKEN_PROGRAM:
        raise ValueError(f"unsupported token program: {account.get('owner')}")
    encoded = account.get("data")
    if not isinstance(encoded, list) or len(encoded) < 2 or encoded[1] != "base64":
        raise ValueError("unexpected RPC account encoding")
    result = parse_mint(base64.b64decode(encoded[0], validate=True))
    result.update({"mint": mint, "program": account["owner"],
                   "slot": data.get("context", {}).get("slot")})
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rpc", default="https://api.mainnet-beta.solana.com",
                        help="public Solana JSON-RPC endpoint; never include private credentials")
    parser.add_argument("--check", action="store_true",
                        help="fail if the authority or decimals changed since 2026-11-05")
    args = parser.parse_args(argv)
    report = {
        "network": "solana-mainnet",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "official_mint": None,
        "notes": "Candidate labels are documentation only; a wallet signature is needed to prove ownership.",
        "mints": {}, "changes": [],
    }
    for label, mint in MINTS.items():
        try:
            result = get_account(args.rpc, mint)
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"Could not verify {label}: {exc}", file=sys.stderr)
            return 2
        report["mints"][label] = result
        for field, expected in EXPECTED[label].items():
            if result[field] != expected:
                report["changes"].append({
                    "candidate": label, "field": field,
                    "previous": expected, "current": result[field],
                })
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.check and report["changes"]:
        print("On-chain controls changed; review original transactions before editing published facts.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
