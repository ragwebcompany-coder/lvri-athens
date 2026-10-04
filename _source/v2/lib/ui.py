# -*- coding: utf-8 -*-
"""Markup layer: head, chrome, overlays, cards, rows, sections.

Design rules for this version, deliberately narrow, so the site reads as
designed rather than generated:
  · one accent colour, taken from the clinic's own uniforms (#4a3ac9)
  · one serif (Literata) for anything that is a title, one grotesk (Inter) for
    everything else
  · no gradients, no glows, no abstract generated artwork
  · real photography where it exists; typography where it does not
"""
import re, os, json, html, struct
from content import (SITE, CONDITIONS, TREATMENTS, ARTICLES, GUIDE_STEPS, RED_FLAGS,
                     KEGEL, CONDS, TREATS, rel, article_title,
                     article_pretty_date, read_minutes, plain, TODAY,
                     ARTICLE_IMAGES, HREFLANG, DOCTOR)
from content import ROOT as _C_ROOT

ASSET_V = "6"

# ── icons ────────────────────────────────────────────────────────────────────
I = {
 "search": '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.6"/><path d="M16.5 16.5 21 21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
 "play": '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>',
 "plus": '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" aria-hidden="true"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "check": '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "left": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" aria-hidden="true"><path d="M14.5 5 8 12l6.5 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "right": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" aria-hidden="true"><path d="M9.5 5 16 12l-6.5 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "close": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true"><path d="M5 3h3.5l1.7 4.2-2.1 1.5a12.5 12.5 0 0 0 6.2 6.2l1.5-2.1L20 14.5V18a2 2 0 0 1-2.2 2A16.8 16.8 0 0 1 3 6.2 2 2 0 0 1 5 3z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="m4 7 8 5.5L20 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.6"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "lock": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="1.6"/></svg>',
 "bookmark": '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" aria-hidden="true"><path d="M6 4h12v17l-6-4-6 4z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
 "sliders": '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" aria-hidden="true"><path d="M4 8h10M18 8h2M4 16h4M12 16h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="16" cy="8" r="2" stroke="currentColor" stroke-width="1.6"/><circle cx="10" cy="16" r="2" stroke="currentColor" stroke-width="1.6"/></svg>',
 "burger": '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
 "ext": '<svg viewBox="0 0 24 24" width="11" height="11" fill="none" aria-hidden="true"><path d="M8 16 16 8M9 8h7v7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5h1.65V3.6c-.29-.04-1.27-.12-2.41-.12-2.39 0-4.02 1.46-4.02 4.13v2.3H7.5V13h2.77v8h3.23z"/></svg>',
 "yt": '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.75-1.77C18.3 5 12 5 12 5s-6.3 0-7.85.43A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.75 1.77C5.7 19 12 19 12 19s6.3 0 7.85-.43a2.5 2.5 0 0 0 1.75-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3-5.2 3z"/></svg>',
}

INVASIVE = {"non": ("Μη επεμβατικό", 1), "minor": ("Ελάχιστα επεμβατικό", 2),
            "surgical": ("Χειρουργικό", 3)}


def hue(seed):
    """Kept so the search index keeps a stable shape; the interface is monochrome."""
    return 250


def lvl_badge(invasive):
    label, n = INVASIVE[invasive]
    return (f'<span class="lvl" data-lvl="{n}"><b aria-hidden="true"><i></i><i></i><i></i></b>'
            f'{label}</span>')


# ── head / chrome ────────────────────────────────────────────────────────────
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&"
         "family=Roboto+Condensed:wght@400;500;700&display=swap")


def head(*, title, desc, depth, canonical, lang="el", jsonld=None, body_class="",
         image=None, og_type="website", noindex=False, preload=None):
    """`image` is the page's own photograph (og:image), `preload` the LCP image
    stem to fetch early, `noindex` keeps utility pages out of the index."""
    r = rel(depth)
    og_dim = _img_size(image) if image else None
    if not og_dim or og_dim[0] < 600:          # too small for a large social card
        image, og_dim = "clinic-team.jpg", _img_size("clinic-team.jpg")
    og_img = f"{SITE['domain']}/assets/img/{image}"
    og_size = (f'<meta property="og:image:width" content="{og_dim[0]}">\n'
               f'<meta property="og:image:height" content="{og_dim[1]}">\n') if og_dim else ""
    robots = ("noindex, follow" if noindex else
              "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    alt = ""
    pair = HREFLANG.get(canonical)
    if pair and not noindex:
        el_url, en_url = pair
        alt = (f'<link rel="alternate" hreflang="el" href="{SITE["domain"]}/{el_url}">\n'
               f'<link rel="alternate" hreflang="en" href="{SITE["domain"]}/{en_url}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{SITE["domain"]}/{el_url}">\n')
    pre = (f'<link rel="preload" as="image" href="{r}assets/img/{preload}.webp" '
           f'type="image/webp" fetchpriority="high">\n') if preload else ""
    ld = ""
    for block in (jsonld or []):
        ld += ('<script type="application/ld+json">'
               + json.dumps(block, ensure_ascii=False, separators=(",", ":"))
               + "</script>\n")
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE['domain']}/{canonical}">
{alt}<link rel="icon" href="{r}assets/img/favicon-144.png" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/img/favicon-144.png">
<meta name="geo.region" content="{SITE['region_iso']}">
<meta name="geo.placename" content="{SITE['locality']}">
<meta name="geo.position" content="{SITE['lat']};{SITE['lng']}">
<meta name="ICBM" content="{SITE['lat']}, {SITE['lng']}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{'el_GR' if lang == 'el' else 'en_GB'}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE['domain']}/{canonical}">
<meta property="og:image" content="{og_img}">
{og_size}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="{r}assets/css/v2.css?v={ASSET_V}">
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');
try{{if(localStorage.getItem('lvri2:motion')==='off')document.documentElement.dataset.motion='off';
if(localStorage.getItem('lvri2:contrast')==='high')document.documentElement.dataset.contrast='high';}}catch(e){{}}</script>
{ld}</head>
<body class="{body_class}" data-depth="{depth}" data-lang="{lang}">
<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a>
'''


NAV = [
    ("therapeies/", "Θεραπείες", "therapeies"),
    ("pathiseis/", "Παθήσεις", "pathiseis"),
    ("odigos-symptomaton/", "Οδηγός συμπτωμάτων", "odigos"),
    ("vinteo/", "Βίντεο", "vinteo"),
    ("gallery/", "Gallery", "gallery"),
    ("arthra/", "Άρθρα", "arthra"),
    ("i-kliniki/", "Η κλινική", "kliniki"),
    ("epikoinonia/", "Επικοινωνία", "epikoinonia"),
]


def wordmark(depth, href=""):
    r = rel(depth)
    return (f'<a class="tb__logo" href="{r}{href}" aria-label="LVRI Athens, αρχική">'
            f'<span class="tb__word">LVRI<em>Athens</em></span></a>')


def topbar(depth, active=""):
    r = rel(depth)
    links = "".join(
        f'<a class="tb__link{" is-on" if slug == active else ""}" href="{r}{href}">{label}</a>'
        for href, label, slug in NAV)
    return f'''<header class="tb" id="topbar" data-at-top="1">
  <div class="tb__in">
    {wordmark(depth)}
    <nav class="tb__nav" aria-label="Κύρια πλοήγηση">{links}</nav>
    <div class="tb__right">
      <button class="tb__ic" type="button" data-open="palette" aria-label="Αναζήτηση, Ctrl ή ⌘ και K">{I['search']}</button>
      <a class="tb__ic" href="{r}i-lista-mou/" aria-label="Η λίστα μου">{I['bookmark']}<span class="tb__badge" data-mylist-count hidden>0</span></a>
      <button class="tb__ic" type="button" data-open="settings" aria-label="Ρυθμίσεις εμφάνισης">{I['sliders']}</button>
      <a class="tb__call" href="tel:{SITE['phone_href']}">{I['phone']}<span>{SITE['phone']}</span></a>
      <button class="btn btn--cta tb__cta" type="button" data-open="book">Ραντεβού</button>
      <button class="tb__ic tb__burger" type="button" data-open="drawer" aria-label="Μενού">{I['burger']}</button>
    </div>
  </div>
  <div class="tb__scan" aria-hidden="true"></div>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="drawer__sheet" role="dialog" aria-modal="true" aria-label="Μενού">
    <button class="drawer__x" type="button" data-close aria-label="Κλείσιμο">{I['close']}</button>
    <nav class="drawer__nav">{links}</nav>
    <a class="btn btn--ghost" href="{r}askiseis-kegel/">Ασκήσεις Kegel</a>
    <a class="btn btn--ghost" href="{r}i-lista-mou/">Η λίστα μου</a>
    <button class="btn btn--cta" type="button" data-open="book">Ζητήστε ραντεβού</button>
    <a class="drawer__tel" href="tel:{SITE['phone_href']}">{I['phone']}<span>{SITE['phone']}</span></a>
  </div>
