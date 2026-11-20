# True financial AI execution: Solana wallets, Saudi business checkout, and regulated bank payment initiation
**Researched:** 2026-11-20 | **Status:** grounded architecture; provider eligibility, account access, funding and live settlement **not connected**.

## Financial autonomy is real, but a chatbot is NOT a licensed payment institution
An AI agent can generate a transaction, verify policy, call a delegated signer or licensed payments provider, then validate the transaction receipt. The LLM must not have unrestricted key/control over the owner's principal wallet. The **signer/provider policy**, not an editable prompt, must enforce financial limits. The agent and payment layer should be hosted on a monitored server for a recurring business workflow.

### A. Solana / VoltZilla
- Solana's documented signing backends include Turnkey, Crossmint, Privy, CDP and Fireblocks. Turnkey's Solana policy engine supports transaction amount, destinations and program interactions. Source: https://solana.com/docs/tools/keychain/choosing-a-backend and https://www.turnkey.com/blog/introducing-solana-policy-engine .
- For agent app code, Solana Agent Kit: https://solana.com/solutions/ai ; and Turnkey's signing examples: https://github.com/tkhq/turnkey-agent-skills/tree/main/skills/signing-transactions .
- Fund an **independent operational wallet** only after identity/KYC and provider-country eligibility are established. This wallet can pay approved vendors, perform authorized swaps if platform/market eligible, and pay fees. It must never inherit the creator-wallet's full mint authority automatically.
- Programmatic transfers require actual network transaction fees, on-chain signer access, and a confirmed transaction ID. A token mint to 7m, transfers and DEX swaps are separate transactions with separate authority/amount approvals.
- The proof-page wallet message signature is **not** permission to mint, swap, transfer or reveal key material.

### B. Saudi storefront
- Shopify Flow can automate order screening, tagging, fulfilment and payment capture where capture mode/permissions allow; it is not a bank or merchant PSP itself. Sources: https://help.shopify.com/en/manual/shopify-flow/reference and https://help.shopify.com/en/manual/shopify-flow/reference/actions/capture-payment .
- Use a **SAMA-licensed merchant PSP** such as Tap or Moyasar for customer SAR/mada/card payments and settlement. Official registry: https://sama.gov.sa/en-US/Supervision/LicenseEntities/Pages/Licensed_Payment_Service_Providers_companies.aspx .
- An operations agent can reconcile PSP webhook receipts, orders, invoices and inventory, generate supplier payouts and refund proposals, apply vendor approval limits and retain immutable accounting evidence.
- A payment provider's merchant agreement, APIs, verified endpoint signatures, KYC, credentials, payout eligibility and explicit payment authorization decide which steps can run automatically; do not claim merchant balances or transfers without provider receipts.

### C. Direct bank payments in Saudi Arabia (Open Banking)
- SAMA issued the Open Banking Framework and PIS second release; in March 2026 licensing of fintech providers after the sandbox began. Sources: https://www.openbanking.sama.gov.sa/index-en.html and https://sama.gov.sa/en-US/MediaCenter/News/Pages/news-1135.aspx .
- Example API: Arab National Bank's Payment Initiation Service specification https://connect.anb.com.sa/apis/api/open-banking-PIS explicitly requires a **licensed PISP** and **consent**; a merchant or standalone chatbot cannot invoke it without authorized provider integration.
- For a Saudi agentic company payment, business owner → authorized PISP/provider → customer/treasury account consent → policy check → bank transfer API → bank settlement confirmation. Not a workaround for Saudi financial-service rules.

## Working implementation delivered in this repository
- [agent-finance/treasury.py](../agent-finance/treasury.py): transaction-intent policy, idempotency, per-transaction/daily budgets, SQLite audit reservations, **no financial broadcast**.
- [agent-finance/solana_snapshot.py](../agent-finance/solana_snapshot.py): canonical read-only Solana mint and 7m mathematics.
- [agent-finance/tests](../agent-finance/tests): 11 unit tests passed locally 2026-11-20.
- [agent-finance/README.md](../agent-finance/README.md): run instructions, exact limitations and production steps.

## Operational rollout checklist
- [x] Research official agent-wallet, issuer and PIS infrastructure, license perimeter, and support links.
- [x] Create and verify read-only RPC observer and fail-closed finance policy code with 11 locally passing tests; publish source on GitHub.
- [x] Preserve VZLA exact-mint separation and check token one-million current authority using provider-backed RPC.
- [ ] Confirm the owner-controlled wallet and merchant/PISP identity on a production provider's verified account (no current Turnkey/Crossmint/PISP login in these connected tool sessions).
- [ ] Configure independent signer policy *at the signer layer* and production-grade durable ledger; add transaction decoding, simulator, fee caps and trusted receipt verifier.
- [ ] Create funded operational wallet/approved merchant account and authorize explicit amounts. **Do not fund blindly**.
- [ ] Deploy a 24/7 server/runner with monitoring, incident switch and backup; execute a minimal authorized production test; confirm its receipt.
- [ ] Launch only if Saudi legal and PSP requirements permit the selected activity.

**Do not call a policy-reserved intent a payment, a quote an executed swap, or read-only code a live trading bot.**
