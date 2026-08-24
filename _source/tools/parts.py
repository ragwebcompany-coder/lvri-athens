# -*- coding: utf-8 -*-
"""Shared markup: head, header, drawer, footer, overlays, icons."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content"))
from data import SITE, CONDITIONS, TREATMENTS

I = {
 "search": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "chev": '<svg class="nav__chev" width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "phone": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 3h3.5l1.7 4.2-2.1 1.5a12.5 12.5 0 006.2 6.2l1.5-2.1L20 14.5V18a2 2 0 01-2.2 2A16.8 16.8 0 013 6.2 2 2 0 015 3z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
 "mail": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.7"/><path d="M4 7l8 5.5L20 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "pin": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.6" stroke="currentColor" stroke-width="1.7"/></svg>',
 "clock": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.7"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "lock": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5" stroke="currentColor" stroke-width="1.8"/><path d="M8 10V7a4 4 0 018 0v3" stroke="currentColor" stroke-width="1.8"/></svg>',
 "play": '<svg width="46" height="46" viewBox="0 0 46 46" fill="none" aria-hidden="true"><circle cx="23" cy="23" r="21" stroke="currentColor" stroke-width="1.6" opacity=".8"/><path d="M19 15.5l12 7.5-12 7.5z" fill="currentColor"/></svg>',
 "pdf": '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 3v5h5" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
 "up": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 19V6M6 11l6-6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "close": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "left": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.5 5L8 12l6.5 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "right": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 5L16 12l-6.5 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "fb": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5h1.65V3.6c-.29-.04-1.27-.12-2.41-.12-2.39 0-4.02 1.46-4.02 4.13v2.3H7.5V13h2.77v8h3.23z"/></svg>',
 "yt": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 00-1.75-1.77C18.3 5 12 5 12 5s-6.3 0-7.85.43A2.5 2.5 0 002.4 7.2 26 26 0 002 12a26 26 0 00.4 4.8 2.5 2.5 0 001.75 1.77C5.7 19 12 19 12 19s6.3 0 7.85-.43a2.5 2.5 0 001.75-1.77A26 26 0 0022 12a26 26 0 00-.4-4.8zM10 15V9l5.2 3-5.2 3z"/></svg>',
 "shield": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3l7.5 3v5.5c0 4.6-3.1 8.5-7.5 9.5-4.4-1-7.5-4.9-7.5-9.5V6L12 3z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
}


def rel(depth):
    return "../" * depth if depth else ""


# UI strings. The clinical copy stays in Greek; the shell speaks the page's language.
T = {
    "el": dict(
        skip="Μετάβαση στο περιεχόμενο", nav_label="Κύρια πλοήγηση",
        clinic="Η κλινική", conditions="Παθήσεις", treatments="Θεραπείες",
        both="Παθήσεις & θεραπείες", guide="Οδηγός συμπτωμάτων", kegel="Ασκήσεις Kegel",
        articles="Άρθρα", gallery="Gallery", contact="Επικοινωνία",
        book="Ραντεβού", search="Αναζήτηση (Ctrl+K)", menu="Μενού", other_lang="EN",
        all_conditions="Όλες οι παθήσεις", compare="Σύγκριση θεραπειών",
        search_ph="Πάθηση, θεραπεία ή άρθρο…", search_hint="Γράψτε τουλάχιστον 2 χαρακτήρες.",
        hours="Ωράριο", terms="Όροι χρήσης & απόρρητο", other_lang_full="English",
        tagline="Κέντρο κοσμητικής γυναικολογίας και επανορθωτικής χειρουργικής πυέλου στην Αθήνα, από το 2008.",
        call="Κλήση", top="Επιστροφή στην κορυφή", close="Κλείσιμο",
        prev="Προηγούμενο", next="Επόμενο", view="Προβολή",
        ck_title="Cookies",
        ck_body="Κρατάμε μόνο ό,τι χρειάζεται για να λειτουργεί ο ιστότοπος. Τα υπόλοιπα τα αποφασίζετε εσείς.",
        ck_need="Απαραίτητα", ck_stats="Στατιστικά χρήσης", ck_always="Πάντα ενεργά",
        ck_save="Αποθήκευση επιλογών", ck_min="Μόνο τα απαραίτητα",
        bk_title="Ζητήστε ραντεβού", bk_sub="Απαντάμε την ίδια ή την επόμενη εργάσιμη.",
        bk_name="Ονοματεπώνυμο", bk_name_err="Συμπληρώστε το όνομά σας.",
        bk_phone="Τηλέφωνο", bk_phone_err="Χρειαζόμαστε έναν τρόπο να σας βρούμε.",
        bk_email="Email", bk_optional="Προαιρετικό.",
        bk_topic="Τι θα θέλατε να συζητήσουμε;", bk_unsure="Δεν είμαι σίγουρη",
        bk_date="Προτιμώμενη ημερομηνία", bk_sunday="Την Κυριακή είμαστε κλειστά.",
        bk_time="Προτιμώμενη ώρα", bk_note="Θέλετε να μας πείτε κάτι ακόμη;",
        bk_note_ph="Ό,τι νομίζετε ότι μας βοηθά να προετοιμαστούμε.",
        bk_consent="Συμφωνώ να χρησιμοποιήσετε τα στοιχεία μου για να επικοινωνήσετε μαζί μου. Διάβασα τους",
        bk_consent_link="όρους & την πολιτική απορρήτου", bk_consent_err="Χρειαζόμαστε τη συγκατάθεσή σας.",
        bk_nostore="Τίποτα δεν αποθηκεύεται εδώ.", bk_cancel="Άκυρο", bk_send="Αποστολή",
    ),
    "en": dict(
        skip="Skip to content", nav_label="Main navigation",
        clinic="The clinic", conditions="Conditions", treatments="Treatments",
        both="Conditions & treatments", guide="Symptom guide", kegel="Kegel exercises",
        articles="Articles", gallery="Gallery", contact="Contact",
        book="Book", search="Search (Ctrl+K)", menu="Menu", other_lang="ΕΛ",
        all_conditions="All conditions", compare="Compare treatments",
        search_ph="Condition, treatment or article…", search_hint="Type at least 2 characters.",
        hours="Opening hours", terms="Terms & privacy", other_lang_full="Ελληνικά",
        tagline="Cosmetic gynaecology and pelvic floor reconstruction in Athens, since 2008.",
        call="Call", top="Back to top", close="Close",
        prev="Previous", next="Next", view="View",
        ck_title="Cookies",
        ck_body="We keep only what the site needs to work. The rest is up to you.",
        ck_need="Essential", ck_stats="Usage statistics", ck_always="Always on",
        ck_save="Save choices", ck_min="Essential only",
        bk_title="Request a consultation", bk_sub="We reply the same or next working day.",
        bk_name="Full name", bk_name_err="Please tell us your name.",
        bk_phone="Phone", bk_phone_err="We need a way to reach you.",
        bk_email="Email", bk_optional="Optional.",
        bk_topic="What would you like to discuss?", bk_unsure="I am not sure",
        bk_date="Preferred date", bk_sunday="We are closed on Sundays.",
        bk_time="Preferred time", bk_note="Anything else we should know?",
        bk_note_ph="Whatever helps us prepare for your visit.",
        bk_consent="I agree that you may use my details to contact me. I have read the",
        bk_consent_link="terms & privacy policy", bk_consent_err="We need your consent.",
        bk_nostore="Nothing is stored on this site.", bk_cancel="Cancel", bk_send="Send",
    ),
}


def head(title, desc, depth, canonical, *, lang="el", alt=None, jsonld=None,
         og_image="assets/img/clinic-team.jpg"):
    b = rel(depth)
    ld = "".join('<script type="application/ld+json">%s</script>'
                 % json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (jsonld or []))
    alt_links = ""
    if alt:
        alt_links = '<link rel="alternate" hreflang="%s" href="%s/%s">' % (
            alt[0], SITE["domain"], alt[1].lstrip("/"))
    return f"""<!doctype html>
