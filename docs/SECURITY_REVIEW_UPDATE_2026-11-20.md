# VoltZilla security & evidence review — 20 November 2026
**Scope:** Solana canonical mint authority and public-account observations, public GitHub Pages source and automated content controls.
**Assessment type:** developer-maintained technical review, **NOT a certified independent external audit**.

## 1. Observed on-chain risk controls
| Mint | Canonical observed supply | Authority observations | Current risk summary |
| --- | ---: | --- | --- |
| `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump` | 1,007,005,921.840554 (6 decimals) | Token-2022; mint=null; freeze=null | No normal new mint permission; Pump.fun curve not graduated; indexed market price does not guarantee executable sell quote |
| `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9` | 1,000,000 (9 decimals) | Original SPL; **mint authority 28fU8... active**; freeze=null; metadata mutable | Issuance/concentration risk; 100% of supply seen in one owner's token account; conditional 7m plan only after owner signing |
| `3cPWF3eKjcq4Y8d2oVXDRaN8ipKBHuyK1uYWY4GT7ray` | 1,000,000,000 (6 decimals) | Original SPL; mint=null; freeze=null; metadata nonmutable in source snapshot | Separate Raydium LaunchLab curve, not graduated; not GDY token and not a verified liquid CPMM pool |

Sources: canonical Nova/Helius safety reads as of 20 November 2026 UTC, data reconciliation [FOUR_MINT_RECONCILIATION_2026-11-20.md](FOUR_MINT_RECONCILIATION_2026-11-20.md), and public mainnet transaction references in [project-manifest.json](../project-manifest.json). Nova index prices and holders may be cached, delayed or incomplete. Do not attribute current wallet control to a human without a valid owner signature.

## 2. Public website technical safeguards implemented
- `https://itsaaa1.github.io/market.html`: DEX Screener only as **optional remote source**, conditional to **exact base mint + Solana chain**; sorts available pools by published USD liquidity and displays 24h volume for the chosen pool. Missing market data remains visibly unknown instead of fabricating live trades. Legacy Pump.fun market quote is timestamped as historical/indexed, not guaranteed executable.
- `https://itsaaa1.github.io/wallet.html`: read-only `getBalance` and `getTokenAccountsByOwner` on a **fixed public creator wallet**; historical balances are explicitly labeled, update errors do not falsely mark a live balance, USD snapshot is not silently recomputed from current units.
- `https://itsaaa1.github.io/verify-wallet.html`: Phantom signs **readable message** for the GDY creator wallet `GGSqp...NJiD`; exact public-key check, cryptographic nonce and expiry, Ed25519 local verification, no token transfer.
- `https://itsaaa1.github.io/verify-spl-wallet.html`: independent signed-message challenge for 1m SPL token **mint authority** wallet `28fU8...Upi4` before evaluating a 7m supply plan. Signs **no transaction**, does **not** mint any tokens.
- Static site checks extended to market, wallet, roadmap, and both signature pages. The validator checks link source, identity, correct contract and absence of key-export/transaction helpers on signature pages.
- The full on-chain issuance plan is separate: [SEVEN_MILLION_SUPPLY_EXECUTION_PLAN_2026-11-20.md](SEVEN_MILLION_SUPPLY_EXECUTION_PLAN_2026-11-20.md).

## 3. Previous GitHub Actions failures and interpretation
Two specific **historical pull-request** runs were inspected in their original job logs (not assumed to describe the current default branch):
- VoltZilla source claim verification **run 44680707363** (20 Nov, 05:24 UTC): `release_preflight.py --check` returned 3 missing/inconsistent candidate-mint diagnostics in PR merge head; the job stopped before later assertions. The **current default-branch manifest** now preserves all four candidates, matches the GDY creator and keeps every release gate false. That structural parity was checked read-only on 20 Nov after inspecting the log. This **does not prove the Python CI passed** on current main.
- Static-site validation **run 44680343268** (20 Nov, 05:20 UTC): `tests/check_content.py` rejected the newly evidenced date **“مايو 2026”** in the old PR status page under its previous validation conditions. Current default-branch validation code names the specific unsupported claim `إطلاق GDY في مايو 2026` (GDY was April), without banning truthful reference to the **distinct Raydium launch in May**. This does not make a historical failed run green; it corrects the interpretation of the error.
- **CI verification limitation:** no completed successful current-main CI run has been independently confirmed by this document. The code can be audited with the repository's `python3 tests/check_content.py` and `python3 -m unittest discover -s tests -p 'test_*.py' -v` in the website repo, and `python3 scripts/release_preflight.py --check` + `--release` in the primary repo. Expected release exit status remains **2**, proving no public-ready release until all gates have evidence.

## 4. Remaining important security and governance gaps
- [ ] Actual wallet signatures proving present control of each chosen wallet. Signature proof does NOT alone establish legal identity or approve issuance.
- [ ] Verify **full mint and burn lineage** around Pump.fun Mayhem (~7.0059m extra above 1b canonical) from transaction data, rather than relying on one index.
- [ ] Independent expert audit of deployed Token-2022 extensions and platform interactions; a static JS site check is **not** a smart contract audit.
- [ ] External legal review for Saudi-directed token marketing, distribution, or fundraising.
- [ ] Confirm up-to-date on-chain market depth, sellability and withdrawal terms before any new LP funding or public purchase claims.
- [ ] Verify X account link and correct misleading Genspark legacy site from the **authenticated publishing account** (not achievable via a GitHub source commit).
- [ ] Perform a final penetration/security review of the static site's public resources, CSP and RPC/browser behavior (CORS/rate limits), plus brand social impersonation controls.

**No new tokens were minted, authorities changed, transactions sent, keys stored or funds transferred during this audit update.**
