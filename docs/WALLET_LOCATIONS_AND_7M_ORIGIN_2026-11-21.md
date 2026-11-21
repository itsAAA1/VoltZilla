# VoltZilla — which app holds each creator wallet, and where "7,000,000" came from
**Reviewed:** 2026-11-21 (Asia/Riyadh) | **Status:** evidence record, no on-chain change

## 1. Wallet locations

| Address | Role | Held in | Evidence |
|---|---|---|---|
| `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4` | Mint authority of the 1M SPL mint `DHxSt…yN9`; creator of the Raydium LaunchLab mint `3cPWF3…7ray` | **Solflare** | An "Onramper x Solflare via MoonPay" purchase of 0.255 SOL on 2026-04-11 09:46:29 UTC was delivered to this address: tx `L5e6u7eP56sLWdPpGFc5PZtGE3GZetrSzvi7XU1vTW68FxPgPGiz1Joh7rgTGbpLPnjvcVgpx9C2KTvpPRoN6KY` (signer: MoonPay hot wallet `5F1se…xUq1`). |
| `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD` | Creator of the Pump.fun mint `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump` | **Pump.fun account `voltzilla_vzla`** | https://pump.fun/profile/GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD shows username `voltzilla_vzla`, joined 2026-04-04, 1 coin created (VoltZilla). |

Consequence: the proof pages failed from Phantom because neither address is a Phantom account. `verify-spl-wallet.html` now supports Solflare (itsAAA1.github.io commit `9490f44`, CI and Pages deploy passed).

Pump.fun notice: external-wallet sign-in on pump.fun web ends **2026-11-30 15:00 UTC**; accounts that sign in with a wallet must add an email/social login before then (https://pump.fun/docs/wallet-login-changes).

## 2. Origin of the "7,000,000" figure

- No request for 7,000,000 VZLA was found in the owner's email or prior conversations.
- The legacy Genspark site (https://kvuznrxi.gensparkspace.com/) shows "إجمالي العرض 7,000,000 VZLA" **and** a wallet widget showing `@voltzilla_vzla`, `0.40 SOL` and `7.01M VZLA`, which are the Pump.fun profile figures of `GGSqp…JiD`.
- On-chain, `GGSqp…JiD` holds **7,005,921.840554 VZLA** of `GDY…pump`: bought 8,869,142.889262 in the creation transaction `2frB6…VC23U`, then sold 1,863,221.048708 (tx `3Jpzyt9z…oCrd`).
- **Conclusion (strong inference):** "7,000,000" is the creator wallet's balance that the Genspark site mislabelled as total supply. It is not an external requirement. The actual supply of `GDY…pump` is 1,007,005,921.840554.

Implication for `SEVEN_MILLION_SUPPLY_EXECUTION_PLAN_2026-11-20.md`: minting 6,000,000 extra units on `DHxSt…yN9` is not required by any party. Do not execute it on the basis of the Genspark figure.

## 3. Genspark errors still live (needs owner login to fix)

- "Contract Address" shows the wallet `GGSqp…` instead of the mint `GDY…pump`.
- Negative counters (-27.2M supply, -4,669 holders, -13,616 members), and a fabricated ticker (price, 24h volume $12,450, 45,000+ transactions, 67% long-term holders).
- Unimplemented claims (open-source contract, periodic burn, Arabic wallet app, EVM network, exchange listings) and dead Telegram/Discord/TikTok links.

## 4. Social identity mismatch

The X link stored in the `GDY…pump` Pump.fun metadata is `https://x.com/VoltZillaSOL`; the project's X account in use is `https://x.com/voltzillasol1`. These are different handles and need one canonical choice.