</div>'''


def credit(lang="el"):
    """Η υπογραφή του κατασκευαστή στο κάτω μέρος κάθε σελίδας. Δικό της μπλοκ,
    όχι χαμένη μέσα στη γραμμή των όρων χρήσης."""
    kicker = "Made by"
    return f'''<div class="wrap ft__by">
    <a href="{SITE['credit']['url']}" rel="noopener" target="_blank">
      <span class="ft__by-mark" aria-hidden="true">A</span>
      <span>
        <span class="ft__by-k">{kicker}</span>
        <span class="ft__by-n">{SITE['credit']['name']}{I['ext']}</span>
      </span>
    </a>
  </div>'''


def footer(depth):
    r = rel(depth)
    hours = "".join(f"<li><span>{d}</span><b>{t}</b></li>" for d, t in SITE["hours"])
    treats = "".join(f'<li><a href="{r}therapeies/{t["slug"]}/">{t["title"]}</a></li>' for t in TREATMENTS)
    conds = "".join(f'<li><a href="{r}pathiseis/{c["slug"]}/">{c["title"]}</a></li>' for c in CONDITIONS)
    return f'''<footer class="ft">
  <div class="wrap ft__grid">
    <div class="ft__brand">
      {wordmark(depth)}
      <p class="ft__tag">{SITE['legal']}. Κοσμητική γυναικολογία και επανορθωτική
        χειρουργική πυέλου στην Αθήνα, από το {SITE['founded']}.</p>
      <div class="ft__soc">
        <a href="{SITE['social']['facebook']}" rel="noopener" target="_blank" aria-label="Facebook">{I['fb']}</a>
        <a href="{SITE['social']['youtube']}" rel="noopener" target="_blank" aria-label="YouTube">{I['yt']}</a>
      </div>
    </div>
    <div><h3>Θεραπείες</h3><ul>{treats}</ul></div>
    <div><h3>Παθήσεις</h3><ul>{conds}</ul></div>
    <div><h3>Εργαλεία</h3><ul>
      <li><a href="{r}odigos-symptomaton/">Οδηγός συμπτωμάτων</a></li>
      <li><a href="{r}askiseis-kegel/">Ασκήσεις Kegel</a></li>
      <li><a href="{r}therapeies/#compare">Σύγκριση θεραπειών</a></li>
      <li><a href="{r}vinteo/">Βίντεο</a></li>
      <li><a href="{r}gallery/">Gallery</a></li>
      <li><a href="{r}i-lista-mou/">Η λίστα μου</a></li>
      <li><a href="{r}dr-mirillas/">Dr. Κ. Μυρίλλας</a></li>
    </ul></div>
    <div class="ft__nap"><h3>Επικοινωνία</h3>
      <ul class="ft__contact">
        <li>{I['pin']}<span>{SITE['address']}<br>{SITE['postcode']}, {SITE['region']}</span></li>
        <li>{I['phone']}<a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
        <li>{I['mail']}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
      </ul>
      <ul class="ft__hours">{hours}</ul>
    </div>
  </div>
  <div class="wrap ft__base">
    <p>© {TODAY[:4]} {SITE['name']} · {SITE['legal']}</p>
    <p><a href="{r}oroi-chrisis/">Όροι χρήσης & απόρρητο</a> · <a href="{r}en/">English</a></p>
  </div>
  <p class="ft__disclaimer">Το περιεχόμενο είναι ενημερωτικό και δεν υποκαθιστά την ιατρική
    εξέταση. Κάθε περιστατικό αξιολογείται ξεχωριστά.</p>
  {credit("el")}
