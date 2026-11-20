# VoltZilla VZLA — Four-mint reconciliation and execution boundaries
**Review:** 20 November 2026 (Saudi time) | **Evidence:** direct Helius-backed canonical mint read and Solana Tracker profile through Nova; GitHub repository releases. **Read-only technical analysis. Not an independent certified audit or legal opinion.**

## Token identifiers that MUST NOT be conflated

| Token | Program | Supply observed | Mint authority | Creator / provenance | Market / conclusion |
| --- | --- | --- | --- | --- | --- |
| `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump` | Token-2022 | 1,007,005,921.840554 (6 decimals) | null | Pump.fun linked creator `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD`, creation 4 Apr 2026 | Pump.fun bonding curve; not graduated. Preferred creator-matched candidate pending wallet signature. |
| `3cPWF3eKjcq4Y8d2oVXDRaN8ipKBHuyK1uYWY4GT7ray` | Original SPL | 1,000,000,000 (6 decimals) | null | Indexed deployment wallet `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4`, 15 May 2026; [creation tx](https://solscan.io/tx/3NybCdX9VssTzAdM2TKDNPnGWTn6SNr1H4GjzEDpVSeThxrE8kiasCZnHbnfjApZcUTonYqNe5WfA2XcnnCLkvA8) | Raydium LaunchLab indexed curve `J1nse1K58AcjDEtCdkL7nFByUNwjGuTkupxiKtwuxXAz`. Not a verified graduated CPMM pool. |
| `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9` | Original SPL | 1,000,000 (9 decimals) | `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4` ACTIVE at earlier November snapshot | Historical creator-linked candidate | No verified tradable pair. |
| `JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump` | Pump.fun | 999,992,926.771367 (6 decimals) | null | Different 2024 creator (not linked to owner's wallets) | Unrelated name lookalike unless new ownership evidence appears. |

**Critical distinction:** A public creator address is verifiable from chain transactions but does NOT prove a named human currently controls it. `GGSqp...` and `28fU8...` may both be connected to the user's history, but their relation and private signing authority require separate wallet signatures. No token is silently substituted as official in `project-manifest.json`.

## Additional Helius independent checks of Raydium LaunchLab token (2026-11-20T05:18:06Z)

- Standard SPL Token program `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`.
- Name/symbol VoltZilla/VZLA; 6 decimal places, 1,000,000,000 supply.
- `mintAuthority=null`, `freezeAuthority=null`: neither authority can normally be re-created by editing a GitHub file.
- Metaplex update authority `WLHv2UAZm6z4KyaaELi5pjdbJh6RESMva1Rnn8pJVVh`; metadata `isMutable=false`. A Metaplex creator field is NOT necessarily the launchpad transaction's deployer.
- Largest token account `GfF4...RA7p`: 996,472,538.911747 (~99.6473%) in an indexed owner associated with the launch state; creator wallet `28fU8...` token account: 3,527,461.088253 (~0.3527%). Do NOT call curve inventory a private insider allocation.
- Solana Tracker profile indexed Raydium LaunchLab launchpad state, 2 indexed holders, trading volume24h=0 in its last available snapshot and a market price/LP value with **upstream freshness unknown**. Do not publish that indexed USD quote as a fresh real-time executable rate.
- No guarantee of external tracked exchange listing, Raydium CPMM graduation, market liquidity, token sellability or regulatory status.

## Pump.fun GDY settings are not ordinary application features

- `isMayhemMode=true` means historically launched with Mayhem. The Pump.fun page displayed *Mayhem completed / ended* and the mode's startup period is not restored by site/source editing.
- `isCashbackCoin=true` is the launching fee/rewards configuration. It is not a promise of free money, and reward delivery depends on qualifying fee transactions and platform behavior.
- `isHolderReward=false`: not enabled. Pump.fun terms allow conversion of a Cashback coin to Holder Rewards only through a **community takeover (CTO)**. Merely changing an app's configuration or running a bot cannot activate protocol holder rewards. A real CTO requires eligible platform mechanics and/or authenticated actions; no CTA is claimed or initiated.
- `mintAuthority=null`, `freezeAuthority=null` on GDY: revoked permissions are not "broken" or "disabled features" waiting for a code edit.

References: [Pump.fun terms](https://pump.fun/docs/terms-and-conditions), [Pump.fun fees](https://pump.fun/docs/fees), [Pump.fun Mayhem](https://pump.fun/docs/mayhem-mode), [Solana Set Authority](https://solana.com/docs/tokens/basics/set-authority).

## Free code and verification implemented vs owner-controlled steps

- **Written and testable for US$0 platform fees:** public site, whitepaper, risk disclosures, proof-of-control page, on-chain mint auditors, GitHub CI and truthful listing application packet.
- **Signature challenge:** [https://itsaaa1.github.io/verify-wallet.html](https://itsaaa1.github.io/verify-wallet.html) requests only a signed readable message, validates the expected public key via browser Ed25519, and outputs a public record. No transaction is constructed, funds transferred, credential requested or network POST made. The account owner must operate their own wallet; the existence of the page is **not** a signed proof.
- **Actual current user signature:** PENDING. A signed proof for GDY doesn't prove control of the Raydium creator `28fU8...`; that would need a second public-key challenge if selected as official instead.
- **Listings:** CoinGecko/CoinMarketCap requests NOT submitted; no listing approval receipt.
- **Finance:** No capital transfer, liquidity deposit or market-making service performed. The existing GDY launch requires no new token mint. A separately created Raydium pool is OPTIONAL and should not fragment liquidity without a reason.
- **Third-party legal/cyber audit:** provider quotes and signed reviews NOT obtained. Internal tests can't be labeled independent certificates.
- **Compatibility:** Wallet signed messages may require Phantom browser/extension and WebCrypto Ed25519 support; the page shows an explicit error when unsupported and never falsely displays success.

## Budget snapshot, NOT a funding demand

The original cost table [BUDGET_LIQUIDITY_2026-11-20.md](BUDGET_LIQUIDITY_2026-11-20.md) uses an indicative SOL price of **US$73.04 / SAR 273.90 per SOL** at the time:
- Existing code, GitHub Pages, basic public docs, free CMC/CG application routes: **$0 / SAR 0** provider fee.
- Optional separate Raydium CPMM setup fee and account rent **~0.19 SOL**: **~$13.88 / SAR 52.04**, plus both sides of seed liquidity, network fees and slippage.
- An OPTIONAL example with quote-side 1 SOL seed + 0.19 SOL overhead: **~$86.92 / SAR 325.94**, plus appropriate token seed and unquoted extras. Not a meaningful guaranteed depth.
- ~32.05 SOL shown on old Pump curve page: **NOT a creator invoice**; graduation depends on collective activity/curve state.
- Independent legal/security reports, exchange listing (if required), and effective market depth: **no defensible universal fixed price**. Request authentic quotes; neither money nor approvals are prerequisites for the static site.

**Conclusion:** The repository can be maintained and the public evidence prepared, but the project is **not independently audited, owner-signed, graduated, broadly listed or fully capitalized**. Do not promise it is “100% complete” without the missing third-party and wallet evidence.
