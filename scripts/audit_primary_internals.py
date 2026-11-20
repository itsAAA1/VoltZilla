#!/usr/bin/env python3
"""Read-only, fail-closed audit of the actual creator-matched Pump.fun Token-2022 mint.

No wallet access. Inspects canonical mint bytes and top SPL token accounts via
Solana JSON-RPC, rather than trusting explorer percentages or promotional copy.

Usage:
  python3 scripts/audit_primary_internals.py --check > primary-internals.json
  python3 scripts/audit_primary_internals.py --rpc https://your-public-rpc
"""
import argparse
import base64
import json
import struct
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN

from inspect_mints import TOKEN_2022_PROGRAM as PROGRAM, b58encode, parse_mint
from release_preflight import decode_pubkey

MINT = "GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump"
POOL = "6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk"
CREATOR = "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD"
EXPECTED_SUPPLY_RAW = "1007005921840554"
EXPECTED_EXTENSIONS = {"MetadataPointer", "TokenMetadata"}
# Only a FALLBACK sample of the three token accounts observed in the dated
# canonical safety snapshot, NOT an exhaustive live token-account index.
KNOWN_ACCOUNTS = (
    "HRa4LY8PLdhKG9YUvxafqjFzaqD7bXAiWU9FodrSpA9T",
    "EPKbdTsaYqqBGcjHHcEWM7EyHr8Buzqw3rGPB1wsCCf1",
    "HCK1BeLUUnB7pbveuG2jmf4u1r4TpAKE1QQmt4M1wcUJ",
)
# Public endpoint list, selected only after failing the preceding provider.
DEFAULT_RPCS = (
    "https://solana-rpc.publicnode.com",
    "https://public-solana-mainnet.rpcnode.dev",
    "https://api.mainnet-beta.solana.com",
)

# Solana Token-2022 ExtensionType values, not a whitelist of safe extensions.
# Unknown future extensions fail closed in the strict on-chain check.
EXTENSIONS = {
    1: "TransferFeeConfig", 2: "TransferFeeAmount", 3: "MintCloseAuthority",
    4: "ConfidentialTransferMint", 5: "ConfidentialTransferAccount",
    6: "DefaultAccountState", 7: "ImmutableOwner", 8: "MemoTransfer",
    9: "NonTransferable", 10: "InterestBearingConfig", 11: "CpiGuard",
    12: "PermanentDelegate", 13: "NonTransferableAccount", 14: "TransferHook",
    15: "TransferHookAccount", 16: "ConfidentialTransferFeeConfig",
    17: "ConfidentialTransferFeeAmount", 18: "MetadataPointer",
    19: "TokenMetadata", 20: "GroupPointer", 21: "TokenGroup",
    22: "GroupMemberPointer", 23: "TokenGroupMember",
    24: "ConfidentialMintBurn", 25: "ScaledUiAmountConfig",
    26: "PausableConfig", 27: "PausableAccount",
}


def parse_mint_extensions(raw):
    """Read binary TLV mint extensions after 82-byte base + 83 pad + type byte."""
    if len(raw) == 82:
        return []
    if len(raw) < 166:
        raise ValueError("truncated Token-2022 extended mint")
    if raw[165] != 1:
        raise ValueError("incorrect Token-2022 account type (expected mint=1)")
    if any(raw[82:165]):
        raise ValueError("unexpected nonzero padding before extension area")
    pos, entries, seen = 166, [], set()
    while pos < len(raw):
        if len(raw) - pos < 4:
            if any(raw[pos:]):
                raise ValueError("truncated Token-2022 extension header")
            break
        tag, length = struct.unpack_from("<HH", raw, pos)
        pos += 4
        if tag == 0 and length == 0:
            if any(raw[pos:]):
                raise ValueError("nonzero data after TLV terminator")
            break
        if tag == 0 or tag in seen:
            raise ValueError("invalid or duplicate Token-2022 extension type")
        if length > len(raw) - pos:
            raise ValueError("truncated Token-2022 extension payload")
        seen.add(tag)
        entries.append({
            "type": tag,
            "name": EXTENSIONS.get(tag, f"Unknown({tag})"),
            "byte_length": length,
        })
        pos += length
    return entries


def risk_extension_names(extensions):
    """Conservative: only the two observed metadata extension kinds are allowed."""
    return [e["name"] for e in extensions if e["name"] not in EXPECTED_EXTENSIONS]


