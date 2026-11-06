#!/usr/bin/env python3
"""Keep sharing previews in the initial HTML, including generated service/locales."""
import html
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://talamantes-roofing.vercel.app"
IMAGE = ORIGIN + "/assets/roof-hero.jpg"
START = "<!-- Link sharing preview -->"
END = "<!-- End link sharing preview -->"


class PageHead(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.language = "en"
        self.canonical = self.description = self.title = ""
        self.in_title = False
        self.feed(source.split("</head>", 1)[0])

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "html":
            self.language = values["lang"]
        elif tag == "meta" and values.get("name") == "description":
            self.description = values["content"]
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values["href"]
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def add_share_metadata(source):
    source = re.sub(r"  " + re.escape(START) + r".*?" + re.escape(END) + r"\n", "", source, flags=re.S)
    head = PageHead(source)
    assert head.title and head.description and head.canonical, "Sharing needs a title, description, and canonical URL."
    spanish = head.language == "es"
    title = head.title
    if head.canonical in {ORIGIN + "/", ORIGIN + "/es/"}:
        title = "Talamantes Roofing | " + ("Techos en Los Ángeles" if spanish else "Los Angeles Roofing")
    alt = ("Ilustración de una casa de California con techo de tejas asfálticas y entrada arqueada."
           if spanish else "Illustration of a California home with a shingle roof and arched entryway.")
    properties = {
        "og:type": "website",
        "og:site_name": "Talamantes Roofing",
        "og:title": title,
        "og:description": head.description,
        "og:url": head.canonical,
        "og:locale": "es_US" if spanish else "en_US",
        "og:locale:alternate": "en_US" if spanish else "es_US",
        "og:image": IMAGE,
        "og:image:secure_url": IMAGE,
        "og:image:type": "image/jpeg",
        "og:image:width": "1536",
        "og:image:height": "1024",
        "og:image:alt": alt,
    }
    twitter = {
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": head.description,
        "twitter:image": IMAGE,
        "twitter:image:alt": alt,
    }
    block = "  " + START + "\n"
    for attribute, values in [("property", properties), ("name", twitter)]:
        for key, value in values.items():
            block += f'  <meta {attribute}="{key}" content="{html.escape(value, quote=True)}">\n'
    block += "  " + END + "\n"
    if 'prefix="og: https://ogp.me/ns#"' not in source:
        source = source.replace('<html lang="' + head.language + '">', '<html lang="' + head.language + '" prefix="og: https://ogp.me/ns#">', 1)
    return source.replace("</head>", block + "</head>", 1)


if __name__ == "__main__":
    pages = list(ROOT.glob("*.html")) + list((ROOT / "es").glob("*.html"))
    for page in pages:
        page.write_text(add_share_metadata(page.read_text()))
    print(f"Updated sharing metadata on {len(pages)} pages.")
