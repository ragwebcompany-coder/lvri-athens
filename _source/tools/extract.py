# -*- coding: utf-8 -*-
"""Lifts the editorial body out of every page of the legacy WordPress mirror.

The new site is built from the client's own copy, so this keeps the medical
text byte-for-byte and throws away only the theme's markup.
"""
import re, os, json, html, glob
from html.parser import HTMLParser

SRC = "lvriathens.com"
OUT = "lvri-new/content/legacy.json"

KEEP = {"h2", "h3", "h4", "h5", "p", "ul", "ol", "li", "strong", "b", "em", "i",
        "blockquote", "table", "thead", "tbody", "tr", "th", "td", "br", "sup", "sub"}
VOID = {"br", "img"}

# Theme furniture that never carries editorial copy. Matched per class token,
# so `has-post-thumbnail` on the <article> is not mistaken for `post-thumbnail`.
DROP_TOKEN = re.compile(
    r"^(post-thumbnail|fancy-date|entry-meta|post-meta|entry-tags|related.*|sidebar.*|"
    r"widget.*|vc_cta3.*|vc_btn3.*|vc_empty_space.*|breadcrumbs?|share.*|comments?|"
    r"main-nav|mini-nav|pagination|dt-shortcode.*|portfolio.*|blog-shortcode.*|"
    r"testimonials?|team.*|soc-ico.*|gallery-shortcode.*|slider.*|owl-.*|wpml.*|"
    r"searchform|screen-reader-text|assistive-text|wf-cell)$"
)


def is_furniture(cls: str) -> bool:
    return any(DROP_TOKEN.match(tok) for tok in cls.split())


class Lifter(HTMLParser):
    """Whitelist-serialises the editorial subtree, skipping theme furniture."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip_depth = 0
        self.skip_stack = []
        self.depth = 0
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.depth += 1
        if self.skip_depth:
            return
        cls = " ".join(filter(None, [a.get("class", ""), a.get("id", "")]))
        if tag in ("script", "style", "noscript", "aside", "nav", "form", "footer"):
            self.skip_depth = self.depth
            return
        if cls and is_furniture(cls):
            self.skip_depth = self.depth
            return
        if tag == "img":
            src = (a.get("data-src") or a.get("src") or "").split("?")[0]
            if "/wp-content/uploads/" in src:
                self.imgs.append(re.sub(r"^.*?wp-content/uploads/", "wp-content/uploads/", src))
            return
        if tag == "a":
            href = a.get("href", "")
            self.out.append(f'<a href="{html.escape(href, quote=True)}">')
            return
        if tag in KEEP:
            self.out.append(f"<{tag}>" if tag != "br" else "<br>")

    def handle_endtag(self, tag):
        if self.skip_depth and self.depth <= self.skip_depth:
            self.skip_depth = 0
        elif not self.skip_depth:
            if tag == "a":
                self.out.append("</a>")
            elif tag in KEEP and tag not in VOID:
                self.out.append(f"</{tag}>")
        if tag not in VOID:
            self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        if not self.skip_depth:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip_depth:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip_depth:
            self.out.append(f"&#{name};")


def tidy(frag: str) -> str:
    frag = re.sub(r"<(p|li|h[2-5]|blockquote)>\s*(&nbsp;|\s)*</\1>", "", frag)
    frag = re.sub(r"<a href=\"\"></a>", "", frag)
    frag = re.sub(r"<a href=\"[^\"]*\">\s*</a>", "", frag)
    frag = re.sub(r"[ \t]+", " ", frag)
    frag = re.sub(r"\n\s*\n+", "\n", frag)
    frag = re.sub(r"(</(?:p|h[2-5]|ul|ol|li|blockquote|table|tr)>)", r"\1\n", frag)
    return frag.strip()


def slice_content(doc: str) -> str:
    i = doc.find('<div id="content"')
    if i < 0:
        return ""
    j = doc.find('<div id="sidebar"', i)
    k = doc.find("</div><!-- #content -->", i)
    end = min(x for x in (j, k, len(doc)) if x > 0)
    return doc[i:end]


def extract(path: str):
    doc = open(path, encoding="utf-8", errors="ignore").read()
    seg = slice_content(doc)
    if not seg:
        return None
    lifter = Lifter()
    lifter.feed(seg)
    body = tidy("".join(lifter.out))
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', doc, re.S)
    h = re.search(r'<div class="page-title-head hgroup"><h1[^>]*>(.*?)</h1>', doc, re.S)
    dt = re.search(r'<span class="entry-month">(.*?)</span><span class="entry-date updated">(\d+)</span><span class="entry-year">(\d+)</span>', doc, re.S)
    return {
        "title": html.unescape(t.group(1)).strip() if t else "",
        "description": html.unescape(d.group(1)).strip() if d else "",
        "h1": html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip() if h else "",
        "date": [dt.group(1), dt.group(2), dt.group(3)] if dt else None,
        "html": body,
        "images": list(dict.fromkeys(lifter.imgs)),
        "text_len": len(re.sub(r"<[^>]+>", "", body)),
    }


def main():
    targets = [f"{SRC}/index.html", f"{SRC}/en/index.html"]
    targets += [t for t in sorted(glob.glob(f"{SRC}/*/index.html")) + sorted(glob.glob(f"{SRC}/en/*/index.html"))
                if not re.search(r"/(wp-|author|category)", t)]
    pages = {}
    for path in targets:
        slug = path[len(SRC) + 1:].replace("/index.html", "").replace("index.html", "home") or "home"
        if slug == "en":
            slug = "en/home"
        rec = extract(path)
        if rec:
            pages[slug] = rec
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(pages, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for s, r in pages.items():
        print(f"{s:66s} text={r['text_len']:6d} imgs={len(r['images']):2d} {'date=' + '/'.join(r['date']) if r['date'] else ''}")


main()
