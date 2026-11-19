<div align="center">

# ⚡ VoltZilla (VZLA)
### وحش الطاقة الرقمي على شبكة Solana

[![Solana](https://img.shields.io/badge/Blockchain-Solana-9945FF?style=for-the-badge&logo=solana)](https://solana.com)
[![Token](https://img.shields.io/badge/Token-VZLA-FFD700?style=for-the-badge)](#-معلومات-التوكن)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter)](https://x.com/voltzillasol1)

<img src="https://raw.githubusercontent.com/itsAAA1/VoltZilla/main/assets/logo.png" alt="VoltZilla Logo" width="200"/>

> **"القوة لا تُوقف — الطاقة لا تُكبَّل — VoltZilla لا يُهزم"**

</div>

---

## 🌩️ ما هو VoltZilla؟

**VoltZilla (VZLA)** هو توكن ميم مبني على شبكة **Solana** عالية السرعة، يجمع بين طاقة البرق وقوة البلوكشين. ليس مجرد عملة — بل هو **حركة**، **مجتمع**، و**فرصة**.

تم تقديم مشروع VZLA بروح المقاتل الرقمي الذي لا يستسلم، مستوحى من قوة الكهرباء وسرعة الصاعقة. كل معاملة على شبكة Solana تحمل بصمة VoltZilla.

---

**تدقيق أحدث (20 نوفمبر 2026):** [العقد الذي أنشأته محفظتك على Pump.fun](docs/PUMPFUN_PRIMARY_AUDIT_2026-11-20.md)؛ تقرير الجاهزية السابق [أُبقي للتاريخ](docs/RELEASE_READINESS_2026-11-20.md) ولا يمثل أحدث اكتشاف.

**حالة التوثيق (5 نوفمبر 2026):** الحساب الاجتماعي الذي أكده صاحب المشروع هو [@voltzillasol1](https://x.com/voltzillasol1). توجد تناقضات بين المستودعات والموقع في عنوان التوكن والخانات العشرية والتوزيع وتاريخ الإنشاء. الأرقام أدناه بيانات مسودة، وليست توثيقًا على الشبكة أو توصية تداول.

## ⚡ تم العثور على إطلاق VoltZilla على Pump.fun — تصحيح موثّق (20 نوفمبر 2026)

**المرشح الأول للعقد الأصلي المرتبط بمحفظة صاحب المشروع:** `GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump` — [صفحة VoltZilla الحية على Pump.fun](https://pump.fun/coin/GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump) — [معاملة إنشائه](https://solscan.io/tx/2frB6tsVzkEyPuteLX35fSbcKvq16fj3UbwD5pyQnhm3Mhgbutc3FGrB64tFacggnP1dkrC37EL26hsKZKQVC23U).

- منشئ التوكن المثبت على Pump.fun وفي بيانات السلسلة: `GGSqpEPw3WDvfqJRj6frvrTz1C2wcUz28Sgfdg2NNJiD`، وهو العنوان الذي ظهر في شاشة صاحب المشروع. الإنشاء 4 أبريل 2026.
- هذا **توكن Token-2022 مختلف** عن عنوان SPL ذا المليون وعن عنوان Pump.fun تاريخي من 2024. لا يجوز جمع المعروض أو استخدام تصاميم توزيعهما معه.
- فحص Helius/Solana: 6 خانات عشرية، معروض لحظة الفحص `1,007,005,921.840554`، سلطة السك والتجميد ملغاة. يظهر نحو `7,005,921.840554` توكن في محفظة المُنشئ، والباقي في حساب منحنى Pump.fun. لا يعني ذلك بيعًا عامًا واسعًا.
- صفحة Pump.fun تعرض: منحنى غير متخرج، 0 دولار حجم تداول في 24 ساعة، وسيولة واجهة ~0.07 SOL، وشراء/حرق آلي ضمن إعداد Mayhem؛ القيم تتغير مع الوقت وليست وعدًا.
- **بقي إثبات التحكم الحالي بالمحفظة بتوقيع آمن، وحسم حساب X**: صفحة Pump.fun تستخدم `@VoltZillaSOL` بينما صاحب المشروع سبق أن أكد `@voltzillasol1`. لا ننسب الاثنين كحساب رسمي واحد.
- لا يوجد طلب CoinGecko أو CoinMarketCap مؤكّد الإرسال حتى الآن. انظر [تقرير العقد الحقيقي وخطة الإدراج والتكاليف](docs/PUMPFUN_PRIMARY_AUDIT_2026-11-20.md) و[ملف تقديم الإدراج](docs/LISTING_APPLICATION_PACK.md).

**مهم:** الفقرة التالية عن العنوان ذي المليون هي **توثيق تاريخي لعقد منفصل، وليست مواصفات عقد Pump.fun المرتبط بالمحفظة**.

## 🔬 بيانات العقد المنفصل ذات المليون — سجل تاريخي

**On-chain inspection — 5 November 2026 (Solana mainnet; Helius RPC via Nova):** The owner previously supplied mint `DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9`. The mint exists as **VoltZilla (VZLA)**, SPL Token (standard Token Program), **1,000,000 current units**, **9 decimals**. Mint authority remains active (more tokens can be created); freeze authority is null; metadata update authority is active. The largest reported token account holds **100% of the current supply**. No reliable spot price or verified liquidity pair was returned. This validates observable mint data **but not a cryptographic signature proving the owner's control or public approval of this mint as the project's sole official address**. Never call this supply immutable, decentralized, tradeable, or liquidity-locked without separate evidence. Another mint shown in an old whitepaper (`JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump`) is **a separate token** with **6 decimals** and approximately **999,992,926.77** current units; its authorities and creator differ, so those figures must not be merged.

## 🧪 أداة الفحص المباشر للتوكن — قراءة فقط

أُضيفت أداة Python تعمل على قراءة حسابَي SPL Token من Solana mainnet عبر JSON-RPC، دون أي مفاتيح خاصة أو توقيع معاملات:

```bash
python3 scripts/inspect_mints.py --check
python3 -m unittest discover -s tests -p "test_*.py" -v
```

- تفحص العنوان الذي أبلغ به صاحب المشروع [DHxStA9…N9](https://solscan.io/token/DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9) والعنوان المنشور قديمًا [JBaHD…pump](https://solscan.io/token/JBaHDseUdFEVbAik7rojwC8ZZ8EjyBi1qQPoK9tLpump) **بشكل منفصل**.
- `--check` يقارن **المعروض الخام، الخانات العشرية، سلطة السك، وسلطة التجميد** بلقطة 5 نوفمبر 2026؛ إذا تغيرت، تتوقف المهمة للمراجعة. تغيّر الكمية في عنوان سلطة سكه مفعلة ممكن، وهذا ليس وحده دليل مخالفة.
- **لا** تثبت هذه الأداة ملكية المحفظة أو هوية المشروع، ولا تغيّر العقد أو صلاحياته، ولا تثبت سعرًا أو سيولة أو إدراجًا.
- بيانات `update authority` الخاصة بالـMetaplex تحتاج فحص حساب ميتاداتا منفصل؛ ولا تدعي أداة SPL Mint أنها تفحصها.

**للتفريق بين الإثباتين:** رصد بيانات التوكن على السلسلة لا يساوي اعتماد عنوانه رسميًا؛ اعتماد العنوان يحتاج إثباتًا موثوقًا من المحفظة ذات الصلاحية.

---

## 📊 معلومات التوكن

| المعلومة | التفاصيل |
|---|---|
| **الاسم** | VoltZilla |
| **الرمز** | VZLA |
| **الشبكة** | Solana (SPL Token) |
| **توكن Pump.fun المرتبط بمنشئك** | \`GDYcem...pump\`؛ المعروض المرصود 1,007,005,921.840554؛ 6 خانات عشرية؛ سلطة السك والتجميد غير موجودتين. راجع التدقيق الأحدث. |
| **المنصة** | Pump.fun للعقد GDYcem…، وهو غير متخرج من منحنى الإطلاق |
| **نوع التوكن** | Meme Token |

---

## 🚀 خارطة الطريق (مراحل مشروطة وغير مكتملة)

**الحالة الحالية:** إطلاق Pump.fun الأصلي موجود ومثبت بصفحة المُنشئ، لكن المنحنى غير مكتمل والهوية الموقعة والإدراجات ليست مثبتة. لم يُقدَّم أي طلب بعد إلى CoinGecko أو CoinMarketCap. المرحلة الثانية مشروطة أولًا باعتماد عنوان التوكن. راجع [STATUS.md](STATUS.md).

### المرحلة الأولى - التحقق ⚡
- [ ] التحقق من عنوان التوكن الرسمي على Solana
- [ ] إنشاء قنوات إضافية للمجتمع عند الإعلان عنها رسميًا
- [ ] إثبات وجود زوج تداول قبل أي طلب تحديث DexScreener
- [ ] توثيق عدد الحاملين عند توفره

### المرحلة الثانية - بعد اعتماد العنوان ⏳
- [ ] تقييم طلب CoinGecko — لم يُقدَّم بعد
- [ ] تقييم طلب CoinMarketCap — لم يُقدَّم بعد
- [ ] تقييم شراكات بعد توثيق المشروع
- [ ] نشر بيانات النمو القابلة للتحقق

### المرحلة الثالثة - الهيمنة 👑
- [ ] دراسة جدوى أي طلب إدراج مركزي
- [ ] دراسة أفكار NFT قبل الإعلان عن إطلاقها
- [ ] تقييم نظام مكافآت وفق الضوابط الفنية والقانونية
- [ ] تحديث الخارطة بما يُثبت تنفيذه

---

## 💡 لماذا VoltZilla؟

- ⚡ **شبكة Solana** — الشبكة المذكورة للمشروع؛ لا تعد الوثيقة بتكلفة أو سرعة محددة
- 🔥 **المجتمع** — حساب X المعتمد فقط؛ لا توجد أرقام مجتمع موثقة
- 💎 **الشفافية قيد الاستكمال** — لا تتوفر حاليًا معلومات كافية لاعتماد عنوان توكن واحد وتوزيعه
- ⚠️ **لا توجد وعود بالنمو أو العائد** — الخارطة أدناه أهداف غير مضمونة

---

## 🔗 روابط مهمة

| المنصة | الرابط |
|---|---|
| **DexScreener** | [بحث عام عن العملات](https://dexscreener.com/solana) — ليس رابط زوج تداول موثق |
| **Phantom Wallet** | [المحفظة الرسمية للتطبيق](https://phantom.app) — ليس رابط شراء VZLA |
| **Twitter/X** | [@voltzillasol1](https://x.com/voltzillasol1) |

---

## ⚠️ إخلاء المسؤولية

هذا التوكن هو توكن ميم للترفيه والمجتمع. **لا يُعدّ استثماراً ماليًا**. تداول المشفرات ينطوي على مخاطر عالية. لا تستثمر أكثر مما تتحمل خسارته.

---

<div align="center">

**⚡ VoltZilla — الطاقة لا تنتهي ⚡**

Made with ⚡ by the VoltZilla Community

</div>
