# VoltZilla (VZLA) — Corrected Pump.fun launch dossier
**Reviewed:** 20 November 2026 (Asia/Riyadh) | **Scope:** public read-only on-chain, Pump.fun project page, repository source, official listing/fee documentation.

> **Supersedes the 2-mint assumption in the prior audit.** This is a source-grounded technical preflight, **not** an independent audit certificate, legal opinion, listing acceptance, or promise of liquidity or earnings.

## 1. Which token is likely the user's actual Pump.fun project?

**Primary creator-linked token (the strongest match to the user's Pump.fun screenshot and wallet):**

- Project: VoltZilla / VZLA, network Solana, **Token-2022** program `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`.
- Contract mint: `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump`
- Original on-chain creator wallet: `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD`
- Creation transaction: `2frB6tsVzkEyPuteLX35fSbcKvq16fj3UbwD5pyQnhm3Mhgbutc3FGrB64tFacggnP1dkrC37EL26hsKZKQVC23U`
- Created: 4 April 2026 (~13:11:41 UTC), via Pump.fun.
- Original coin listing: https://pump.fun/coin/GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump
- Original creator account profile: https://pump.fun/profile/GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD
- Solscan creation transaction: https://solscan.io/tx/2frB6tsVzkEyPuteLX35fSbcKvq16fj3UbwD5pyQnhm3Mhgbutc3FGrB64tFacggnP1dkrC37EL26hsKZKQVC23U

**Evidence chain:** The user's screenshot displays public wallet `GGSq...NJiD`. Pump.fun independently labels this wallet as the creator of GDYcem, and the on-chain Pump bonding-curve creator attribution and wallet's purchase transaction match exactly. This is much stronger than matching only by ticker or logo. Still, a new non-financial wallet signature is needed to prove the user **currently controls** the private signing key.

## 2. Reconciled on-chain snapshot

**Helius-backed canonical mint safety read** at `2026-11-19T22:35:58Z`:
- Name/symbol VoltZilla/VZLA; program Token-2022; **decimals 6**.
- Supply `1,007,005,921.840554` VZLA at that instant. **Do not market exactly one billion as a fixed maximum** without reconciling the Token-2022/Mayhem and supply records; observed supply differs from 1,000,000,000.
- Mint authority `null`; freeze authority `null`; metadata update authority `null`. No authority to mint more on that token, according to this snapshot.
- Largest token account, controlled by the bonding curve `6PpZaXsSnXCwm37W1PkMtmG1kCLjYNXk95eLoHMsFXBk`, held **1,000,000,000** (99.3043% of current total); creator's token account held **7,005,921.840554** (0.6957%). **Bonding curve supply is not the private developer allocation**.
- Creator wallet indexed holdings included ~0.39556 SOL and ~7.00592M VZLA at that instant. Indexed balances are not verified spending balances.
- Wallet trading history includes a `0.250039067 SOL` purchase for `8,869,142.889262` VZLA and a later partial disposal of `1,863,221.048708` VZLA for `0.019434607 SOL`. Those are past transactions, not a present user command.

**Pump.fun page inspected live** on 20 November 2026:
- The token page is live and shows creator `voltzilla_vzla`, 2 holders, 24h volume **$0**, creator-held ~7.01M VZLA, and a bonding-curve graduation progress of **0%**.
- Page's liquidity field showed **~0.07 SOL (~$5.30)** at that check. This is a user-interface liquidity snapshot; **do not replace it with the ~$2,474 indexed virtual reserve value** from a different source. Recheck just before any trade.
- Graduation display showed a remaining **~32.05 SOL** (~$2,345 in that snapshot). This is a price-dependent curve target/collective market activity indicator, **not a fixed user fee or a request to fund**.
- Mayhem mode showed *completed* (mode ended), which does **not** mean the bonding curve graduated. Cashback/agent buyback parameters were present; no realized buyback revenue was shown. Treat special mechanics as launched historical settings; current ability to modify them is not established.
- DEX Screener `GET /token-pairs/v1/solana/GDYcem...` returned `[]`; there is **no independently indexed external liquidity pool** in this test. This does not mean the Pump bonding curve does not exist.

## 3. Other similar ticker mints — DO NOT SUBSTITUTE

A. `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9`: SPL Token (original program), 9 decimals, 1M observed supply, mint authority active at `28fU8...`, 100% token-account concentration. Distinct from Pump.fun creator-linked project; not evidence of the Pump.fun launch.

B. `JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump`: historical independent Pump.fun token, October 2024, unrelated creator wallet `HnGQ...`; 6 decimals, ~999,992,926.77 observed supply. The name/symbol and old draft do **not** prove ownership. Its misleading promotional claims must not be reused.

There are additional coins using the label VoltZilla/VZLA on Solana. **Only exact contract address and creator/transaction evidence disambiguate the project.**

## 4. Actual distribution vs proposed allocation

**Reality:** This Pump.fun launch was created on a bonding curve (not a standard owner-preminted 1M fixed-supply token with 40/30/20/10 allocation). The observed chain balances are ~99.3043% in a curve account and ~0.6957% in the creator account, measured against the observed minted supply. We cannot declare the former as “liquidity locked” or an airdrop/team allocation.

**Proposed governance policy (not executed):**
1. Publish exact creator, token program, revocable authorities and current creator-owned percentage whenever the figures change.
2. Do **not** claim a tokenomics split not represented by transfers/vesting accounts. If a future community rewards pool is set up, it must be funded from a disclosed address and show public transfer signatures.
3. No secret mint, presale guarantee, market manipulation, bot-created synthetic volume, or promises of profit.
4. Document current Mayhem/cashback/buyback settings as provider-observed behavior, not guaranteed earnings.

**The previous allocation drafts (40/30/20/10; 80/10/5/5) are historical ideas for a different design and are not suitable as the actual Pump.fun allocation.**

## 5. Listing workflow and current submission state

**CoinGecko:** exact GDYcem token search returned NOT_FOUND. **Correction (20 Nov):** Preview listings demand official evidence of a scheduled future Token Generation Event. The GDY token was already created in April 2026; do not misrepresent it as an upcoming TGE to evade active-market criteria. Official application https://partner.coingecko.com/request-form/new offers:
- Active listing: requires active trading on a tracked venue.
- **Preview Mode**: available even without an actively trading market; the application still undergoes project screening and may be rejected.
- Standard/Regular Pass: free; Fast Pass is optional and not required for eligibility.
- **Submission:** not performed; no receipt exists. Submission package is [LISTING_APPLICATION_PACK.md](LISTING_APPLICATION_PACK.md).

**CoinMarketCap:** a tracked listing generally calls for a working website, explorer and material trading volume on a CMC-tracked exchange. Its DEXScan may index separate unverified token pages automatically, but that **is not** the same as a reviewed verified tracked listing. The ordinary request path is https://coinmarketcap.com/request/. **Submission:** not performed; no receipt exists.

**DexScreener/GeckoTerminal:** may display actual active pool data; observed DexScreener external pair response was empty. Pump.fun's existing curve is not a Raydium pool. Avoid purchasing optional profile boosts or GeckoTerminal fast passes before exact identity, social accounts and pool status have been reconciled.

## 6. Current cost and liquidity — no speculative financial promises

For illustration only, **SOL ≈ US$73.04**, US$1 ≈ SAR 3.75 (historical/current indicative sources in November 2026); costs change with network, SOL price, venue and market demand:

| Path | Cost | Interpretation |
|---|---|---|
| Correct existing GitHub Pages, documentation, free listing request | **$0 / SAR 0** platform fee | Subject to existing account limits. No paid admission guaranteed. |
| Pump.fun token creation for an entirely new token | No Pump platform creation fee; chain rent/transaction fees apply | **Not needed**: creator-linked GDYcem is already minted and listed on Pump. |
| Pump.fun graduatation display | ~32.05 SOL ≈ **$2,340 / SAR 8,775** at ~$73/SOL | **NOT** a creator fee nor the amount the owner must pay; indicative collective curve progress and price-dependent. |
| Separate new Raydium CPMM pool | ~0.19 SOL ≈ **$13.87 / SAR 52.01** fixed+rent, **plus all actual seed liquidity** | Not required for Pump.fun launch. Separate pool changes price formation and carries market/impermanent-loss risks. |
| Example separate Raydium 0.2 SOL seed | ~0.39 SOL total ≈ **$28.47 / SAR 106.76** | Tiny pool, NOT enough to claim meaningful public liquidity, eligibility or a safe price. |
| Example separate Raydium 1 SOL seed | ~1.19 SOL total ≈ **$86.87 / SAR 325.76** | An optional scenario, not a recommendation or guaranteed depth. |
| Optional GeckoTerminal token-info Fast Pass | **$199 ≈ SAR 746.25**, before applicable tax | Official published optional priority review fee; does not guarantee listing. |
| Independent legal counsel / independent code audit | **Quote required** | No verified universal provider price. A checklist/self-review is not an independent signed report. |

**Do not launch a second pool or pay to “complete” the curve by buying your own supply as a prerequisite for documentation or free listing consideration.** No funds moved by this report.

## 7. Legal and financial communications review

The issuer's domicile, legal form, offered token rights, actual solicitation targets, accepted payment flows, social promotions and applicable jurisdiction must be established before a legal green light. Saudi Arabia has no general blanket retail cryptocurrency issuance approval that can be inferred from deploying a token on Solana, and authorities have issued consumer risk warnings. If the token is advertised as an investment, guaranteed return, payment instrument, security or pooled fund, additional regulated activity issues may arise.

**Specific copy problems identified:**
- On-chain legacy descriptions use claims of explosive performance, assured liquidity and anti-rug protection; **do not replicate**.
- Even the original creator-linked Pump metadata includes “growth”/“designed to dominate”; this is marketing language, not future performance proof.
- The website, README and whitepaper should explicitly say it is a high-risk meme/community token with **no guarantee of profit, liquidity, redemption or exchange acceptance**.
- The brand alludes to a famous monster; trademark/brand similarity deserves an independent trademark search before paid promotion. This audit makes no infringement conclusion.
- **No independent licensed Saudi counsel has signed an opinion.** No “legally approved” claims may be made.

## 8. Security, account and brand blockers

1. **Signer proof**: public creator/transaction match exists, but no human owner-signed challenge yet; see [SECURITY_RECOVERY.md](SECURITY_RECOVERY.md).
2. **Previously displayed credential material**: there was a past screenshot containing a wallet recovery phrase and private key. Do not copy into GitHub, form attachments or any chatbot. If those are real, rotate exposed keys and migrate funds to a fresh wallet using trusted wallet software; mint authority already null for GDYcem, so do not claim that token's mint control can be transferred.
3. **Social mismatch:** GDYcem metadata links `https://x.com/VoltZillaSOL`, while owner previously reported `https://x.com/voltzillasol1`. Do not fabricate a redirect or ownership relation. Original token metadata update authority is null; correcting public aggregator/social descriptions may require provider processes.
4. **Proof of independent audit/legal review:** not obtained. Internal static checks are not certification.
5. **Support & crisis runbook:** publish a project-controlled verifiable contact and key-compromise response before accepting customer funds/promoting sales.
6. **No verified third-party exchange listing acceptance**. Keep receipts for submissions; no assertions of approval until provider confirms.

## 9. What can be done without the user's wallet signature

- Align all GitHub repositories and the free GitHub Pages site with the creator-linked GDYcem evidence, visibly separate misleading lookalike contracts.
- Publish dated chain-status reports, user-facing risks, fee examples, and the official original Pump.fun token link.
- Implement read-only daily tests and listing packet validation, prepare applications without submitting unsupported fields.
- Verify source, CI, public website, and catalog of missing legal/external evidence.

**Requires actual owner action/signing or outside party:** changing wallet holdings, adding or withdrawing liquidity, confirming a wallet message, taking custody, externally certified security/legal opinion, CAPTCHA/account sign-in to listing providers, payments, and receipt-based submission acceptance.

## Sources

- Official on-chain creator-linked token: https://pump.fun/coin/GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump
- Token creation: https://solscan.io/tx/2frB6tsVzkEyPuteLX35fSbcKvq16fj3UbwD5pyQnhm3Mhgbutc3FGrB64tFacggnP1dkrC37EL26hsKZKQVC23U
- Solana token docs: https://solana.com/docs/tokens
- Official Pump fee schedule: https://pump.fun/docs/fees
- Raydium docs pool fees: https://github.com/raydium-io/raydium-docs-v1/blob/main/reference/fee-comparison.mdx
- CoinGecko listing: https://support.coingecko.com/articles/9489827481-how-to-list-a-new-cryptocurrency-on-coingecko
- CoinGecko preview: https://support.coingecko.com/articles/2654097937-how-to-list-an-upcoming-token-preview-mode
- CMC listing criteria: https://support.coinmarketcap.com/hc/en-us/articles/360043659351-Listings-Criteria
- SAMA USD/SAR: https://sama.gov.sa/en-US/Currency/FinExc/Pages/Currency.aspx