<html lang="{lang}" data-base="{b or './'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE['domain']}/{canonical.lstrip('/')}">
<link rel="alternate" hreflang="{lang}" href="{SITE['domain']}/{canonical.lstrip('/')}">{alt_links}
<meta name="theme-color" content="#0b1038">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="{'el_GR' if lang == 'el' else 'en_GB'}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE['domain']}/{canonical.lstrip('/')}">
<meta property="og:image" content="{SITE['domain']}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{b}assets/img/favicon-144.png" sizes="144x144">
<link rel="apple-touch-icon" href="{b}assets/img/favicon-144.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Commissioner:wght@300..700&amp;family=GFS+Didot&amp;display=swap">
<link rel="stylesheet" href="{b}assets/css/lvri.css">
<script>document.documentElement.className+=" js";</script>
{ld}</head>"""


def search_overlay(lang="el"):
    t = T[lang]
    return f"""<div class="search" role="dialog" aria-modal="true" aria-label="{t['search']}" aria-hidden="true">
  <div class="search__panel">
    <div class="search__field">{I['search']}
      <label class="vh" for="search-input">{t['search']}</label>
      <input id="search-input" type="search" placeholder="{t['search_ph']}" autocomplete="off">
      <button class="search__kbd" data-search-close>ESC</button>
    </div>
    <div class="search__results" id="search-results">
      <p class="search__empty">{t['search_hint']}</p>
    </div>
  </div>
