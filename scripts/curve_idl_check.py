#!/usr/bin/env python3
"""Read-only diagnostic: GDY creator-fee vault and fee flows in the curve's transactions."""
import sys
sys.path.insert(0, "scripts")
from pump_curve_status import rpc, find_program_address, b58decode, PUMP_PROGRAM

RPC = "https://api.mainnet-beta.solana.com"
CURVE = "6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk"
CREATOR = "GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD"
call = lambda m, p: rpc(RPC, m, p)

vault, _ = find_program_address([b"creator-vault", b58decode(CREATOR)], PUMP_PROGRAM)
info = call("getAccountInfo", [vault, {"encoding": "base64"}])["value"]
print("CREATOR_VAULT", vault, "lamports", info["lamports"] if info else None, "owner", info["owner"] if info else None)
vsigs = call("getSignaturesForAddress", [vault, {"limit": 1000}])
print("VAULT_TX_COUNT", len(vsigs))

sigs = call("getSignaturesForAddress", [CURVE, {"limit": 1000}])
tot_vault = 0
for s in reversed(sigs):
    tx = call("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
    pre, post = tx["meta"]["preBalances"], tx["meta"]["postBalances"]
    d = lambda a: (post[keys.index(a)] - pre[keys.index(a)]) if a in keys else None
    signer = keys[0]
    logs = " ".join(l for l in (tx["meta"]["logMessages"] or []) if "Instruction:" in l)
    dv = d(vault)
    tot_vault += dv or 0
    print("TX", s["signature"][:12], "signer", signer[:6], "curve_d", d(CURVE), "vault_d", dv, "creator_d", d(CREATOR), "|", logs[:160])
print("VAULT_DELTA_SUM_IN_CURVE_TXS", tot_vault)
for s in vsigs[:10]:
    tx = call("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    logs = " ".join(l for l in (tx["meta"]["logMessages"] or []) if "Instruction:" in l)
    print("VAULT_TX", s["signature"][:12], s.get("blockTime"), "|", logs[:160])