</footer>'''


# ── cards ────────────────────────────────────────────────────────────────────
def _save_btn(item_id, title, url, kind):
    payload = html.escape(json.dumps({"id": item_id, "t": title, "u": url, "k": kind},
                                     ensure_ascii=False), quote=True)
    return (f'<button class="nf-save" type="button" data-save=\'{payload}\' '
            f'aria-label="Προσθήκη στη λίστα μου">{I["plus"]}{I["check"]}</button>')


def save_inline(item_id, title, url, kind, label="Αποθήκευση"):
    payload = html.escape(json.dumps({"id": item_id, "t": title, "u": url, "k": kind},
                                     ensure_ascii=False), quote=True)
    return (f'<button class="btn btn--line save-inline" type="button" '
            f'data-save=\'{payload}\'>{I["plus"]}{I["check"]}<span>{label}</span></button>')


def card_art(title, depth, *, image=None, alt="", w=800, h=600, kicker=""):
    """Real photography when the clinic has it, a typographic title poster when it does
    not. Add an `image` key to the entry in data.py and the photograph takes over,
    the poster is the placeholder, not the design."""
    if image:
        return pic(image, alt or title, w, h, depth)
    return f'''<span class="nf-poster">
        {f'<span class="nf-poster__k">{html.escape(kicker)}</span>' if kicker else ''}
        <span class="nf-poster__t">{html.escape(title)}</span>
        <span class="nf-poster__rule" aria-hidden="true"></span>
      </span>'''


def hero_photo(image, alt, depth):
    """Opening tag for a page hero that carries a photograph behind the title.
    Falls back to the plain hero when the entry has no image yet."""
    if not image:
        return '<section class="page-hero">'
    return (f'<section class="page-hero page-hero--photo">'
            f'<span class="page-hero__bg" aria-hidden="true">'
            f'{pic(image, "", 1200, 900, depth, eager=True)}</span>')


def photo_tile(image, alt, depth, *, kicker, heading, body="", extra_attrs=""):
    """A .tile with a 4:3 photograph on top. Without an image it degrades to the
    plain text tile, so a missing photo never breaks the grid."""
    ph = (f'<span class="tile__ph">{pic(image, alt, 800, 600, depth)}</span>'
          if image else '')
    cls = "tile tile--photo" if image else "tile"
    inner = (f'<span class="tile__n">{kicker}</span>{heading}{body}')
    if image:
        return f'<article class="{cls}"{extra_attrs}>{ph}<span class="tile__body">{inner}</span></article>'
    return f'<article class="{cls}"{extra_attrs}>{inner}</article>'


def _slide(inner, save=""):
    return f'<div class="nf-slide">{inner}{save}</div>'


def treatment_card(t, depth, *, n=None):
    r, m = rel(depth), t["matrix"]
    meta = " · ".join(html.escape(x) for x in (m["setting"], m["sessions"]))
    art = card_art(t['title'], depth, image=t.get('image'), alt=t['title'], kicker=t['short'])
    overlay = (f'<span class="nf-card__overlay">'
               f'<span class="nf-card__kicker">{html.escape(t["short"])}</span>'
               f'<span class="nf-card__title">{html.escape(t["title"])}</span></span>'
               if t.get('image') else '')
    card = f'''<a class="nf-card" href="{r}therapeies/{t['slug']}/">
    <span class="nf-card__img">
      {art}
      <span class="nf-card__badge">{lvl_badge(t['invasive'])}</span>
      {overlay}
    </span>
    <span class="nf-card__panel">
      <p>{meta}</p><span class="btn btn--sm btn--line">Δείτε</span>
    </span>
  </a>'''
    return _slide(card, _save_btn(t['slug'], t['title'], f"therapeies/{t['slug']}/", 'treatment'))


def condition_card(c, depth):
    r = rel(depth)
    num, unit = c["stat"]
    art = card_art(c['title'], depth, image=c.get('image'), alt=c['title'], kicker="Πάθηση")
    overlay = (f'<span class="nf-card__overlay"><span class="nf-card__kicker">Πάθηση</span>'
               f'<span class="nf-card__title">{html.escape(c["title"])}</span></span>'
               if c.get('image') else '')
    card = f'''<a class="nf-card" href="{r}pathiseis/{c['slug']}/">
    <span class="nf-card__img">
      {art}
      <span class="nf-card__stat">{html.escape(num)}</span>
      {overlay}
    </span>
    <span class="nf-card__panel">
      <p>«{html.escape(c['plain'])}»</p><span class="btn btn--sm btn--line">Δείτε</span>
    </span>
  </a>'''
    return _slide(card, _save_btn(c['slug'], c['title'], f"pathiseis/{c['slug']}/", 'condition'))


def article_card(slug, tag, depth):
    r, title = rel(depth), article_title(slug)
    img = ARTICLE_IMAGES.get(slug)
    overlay = (f'<span class="nf-card__overlay"><span class="nf-card__kicker">{html.escape(tag)}</span>'
               f'<span class="nf-card__title">{html.escape(title)}</span></span>'
               if img else '')
    card = f'''<a class="nf-card" href="{r}arthra/{slug}/">
    <span class="nf-card__img">
      {card_art(title, depth, image=img, alt=title, kicker=tag)}
      {overlay}
    </span>
    <span class="nf-card__panel">
      <p>{article_pretty_date(slug)} · {read_minutes(slug)}′</p>
      <span class="btn btn--sm btn--line">Διαβάστε</span>
    </span>
  </a>'''
    return _slide(card, _save_btn(slug, title, f"arthra/{slug}/", 'article'))


def video_time(secs):
    """«8:41» ή «1:03:12», ό,τι χρειάζεται η διάρκεια."""
    h, m, sec = secs // 3600, secs // 60 % 60, secs % 60
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def video_card(v, depth, *, kicker=""):
    """Κάρτα βίντεο. Δεν φορτώνει iframe: μόνο το thumbnail του YouTube, και το
    κλικ ανοίγει τον player σε overlay (js: [data-video])."""
    title, secs, year = v["title"], v.get("secs") or 0, (v.get("date") or "")[:4]
    dur = video_time(secs) if secs else ""
    meta = " · ".join(x for x in (year, dur) if x)
    return _slide(f'''<button class="nf-card nf-card--video" type="button" data-video="{v["id"]}"
    aria-label="Αναπαραγωγή: {html.escape(title, quote=True)}">
    <span class="nf-card__img">
      <img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" alt="{html.escape(title, quote=True)}" loading="lazy"
           decoding="async" width="480" height="360">
      <span class="nf-card__play" aria-hidden="true"><span>{I['play']}</span></span>
      {f'<span class="nf-card__dur">{dur}</span>' if dur else ''}
      <span class="nf-card__overlay">
        <span class="nf-card__kicker">{html.escape(kicker or year or "Βίντεο")}</span>
        <span class="nf-card__title">{html.escape(title)}</span>
      </span>
    </span>
    <span class="nf-card__panel">
      <p>{html.escape(meta)}</p><span class="btn btn--sm btn--line">Παίξτε</span>
    </span>
  </button>''')


def row(*, rid, title, cards, eyebrow="", all_href=None, all_label="Όλα", kind="",
        extra_attrs=""):
    """A Netflix-style rail: title left, arrows right, cards scrolling under it."""
    if not cards:
        return ""
    more = (f'<a class="nf-row__all" href="{all_href}">{all_label}</a>' if all_href else "")
    head = title if not eyebrow else f'{title} <em>{eyebrow}</em>'
    return f'''<section class="nf-row {kind}" data-row id="{rid}" {extra_attrs}>
  <div class="nf-row__head">
    <h2 class="nf-row__title">{head}</h2>
    <div class="nf-row__nav">{more}
      <button class="nf-row__btn row__nav row__nav--l" type="button" aria-label="Προηγούμενα" tabindex="-1">{I['left']}</button>
      <button class="nf-row__btn row__nav row__nav--r" type="button" aria-label="Επόμενα">{I['right']}</button>
    </div>
  </div>
  <div class="nf-row__viewport row__track" tabindex="0" role="list"
       aria-label="{html.escape(re.sub(r'<[^>]+>', '', title))}">
    <div class="nf-row__track">{''.join(cards)}</div>
  </div>