def parse_token_account(raw, expected_mint):
    if len(raw) < 165:
        raise ValueError("truncated SPL Token account")
    onchain_mint = b58encode(raw[:32])
    if onchain_mint != expected_mint:
        raise ValueError(f"token account has wrong mint {onchain_mint}")
    if raw[108] != 1:
        raise ValueError("token account is not initialized")
    return {
        "owner": b58encode(raw[32:64]),
        "amount_raw": str(struct.unpack_from("<Q", raw, 64)[0]),
    }


def select_token_accounts(largest):
    """Use provider-discovered top-20 when possible, else labelled partial sample."""
    if largest is None:
        return list(KNOWN_ACCOUNTS), "known_snapshot_partial"
    if not isinstance(largest, list):
        raise ValueError("unexpected largest token account response type")
    return [entry["address"] for entry in largest], "rpc_top20"


def describe_authorities(state):
    return {
        "mint_authority_revoked": state["mint_authority"] is None,
        "freeze_authority_revoked": state["freeze_authority"] is None,
        "proves_human_owner": False,
        "proves_liquidity_lock": False,
    }


def reconcile_holders(supply_ui, accounts, decimals):
    """Use exact raw balances and canonical total mint supply, never provider %."""
    supply_ui = Decimal(str(supply_ui))
    unit = Decimal(10) ** decimals
    raw_supply = supply_ui * unit
    if raw_supply != raw_supply.to_integral_value() or raw_supply < 0:
        raise ValueError("non-integral or negative mint supply")
    amount_sum = 0
    holders = []
    seen = set()
    for entry in accounts:
        raw = int(entry["raw"])
        owner = entry["owner"]
        if raw < 0:
            raise ValueError("negative token account balance")
        if entry.get("token_account") in seen and entry.get("token_account") is not None:
            raise ValueError("duplicate token account")
        if entry.get("token_account") is not None:
            seen.add(entry["token_account"])
        amount_sum += raw
        share = (Decimal(raw) / raw_supply * 100) if raw_supply else Decimal(0)
        pct = f"{share.quantize(Decimal('0.00000001'), rounding=ROUND_HALF_EVEN):.8f}"
        holders.append({
            "token_account": entry.get("token_account"),
            "owner": owner,
            "amount_ui": str(Decimal(raw) / unit),
            "share_percent": pct,
            "category": "pumpfun_curve" if owner == POOL else ("creator_wallet" if owner == CREATOR else "other"),
        })
    if amount_sum > raw_supply:
        raise ValueError("top token accounts exceed canonical minted supply (RPC slot mismatch or bad data)")
    by_owner = lambda key: sum(int(e["raw"]) for e in accounts if e["owner"] == key)
    pct_owner = lambda key: f"{((Decimal(by_owner(key)) / raw_supply * 100) if raw_supply else Decimal(0)).quantize(Decimal('0.00000001'), rounding=ROUND_HALF_EVEN):.8f}"
    return {
        "supply_ui": str(supply_ui),
        "accounted_ui": str(Decimal(amount_sum) / unit),
        "unaccounted_ui": "0" if raw_supply == amount_sum else str((raw_supply - amount_sum) / unit),
        "pool_share_percent": pct_owner(POOL),
        "creator_share_percent": pct_owner(CREATOR),
        "holders": holders,
        "meaning": "Share of currently issued on-chain supply, not holders' circulating-float allocation. Curve inventory is not creator treasury.",
    }


