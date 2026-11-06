#!/usr/bin/env python3
"""Check crawlable locale pages, reciprocal alternates, and local asset links."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://talamantes-roofing.vercel.app"
PAGES = {
    "/": ("index.html", "en", "/es/"),
    "/past-work.html": ("past-work.html", "en", "/es/past-work.html"),
    "/es/": ("es/index.html", "es", "/"),
    "/es/past-work.html": ("es/past-work.html", "es", "/past-work.html"),
}
for service in json.loads((ROOT / "tools/services.json").read_text()):
    slug = service["slug"] + ".html"
    PAGES["/" + slug] = (slug, "en", "/es/" + slug)
    PAGES["/es/" + slug] = ("es/" + slug, "es", "/" + slug)


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.text.append(text)


def check():
    docs = {url: Document(ROOT / file) for url, (file, _, _) in PAGES.items()}
    checked = 0
    for url, (filename, language, alternate) in PAGES.items():
        doc = docs[url]
        assert next(a["lang"] for t, a in doc.tags if t == "html") == language, filename
        canonical = [a["href"] for t, a in doc.tags if t == "link" and a.get("rel") == "canonical"]
        assert canonical == [ORIGIN + url], (filename, canonical)
        meta = {a.get("property", a.get("name")): a.get("content") for t, a in doc.tags if t == "meta"}
        assert meta["og:url"] == canonical[0], filename
        assert meta["og:type"] == "website" and meta["og:site_name"] == "Talamantes Roofing", filename
        assert meta["og:image"] == meta["twitter:image"] == ORIGIN + "/assets/roof-hero.jpg", filename
        assert meta["og:description"] == meta["twitter:description"] == meta["description"], filename
        assert meta["og:title"] == meta["twitter:title"] and meta["og:title"], filename
        assert meta["og:image:alt"] == meta["twitter:image:alt"] and meta["og:image:alt"], filename
        assert meta["og:locale"] == ("es_US" if language == "es" else "en_US"), filename
        assert meta["twitter:card"] == "summary_large_image", filename
        expected = {language: ORIGIN + url, "es" if language == "en" else "en": ORIGIN + alternate}
        alternates = {a["hreflang"]: a["href"] for t, a in doc.tags if t == "link" and a.get("rel") == "alternate"}
        assert all(alternates.get(lang) == target for lang, target in expected.items()), filename
        assert alternates["x-default"] == ORIGIN + (url if language == "en" else alternate), filename
        switches = [(t, a) for t, a in doc.tags if "data-language-toggle" in a]
        assert len(switches) == 2 and all(t == "a" for t, _ in switches), filename
        assert all(urljoin(ORIGIN + url, a["href"]) == ORIGIN + alternate for _, a in switches), filename
        assert sum(t == "h1" for t, _ in doc.tags) == 1, filename
        if language == "es":
            copy = " ".join(doc.text)
            for english in ["Free Estimate", "Areas Served", "Friendly workers", "Your free estimate starts here."]:
                assert english not in copy, (filename, english)
            assert "Llame al 818-395-8754" in copy, filename
        for tag, attrs in doc.tags:
            for key in ("href", "src", "poster", "data-full"):
                if key not in attrs:
                    continue
                target = urlsplit(urljoin(ORIGIN + url, attrs[key]))
                if target.scheme not in {"http", "https"} or target.netloc != urlsplit(ORIGIN).netloc:
                    continue
                path = unquote(target.path).lstrip("/")
                if not path or path.endswith("/"):
                    path += "index.html"
                file = ROOT / path
                assert file.is_file(), (filename, key, attrs[key])
                if target.fragment:
                    ids = {a["id"] for _, a in Document(file).tags if "id" in a}
                    assert target.fragment in ids, (filename, attrs[key])
                checked += 1
    script = (ROOT / "script.js").read_text()
    assert "localStorage" not in script and "setLanguage(" not in script
    sitemap = ET.parse(ROOT / "sitemap.xml")
    urls = [element.text for element in sitemap.findall("{*}url/{*}loc")]
    assert len(urls) == len(PAGES) and set(urls) == {ORIGIN + url for url in PAGES}
    robots = RobotFileParser()
    robots.parse((ROOT / "robots.txt").read_text().splitlines())
    assert robots.site_maps() == [ORIGIN + "/sitemap.xml"]
    for url in urls:
        assert robots.can_fetch("Googlebot", url), url
    for url, doc in docs.items():
        directives = [a.get("content", "") for tag, a in doc.tags if tag == "meta" and a.get("name", "").lower() in {"robots", "googlebot"}]
        assert not any("noindex" in d.lower() or "none" in d.lower() for d in directives), url
    services = json.loads((ROOT / "tools/services.json").read_text())
    for service in services:
        for locale, lang in [("", 0), ("/es", 1)]:
            url = locale + "/" + service["slug"] + ".html"
            doc = docs[url]
            content = " ".join(" ".join(doc.text).split())
            for key in ("heading", "lead", "intro", "overviewTitle", "overview", "heroCaption"):
                assert " ".join(service[key][lang].split()) in content, (url, key)
            for section in ("features", "process", "faqs"):
                for pair in service[section]:
                    for text in pair:
                        assert " ".join(text[lang].split()) in content, (url, text[lang])
            assert sum(t == "details" for t, _ in doc.tags) == 3, url
            assert any(t == "a" and a.get("href") == service["slug"] + ".html" for t, a in docs[locale + "/"].tags), url
    print(f"PASS: {len(PAGES)} static language pages, reciprocal language links, and {checked} local links/assets.")
    print(f"PASS: sitemap lists all {len(PAGES)} canonical pages; robots.txt permits Googlebot and advertises the sitemap.")
    print(f"PASS: Open Graph and large-image sharing tags are present in the initial HTML of all {len(PAGES)} pages.")


if __name__ == "__main__":
    check()
