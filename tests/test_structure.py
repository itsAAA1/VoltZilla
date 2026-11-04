"""Offline integration checks for the VoltZilla repository source site and metadata."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website" / "index.html"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.mains = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        if tag == "main":
            self.mains += 1


class SourceWebsiteIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SITE.read_text(encoding="utf-8")
        cls.doc = Parser()
        cls.doc.feed(cls.html)

    def test_main_and_mobile_navigation(self):
        self.assertEqual(self.doc.mains, 1)
        self.assertIn('id="main-content"', self.html)
        self.assertIn('href="#main-content"', self.html)
        self.assertIn('<details class="mobile-nav">', self.html)
        self.assertIn('.mobile-nav{display:block}', self.html)
        self.assertIn('position: sticky; top:0', self.html)
        self.assertIn('prefers-reduced-motion:reduce', self.html)

    def test_accessibility_without_javascript(self):
        self.assertNotIn('onclick=', self.html)
        self.assertNotIn("new IntersectionObserver", self.html)
        self.assertNotIn("e.preventDefault()", self.html)
        self.assertIn("a:focus-visible", self.html)
        self.assertIn("href=\"#contract\"", self.html)

    def test_anchor_targets_and_external_security(self):
        duplicates = [id for id, count in Counter(self.doc.ids).items() if count != 1]
        self.assertFalse(duplicates, "Duplicate HTML ids")
        for link in self.doc.links:
            href = link.get("href", "")
            self.assertTrue(href and href != "#")
            if href.startswith("#"):
                self.assertIn(href[1:], self.doc.ids, f"Broken anchor {href}")
            elif href.startswith(("http://", "https://")):
                self.assertEqual(urlsplit(href).scheme, "https")
            else:
                self.assertTrue((SITE.parent / href).is_file(), f"Missing local file {href}")
            if link.get("target") == "_blank":
                rel = set((link.get("rel") or "").split())
                self.assertIn("noopener", rel)
                self.assertIn("noreferrer", rel)

    def test_canonical_and_verification_state(self):
        self.assertIn('<link rel="canonical" href="https://itsaaa1.github.io/">', self.html)
        self.assertIn("لم يتم اعتماد عنوان توكن رسمي", self.html)
        self.assertIn("لم يُقدَّم أي طلب إدراج بعد", self.html)
        self.assertNotIn("HOLD VZLA", self.html)
        self.assertNotIn("UNSTOPPABLE", self.html)

    def test_metadata_and_document_status(self):
        metadata = json.loads((ROOT / "assets" / "metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["name"], "VoltZilla")
        self.assertEqual(metadata["symbol"], "VZLA")
        self.assertEqual(metadata["external_url"].rstrip("/"), "https://itsaaa1.github.io")
        self.assertTrue((ROOT / "assets" / "logo.png").is_file())
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("CoinGecko application", status)
        self.assertIn("Not submitted", status)
        self.assertIn("CoinMarketCap application", status)
        self.assertIn("Not verified", status)


if __name__ == "__main__":
    unittest.main()
