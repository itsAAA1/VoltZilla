#!/usr/bin/env python3
"""Read-only diagnostic: decode the GDY bonding-curve account with the official Pump IDL."""
import base64, json, sys, urllib.request
sys.path.insert(0, "scripts")
from pump_curve_status import rpc, b58encode

RPC = "https://api.mainnet-beta.solana.com"
CURVE = "6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk"
IDL_URLS = ["https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json",
            "https://raw.githubusercontent.com/pump-fun/pump-public-docs/master/idl/pump.json"]
idl = None
for u in IDL_URLS:
    try:
        idl = json.loads(urllib.request.urlopen(u, timeout=30).read()); print("IDL", u); break
    except Exception as e:
        print("IDL_ERR", u, repr(e))
types = {t["name"]: t for t in idl.get("types", [])}
bc = types["BondingCurve"]["type"]["fields"]
print("IDL_FIELDS", json.dumps(bc))
raw = base64.b64decode(rpc(RPC, "getAccountInfo", [CURVE, {"encoding": "base64"}])["value"]["data"][0])
print("ACCOUNT_LEN", len(raw))
o = 8
sizes = {"u64": 8, "u32": 4, "u16": 2, "u8": 1, "bool": 1, "pubkey": 32, "publicKey": 32, "i64": 8}
for f in bc:
    t = f["type"]
    if isinstance(t, str) and t in sizes:
        n = sizes[t]; c = raw[o:o+n]
        v = b58encode(c) if n == 32 else (bool(c[0]) if t == "bool" and c else int.from_bytes(c, "little"))
        print("FIELD", f["name"], t, v); o += n
    else:
        print("FIELD_COMPLEX", f["name"], json.dumps(t)); break
print("REST_HEX", raw[o:].hex())
