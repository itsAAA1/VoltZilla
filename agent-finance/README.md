# VoltZilla — Agent Finance Core (tested prototype)

Status: PRE-FLIGHT ENGINE + REAL READ-ONLY SOLANA RPC CALLS. NOT A LIVE MONEY SENDER.

## What actually works
- solana_snapshot.py reads a specific mint using Solana RPC getAccountInfo + getTokenSupply, checks active mint authority, decimals and current amount needed to reach 7,000,000 VZLA.
- treasury.py performs strict intent validation and atomic SQLite reservations under recipient whitelist, per-transaction and daily spending caps, expiration and idempotency rules.
- Tests were executed locally on 2026-11-20: 11/11 passed. The live RPC attempt in this assistant environment failed because DNS was blocked. A separate connected Nova/Helius read confirmed the DHx supply remains 1,000,000 and its mint authority is 28fU8... at 09:38 UTC.
- A transaction is NEVER sent by these scripts. No wallet key is imported. The example policy blocks all execution by default. Even a reserved intent is NOT a confirmed transfer.

## Run locally

  cd agent-finance
  python -m unittest discover -s tests -v
  python solana_snapshot.py --mint DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9

The second command needs real network access; public Solana RPC is rate-limited, so a production service requires its own reliable provider.

## Transition to actual autonomous spending (NOT YET CONNECTED)
1. Set up an **independent** operational wallet with an approved signing provider such as Turnkey. Keep treasury funds outside the AI process.
2. Enforce recipient, amount, token, program, and time policies **in Turnkey at signing**, independent of this editable local Python preflight.
3. Connect an approved Solana transaction-building SDK or payment API; parse and simulate the COMPLETE transaction before signing. Do not let a language model transmit arbitrary opaque signed instructions.
4. Verify the blockchain transaction independently before marking it completed; implement durable audit logs, wallet alerts, retries and kill switch.
5. For a Saudi shop/company, separate merchant PSP collections (Tap/Moyasar through approved merchant agreements) from crypto custody and trading; check Saudi laws and provider eligibility.

## 7-million VZLA status
The owner-reported DHx mint had 1,000,000 VZLA and 9 decimals, with active authority 28fU8.... The theoretical additional mint to reach 7m is 6,000,000 VZLA (6,000,000,000,000,000 raw units), **only if** the owner proves controlling that wallet and explicitly approves that mint. It is NOT the separate GDY Pump.fun mint, whose mint authority has been revoked. None of these scripts mint tokens or authorize issuance.

Full owner review: https://github.com/itsAAA1/VoltZilla/blob/main/docs/SEVEN_MILLION_SUPPLY_EXECUTION_PLAN_2026-11-20.md
Turnkey signing guidance: https://www.turnkey.com/blog/introducing-solana-policy-engine
Solana wallet signing guidance: https://solana.com/docs/tools/keychain/choosing-a-backend

## Risk and truthfulness
- Production funds and customer balances must remain under licensed provider and genuine wallet custody controls.
- No independent security audit, Saudi financial regulatory licence, Turnkey onboarding, deployed agent server, bank connectivity, funded operational wallet or signed live transaction is claimed.
- The code is a verifiable functional starting component, not an autopilot business with guaranteed profits.
