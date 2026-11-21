#!/usr/bin/env python3
"""Read-only: who can change GDY's name/symbol/URI/socials, and what the metadata JSON says."""
import base64, json, struct, sys, urllib.request
sys.path.insert(0, "scripts")
from pump_curve_status import rpc, find_program_address, b58decode, b58encode, MINT

RPC = "https://api.mainnet-beta.solana.com"
METAPLEX = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
call = lambda m, p: rpc(RPC, m, p)

mint = call("getAccountInfo", [MINT, {"encoding": "jsonParsed"}])["value"]
info = mint["data"]["parsed"]["info"]
print("token_program_owner", mint["owner"])
print("mint_authority", info.get("mintAuthority"), "freeze_authority", info.get("freezeAuthority"))
for ext in info.get("extensions", []):
    print("EXT", json.dumps(ext))

uri = None
for ext in info.get("extensions", []):
    if ext.get("extension") == "tokenMetadata":
        uri = ext["state"].get("uri")

pda, _ = find_program_address([b"metadata", b58decode(METAPLEX), b58decode(MINT)], METAPLEX)
acc = call("getAccountInfo", [pda, {"encoding": "base64"}])["value"]
print("metaplex_pda", pda, "exists", acc is not None)
if acc:
    d = base64.b64decode(acc["data"][0]); o = 1
    ua = b58encode(d[o:o+32]); o += 64
    def s():
        global o
        n = struct.unpack_from("<I", d, o)[0]; o += 4; v = d[o:o+n].rstrip(b"\0").decode(); o += n; return v
    name, sym, u = s(), s(), s(); o += 2
    if d[o]: n = struct.unpack_from("<I", d, o+1)[0]; o += 5 + 34*n
    else: o += 1
    print("metaplex update_authority", ua, "name", name, "symbol", sym, "uri", u,
          "primary_sale", d[o], "is_mutable", d[o+1])
    uri = uri or u

if uri:
    try:
        req = urllib.request.Request(uri, headers={"User-Agent": "voltzilla-meta/1"})
        print("URI_JSON", urllib.request.urlopen(req, timeout=30).read()[:3000].decode(errors="replace"))
    except Exception as e:
        print("URI_FETCH_ERROR", repr(e))

CURVE = "6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk"
sigs = call("getSignaturesForAddress", [CURVE, {"limit": 1000}])
from datetime import datetime, timezone
print("curve_tx_count", len(sigs))
for s in sigs[:5] + sigs[-3:]:
    print("SIG", s["signature"][:16], datetime.fromtimestamp(s["blockTime"], timezone.utc).isoformat() if s.get("blockTime") else None, "err" if s.get("err") else "ok")
cid = uri.rsplit("/", 1)[-1] if uri else None
for gw in ("https://pump.mypinata.cloud/ipfs/", "https://gateway.pinata.cloud/ipfs/", "https://dweb.link/ipfs/"):
    try:
        req = urllib.request.Request(gw + cid, headers={"User-Agent": "Mozilla/5.0"})
        print("URI_JSON", gw, urllib.request.urlopen(req, timeout=30).read()[:3000].decode(errors="replace")); break
    except Exception as e:
        print("URI_FETCH_ERROR", gw, repr(e))