def rpc_call(url, method, params, attempts=3):
    body = json.dumps({"jsonrpc": "2.0", "id": 1,
                       "method": method, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        url, body, headers={"Content-Type": "application/json",
                            "User-Agent": "VoltZilla-internals-readonly/1.0"}, method="POST")
    last_error = None
    for n in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=22) as resp:
                data = json.load(resp)
            if "error" in data:
                raise ValueError(f"Solana RPC {method}: {data['error']}")
            if "result" not in data:
                raise ValueError(f"Solana RPC {method}: no result")
            return data["result"]
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in (429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
        if n < attempts-1:
            time.sleep(1 + n)
    raise RuntimeError(f"Solana RPC {method} request failed after {attempts} attempts: {last_error}")


def decode_rpc_bytes(value):
    if value is None:
        raise ValueError("missing Solana account data")
    data = value.get("data")
    if not isinstance(data, list) or len(data) != 2 or data[1] != "base64":
        raise ValueError("RPC did not return base64 data")
    return base64.b64decode(data[0], validate=True)


def observe(rpc_url):
    mint_info = rpc_call(rpc_url, "getAccountInfo",
                         [MINT, {"encoding": "base64", "commitment": "finalized"}])
    mint_account = mint_info.get("value")
    if not mint_account or mint_account.get("owner") != PROGRAM:
        raise ValueError("primary mint missing or wrong Token-2022 program")
    raw_mint = decode_rpc_bytes(mint_account)
    mint = parse_mint(raw_mint)
    extension_list = parse_mint_extensions(raw_mint)
    if mint["decimals"] != 6:
        raise ValueError("unexpected primary mint decimal precision")
    if mint["mint_authority"] is not None or mint["freeze_authority"] is not None:
        raise ValueError("unexpected active mint or freeze authority")
    # Some free public Solana endpoints rate-limit this expensive index method.
    # Canonical balance and account ownership are still verifiable via read-only
    # getMultipleAccounts on *known* account addresses; label partial coverage.
    largest, summary, largest_error = None, None, None
    try:
        largest = rpc_call(rpc_url, "getTokenLargestAccounts",
                           [MINT, {"commitment": "finalized"}], attempts=2)
        summary = largest.get("value")
    except (ValueError, RuntimeError, urllib.error.URLError, OSError) as exc:
        largest_error = type(exc).__name__ + ": " + str(exc)[:180]
    addrs, account_scope = select_token_accounts(summary)
    if len(set(addrs)) != len(addrs):
        raise ValueError("duplicate largest-token-account address")
    owner_lookup = rpc_call(rpc_url, "getMultipleAccounts",
                            [addrs, {"encoding": "base64", "commitment": "finalized"}]) if addrs else {"value": []}
    values = owner_lookup.get("value")
    if not isinstance(values, list) or len(values) != len(addrs):
        raise ValueError("getMultipleAccounts incomplete result")
    parsed = []
    reported_rows = summary if summary is not None else [None] * len(addrs)
    for label, reported, acct in zip(addrs, reported_rows, values):
        if not acct or acct.get("owner") != PROGRAM:
            raise ValueError(f"missing or invalid token account {label}")
        details = parse_token_account(decode_rpc_bytes(acct), MINT)
        # Distinct finalized RPC calls may observe different slots; flag instead
        # of silently inventing a reconciled quantity.
        if summary is not None and details["amount_raw"] != str(reported["amount"]):
            raise ValueError("RPC returned differing token amounts across sampled slots")
        parsed.append({**details, "raw": details["amount_raw"], "token_account": label})
    alloc = reconcile_holders(Decimal(mint["supply_ui"]), parsed, mint["decimals"])
    flags = {
        "unexpected_extensions": risk_extension_names(extension_list),
        "extension_set_changed": {e["name"] for e in extension_list} != EXPECTED_EXTENSIONS,
        "supply_changed_since_baseline": mint["supply_raw"] != EXPECTED_SUPPLY_RAW,
        "top_account_balance_unaccounted": alloc["unaccounted_ui"] != "0",
    }
    return {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "network": "solana-mainnet",
        "mint": MINT,
        "program": PROGRAM,
        "source": "direct read-only Solana JSON-RPC (finalized)",
        "slots": {
            "mint": mint_info.get("context", {}).get("slot"),
            "largest": largest.get("context", {}).get("slot") if largest else None,
            "owners": owner_lookup.get("context", {}).get("slot"),
        },
        "mint_state": mint,
        "authorities": describe_authorities(mint),
        "extensions": extension_list,
        "holders": alloc,
        "holder_discovery": {"coverage": account_scope,
                             "largest_account_rpc_error": largest_error,
                             "note": "Top 20 is not a holder census. When known_snapshot_partial, no live discovery of other token accounts was possible."},
        "review_flags": flags,
        "mayhem_cashback_note": "Mayhem/cashback settings are Pump.fun program account state; this mint-level RPC scan does not independently parse agent parameters or trade execution.",
        "ownership_note": "Creator wallet is on-chain provenance, but no human owner signature was requested or produced.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rpc", action="append", default=[],
                        help="may be specified more than once; otherwise try public RPC fallback list")
    parser.add_argument("--check", action="store_true", help="fail if current internals differ from documented review baseline")
    args = parser.parse_args(argv)
    report, errors = None, []
    for url in (args.rpc or DEFAULT_RPCS):
        try:
            report = observe(url)
            report["rpc_endpoint"] = url
            break
        except (ValueError, RuntimeError, urllib.error.URLError, OSError) as exc:
            errors.append({"endpoint": url, "error": str(exc)[:260]})
            print(f"RPC endpoint unavailable or inconsistent ({url}): {exc}", file=sys.stderr)
    if report is None:
        print(json.dumps({"verified": False, "errors": errors}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    flags = report["review_flags"]
    if args.check and any(flags.values()):
        print("PRIMARY AUDIT: manual review required due to extension, authority or supply changes", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