</section>'''


_IMG_DIRS = [d for d in (
    os.path.join(_C_ROOT, "lvri-new", "site", "assets", "img"),   # working tree
    os.path.join(os.path.dirname(_C_ROOT), "assets", "img"),      # deployment repo
    os.path.join(_C_ROOT, "assets", "img"),
) if os.path.isdir(d)]

_DIM_CACHE = {}


def _img_size(name):
    """Intrinsic size of an asset, straight from the file header, no Pillow, so
    build.py keeps its "Python 3 and nothing else" promise. Returns None when the
    file is missing or the format is one we do not parse, and the caller then
    falls back to the nominal size it asked for."""
    if name in _DIM_CACHE:
        return _DIM_CACHE[name]
    size = None
    try:
        path = next(p for p in (os.path.join(d, name) for d in _IMG_DIRS)
                    if os.path.isfile(p))
    except StopIteration:
        _DIM_CACHE[name] = None
        return None
    try:
        with open(path, "rb") as fh:
            head = fh.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                size = struct.unpack(">II", head[16:24])
            elif head[:2] == b"\xff\xd8":                      # JPEG: walk to a SOF marker
                fh.seek(2)
                while True:
                    b = fh.read(1)
                    if not b:
                        break
                    if b != b"\xff":
                        continue
                    while b == b"\xff":
                        b = fh.read(1)
                    marker = b[0]
                    if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                        continue
                    seg = fh.read(2)
                    if len(seg) < 2:
                        break
                    ln = struct.unpack(">H", seg)[0]
                    if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                        d = fh.read(5)
                        size = (struct.unpack(">H", d[3:5])[0], struct.unpack(">H", d[1:3])[0])
                        break
                    fh.seek(ln - 2, 1)
    except OSError:
        size = None
    _DIM_CACHE[name] = size
    return size


def pic(name, alt, w, h, depth, *, sizes="", eager=False):
    r = rel(depth)
    stem = name.rsplit(".", 1)[0]
    real = _img_size(name)
    if real:
        w, h = real
    attrs = (f' width="{w}" height="{h}" alt="{html.escape(alt, quote=True)}"'
             f'{" sizes=" + chr(34) + sizes + chr(34) if sizes else ""}'
             f'{" fetchpriority=" + chr(34) + "high" + chr(34) if eager else " loading=" + chr(34) + "lazy" + chr(34)}'
             f' decoding="async"')
    return (f'<picture><source srcset="{r}assets/img/{stem}.webp" type="image/webp">'
            f'<img src="{r}assets/img/{name}"{attrs}></picture>')


# ── hero ─────────────────────────────────────────────────────────────────────
def billboard(depth):
    r = rel(depth)
    return f'''<section class="hero-section">
  <picture style="display:contents"><source srcset="{r}assets/img/clinic-team.webp" type="image/webp">
  <img class="hero-bg" src="{r}assets/img/clinic-team.jpg" width="1200" height="800"
       alt="Ο Dr. Κωνσταντίνος Μυρίλλας με την ομάδα του LVRI Athens στο ιατρείο στον Βύρωνα" fetchpriority="high"></picture>
  <div class="hero-overlay">
    <div class="hero-content">
      <h1 class="hero-h1"><span class="hero-title"><span>LVRI</span><span>Athens</span></span>
        <span class="hero-subtitle">{html.escape(SITE['home_h1'])}</span></h1>
      <div class="hero-badge-row">
        <span class="hero-badge" aria-hidden="true"><span>ΑΠΟ</span><span>08</span></span>
        <span class="hero-badge-text">Κοσμητική γυναικολογία στην Αθήνα από το {SITE['founded']}</span>
      </div>
      <p class="hero-description">Ακράτεια ούρων, πρόπτωση, ξηρότητα και χαλάρωση κόλπου.
        Πέντε θεραπείες με laser, από μια ανώδυνη συνεδρία στο ιατρείο μέχρι πλήρη
        ανάπλαση στο χειρουργείο.</p>
      <div class="hero-buttons">
        <button class="btn btn--cta" type="button" data-open="book">{I['play']}Ζητήστε ραντεβού</button>
        <a class="btn btn--ghost" href="{r}odigos-symptomaton/">Οδηγός συμπτωμάτων</a>
      </div>
      <a class="hero-pdf" href="{r}assets/docs/lvri-athens.pdf" target="_blank" rel="noopener">
        <span class="hero-pdf__cover">{pic("pdf-lvr-cover.jpg", "", 720, 818, depth)}</span>
        <span class="hero-pdf__body">
          <span class="hero-pdf__k">Το έντυπο του ιατρείου</span>
          <span class="hero-pdf__t">Laser Vaginal Rejuvenation</span>
          <span class="btn btn--cta btn--sm">Διαβάστε το PDF</span>
        </span>
      </a>
    </div>
  </div>