</div>"""


def drawer(depth, lang="el"):
    b, t = rel(depth), T[lang]
    if lang == "en":
        links = "".join(f'<div class="drawer__group"><a class="drawer__top" href="{b}en/{s}/">{n}</a></div>'
                        for s, n in EN_NAV)
        return f"""<div class="drawer" id="drawer">
  <div class="drawer__group"><a class="drawer__top" href="{b}en/">LVRI Athens</a></div>
  {links}
  <div class="drawer__group"><a class="drawer__top" href="{b}">{t['other_lang_full']}</a></div>
  <div class="drawer__cta">
    <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
  </div>
</div>"""
    conds = "".join(f'<a href="{b}pathiseis/{c["slug"]}/">{c["title"]}</a>' for c in CONDITIONS)
    treats = "".join(f'<a href="{b}therapeies/{x["slug"]}/">{x["title"]}</a>' for x in TREATMENTS)
    return f"""<div class="drawer" id="drawer">
  <div class="drawer__group"><a class="drawer__top" href="{b}i-kliniki/">{t['clinic']}</a></div>
  <div class="drawer__group">
    <button class="drawer__top" aria-expanded="false">{t['conditions']} {I['chev']}</button>
    <div class="drawer__panel"><a href="{b}pathiseis/">{t['all_conditions']}</a>{conds}</div>
  </div>
  <div class="drawer__group">
    <button class="drawer__top" aria-expanded="false">{t['treatments']} {I['chev']}</button>
    <div class="drawer__panel"><a href="{b}therapeies/">{t['compare']}</a>{treats}</div>
  </div>
  <div class="drawer__group"><a class="drawer__top" href="{b}odigos-symptomaton/">{t['guide']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}askiseis-kegel/">{t['kegel']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}arthra/">{t['articles']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}gallery/">{t['gallery']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}epikoinonia/">{t['contact']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}en/">{t['other_lang_full']}</a></div>
  <div class="drawer__cta">
    <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
  </div>
