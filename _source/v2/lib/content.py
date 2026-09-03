# -*- coding: utf-8 -*-
"""Content layer for version 2.

Reads the same source of truth as version 1 — `lvri-new/content/data.py` and
`lvri-new/content/legacy.json` — so there is one place to edit copy and both
sites stay in sync. Nothing here is invented: every figure comes from the
clinic's own published pages.
"""
import os, re, sys, json, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
ROOT = os.path.dirname(V2)


def _find(*candidates):
    """The generator runs from two places: the working tree (next to lvri-new/) and the
    deployment repo (as _source/v2/, next to _source/content/). Resolve either."""
    for c in candidates:
        if os.path.isdir(c):
            return c
    raise SystemExit("δεν βρέθηκε ο φάκελος περιεχομένου: " + " | ".join(candidates))


CONTENT = _find(os.path.join(ROOT, "lvri-new", "content"),   # working tree
                os.path.join(ROOT, "content"))               # deployment repo
TOOLS = _find(os.path.join(ROOT, "lvri-new", "tools"),
              os.path.join(ROOT, "tools"))

sys.path.insert(0, CONTENT)
from data import (SITE, CONDITIONS, TREATMENTS, ARTICLES, GUIDE_STEPS,   # noqa: E402
                  RED_FLAGS, KEGEL, VIDEOS, EN_PAGES, MONTHS)

