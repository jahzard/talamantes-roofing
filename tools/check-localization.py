#!/usr/bin/env python3
"""Check crawlable locale pages, reciprocal alternates, and local asset links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://talamantes-roofing.vercel.app"
PAGES = {
    "/": ("index.html", "en", "/es/"),
    "/past-work.html": ("past-work.html", "en", "/es/past-work.html"),
    "/es/": ("es/index.html", "es", "/"),
    "/es/past-work.html": ("es/past-work.html", "es", "/past-work.html"),
}


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
    print(f"PASS: 4 static language pages, reciprocal language links, and {checked} local links/assets.")


if __name__ == "__main__":
    check()
