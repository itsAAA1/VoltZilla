#!/usr/bin/env python3
"""Fail-closed, offline VoltZilla release readiness preflight.

Usage:
  python3 scripts/release_preflight.py --check     # validates manifest, exit 0 for well-formed file
  python3 scripts/release_preflight.py --release   # exit 2 until every evidenced release gate is satisfied
  python3 scripts/release_preflight.py             # print neutral status JSON

This script never connects to a wallet, signs a transaction or changes the chain.
Boolean gate fields are owner-provided attestations, not independently verified evidence.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "project-manifest.json"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
REQUIRED_GATES = (
    "owner_signed_identity_proof", "official_mint_approved",
    "tokenomics_and_allocation_verified", "authority_policy_approved",
    "trading_pair_and_liquidity_verified", "independent_security_review",
    "legal_and_marketing_review", "public_site_verified",
    "support_and_incident_runbook_ready",
)


def decode_pubkey(address):
    if not isinstance(address, str) or not 32 <= len(address) <= 44:
        raise ValueError("Solana address format invalid")
    n = 0
    for ch in address:
        if ch not in ALPHABET:
            raise ValueError("Solana address has invalid base58 character")
        n = 58 * n + ALPHABET.index(ch)
    prefix = len(address) - len(address.lstrip("1"))
    data = bytes(prefix) + (n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b"")
    if len(data) != 32:
        raise ValueError("Solana public address must encode 32 bytes")
    return data


def validate(manifest):
    issues = []
    def fail(message):
        issues.append(message)
    if not isinstance(manifest, dict):
        return ["Manifest root must be an object"]
    if manifest.get("schema_version") != 1:
        fail("Unsupported schema version")
    project = manifest.get("project")
    if not isinstance(project, dict) or project.get("network") != "solana-mainnet" or project.get("symbol") != "VZLA":
        fail("Project identity or network mismatched")
    if isinstance(project, dict) and project.get("confirmed_social_x") != "https://x.com/voltzillasol1":
        fail("Official account must match owner-confirmed source")
    candidates = manifest.get("candidates")
    ids, addresses = set(), set()
    if not isinstance(candidates, list) or len(candidates) != 4:
        fail("Four separate candidate mints (including creator-linked Pump.fun and Raydium mints) must be preserved until reconciliation")
        candidates = []
    for i, c in enumerate(candidates):
        if not isinstance(c, dict):
            fail(f"Candidate {i} must be an object")
            continue
        if not isinstance(c.get("id"), str) or c["id"] in ids:
            fail(f"Candidate {i} has missing or duplicate id")
        else:
            ids.add(c["id"])
        try:
            decode_pubkey(c.get("mint"))
            if c["mint"] in addresses:
                fail("Duplicate candidate mint")
            addresses.add(c["mint"])
            if c.get("mint_authority") is not None:
                decode_pubkey(c["mint_authority"])
            if c.get("freeze_authority") is not None:
                decode_pubkey(c["freeze_authority"])
        except ValueError as e:
            fail(f"Candidate {i}: {e}")
        if type(c.get("decimals")) is not int or not 0 <= c["decimals"] <= 18:
            fail(f"Candidate {i}: decimals out of range")
        try:
            if Decimal(c.get("observed_supply")) < 0:
                fail(f"Candidate {i}: supply cannot be negative")
        except (InvalidOperation, TypeError):
            fail(f"Candidate {i}: observed supply invalid")
        try:
            observed = dt.datetime.fromisoformat(c["observed_at_utc"].replace("Z", "+00:00"))
            if observed.tzinfo is None:
                fail(f"Candidate {i}: timestamp needs timezone")
        except (ValueError, TypeError, KeyError):
            fail(f"Candidate {i}: invalid observed timestamp")
    preferred = manifest.get("preferred_mint_candidate")
    if preferred is not None:
        try:
            decode_pubkey(preferred)
            if preferred not in addresses:
                fail("Preferred mint must match an inspected candidate")
        except ValueError as e:
            fail(f"Preferred mint: {e}")
    if not any(
        isinstance(c, dict) and
        c.get("id") == "pumpfun_creator_linked_primary" and
        c.get("mint") == preferred and
        c.get("creator_wallet") == "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD"
        for c in candidates
    ):
        fail("Creator-linked primary Pump.fun mint evidence mismatch")
    official = manifest.get("official_mint")
    if official is not None:
        try:
            decode_pubkey(official)
            if official not in addresses:
                fail("Official mint must match an inspected candidate")
        except ValueError as e:
            fail(f"Official mint: {e}")
    if type(manifest.get("owner_identity_verified")) is not bool:
        fail("Owner identity flag must be bool")
    gates = manifest.get("release_gates")
    if not isinstance(gates, dict):
        fail("Release gates must be an object")
    else:
        for g in REQUIRED_GATES:
            if type(gates.get(g)) is not bool:
                fail(f"Release gate {g} must be bool")
        if set(gates) != set(REQUIRED_GATES):
            fail("Unexpected or missing release gate keys")
    forbidden = ("seed_phrase", "recovery_phrase", "private_key", "secret_key", "mnemonic", "wallet_password")
    serialized = json.dumps(manifest, ensure_ascii=False).lower()
    for key in forbidden:
        if f'"{key}"' in serialized:
            fail("Manifest must not store secret-bearing fields")
    return issues


def readiness(manifest):
    gates = manifest["release_gates"]
    missing = [g for g in REQUIRED_GATES if gates[g] is not True]
    if manifest["official_mint"] is None:
        missing.insert(0, "official_mint_not_selected")
    if manifest["owner_identity_verified"] is not True:
        missing.insert(0, "owner_identity_not_verified")
    return {"ready_for_public_release": not missing, "missing": missing,
            "note": "Flags alone are insufficient: independently review supporting original evidence before release."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--release", action="store_true")
    args = p.parse_args(argv)
    try:
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 1
    issues = validate(m)
    if issues:
        print(json.dumps({"valid": False, "errors": issues}, ensure_ascii=False, indent=2))
        return 1
    result = {"valid": True, **readiness(m)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.release and not result["ready_for_public_release"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
