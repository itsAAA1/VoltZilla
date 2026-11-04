"""Offline content guard: unsupported VoltZilla claims must not reappear.
Run: python3 tests/check_claims.py"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_X = "https://x.com/voltzillasol1"
failures = []

def check(cond, msg):
    if not cond:
        failures.append(msg)

html = (ROOT / "website/index.html").read_text(encoding="utf-8")
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v: self.hrefs.append(v)
p = Links(); p.feed(html)
x_links = {h for h in p.hrefs if re.search(r"(^|//)(www\.)?(x|twitter)\.com/", h)}
check(x_links == {OFFICIAL_X}, f"only the official X link is allowed, found {x_links}")
for bad in ("t.me/", "discord.gg", "discord.com/invite", "pump.fun/", "raydium.io/swap"):
    check(not any(bad in h for h in p.hrefs), f"unverified link present: {bad}")
check("https://dexscreener.com/solana" not in html, "generic DexScreener search must not be presented as a listing")
for phrase in ("TO THE MOON", "تداول الآن", "مبروك!", "اشتري Solana", "افتح Raydium", "نسخ 📋", "copyContract"):
    check(phrase not in html, f"unsupported phrase in website/index.html: {phrase}")
check(not re.search(r'stat-number">\s*(1B|0%|∞)\s*<', html), "unverified supply/tax/growth stat shown as fact")
check("لا تشترِ الآن" in html, "no-buy verification notice missing")
check('id="contract"' in html, "contract verification anchor missing")
check('class="roadmap-dot dot-done"' not in html, "phase 1 marked complete without verification")
check('class="roadmap-dot dot-active"' not in html, "phase 2 marked active without verification")
check('لم يُقدَّم أي طلب إدراج بعد' in html, "no-submission notice missing")
check(not re.search(r'<div class="token-pct">\s*\d+%', html), "historical percentage presented as live tokenomics")
check("لم يتم اعتماد عنوان توكن رسمي" in html, "unverified-address notice missing")

for rel in ("README.md", "docs/CoinGecko_Application.md", "docs/DexScreener_Update.md", "docs/Income_Plan.md", "STATUS.md"):
    t = (ROOT / rel).read_text(encoding="utf-8")
    for bad in ("100,000 ريال", "انعدام الضرائب", "الفريق (مقفلة)", "Pump.fun → Raydium", "- [x] إنشاء التوكن",
                "ثقة المستثمرين ستزيد", "إمكانية نمو هائلة", "Binance: ~", "PayPal: ~"):
        check(bad not in t, f"{rel}: unsupported claim '{bad}'")
check("لم يُقدَّم طلب بعد" in (ROOT / "docs/CoinGecko_Application.md").read_text(encoding="utf-8"), "CoinGecko document must say NOT SUBMITTED")
check("لم يُقدَّم أي طلب بعد" in (ROOT / "README.md").read_text(encoding="utf-8"), "README status not synchronized")
meta = json.loads((ROOT / "assets/metadata.json").read_text(encoding="utf-8"))
check("gains" not in meta["description"].lower() and "explosive" not in meta["description"].lower(), "metadata promises gains")
check(meta["symbol"] == "VZLA" and meta["external_url"] == "https://itsaaa1.github.io", "metadata identity fields changed")

if failures:
    print("\n".join("FAIL: " + f for f in failures)); sys.exit(1)
print("OK: VoltZilla claim checks passed")
