# VoltZilla — wallet identity proof, supply security and incident checklist
**Date:** 20 Nov 2026. **Read-only technical review only**, not an independently signed security certificate.

## The matching creator on-chain
- Pump.fun contract `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump` was created by public wallet `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD` in transaction `2frB6tsVzkEyPuteLX35fSbcKvq16fj3UbwD5pyQnhm3Mhgbutc3FGrB64tFacggnP1dkrC37EL26hsKZKQVC23U`.
- This ties a **public Solana wallet to a token's on-chain creation**, not the wallet's current private control to a particular human owner. No off-chain signed proof has yet been received.
- Solana Token-2022 mint at latest canonical snapshot had: 6 decimals, current mint authority null, freeze authority null, token extensions `metadataPointer` and `tokenMetadata` recorded by the research source. Confirm separately any Mayhem/cashback settings and whether the holder reward logic has moved funds; a token's standard authority checks alone do not audit provider contracts.

## What a safe signature means
A wallet **message signature** authenticates a string by an Ed25519 signature. It is **not a transaction**, no SOL needs to be transferred and no approval for unlimited spending is required.

Use a human-readable, single-purpose challenge such as:
```text
VoltZilla ownership / account-control proof
Domain: https://itsaaa1.github.io
Network: Solana mainnet-beta
Project token: GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump
Expected signer: GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD
Purpose: Prove current control of the public creator wallet only; NOT a transaction or permission to transfer tokens
Nonce: [fresh independent random value]
Issued UTC: [current timestamp]
Expires UTC: [short expiry]
```
The exact signed bytes, signature (Base58/Base64 as specified), and signer public key may then be checked with Ed25519 verification, matching the expected creator wallet and the fresh nonce. The nonce and timestamps must be generated **when signing** and verified at the same time; do not copy an example as a previously accepted or still-valid proof.

**Never supply a seed phrase or private key.** If the wallet UI asks to approve spending, a token allowance, a network switch or a transaction, it is **not** the requested proof task. If the wallet software has no sign-message UI, another trusted non-custodial sign-message tool may be needed; do not install unknown dApps just to pass an audit.

## Third-party audit and security checklist
- [x] Two historical lookalikes separated from the creator-matched GDY token.
- [x] Canonical Token-2022 mint, supply, current mint/freeze authorities inspected by read-only provider.
- [x] Pump.fun creator and creation transaction independently cross-linked.
- [x] Read-only Python RPC monitor updated to parse Token-2022 extended mint data; GitHub CI and site tests observed successful.
- [ ] Independent specialist review of Token-2022 extension state and any associated Mayhem/cashback/buyback code or programs.
- [ ] Confirm the source of any supply change from nominal 1B to observed 1,007,005,921.840554 using transactions and extension program data.
- [ ] Latest signature proving current creator-wallet access.
- [ ] Official published statement linking the GDY mint to a social account controlled by the project and signed/documented verification.
- [ ] Confirm the true supply allocated to insiders, contract/curve, and operational wallets; avoid calling bonding-curve inventory developer-owned.
- [ ] Independent legal advice for proposed fundraising and public marketing; no certification available here.
- [ ] Detect lookalike sites and false DEX listings; maintain escalation contact through [GitHub Issues](https://github.com/itsAAA1/VoltZilla/issues).

## Wallet access and credential-exposure response

- A public address or on-chain creation transaction **cannot reveal a secret key**, and a read-only connection to Phantom cannot discover every separate recovery phrase imported in the past.
- If a seed phrase or private key has been copied to an untrusted environment, treat all addresses derived from that phrase/key as potentially exposed. Revoke dApp access where appropriate, but note that revoking app permissions **does not rotate a private key**.
- Restore an older wallet only with its original trusted Apple/Google sign-in, original recovery phrase, or its original per-account private key **inside the wallet application**. Creating a new account from a different phrase will not recreate the old creator address.
- For a potentially exposed wallet that still has assets, generate an entirely new wallet with independently stored recovery material and migrate legitimate holdings through owner-approved transactions after verifying the new receiving address. Check fees and supported assets; never migrate untrusted spam assets automatically.
- Never paste recovery material into GitHub, websites, chat messages, freelance marketplaces, or automated agents. A public-key match or a wallet-signature test must not be described as historical custody proof beyond its actual scope.

## Non-reversible vs safe actions
- Safe read-only: explorer lookups, checks, calculating fees, status/docs/FAQ updates.
- Requires public confirmation and exact amounts: transfers, buys, buys to move the Pump curve, LP deposits, exchange fees, wallet migrations.
- A revoked mint authority cannot simply be turned back on; do not attempt any on-chain change without understanding the token's current program and governance.

**Result:** Internal technical review identifies clear risks and support procedures, **but no independent third party has audited or certified this project**.