</div>"""


EN_NAV = [("the-clinic", "The Clinic"), ("urinary-incontinence", "Urinary Incontinence"),
          ("vaginal-atrophy", "Vaginal Atrophy"), ("vaginal-dryness", "Vaginal Dryness"),
          ("vaginal-tightening-laser", "Vaginal Tightening"),
          ("designer-laser-vaginoplasty", "Designer Laser Vaginoplasty")]


def header(depth, active="", lang="el"):
    b, t = rel(depth), T[lang]
    cur = lambda k: ' aria-current="page"' if active == k else ""
    if lang == "en":
        items = "".join(
            f'<div class="nav__item"><a class="nav__link" href="{b}en/{s}/"{cur(s)}>{n}</a></div>'
            for s, n in EN_NAV[:4])
        nav = f"""<nav class="nav" aria-label="{t['nav_label']}">
        <div class="nav__item"><a class="nav__link" href="{b}en/"{cur('home')}>LVRI Athens</a></div>
        {items}
      </nav>"""
        lang_link = f'<a class="lang" href="{b}" hreflang="el">{t["other_lang"]}</a>'
    else:
        conds = "".join(
            f'<a class="mega__link" href="{b}pathiseis/{c["slug"]}/"><b>{c["title"]}</b>'
            f'<span>{c["plain"]}</span></a>' for c in CONDITIONS)
        treats = "".join(
            f'<a class="mega__link" href="{b}therapeies/{x["slug"]}/"><b>{x["title"]}</b>'
            f'<span>{x["short"]}</span></a>' for x in TREATMENTS)
        nav = f"""<nav class="nav" aria-label="{t['nav_label']}">
        <div class="nav__item"><a class="nav__link" href="{b}i-kliniki/"{cur('clinic')}>{t['clinic']}</a></div>
        <div class="nav__item" data-mega>
          <button class="nav__link" aria-expanded="false">{t['both']} {I['chev']}</button>
          <div class="mega">
            <div class="mega__col"><p class="mega__title">{t['conditions']}</p>{conds}</div>
            <div class="mega__col"><p class="mega__title">{t['treatments']}</p>{treats}</div>
          </div>
        </div>
        <div class="nav__item"><a class="nav__link" href="{b}odigos-symptomaton/"{cur('guide')}>{t['guide']}</a></div>
        <div class="nav__item"><a class="nav__link" href="{b}arthra/"{cur('articles')}>{t['articles']}</a></div>
        <div class="nav__item nav__item--optional"><a class="nav__link" href="{b}gallery/"{cur('gallery')}>{t['gallery']}</a></div>
        <div class="nav__item"><a class="nav__link" href="{b}epikoinonia/"{cur('contact')}>{t['contact']}</a></div>
      </nav>"""
        lang_link = f'<a class="lang" href="{b}en/" hreflang="en">{t["other_lang"]}</a>'

    return f"""<a class="skip" href="#main">{t['skip']}</a>
<header class="header">
  <div class="wrap header__bar">
    <a class="brand" href="{(b + 'en/') if lang == 'en' else (b or './')}">
      <img src="{b}assets/img/logo.png" alt="{SITE['legal']}" width="148" height="46"></a>
    {nav}
    <div class="header__tools">
      <button class="icon-btn" data-search-open aria-label="{t['search']}">{I['search']}</button>
      {lang_link}
      <button class="btn btn--sm" data-book-open>{t['book']}</button>
      <button class="icon-btn burger" aria-label="{t['menu']}" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span><span></span></button>
    </div>
  </div>
</header>
{drawer(depth, lang)}
{search_overlay(lang)}"""


def footer(depth, lang="el"):
    b, t = rel(depth), T[lang]
    rows = SITE["hours_en"] if lang == "en" else SITE["hours"]
    hours = "".join(f"<div><span>{a}</span><span>{c}</span></div>" for a, c in rows)
    if lang == "en":
        col1 = "".join(f'<li><a href="{b}en/{s}/">{n}</a></li>' for s, n in EN_NAV[:3])
        col2 = "".join(f'<li><a href="{b}en/{s}/">{n}</a></li>' for s, n in EN_NAV[3:])
        h1, h2 = t["conditions"], t["treatments"]
        addr = SITE["address_en"]
    else:
        col1 = "".join(f'<li><a href="{b}pathiseis/{c["slug"]}/">{c["title"]}</a></li>' for c in CONDITIONS)
        col2 = "".join(f'<li><a href="{b}therapeies/{x["slug"]}/">{x["title"]}</a></li>' for x in TREATMENTS)
        h1, h2 = t["conditions"], t["treatments"]
        addr = SITE["address"]
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="{b}assets/img/logo.png" alt="{SITE['legal']}" width="168" height="53" loading="lazy">
        <p class="small" style="margin-top:1.1rem;max-width:34ch;color:#a7afd0">{t['tagline']}</p>
        <div class="socials" style="margin-top:1.5rem">
          <a href="{SITE['social']['facebook']}" rel="noopener" target="_blank" aria-label="Facebook">{I['fb']}</a>
          <a href="{SITE['social']['youtube']}" rel="noopener" target="_blank" aria-label="YouTube">{I['yt']}</a>
        </div>
      </div>
      <div><h4>{h1}</h4><ul>{col1}</ul></div>
      <div><h4>{h2}</h4><ul>{col2}</ul></div>
      <div>
        <h4>{t['contact']}</h4>
        <ul style="margin-bottom:1.6rem">
          <li><a href="{SITE['map']}" rel="noopener" target="_blank">{addr}</a></li>
          <li><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        </ul>
        <h4>{t['hours']}</h4>
        <div class="footer__hours">{hours}</div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2008–2026 {SITE['legal']}</span>
      <span style="display:flex;gap:1.25rem;flex-wrap:wrap">
        <a href="{b}oroi-chrisis/">{t['terms']}</a>
        <a href="{(b + 'en/') if lang == 'el' else b}">{t['other_lang_full']}</a>
      </span>
    </div>
  </div>
</footer>"""


