#!/usr/bin/env python3
"""Generate committed Spanish HTML from the English pages and script.js copy.

Run after editing either English page or the translation dictionary. The published
site serves ordinary HTML and does not need Python or JavaScript to translate it.
"""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from share_metadata import add_share_metadata

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://talamantes-roofing.vercel.app"
COPY = json.loads(re.search(
    r"const spanishCopy = (\{.*?\n\});", (ROOT / "script.js").read_text(), re.S
).group(1))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class SpanishPage(HTMLParser):
    def __init__(self, filename):
        super().__init__(convert_charrefs=False)
        self.filename = filename
        self.output = []
        self.pending = []
        self.stack = []

    def flush_text(self):
        raw = "".join(self.pending)
        self.pending.clear()
        if not raw:
            return
        if any(tag in {"script", "style", "svg"} for tag, _ in self.stack):
            self.output.append(raw)
            return
        if any(switch for _, switch in self.stack):
            self.output.append("View in English")
            return
        decoded = html.unescape(raw)
        text = decoded.strip()
        if text in COPY:
            translated = decoded.replace(text, COPY[text], 1)
            self.output.append(html.escape(translated, quote=False))
        else:
            self.output.append(raw)

    def handle_starttag(self, tag, attrs):
        self.flush_text()
        values = dict(attrs)
        switch = "data-language-toggle" in values
        for key, value in attrs:
            if value is None:
                continue
            if key in {"aria-label", "alt", "data-caption", "data-alt"}:
                values[key] = COPY.get(value, value)
            elif tag == "meta" and key == "content" and values.get("name") == "description":
                values[key] = COPY[value]
            elif key in {"src", "poster", "data-full", "href"} and (
                value.startswith("assets/") or value in {"styles.css", "script.js", "gallery.js"}
            ):
                values[key] = "../" + value
        if tag == "html":
            values["lang"] = "es"
        if tag == "link" and values.get("rel") == "canonical":
            suffix = "/es/" if self.filename == "index.html" else "/es/" + self.filename
            values["href"] = ORIGIN + suffix
        if switch:
            values.update({
                "href": "../" if self.filename == "index.html" else "../" + self.filename,
                "lang": "en", "hreflang": "en", "aria-label": "View this page in English",
            })
        rendered = "".join(
            f" {key}" if value is None else f' {key}="{html.escape(value, quote=True)}"'
            for key, value in values.items()
        )
        self.output.append(f"<{tag}{rendered}>")
        if tag not in VOID:
            self.stack.append((tag, switch))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.output[-1] = self.output[-1][:-1] + "/>"
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        self.flush_text()
        self.output.append(f"</{tag}>")
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        self.pending.append(data)

    def handle_entityref(self, name):
        self.pending.append(f"&{name};")

    def handle_charref(self, name):
        self.pending.append(f"&#{name};")

    def handle_decl(self, decl):
        self.flush_text()
        self.output.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.flush_text()
        self.output.append(f"<!--{data}-->")


def generate():
    (ROOT / "es").mkdir(exist_ok=True)
    services = json.loads((ROOT / "tools/services.json").read_text())
    for filename in ["index.html", "past-work.html"] + [s["slug"] + ".html" for s in services]:
        parser = SpanishPage(filename)
        parser.feed((ROOT / filename).read_text())
        parser.close()
        parser.flush_text()
        (ROOT / "es" / filename).write_text(add_share_metadata("".join(parser.output)))
        print(f"Generated es/{filename}")


if __name__ == "__main__":
    generate()
