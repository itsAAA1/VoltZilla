# Wallet-control proofs / إثباتات التحكم في المحافظ

Each JSON file is a message signed with Solana `signMessage` (Ed25519, UTF-8). It proves that the private key of the named public wallet signed that exact text at that time. It is **not** a transaction, does not move funds, does not mint, and does not select an official mint.

| Wallet | Role | Status | Record |
|---|---|---|---|
| `28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4` | Mint authority of `DHxSt…yN9`; deployer of `3cPWF3…7ray` | **Signed and verified** — 2026-11-21 10:22:59 UTC, Solflare | [2026-11-21_28fU8_wallet-control.json](2026-11-21_28fU8_wallet-control.json) |
| `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD` | Creator of `GDYcem…pump` (Pump.fun account `voltzilla_vzla`) | **Signed and verified** — 2026-11-21 16:37:59 UTC, offline Ed25519 using requester-supplied key (not in-app) | [2026-11-21_GGSqp_wallet-control.json](2026-11-21_GGSqp_wallet-control.json) |

## Verify it yourself

```bash
python3 scripts/verify_wallet_proof.py        # no network, no dependencies (RFC 8032 Ed25519)
```

Or open https://itsaaa1.github.io/proof.html and press the verify button: the browser re-checks the signature with WebCrypto Ed25519.

التحقق: السكربت يعيد بناء نص الرسالة الموقّعة حرفيًا من `message_lines`، ويفك عنوان المحفظة (base58) كمفتاح عام، ويتحقق من التوقيع. أي تغيير في حرف واحد من الرسالة أو تبديل المحفظة يفشل التحقق.

**Provenance:** The GGSqp signature was generated offline using a private key supplied by the requester, not approved in a Pump.fun wallet interface. Signature validation proves that the message matches the wallet public key; it does not prove who exclusively holds the key. Neither proof grants spending authorization.