def book_dialog(depth=0, lang="el"):
    b, t = rel(depth), T[lang]
    topics = ([t["bk_unsure"]] + [c["title"] for c in CONDITIONS] + [x["title"] for x in TREATMENTS])
    opts = "".join(f'<option value="{x}">{x}</option>' for x in topics)
    slots = "".join(f'<button type="button" class="slot" aria-pressed="false">{h}:00</button>'
                    for h in ["09", "10", "11", "12", "13", "14", "15", "16"])
    return f"""<dialog class="book" id="book" data-email="{SITE['email']}" data-phone="{SITE['phone_href']}"
  data-lang="{lang}" aria-labelledby="book-title">
  <form class="book__panel" novalidate>
    <div class="book__head">
      <div>
        <h3 id="book-title">{t['bk_title']}</h3>
        <p class="small muted" style="margin-top:.2rem">{t['bk_sub']}</p>
      </div>
      <button type="button" class="icon-btn" data-book-close aria-label="{t['close']}">{I['close']}</button>
    </div>
    <div class="book__body">
      <div class="fields-2">
        <div class="field">
          <label for="book-name">{t['bk_name']}</label>
          <input id="book-name" name="name" required autocomplete="name">
          <span class="field__err">{t['bk_name_err']}</span>
        </div>
        <div class="field">
          <label for="book-phone">{t['bk_phone']}</label>
          <input id="book-phone" name="phone" type="tel" required autocomplete="tel">
          <span class="field__err">{t['bk_phone_err']}</span>
        </div>
      </div>
      <div class="field">
        <label for="book-email">{t['bk_email']}</label>
        <input id="book-email" name="email" type="email" autocomplete="email">
        <span class="field__hint">{t['bk_optional']}</span>
      </div>
      <div class="field">
        <label for="book-topic">{t['bk_topic']}</label>
        <select id="book-topic" name="topic">{opts}</select>
      </div>
      <div class="fields-2">
        <div class="field">
          <label for="book-date">{t['bk_date']}</label>
          <input id="book-date" name="date" type="date">
          <span class="field__hint" data-day-warn hidden>{t['bk_sunday']}</span>
        </div>
        <div class="field">
          <label id="slot-label">{t['bk_time']}</label>
          <div class="slotgrid" data-slots role="group" aria-labelledby="slot-label">{slots}</div>
          <input type="hidden" id="book-slot" name="slot">
        </div>
      </div>
      <div class="field">
        <label for="book-note">{t['bk_note']}</label>
        <textarea id="book-note" name="note" placeholder="{t['bk_note_ph']}"></textarea>
      </div>
      <div class="field">
        <label class="consent">
          <input type="checkbox" name="consent" required>
          <span>{t['bk_consent']} <a href="{b}oroi-chrisis/">{t['bk_consent_link']}</a>.</span>
        </label>
        <span class="field__err">{t['bk_consent_err']}</span>
      </div>
    </div>
    <div class="book__foot">
      <span class="tiny muted" style="display:flex;align-items:center;gap:.4rem">{I['lock']} {t['bk_nostore']}</span>
      <span style="display:flex;gap:.6rem">
        <button type="button" class="btn btn--ghost btn--sm" data-book-close>{t['bk_cancel']}</button>
        <button type="submit" class="btn btn--sm">{t['bk_send']}</button>
      </span>
    </div>
  </form>
</dialog>"""