</section>'''


# ── symptom guide ────────────────────────────────────────────────────────────
def scanner_data():
    return {
        "steps": [dict(id=s["id"], type=s["type"], q=s["q"], help=s["help"],
                       options=[dict(id=o[0], label=o[1], w=o[2]) for o in s["options"]])
                  for s in GUIDE_STEPS],
        "conditions": {c["slug"]: dict(title=c["title"], lead=c["lead"], plain=c["plain"],
                                       url=f"pathiseis/{c['slug']}/",
                                       treatments=c["treatments"]) for c in CONDITIONS},
        "treatments": {t["slug"]: dict(title=t["title"], short=t["short"], lead=t["lead"],
                                       url=f"therapeies/{t['slug']}/",
                                       invasive=t["invasive"],
                                       level=INVASIVE[t["invasive"]][0]) for t in TREATMENTS},
        "flags": RED_FLAGS,
    }


def scanner_section(depth):
    steps = "".join(f"<li><b>{html.escape(s['q'])}</b>"
                    f"<span>{html.escape(s['help'] or 'Μία επιλογή.')}</span></li>"
                    for s in GUIDE_STEPS)
    return f'''<section class="sec sec--edge" id="scanner">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Εργαλείο</p>
      <h2>Οδηγός συμπτωμάτων</h2>
      <p class="lede">Τέσσερις ερωτήσεις σε καθημερινή γλώσσα. Στο τέλος βλέπετε με ποιες
        παθήσεις ταιριάζει αυτό που περιγράψατε και ποιες θεραπείες συζητούνται συνήθως.
        Ο υπολογισμός γίνεται στη συσκευή σας. Καμία απάντηση δεν αποστέλλεται.</p>
      <p style="margin-top:1.8rem">
        <button class="btn btn--cta btn--lg" type="button" data-open="scanner">Ξεκινήστε</button>
      </p>
    </div>
    <ol class="steps">{steps}</ol>
  </div>
</section>'''


# ── anatomy ──────────────────────────────────────────────────────────────────
ORGANS = {
    "bladder": ("Ουροδόχος κύστη", "Γεμίζει και αδειάζει. Όταν ο σφιγκτήρας ή η στήριξη χαλαρώσει, εμφανίζεται διαφυγή ούρων ή κυστεοκήλη."),
    "uterus": ("Μήτρα", "Στηρίζεται από συνδέσμους και το πυελικό έδαφος. Όταν αυτά υποχωρούν, κατεβαίνει προς τον κόλπο."),
    "vagina": ("Κόλπος", "Ελαστικός σωλήνας με κολλαγόνο και βλεννογόνο. Χάνει ελαστικότητα με τον τοκετό, την ηλικία και την πτώση οιστρογόνων."),
    "rectum": ("Ορθό", "Πιέζει το οπίσθιο τοίχωμα του κόλπου όταν το πυελικό έδαφος αδυνατίσει: ορθοκήλη."),
    "floor": ("Πυελικό έδαφος", "Το μυϊκό «τραμπολίνο» που κρατά τα όργανα στη θέση τους. Οι ασκήσεις Kegel το γυμνάζουν."),
}


def anatomy_section(depth, svg):
    r = rel(depth)
    picks = "".join(f'<button class="an__pick" type="button" data-organ="{k}">{v[0]}</button>'
                    for k, v in ORGANS.items())
    return f'''<section class="an sec--edge" id="anatomia">
  <div class="wrap an__head">
    <p class="eyebrow">Ανατομία</p>
    <h2>Πλάγια τομή της πυέλου</h2>
    <p class="lede">Πατήστε ένα όργανο, ή γυρίστε τον διακόπτη σε «με χαλάρωση» για να δείτε
      τι αλλάζει όταν το πυελικό έδαφος υποχωρεί.</p>
  </div>
  <div class="wrap an__grid">
    <div class="an__stage" data-default="bladder">
      <div class="an__toggle" role="group" aria-label="Κατάσταση διαγράμματος">
        <button type="button" data-state="normal" aria-pressed="true">Φυσιολογική</button>
        <button type="button" data-state="prolapse" aria-pressed="false">Με χαλάρωση</button>
        <span class="an__thumb" aria-hidden="true"></span>
      </div>
      {svg}
    </div>
    <div class="an__side">
      <div class="an__picks">{picks}</div>
      <div class="an__panel" aria-live="polite"></div>
      <a class="btn btn--ghost btn--sm" href="{r}pathiseis/">Όλες οι παθήσεις</a>
    </div>
  </div>
</section>'''


# ── kegel ────────────────────────────────────────────────────────────────────
def kegel_section(depth, *, compact=False, heading=True):
    progs = "".join(
        f'<button class="kg__prog{" is-on" if i == 0 else ""}" type="button" data-prog="{p["id"]}" '
        f'data-c="{p["contract"]}" data-h="{p["hold"]}" data-r="{p["release"]}" data-reps="{p["reps"]}">'
        f'<b>{p["name"]}</b><span>{p["desc"]}</span>'
        f'<i>{p["contract"]}″ σφίξιμο · {p["hold"]}″ κράτημα · {p["release"]}″ χαλάρωση × {p["reps"]}</i></button>'
        for i, p in enumerate(KEGEL))
    head_html = '''<div class="wrap kg__head">
    <p class="eyebrow">Προπόνηση</p>
    <h2>Ασκήσεις Kegel</h2>
    <p class="lede">Αναφέρονται στα κείμενα του ιατρείου ως πρώτη, μη επεμβατική επιλογή για
      την ακράτεια. Ο μετρητής απλώς κρατά τον ρυθμό.</p>
  </div>''' if heading else ""
    return f'''<section class="kg{' kg--compact' if compact else ''} sec--edge" id="kegel">
  {head_html}
  <div class="wrap kg__grid">
    <div class="kg__progs">{progs}</div>
    <div class="kg__stage">
      <div class="kg__ring" data-phase="idle">
        <svg viewBox="0 0 240 240" aria-hidden="true">
          <circle class="kg__trk" cx="120" cy="120" r="104"/>
          <circle class="kg__bar" cx="120" cy="120" r="104"/>
        </svg>
        <div class="kg__core"><b class="kg__phase">Έτοιμη;</b><span class="kg__count">0</span>
          <i class="kg__rep">0 / 0</i></div>
      </div>
      <div class="kg__acts">
        <button class="btn btn--cta" type="button" data-kegel="toggle">Έναρξη</button>
        <button class="btn btn--ghost" type="button" data-kegel="reset">Μηδενισμός</button>
      </div>
      <p class="kg__log">Ολοκληρωμένες συνεδρίες: <b data-kegel-sessions>0</b>
        <button class="linky" type="button" data-kegel="clear">καθαρισμός</button></p>
      <p class="kg__note">Αν νιώσετε πόνο, σταματήστε. Σε επίμονο πρόβλημα, ζητήστε εκτίμηση.</p>
    </div>
  </div>
