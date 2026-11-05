# VoltZilla — سجل حالة التحقق / Verification status
**Last document review:** 5 November 2026

This file describes repository documentation only. It is not proof of on-chain token ownership or listing.

| Item | Current status | Required evidence |
|---|---|---|
| Brand and symbol | VoltZilla (VZLA), proposed labels | Owner project references |
| Official social profile | X: https://x.com/voltzillasol1 | Confirmed by project owner |
| Official mint address / ownership | **Not verified / غير معتمد** | Owner-authenticated address and original Solana transactions |
| Supply, decimals, allocation, authorities | **Observed on-chain for owner-reported mint: 1,000,000 units, 9 decimals, mint authority active, freeze null, metadata mutable, one token account holds 100%; official mint approval and allocation Not verified** | On-chain RPC + owner signature for formal identity |
| Pump.fun launch and date | A **separate legacy mint** was observed as created on Pump.fun on **27 October 2024**; the official launch and owner association remain unconfirmed | Original creation transaction and owner-signed mint identity |
| Liquidity, LP locks/burns, trading pairs | **Not verified for the owner-reported million-unit mint**; the historical mint must not be substituted | Pool addresses, market-specific trades and original transactions |
| DexScreener token listing | **Not verified** | Token-specific page matched to the verified mint |
| CoinGecko application | **Not submitted / لم يُقدَّم بعد** | Submission receipt |
| CoinMarketCap application | **Not submitted / لم يُقدَّم بعد** | Submission receipt |
| Telegram, Discord or other channels | **Not approved** | Project-owner confirmation |

## Verified chain observation (5 November 2026)

**On-chain inspection — 5 November 2026 (Solana mainnet; Helius RPC via Nova):** The owner previously supplied mint `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9`. The mint exists as **VoltZilla (VZLA)**, SPL Token (standard Token Program), **1,000,000 current units**, **9 decimals**. Mint authority remains active (more tokens can be created); freeze authority is null; metadata update authority is active. The largest reported token account holds **100% of the current supply**. No reliable spot price or verified liquidity pair was returned. This validates observable mint data **but not a cryptographic signature proving the owner's control or public approval of this mint as the project's sole official address**. Never call this supply immutable, decentralized, tradeable, or liquidity-locked without separate evidence. Another mint shown in an old whitepaper (`JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump`) is **a separate token** with **6 decimals** and approximately **999,992,926.77** current units; its authorities and creator differ, so those figures must not be merged.

## Roadmap
1. Confirm official mint, ownership and documentation — **incomplete**.
2. Listing preparation and community outreach — **only after verified mint; not currently active**.
3. Further product/partnership research — **proposals, no committed dates**.
4. Expansion or advanced products — **unverified concepts only**.

## Conflicting historical drafts
Prior documents describe different supplies (1 million versus 1 billion), 6 versus 9 decimals, historical dates in 2024 versus draft dates in 2026, and conflicting proposed distributions (40/30/20/10, 80/10/5/5, or bonding-curve). None is endorsed as an approved live allocation. A token address in an old document is not proof it belongs to this project.

## Important distinction: fees and mint identity
Both candidate mint accounts use the original Solana SPL Token Program, which **does not support a Token-2022 native transfer-fee extension**. This is not a declaration of 0% total trade cost: network, routing, liquidity-provider and venue fees may apply. Neither observing a live mint nor seeing a verified Metaplex creator signature proves that the project GitHub account controls the mint authority. Revoked/null freeze authority means the mint has no account-freezing permission, **not that the token is cancelled or inactive**.

A read-only [direct-RPC inspector](scripts/inspect_mints.py) and [daily audit](.github/workflows/onchain-mint-audit.yml) check both mint accounts separately. The monitoring does not authorize or sign on-chain changes, and is not a security audit.

## Before publishing any new verified claim
- [ ] Confirm the mint address with owner-authenticated evidence.
- [ ] Verify chain data: supply, decimals, authorities and distribution.
- [ ] Verify actual liquidity, trading pairs and any locks/burns.
- [ ] Confirm platform and launch date from original evidence.
- [ ] Reconcile and approve a new accurate whitepaper.
- [ ] Submit platform requests only when eligible and record receipts/results.

**Do not publish unsupported trading instructions, market data, performance promises or unofficial social channels.**
