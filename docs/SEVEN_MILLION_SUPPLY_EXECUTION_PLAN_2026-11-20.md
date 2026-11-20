# VoltZilla VZLA — 7,000,000-token supply decision and execution prerequisites
**Reviewed:** 2026-11-20 (Asia/Riyadh) | **Status:** PREPARED / NO ON-CHAIN CHANGE

## What is verified (separate real mints)
1. Pump.fun candidate `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump`: canonical supply **1,007,005,921.840554**, 6 decimals, `mintAuthority=null`. **Cannot reduce or increase this mint's issued supply to 7 million by changing a GitHub file or ordinary wallet setting**. This token also has an unfinished Pump.fun curve; the exact circulating balance changes with transactions and burns.
2. Independent original SPL Token mint `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9`: supply **1,000,000 VZLA**, 9 decimals, active mint authority `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4`; freeze authority null; 100% of the issued supply reported in one token account owned by that authority wallet at the audited snapshot.
3. Raydium LaunchLab candidate `3cPWF3eKjcq4Y8d2oVXDRaN8ipKBHuyK1uYWY4GT7ray`: separate supply 1 billion, 6 decimals, mint authority null. Not convertible to 7m with ordinary mint action.
4. Old 2024 lookalike `JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump`: unrelated project-owner linkage.

**No token mint is yet approved as official by an owner-signed proof**. Do not combine their supply or tell the public that a 7-million coin already launched.

## One existing contract has a conditional route to 7 million
If, and ONLY IF, the owner proves they currently control **28fU8...Upi4**, elects to use the **DHxSt...N9** *separate* SPL mint as the intended 7-million VZLA token, and the canonical on-chain supply and mint authority have not changed:
- Current supply: 1,000,000 VZLA.
- Desired total supply: 7,000,000 VZLA.
- **Potential additional mint: 6,000,000 VZLA** to an explicitly chosen, controlled token account.
- Raw delta at 9 decimals: **6,000,000,000,000,000 base units**.
- After execution, verify `getTokenSupply`, exact token accounts, transaction signature and effective mint authority on canonical Solana RPC.
- If the owner separately chooses a **fixed, non-mintable** supply, revoke mint authority *only after the desired issuance and full review*. Revocation is ordinarily irreversible and requires its own explicit signed operation. DO NOT bundle an authority revocation into an implicit fee payment or sign challenge.
- This route does **not** rename GDY as a 7m coin, migrate GDY holders or guarantee a market, liquidity, price, buyback, distribution, or exchange listing.
- Creating six million more units under one owner may worsen concentration; provide a truthful actual distribution plan before marketing or sale.

## Required verification and execution boundaries
- [ ] Owner signs a **readable message** from wallet `28fU8...Upi4`. Prepared signing challenge: https://itsaaa1.github.io/verify-spl-wallet.html . Message signing alone is free and **does not mint**.
- [ ] Read `getTokenSupply` and `getMint` anew right before the transaction; ensure supply remains 1m, decimals 9 and authority 28fU8.
- [ ] Owner explicitly confirms **the exact mint** to alter and total target 7m (not the other 3 mints), recipient token account and authority policy.
- [ ] Determine network rent/transaction fees from a live wallet quote, not a fabricated fixed price.
- [ ] Authorized owner signs the token mint transaction in their own noncustodial wallet; never upload seed phrase, private key or keypair to an assistant or public repository.
- [ ] After on-chain confirmation, update `project-manifest.json`, site, roadmap and all official descriptions, citing the transaction ID.
- [ ] Perform separate independent safety/legal review before retail fundraising or assertions of exchange/trading readiness.

## Why no payment was requested or token minted
No transaction signature was supplied, wallet control has not been proven, and `official_mint=null`. This is a technically actionable plan, not confirmation that an on-chain supply change occurred. **No funds were transferred and no VZLA were issued during this review.**

## Official Raydium clarification, independently researched 2026-11-20
**Raydium does not impose a universal 7,000,000 VZLA token-supply requirement.** Its LaunchLab creation documentation explicitly states that total supply is configurable **at token creation**, then fixed for that launch. A separate LaunchLab **graduation SOL fundraising target** has a 24 SOL minimum in configurable mode, while JustSendit is described as targeting 85 SOL. Neither is a flat payment of 7 million tokens nor necessarily an upfront creation fee. Source: https://github.com/raydium-io/raydium-docs-v1/blob/main/user-flows/creating-a-launchlab-token.mdx .

The 7,005,921.840554 VZLA seen at the GDY Pump.fun creator wallet is an **observed token balance in a different mint**, not Raydium's required token supply or a payment owed. If someone has demanded 7 million VZLA or SAR, the demanding party, exact contract, amount, service and invoice/message source still need independent verification. **Do not transfer tokens on the basis of a UI number or somebody else's unverified request.**