</section>'''


# ── comparison ───────────────────────────────────────────────────────────────
ROWS_MATRIX = [("setting", "Πού γίνεται"), ("anesthesia", "Αναισθησία"),
               ("sessions", "Συνεδρίες"), ("duration", "Διάρκεια"),
               ("recovery", "Ανάρρωση"), ("pain", "Πόνος")]


def compare_section(depth):
    r = rel(depth)
    heads = "".join(
        f'<th data-inv="{t["invasive"]}">'
        f'<a href="{r}therapeies/{t["slug"]}/">{html.escape(t["title"])}</a>'
        f'{lvl_badge(t["invasive"])}</th>' for t in TREATMENTS)
    body = ""
    for key, label in ROWS_MATRIX:
        cells = "".join(f'<td data-inv="{t["invasive"]}">{html.escape(t["matrix"][key])}</td>'
                        for t in TREATMENTS)
        body += f'<tr><th scope="row">{label}</th>{cells}</tr>'
    treats_row = "".join(
        f'<td data-inv="{t["invasive"]}"><ul>'
        + "".join(f"<li>{html.escape(x)}</li>" for x in t["treats"]) + "</ul></td>"
        for t in TREATMENTS)
    body += f'<tr class="cmp__treats"><th scope="row">Αντιμετωπίζει</th>{treats_row}</tr>'
    return f'''<section class="cmp sec--edge" id="compare">
  <div class="wrap cmp__head">
    <p class="eyebrow">Σύγκριση</p>
    <h2>Πέντε θεραπείες, δίπλα δίπλα</h2>
    <div class="chips" role="group" aria-label="Φίλτρο επεμβατικότητας">
      <button class="chip is-on" type="button" data-inv="all">Όλες</button>
      <button class="chip" type="button" data-inv="non">Μη επεμβατικές</button>
      <button class="chip" type="button" data-inv="minor">Ελάχιστα επεμβατικές</button>
      <button class="chip" type="button" data-inv="surgical">Χειρουργικές</button>
    </div>
  </div>
  <div class="wrap"><div class="cmp__scroll"><table class="cmp__t">
    <thead><tr><th><span class="vh">Χαρακτηριστικό</span></th>{heads}</tr></thead>
    <tbody>{body}</tbody>
  </table></div></div>
</section>'''


# ── shell strings ────────────────────────────────────────────────────────────
# The clinical copy stays Greek; the interface around it speaks the page's language.
T = {
 "el": dict(
  search_label="Αναζήτηση, Ctrl ή ⌘ και K", search_ph="Πάθηση, θεραπεία, άρθρο ή εντολή…",
  results="Αποτελέσματα", nav="πλοήγηση", open="άνοιγμα", toggle="εναλλαγή",
  guide="Οδηγός συμπτωμάτων", close="Κλείσιμο", back="Πίσω", next="Συνέχεια",
  step="Βήμα", of="από", video="Βίντεο", photo="Φωτογραφία", prev_img="Προηγούμενη",
  next_img="Επόμενη", settings="Ρυθμίσεις εμφάνισης", appearance="Εμφάνιση",
  motion="Κίνηση", motion_h="Μεταβάσεις και εφέ κύλισης.",
  contrast="Υψηλή αντίθεση", contrast_h="Πιο έντονο κείμενο και περιγράμματα.",
  data="Δεδομένα",
  data_note="Η λίστα σας, το ιστορικό ανάγνωσης και οι συνεδρίες Kegel μένουν μόνο σε αυτή τη "
            "συσκευή. Δεν φεύγει τίποτα από τον browser.",
  wipe="Διαγραφή τοπικών δεδομένων",
  bk_kicker="Ραντεβού", bk_title="Ζητήστε μια εκτίμηση",
  bk_intro="Απαντάμε την ίδια ή την επόμενη εργάσιμη. Η φόρμα δεν στέλνει τίποτα μόνη της. "
           "ετοιμάζει ένα email που ελέγχετε πριν φύγει.",
  bk_name="Ονοματεπώνυμο", bk_name_err="Συμπληρώστε το όνομά σας.",
  bk_phone="Τηλέφωνο", bk_phone_err="Χρειαζόμαστε έναν τρόπο να σας βρούμε.",
  bk_email="Email", bk_optional="προαιρετικό",
  bk_topic="Τι θα θέλατε να συζητήσουμε;", bk_unsure="Δεν είμαι σίγουρη",
  bk_date="Προτιμώμενη ημερομηνία", bk_sunday="Την Κυριακή είμαστε κλειστά.",
  bk_time="Προτιμώμενη ώρα", bk_note="Θέλετε να μας πείτε κάτι ακόμη;",
  bk_note_ph="Ό,τι μας βοηθά να προετοιμαστούμε.",
  bk_consent="Συμφωνώ να χρησιμοποιήσετε τα στοιχεία μου για να επικοινωνήσετε μαζί μου. Διάβασα τους",
  bk_consent_link="όρους & την πολιτική απορρήτου", bk_consent_err="Χρειαζόμαστε τη συγκατάθεσή σας.",
  bk_cancel="Άκυρο", bk_send="Ετοιμάστε το email",
  bk_fine="Τίποτα δεν αποθηκεύεται σε αυτόν τον ιστότοπο.",
  ck_body="Κρατάμε μόνο ό,τι χρειάζεται για να λειτουργεί ο ιστότοπος. Τα στατιστικά χρήσης τα "
          "αποφασίζετε εσείς.",
  ck_min="Μόνο τα απαραίτητα", ck_ok="Εντάξει", totop="Επιστροφή στην κορυφή",
  terms_url="oroi-chrisis/",
 ),
 "en": dict(
  search_label="Search, Ctrl or ⌘ and K", search_ph="Condition, treatment, article or command…",
  results="Results", nav="navigate", open="open", toggle="toggle",
  guide="Symptom guide", close="Close", back="Back", next="Continue",
  step="Step", of="of", video="Video", photo="Photo", prev_img="Previous",
  next_img="Next", settings="Display settings", appearance="Appearance",
  motion="Motion", motion_h="Transitions and scroll effects.",
  contrast="High contrast", contrast_h="Stronger text and borders.",
  data="Data",
  data_note="Your list, reading history and Kegel sessions stay on this device only. "
            "Nothing leaves the browser.",
  wipe="Delete local data",
  bk_kicker="Appointment", bk_title="Request a consultation",
  bk_intro="We reply the same or next working day. The form sends nothing by itself. It "
           "prepares an email you check before it goes.",
  bk_name="Full name", bk_name_err="Please tell us your name.",
  bk_phone="Phone", bk_phone_err="We need a way to reach you.",
  bk_email="Email", bk_optional="optional",
  bk_topic="What would you like to discuss?", bk_unsure="I am not sure",
  bk_date="Preferred date", bk_sunday="We are closed on Sundays.",
  bk_time="Preferred time", bk_note="Anything else we should know?",
  bk_note_ph="Whatever helps us prepare for your visit.",
  bk_consent="I agree that you may use my details to contact me. I have read the",
  bk_consent_link="terms & privacy policy", bk_consent_err="We need your consent.",
  bk_cancel="Cancel", bk_send="Prepare the email",
  bk_fine="Nothing is stored on this site.",
  ck_body="We keep only what the site needs to work. Usage statistics are up to you.",
  ck_min="Essential only", ck_ok="Got it", totop="Back to top",
  terms_url="oroi-chrisis/",
 ),
}


# ── overlays ─────────────────────────────────────────────────────────────────
def overlays(depth, lang="el"):
    r = rel(depth)
    t = T.get(lang, T["el"])
    topics = "".join(f'<option value="{html.escape(x["title"])}">{html.escape(x["title"])}</option>'
                     for x in list(TREATMENTS) + list(CONDITIONS))
    hours = "".join(f"<li><span>{d}</span><b>{h}</b></li>"
                    for d, h in (SITE["hours"] if lang == "el" else SITE["hours_en"]))
    addr = SITE["address"] if lang == "el" else SITE["address_en"]
    return f'''
