#!/usr/bin/env python3
"""Verify VoltZilla wallet-control proofs (Solana signMessage, Ed25519) offline.

Usage:
    python3 scripts/verify_wallet_proof.py                 # every proofs/*.json
    python3 scripts/verify_wallet_proof.py proofs/x.json   # one file

No network, no dependencies: Ed25519 verification follows the RFC 8032
reference algorithm. A proof shows that the private key of the named public
wallet signed the exact message. It is not a transaction and selects no mint.
Exit code 0 = all valid, 1 = any invalid.
"""
import base64
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

P = 2 ** 255 - 19
D = -121665 * pow(121666, P - 2, P) % P
Q = 2 ** 252 + 27742317777372353535851937790883648493
SQRT_M1 = pow(2, (P - 1) // 4, P)


def b58decode(text):
    n = 0
    for ch in text:
        i = ALPHABET.find(ch)
        if i < 0:
            raise ValueError("invalid base58 character")
        n = n * 58 + i
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(text) - len(text.lstrip("1"))
    return b"\x00" * pad + raw


def _add(a, b):
    x = (a[1] - a[0]) * (b[1] - b[0]) % P
    y = (a[1] + a[0]) * (b[1] + b[0]) % P
    c = 2 * a[3] * b[3] * D % P
    d = 2 * a[2] * b[2] % P
    e, f, g, h = y - x, d - c, d + c, y + x
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _mul(s, pt):
    acc = (0, 1, 1, 0)
    while s:
        if s & 1:
            acc = _add(acc, pt)
        pt = _add(pt, pt)
        s >>= 1
    return acc


def _equal(a, b):
    return (a[0] * b[2] - b[0] * a[2]) % P == 0 and (a[1] * b[2] - b[1] * a[2]) % P == 0


def _recover_x(y, sign):
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P)
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P:
        return None
    if (x & 1) != sign:
        x = P - x
    return x


_GY = 4 * pow(5, P - 2, P) % P
_GX = _recover_x(_GY, 0)
G = (_GX, _GY, 1, _GX * _GY % P)


def _decompress(data):
    if len(data) != 32:
        return None
    y = int.from_bytes(data, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % P)


def ed25519_verify(public, message, signature):
    if len(public) != 32 or len(signature) != 64:
        return False
    a = _decompress(public)
    r = _decompress(signature[:32])
    if a is None or r is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= Q:
        return False
    h = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % Q
    return _equal(_mul(s, G), _add(r, _mul(h, a)))


def check(record):
    """Return a list of problems; empty means the proof is valid and self-consistent."""
    problems = []
    lines = record.get("message_lines")
    if not isinstance(lines, list) or not all(isinstance(x, str) for x in lines):
        return ["message_lines must be a list of strings"]
    message = "\n".join(lines).encode("utf-8")
    wallet = record.get("wallet", "")
    if hashlib.sha256(message).hexdigest() != record.get("message_sha256"):
        problems.append("message_sha256 does not match message_lines")
    if f"Signer: {wallet}" not in lines:
        problems.append("message does not name the wallet as signer")
    for key in ("issued_utc", "expires_utc", "nonce"):
        label = {"issued_utc": "Issued UTC: ", "expires_utc": "Expires UTC: ", "nonce": "Nonce: "}[key]
        if label + str(record.get(key)) not in lines:
            problems.append(f"{key} is not the value inside the signed message")
    try:
        public = b58decode(wallet)
        signature = base64.b64decode(record.get("signature_base64", ""), validate=True)
    except (ValueError, TypeError) as exc:
        return problems + [f"decode error: {exc}"]
    if not ed25519_verify(public, message, signature):
        problems.append("Ed25519 signature does NOT verify for this wallet and message")
    return problems


def main(argv):
    paths = [pathlib.Path(a) for a in argv] or sorted((ROOT / "proofs").glob("*.json"))
    if not paths:
        print("no proof files found")
        return 1
    bad = 0
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        problems = check(record)
        status = "VALID" if not problems else "INVALID"
        print(f"{status}  {path.name}  wallet={record.get('wallet')}  issued={record.get('issued_utc')}")
        for p in problems:
            print("   -", p)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
