# VoltZilla — Security and wallet recovery

**Status:** Prelaunch security review. No on-chain actions are performed by this repository.

## Emergency key-handling rule
Never publish, upload or paste a wallet recovery phrase, private key, keystore, OTP or wallet password into GitHub, support chat, issue templates, CI variables or API requests. A screenshot revealing such credentials should be treated as potentially exposed. If the credential is real, create a new wallet using a trusted wallet app on a controlled device, secure the recovery phrase offline, and migrate any assets and authorities while the existing key can still authorize transactions. Migration may involve network fees and signed transactions; a GitHub commit cannot perform it. If a wallet no longer has control of the mint authority, moving its funds does **not** move token authority.

## Current unresolved authority ownership
- Previously supplied candidate mint: `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9`.
- Read-only mint authority reported on 2026-11-19: `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4`.
- A separate wallet address may be displayed in personal project notes; a public address alone is **not** proof of controlling the mint authority. Do not assume custody or copy any recovery words into this repository.
- An owner-authenticated, **non-transactional** signed challenge can prove possession of a wallet key, but additional original chain evidence is needed to establish the requested relationship to the mint. Only sign readable text from trusted tools. Never sign arbitrary instructions or a transfer to prove identity.

## Prior to any owner-authorized on-chain changes
1. Identify one official mint and verify control of its relevant authority, **without sharing secrets**.
2. Record the complete present state of token accounts, mint/freeze authority, metadata authority, supply, token program and token-holder concentration.
3. Determine whether new authority should be a hardware wallet/multisig, transferred, or made permanently null. Null mint authority may be irreversible; do not revoke automatically.
4. Simulate/test transaction payloads and review actual instructions, fee payer, addresses and signatures before signing.
5. Publish confirmed transaction signatures **after** verification and reconcile project website and whitepaper. Never promise locked liquidity absent the LP address and lock/burn transaction proof.

## Release operations
- No on-chain writes, liquidity actions or paid submissions are allowed by the read-only audit scripts.
- Verify third-party links and domains before linking wallets. Avoid connecting wallets to copied or unsolicited websites.
- Do not infer that a token is safe because freeze authority is null or a scanner reports low risk.
- For incident response, keep transaction IDs and public addresses, not keys or recovery phrases.

References:
- https://solana.com/docs/tokens/basics/set-authority
- https://solana.com/docs/tokens
- https://github.com/itsAAA1/VoltZilla/blob/main/STATUS.md