<div class="ov ov--pal" id="palette" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="pal" role="dialog" aria-modal="true" aria-label="{t['search_label']}">
    <div class="pal__bar">{I['search']}
      <input class="pal__in" type="search" placeholder="{t['search_ph']}"
             autocomplete="off" spellcheck="false" aria-label="{t['search_label']}" aria-controls="pal-res">
      <kbd>ESC</kbd></div>
    <div class="pal__res" id="pal-res" role="listbox" aria-label="{t['results']}"></div>
    <div class="pal__foot"><span><kbd>↑</kbd><kbd>↓</kbd> {t['nav']}</span><span><kbd>↵</kbd> {t['open']}</span>
      <span><kbd>⌘</kbd><kbd>K</kbd> {t['toggle']}</span></div>
  </div>
</div>

<div class="ov ov--full" id="scanner-ov" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="sc" role="dialog" aria-modal="true" aria-labelledby="sc-title">
    <header class="sc__top">
      <p class="eyebrow">{t['guide']}</p>
      <h2 id="sc-title" class="sc__q"></h2>
      <div class="sc__bar"><i></i></div>
      <button class="ov__x" type="button" data-close aria-label="{t['close']}">{I['close']}</button>
    </header>
    <div class="sc__body"></div>
    <footer class="sc__foot">
      <button class="btn btn--ghost" type="button" data-sc="back">{t['back']}</button>
      <p class="sc__step">{t['step']} <b>1</b> {t['of']} <b>{len(GUIDE_STEPS)}</b></p>
      <button class="btn btn--cta" type="button" data-sc="next">{t['next']}</button>
    </footer>
  </div>
</div>

<div class="ov ov--full" id="player" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="pl" role="dialog" aria-modal="true" aria-label="{t['video']}">
    <button class="ov__x" type="button" data-close aria-label="{t['close']}">{I['close']}</button>
    <div class="pl__frame"></div>
  </div>
</div>

<div class="ov ov--full" id="lightbox" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="lb" role="dialog" aria-modal="true" aria-label="{t['photo']}">
    <button class="ov__x" type="button" data-close aria-label="{t['close']}">{I['close']}</button>
    <button class="lb__nav lb__nav--l" type="button" aria-label="{t['prev_img']}">{I['left']}</button>
    <figure class="lb__fig"><img alt=""><figcaption></figcaption></figure>
    <button class="lb__nav lb__nav--r" type="button" aria-label="{t['next_img']}">{I['right']}</button>
  </div>
</div>

<div class="ov ov--side" id="settings" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="st" role="dialog" aria-modal="true" aria-label="{t['settings']}">
    <button class="ov__x" type="button" data-close aria-label="{t['close']}">{I['close']}</button>
    <h2>{t['appearance']}</h2>
    <label class="sw"><input type="checkbox" data-pref="motion"><span class="sw__t"></span>
      <span><b>{t['motion']}</b><i>{t['motion_h']}</i></span></label>
    <label class="sw"><input type="checkbox" data-pref="contrast"><span class="sw__t"></span>
      <span><b>{t['contrast']}</b><i>{t['contrast_h']}</i></span></label>
    <h2>{t['data']}</h2>
    <p class="st__note">{t['data_note']}</p>
    <button class="btn btn--ghost btn--sm" type="button" data-wipe>{t['wipe']}</button>
  </div>
</div>