LEGACY = json.load(open(os.path.join(CONTENT, "legacy.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

CONDS = {c["slug"]: c for c in CONDITIONS}
TREATS = {t["slug"]: t for t in TREATMENTS}

# ── URL map ──────────────────────────────────────────────────────────────────
URLMAP = {
    "home": "", "h-kliniki": "i-kliniki/", "dr-k-mirillas": "dr-mirillas/",
    "david-l-matlock": "dr-matlock/", "epikinonia": "epikoinonia/",
    "oroi-chrisis-politiki-aporritou": "oroi-chrisis/", "iatrika-arthra": "arthra/",
    "photo-gallery": "gallery/", "video-gallery": "gallery/",
}
for _c in CONDITIONS:
    URLMAP[_c["legacy"]] = f"pathiseis/{_c['slug']}/"
for _t in TREATMENTS:
    URLMAP[_t["legacy"]] = f"therapeies/{_t['slug']}/"
for _slug, _tag in ARTICLES:
    URLMAP.setdefault(_slug, f"arthra/{_slug}/")
for _new, _legacy, _title in EN_PAGES:
    URLMAP[_legacy] = f"en/{_new}/"

PID = {
    "3": "oroi-chrisis-politiki-aporritou", "26": "laser-kolpou", "31": "plastiki-aidoiou",
    "37": "david-l-matlock", "41": "dr-k-mirillas", "46": "photo-gallery", "108": "video-gallery",
    "202": "akrateia-ouron", "205": "kolpiki-ksirotita", "207": "proptosi-mitras",
    "227": "iatrika-arthra", "239": "epikinonia", "403": "h-kliniki", "1401": "g-shot",
    "1592": "kysteokhlh", "1594": "orthokili-enterokili", "1630": "anazoogonisi-kolpou",
    "508": "ksirotita-kolpou-kata-tin-emminopausi-to-laser-einai-h-lysi",
    "514": "akrateia-ouron-aitia-kai-therapeia", "521": "akrateia-ouron-prospatheias",
    "526": "arthro-gia-tin-akrateia-ouron", "543": "arthro-gia-tin-kolpiki-proptosi",
    "569": "plastiki-kolpou-vlaves-pou-diorthonei", "573": "plastiki-kolpou-o-dr-myrillas-apanta",
    "592": "to-laser-stin-sygxroni-epoxi", "598": "proto-pagosmio-synedrio-laha-laser",
    "604": "ygieini-kata-tis-kolpitidas", "609": "xeirourgiki-pyelikou-edafous",
    "611": "therapeia-akrateias-ouron-ksirotitas-sysfixis-kolpou",
    "1695": "aidoioplastiki-tonoste-tin-aftopepoithisi-sas-allakste-tin-poiotita-tis-zois-sas",
    "1702": "akrateia-ouron-aitia-diagnosi-therapeia",
    "1709": "apolafste-tin-kathe-mera-kratiste-makria-tin-kolpiki-ksirotita",
    "1716": "mathete-ta-panta-gia-tin-proptosi-mitras",
    "1729": "poies-afora-i-ksirotita-kolpou-kai-pos-tin-antimetopizei-i-sygchroni-iatriki",
    "1814": "en/vaginal-dryness", "1820": "en/vaginal-tightening-laser",
    "1823": "en/vaginal-atrophy", "1826": "en/designer-laser-vaginoplasty",
    "1846": "en/the-clinic", "1869": "en/urinary-incontinence",
}
ALIAS = {
    "akrateia-ouron-gynaikeia": "akrateia-ouron",
    "proptosi-kolpou-mitras": "proptosi-mitras",
    "laser-plastiki-kolpou": "laser-kolpou",
}


def rel(depth):
    return "../" * depth if depth else ""


def url_for(legacy_slug, depth):
    legacy_slug = ALIAS.get(legacy_slug, legacy_slug)
    target = URLMAP.get(legacy_slug)
    return None if target is None else rel(depth) + target


def rewrite_links(markup, depth):
    """Points the clinic's own copy at the version-2 URLs; leaves outside links alone."""
    def repl(m):
        href = m.group(1)
        if href.startswith(("tel:", "mailto:", "#")):
            return m.group(0)
        pid = re.search(r"[?@]p=(\d+)", href)
        if pid and pid.group(1) in PID:
            u = url_for(PID[pid.group(1)], depth)
            if u is not None:
                return f'href="{u}"'
        if "lvriathens.com" in href:
            slug = href.rstrip("/").split("lvriathens.com/")[-1]
            u = url_for(slug, depth)
            return f'href="{u}"' if u is not None else f'href="{rel(depth)}"'
        local = re.match(r"^(?:\.\./)*([a-z0-9\-]+)/index\.html$", href)
        if local:
            u = url_for(local.group(1), depth)
            if u is not None:
                return f'href="{u}"'
        if href.startswith(("http://", "https://")):
            return f'href="{href}" rel="noopener" target="_blank"'
        return f'href="{rel(depth)}"'
    return re.sub(r'href="([^"]*)"', repl, markup)


FAQ_HEAD = re.compile(r"<h2>([^<]*(?:Συχνές ερωτήσεις|Συχνές Ερωτήσεις|FAQ)[^<]*)</h2>", re.I)


def split_faq(markup):
    m = FAQ_HEAD.search(markup)
    if not m:
        return markup, None, []
    before, rest = markup[:m.start()], markup[m.end():]
    pairs = []
    for h in re.finditer(r"<h3>(.*?)</h3>", rest, re.S):
        q = re.sub(r"<[^>]+>", "", h.group(1)).strip()
        nxt = re.search(r"<h3>", rest[h.end():], re.S)
        body = rest[h.end(): h.end() + (nxt.start() if nxt else len(rest))]
        if q and body.strip():
            pairs.append((q, body.strip()))
    if not pairs:
        return markup, None, []
    return before, m.group(1).strip(), pairs


def prose(legacy_slug, depth, drop_faq=True):
    rec = LEGACY.get(legacy_slug)
    if not rec:
        return "", None, []
    body = rec["html"]
    faq_title, pairs = None, []
    if drop_faq:
        body, faq_title, pairs = split_faq(body)
    body = rewrite_links(body, depth)
    body = re.sub(r"<h2>\s*</h2>|<h3>\s*</h3>", "", body)
    return body.strip(), faq_title, pairs


def plain(legacy_slug, limit=None):
    rec = LEGACY.get(legacy_slug)
    if not rec:
        return ""
    t = html.unescape(re.sub(r"<[^>]+>", " ", rec["html"]))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit] if limit else t


SPAMMY = re.compile(r"Τηλ\.?\s*Ραντεβού|Χαμηλό Κόστος|Προσιτ[έή]ς? Τιμ|Super |!{2,}|ΚΛΕΙΣΤΕ ΤΩΡΑ", re.I)


def smart_desc(text, limit=155):
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    parts = [p for p in re.split(r"(?<=[.;!?])\s+", text) if p]
    out = ""
    for part in parts:
        if len(out) + len(part) + 1 <= limit:
            out = (out + " " + part).strip()
            continue
        if len(out) < limit * 0.55:
            room = limit - len(out) - 2
            tail = part[:room].rsplit(" ", 1)[0].rstrip(" ,·—-")
            if tail:
                out = (out + " " + tail).strip() + "…"
        break
    if not out:
        out = text[:limit].rsplit(" ", 1)[0].rstrip(" ,·—-") + "…"
    return out


def meta_desc(legacy_slug, fallback=""):
    rec = LEGACY.get(legacy_slug) or {}
    d = (rec.get("description") or "").strip()
    if not d or SPAMMY.search(d) or d.count("&") > 1:
        d = smart_desc(plain(legacy_slug, 600))
    if not d:
        d = fallback
    return html.escape(d[:158], quote=True)


def seo_title(text, suffix=" | LVRI Athens", cap=70):
    text = text.strip()
    return text if len(text) + len(suffix) > cap else text + suffix


def article_title(slug):
    rec = LEGACY.get(slug) or {}
    t = (rec.get("h1") or rec.get("title") or slug.replace("-", " ")).strip()
    return re.sub(r"\s*\|\s*LVRI.*$", "", t).strip()


def article_date(slug):
    rec = LEGACY.get(slug) or {}
    d = rec.get("date") or []
    if len(d) == 3 and d[0] in MONTHS:
        return f"{d[2]}-{MONTHS[d[0]]}-{int(d[1]):02d}"
    return ""


def article_pretty_date(slug):
    iso = article_date(slug)
    if not iso:
        return ""
    y, m, d = iso.split("-")
    names = ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου",
             "Ιουλίου", "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"]
    return f"{int(d)} {names[int(m) - 1]} {y}"


def read_minutes(legacy_slug):
    words = len(plain(legacy_slug).split())
    return max(1, round(words / 190))