def overlays(depth=0, lang="el"):
    t = T[lang]
    return f"""<div class="lightbox" role="dialog" aria-modal="true" aria-label="{t['view']}" aria-hidden="true">
  <div class="lightbox__stage-wrap" style="width:min(1100px,100%)">
    <div class="lightbox__bar">
      <span class="small" data-lb-caption></span>
      <span style="display:flex;gap:.5rem">
        <span class="lightbox__nav">
          <button type="button" data-lb-prev aria-label="{t['prev']}">{I['left']}</button>
          <button type="button" data-lb-next aria-label="{t['next']}">{I['right']}</button>
        </span>
        <button type="button" class="lightbox__close" aria-label="{t['close']}">{I['close']}</button>
      </span>
    </div>
    <div class="lightbox__stage"></div>
  </div>
</div>

<div class="cookies" role="region" aria-label="{t['ck_title']}">
  <div>
    <h4 style="margin-bottom:.4rem;text-transform:none;letter-spacing:0;font-size:1rem">{t['ck_title']}</h4>
    <p class="small muted">{t['ck_body']}</p>
  </div>
  <div style="display:grid;gap:.65rem">
    <div class="cookies__toggle"><span>{t['ck_need']}</span>
      <label class="switch"><input type="checkbox" checked disabled><i></i><span class="vh">{t['ck_always']}</span></label></div>
    <div class="cookies__toggle"><span>{t['ck_stats']}</span>
      <label class="switch"><input type="checkbox" id="cookie-analytics"><i></i><span class="vh">{t['ck_stats']}</span></label></div>
  </div>
  <div class="cookies__row">
    <button class="btn btn--sm" data-cookie-accept>{t['ck_save']}</button>
    <button class="btn btn--ghost btn--sm" data-cookie-reject>{t['ck_min']}</button>
  </div>
</div>

<button class="totop" aria-label="{t['top']}">{I['up']}</button>

<div class="actionbar">
  <a class="btn btn--ghost btn--sm" href="tel:{SITE['phone_href']}">{I['phone']} {t['call']}</a>
  <button class="btn btn--sm" data-book-open>{t['book']}</button>
</div>"""