<div class="ov ov--mid" id="book" hidden>
  <div class="ov__scrim" data-close></div>
  <div class="bk" role="dialog" aria-modal="true" aria-labelledby="bk-title">
    <button class="ov__x" type="button" data-close aria-label="{t['close']}">{I['close']}</button>
    <div class="bk__side">
      <p class="eyebrow">{t['bk_kicker']}</p>
      <h2 id="bk-title">{t['bk_title']}</h2>
      <p>{t['bk_intro']}</p>
      <ul class="bk__hours">{hours}</ul>
      <p class="bk__nap">{I['pin']}<span>{addr}, {SITE['postcode']}</span></p>
      <p class="bk__nap">{I['phone']}<a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></p>
    </div>
    <form class="bk__form" novalidate>
      <div class="fld"><label for="bk-name">{t['bk_name']}</label>
        <input id="bk-name" name="name" autocomplete="name" required>
        <p class="err">{t['bk_name_err']}</p></div>
      <div class="fld fld--2">
        <div><label for="bk-phone">{t['bk_phone']}</label>
          <input id="bk-phone" name="phone" type="tel" autocomplete="tel" required>
          <p class="err">{t['bk_phone_err']}</p></div>
        <div><label for="bk-mail">{t['bk_email']} <i>{t['bk_optional']}</i></label>
          <input id="bk-mail" name="email" type="email" autocomplete="email"></div>
      </div>
      <div class="fld"><label for="bk-topic">{t['bk_topic']}</label>
        <select id="bk-topic" name="topic"><option value="">{t['bk_unsure']}</option>{topics}</select></div>
      <div class="fld fld--2">
        <div><label for="bk-date">{t['bk_date']}</label>
          <input id="bk-date" name="date" type="date"><p class="err" data-sunday>{t['bk_sunday']}</p></div>
        <div><label for="bk-time">{t['bk_time']}</label>
          <select id="bk-time" name="time"><option value="">Επιλέξτε ώρα</option></select></div>
      </div>
      <div class="fld"><label for="bk-note">{t['bk_note']}</label>
        <textarea id="bk-note" name="note" rows="3" placeholder="{t['bk_note_ph']}"></textarea></div>
      <label class="chk"><input type="checkbox" name="consent" required><span></span>
        <em>{t['bk_consent']} <a href="{r}{t['terms_url']}">{t['bk_consent_link']}</a>.</em></label>
      <p class="err err--consent">{t['bk_consent_err']}</p>
      <div class="bk__acts">
        <button class="btn btn--ghost" type="button" data-close>{t['bk_cancel']}</button>
        <button class="btn btn--cta" type="submit">{t['bk_send']}</button>
      </div>
      <p class="bk__fine">{I['lock']}{t['bk_fine']}</p>
    </form>
  </div>
</div>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="ck" id="cookie" hidden>
  <div class="ck__in">
    <p><b>Cookies.</b> {t['ck_body']}</p>
    <div class="ck__acts">
      <button class="btn btn--ghost btn--sm" type="button" data-ck="min">{t['ck_min']}</button>
      <button class="btn btn--cta btn--sm" type="button" data-ck="all">{t['ck_ok']}</button>
    </div>
  </div>
</div>

<button class="totop" type="button" aria-label="{t['totop']}" hidden>
  <svg viewBox="0 0 24 24" width="17" height="17" fill="none" aria-hidden="true"><path d="M12 19V6M6 11l6-6 6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>
<div class="progress" aria-hidden="true"><i></i></div>
'''


def tail(depth, *, extra_js="", lang="el"):
    r = rel(depth)
    return f'''{overlays(depth, lang)}
<script src="{r}assets/js/v2.js?v={ASSET_V}" defer></script>
{extra_js}
</body>
</html>'''


# ── small helpers ────────────────────────────────────────────────────────────
def crumbs(items, depth):
    r = rel(depth)
    li, ld = "", []
    for i, (label, href) in enumerate(items):
        ld.append({"@type": "ListItem", "position": i + 1, "name": label,
                   "item": f"{SITE['domain']}/{href or ''}"})
        li += (f'<li aria-current="page">{html.escape(label)}</li>' if href is None
               else f'<li><a href="{r}{href}">{html.escape(label)}</a></li>')
    return (f'<nav class="crumbs" aria-label="Διαδρομή"><ol>{li}</ol></nav>',
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld})


def faq_block(title, pairs, prefix="faq"):
    if not pairs:
        return "", None
    items = "".join(f'''<div class="faq__i" id="{prefix}-{i+1}">
  <button class="faq__q" type="button" aria-expanded="false" aria-controls="{prefix}-{i+1}-a">
    <span>{html.escape(q)}</span><span class="faq__s" aria-hidden="true"></span></button>
  <div class="faq__a" id="{prefix}-{i+1}-a" hidden><div>{a}</div></div>
</div>''' for i, (q, a) in enumerate(pairs))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", " ", a).strip()}}
        for q, a in pairs]}
    return f'''<section class="sec sec--edge">
  <div class="wrap wrap--narrow">
    <p class="eyebrow">Ερωτήσεις</p><h2>{html.escape(title or 'Συχνές ερωτήσεις')}</h2>
    <div class="faq">{items}</div>
  </div>
</section>''', ld


def doctor_panel(depth, lang="el"):
    r = rel(depth)
    k, role, cta = (("Υπεύθυνος ιατρός", DOCTOR["role"], "Βιογραφικό") if lang == "el" else
                    ("Your doctor", DOCTOR["role_en"], "Biography (Greek)"))
    name = DOCTOR["name"] if lang == "el" else DOCTOR["name_en"]
    return f'''<div class="panel panel--doc"><h3>{k}</h3>
  <a class="panel__doc" href="{r}dr-mirillas/">{pic("dr-myrillas.jpg", name, 500, 700, depth)}
    <span><b>{html.escape(name)}</b><br>{html.escape(role)}</span></a>
  <a class="btn btn--ghost btn--sm" href="{r}dr-mirillas/">{cta}</a></div>'''


def cta_band(depth, *, title="Μιλήστε με τον γιατρό",
             text="Μια εκτίμηση δεν δεσμεύει σε τίποτα. Ρωτήστε ό,τι σας απασχολεί."):
    return f'''<section class="band">
  <div class="wrap band__in">
    <div><h2>{html.escape(title)}</h2><p>{html.escape(text)}</p></div>
    <div class="band__acts">
      <button class="btn btn--cta btn--lg" type="button" data-open="book">Ζητήστε ραντεβού</button>
      <a class="btn btn--ghost btn--lg" href="tel:{SITE['phone_href']}">{I['phone']}{SITE['phone']}</a>
    </div>
  </div>
</section>'''
