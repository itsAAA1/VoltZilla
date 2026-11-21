#!/usr/bin/env python3
"""Read-only provenance check for the four documented VZLA mints.

For each mint it walks getSignaturesForAddress back to the oldest signature,
then reads that first transaction to record who paid for it (the fee payer,
i.e. the deploying wallet) and when it happened. It also records the newest
activity, so a change in a token's on-chain life shows up in the report.

It never signs anything, never sends a transaction and never uses a private
key. A fee payer proves which wallet deployed a mint, not which human controls
that wallet today; ownership still needs a separate signed message.

Usage:
  python3 scripts/mint_provenance.py
  python3 scripts/mint_provenance.py --check      # exit 1 on a creator mismatch
  python3 scripts/mint_provenance.py --rpc https://your-public-rpc.example
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

MINTS = {
    "pumpfun_creator_linked_primary": "GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump",
    "raydium_launchlab_creator_linked": "3cPWF3eKjcq4Y8d2oVXDRaN8ipKBHuyK1uYWY4GT7ray",
    "owner_reported": "DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9",
    "historical_document": "JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump",
}

# Deployers already documented in docs/FOUR_MINT_RECONCILIATION_2026-11-20.md.
# None means "not linked to the owner; record whatever the chain says".
EXPECTED_CREATOR = {
    "pumpfun_creator_linked_primary": "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD",
    "raydium_launchlab_creator_linked": "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4",
    "owner_reported": "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4",
    "historical_document": None,
}

OWNER_LINKED_WALLETS = {
    "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD",
    "28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4",
    "71HwwRcQKiptoR5juRa4DqJqxbonEQqAK7dRGTXpHErs",
}

PAGE = 1000
MAX_PAGES = 40


def rpc(url, method, params, retries=4):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, body, {"Content-Type": "application/json",
                                                 "User-Agent": "voltzilla-provenance/1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            if "error" in data:
                raise ValueError(f"RPC error: {data['error']}")
            return data["result"]
        except (urllib.error.URLError, ValueError, TimeoutError) as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{method} failed after {retries} tries: {last}")


def iso(ts):
    return None if ts is None else datetime.fromtimestamp(ts, timezone.utc).isoformat()


def walk_signatures(call, mint):
    """Return (newest, oldest, count, complete) by paging back in time."""
    before = None
    newest = oldest = None
    count = 0
    for _ in range(MAX_PAGES):
        opts = {"limit": PAGE}
        if before:
            opts["before"] = before
        page = call("getSignaturesForAddress", [mint, opts])
        if not page:
            return newest, oldest, count, True
        if newest is None:
            newest = page[0]
        oldest = page[-1]
        count += len(page)
        if len(page) < PAGE:
            return newest, oldest, count, True
        before = page[-1]["signature"]
    return newest, oldest, count, False


def fee_payer(tx):
    keys = tx["transaction"]["message"]["accountKeys"]
    first = keys[0]
    return first["pubkey"] if isinstance(first, dict) else first


def inspect(call, label, mint):
    newest, oldest, count, complete = walk_signatures(call, mint)
    out = {
        "label": label,
        "mint": mint,
        "signatures_seen": count,
        "history_complete": complete,
        "latest_activity_utc": iso(newest.get("blockTime")) if newest else None,
    }
    if not oldest:
        out["error"] = "no signatures returned"
        return out
    out["first_signature"] = oldest["signature"]
    out["first_seen_utc"] = iso(oldest.get("blockTime"))
    if not complete:
        out["note"] = "history longer than the page cap; first_signature is not the creation tx"
        return out
    tx = call("getTransaction", [oldest["signature"], {"encoding": "jsonParsed",
                                                         "maxSupportedTransactionVersion": 0}])
    if tx:
        payer = fee_payer(tx)
        out["creator_fee_payer"] = payer
        out["creator_linked_to_owner_wallets"] = payer in OWNER_LINKED_WALLETS
        expected = EXPECTED_CREATOR.get(label)
        out["expected_creator"] = expected
        out["creator_matches_expected"] = None if expected is None else payer == expected
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rpc", default="https://api.mainnet-beta.solana.com",
                        help="public Solana JSON-RPC endpoint; never include private credentials")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if a documented creator does not match the chain")
    args = parser.parse_args()

    def call(method, params):
        return rpc(args.rpc, method, params)

    report = {"observed_at_utc": datetime.now(timezone.utc).isoformat(),
              "rpc": args.rpc, "read_only": True, "mints": []}
    failed = False
    for label, mint in MINTS.items():
        try:
            item = inspect(call, label, mint)
        except Exception as exc:  # report and keep going
            item = {"label": label, "mint": mint, "error": str(exc)}
        report["mints"].append(item)
        if item.get("creator_matches_expected") is False:
            failed = True
        time.sleep(1)
    print(json.dumps(report, indent=2))
    return 1 if (args.check and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