# ── Pelvic-floor diagram ─────────────────────────────────────────────────────
# A schematic sagittal section, drawn for this site. Anterior (pubis) is on the
# left, posterior (sacrum) on the right. Each organ is a focusable hotspot; the
# prolapse toggle shifts the organ groups downward the way the copy describes.
ANATOMY_SVG = """<svg class="anatomy__svg" viewBox="0 0 680 560" role="img"
  aria-label="Σχηματική πλάγια τομή της γυναικείας πυέλου: ουροδόχος κύστη, μήτρα, κόλπος, ορθό και πυελικό έδαφος">
  <defs>
    <linearGradient id="tissue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#dee3f3"/><stop offset="1" stop-color="#bcc5e4"/>
    </linearGradient>
  </defs>

  <!-- Fixed frame: abdominal wall, sacrum, pubic bone, levator sling. -->
  <g id="pf-frame" fill="none" stroke-linecap="round">
    <path d="M198 122c-14 74-8 152 18 226" stroke="#eaedf7" stroke-width="3"/>
    <path d="M456 128c12 62 2 126-34 178l-14 22" stroke="#edeff8" stroke-width="26"/>
    <path d="M456 128c12 62 2 126-34 178l-14 22" stroke="#dfe3f1" stroke-width="1.4"/>
    <ellipse cx="222" cy="350" rx="25" ry="16" fill="#edeff8" stroke="#dfe3f1" stroke-width="1.4" transform="rotate(-24 222 350)"/>
    <path id="pf-floor" d="M228 368c24 84 96 108 166 56" stroke="#b7bfdd" stroke-width="12" opacity=".85"/>
    <circle cx="300" cy="446" r="6" fill="#c6cce7"/>
  </g>

  <!-- Rectum: posterior canal, drawn as a tube. -->
  <g class="hot" id="g-rectum" data-organ="rectum" tabindex="0" role="button"
     aria-label="Ορθό — ορθοκήλη και εντεροκήλη">
    <g class="organ">
      <path class="hot__shape" d="M414 200c6 62-2 112-30 152-14 20-30 38-48 54"
            fill="none" stroke="url(#tissue)" stroke-width="26" stroke-linecap="round"/>
      <path d="M414 200c6 62-2 112-30 152-14 20-30 38-48 54"
            fill="none" stroke="#a5accf" stroke-width="1.2" opacity=".5"/>
    </g>
    <path class="hot__lead" d="M404 300h150" fill="none"/>
    <text class="hot__label" x="562" y="304">Ορθό</text>
    <rect class="hot__hit" x="322" y="184" width="112" height="234"/>
  </g>

  <!-- Uterus: anteverted body plus cervix. -->
  <g class="hot" id="g-uterus" data-organ="uterus" tabindex="0" role="button"
     aria-label="Μήτρα — πρόπτωση μήτρας και κόλπου">
    <g class="organ">
      <path class="hot__shape" d="M342 258l12 34" fill="none"
            stroke="url(#tissue)" stroke-width="24" stroke-linecap="round"/>
      <ellipse class="hot__shape" cx="300" cy="228" rx="60" ry="40"
               transform="rotate(-27 300 228)" fill="url(#tissue)" stroke="#a5accf" stroke-width="1.4"/>
    </g>
    <path class="hot__lead" d="M348 188h206" fill="none"/>
    <text class="hot__label" x="562" y="192">Μήτρα</text>
    <rect class="hot__hit" x="234" y="164" width="140" height="140"/>
  </g>

  <!-- Bladder: anterior to the uterus, with the urethra below it. -->
  <g class="hot" id="g-bladder" data-organ="bladder" tabindex="0" role="button"
     aria-label="Ουροδόχος κύστη — ακράτεια ούρων και κυστεοκήλη">
    <g class="organ">
      <ellipse class="hot__shape" cx="254" cy="302" rx="48" ry="40"
               fill="url(#tissue)" stroke="#a5accf" stroke-width="1.4"/>
      <path class="hot__shape" d="M242 340l-14 52" fill="none"
            stroke="url(#tissue)" stroke-width="10" stroke-linecap="round"/>
    </g>
    <path class="hot__lead" d="M204 302h-72" fill="none"/>
    <text class="hot__label" x="124" y="306" text-anchor="end">Ουροδόχος κύστη</text>
    <rect class="hot__hit" x="204" y="260" width="106" height="140"/>
  </g>

  <!-- Vagina: the canal between bladder and rectum. -->
  <g class="hot" id="g-vagina" data-organ="vagina" tabindex="0" role="button"
     aria-label="Κόλπος — ξηρότητα και χαλάρωση κόλπου">
    <g class="organ">
      <path class="hot__shape" d="M352 296c-14 20-32 38-52 54-16 14-30 28-42 42"
            fill="none" stroke="url(#tissue)" stroke-width="21" stroke-linecap="round"/>
      <path d="M352 296c-14 20-32 38-52 54-16 14-30 28-42 42"
            fill="none" stroke="#a5accf" stroke-width="1.2" opacity=".5"/>
    </g>
    <path class="hot__lead" d="M296 356l-44 62h-120" fill="none"/>
    <text class="hot__label" x="124" y="422" text-anchor="end">Κόλπος</text>
    <rect class="hot__hit" x="248" y="286" width="118" height="118"/>
  </g>

  <g id="pf-floor-label" fill="none">
    <path class="hot__lead" d="M322 458v52h30" stroke-dasharray="3 4"/>
    <text class="hot__label" x="360" y="515" fill="#767c9c">Πυελικό έδαφος</text>
  </g>
</svg>"""


def anatomy_block(depth):
    return f"""<div class="anatomy" id="anatomy" data-default="bladder">
  <div class="anatomy__stage">
    <div class="anatomy__toggle" role="group" aria-label="Κατάσταση διαγράμματος">
      <button type="button" data-state="normal" aria-pressed="true">Φυσιολογική</button>
      <button type="button" data-state="prolapse" aria-pressed="false">Με χαλάρωση</button>
    </div>
    {ANATOMY_SVG}
  </div>
  <div class="anatomy__panel" aria-live="polite"></div>
</div>"""
