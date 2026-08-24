# -*- coding: utf-8 -*-
"""Builds the LVRI Athens static site into lvri-new/site/.

    python3 lvri-new/tools/build.py

Set LVRI_OUT to write somewhere else (e.g. the repo root: LVRI_OUT=.).

Content comes from the clinic's own pages (content/legacy.json, produced by
extract.py) and the editorial structure in content/data.py.
"""
import os, re, sys, json, html, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, HERE)

from data import (SITE, CONDITIONS, TREATMENTS, ARTICLES, GUIDE_STEPS, RED_FLAGS,
                  KEGEL, VIDEOS, EN_PAGES, MONTHS)
import parts
from parts import I, rel, head, header, footer, book_dialog, overlays, anatomy_block

OUT = os.path.abspath(os.environ.get("LVRI_OUT") or os.path.join(ROOT, "site"))
LEGACY = json.load(open(os.path.join(ROOT, "content", "legacy.json"), encoding="utf-8"))
ASSETS = json.load(open(os.path.join(ROOT, "content", "assets.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

# ── URL map ──────────────────────────────────────────────────────────────────
URLMAP = {
    "home": "", "h-kliniki": "i-kliniki/", "dr-k-mirillas": "dr-mirillas/",
    "david-l-matlock": "dr-matlock/", "epikinonia": "epikoinonia/",
    "oroi-chrisis-politiki-aporritou": "oroi-chrisis/", "iatrika-arthra": "arthra/",
    "photo-gallery": "gallery/", "video-gallery": "gallery/",
}
for c in CONDITIONS:
    URLMAP[c["legacy"]] = f"pathiseis/{c['slug']}/"
for t in TREATMENTS:
    URLMAP[t["legacy"]] = f"therapeies/{t['slug']}/"
for slug, _tag in ARTICLES:
    URLMAP.setdefault(slug, f"arthra/{slug}/")
for new, legacy, _t in EN_PAGES:
    URLMAP[legacy] = f"en/{new}/"

# WordPress ?p= ids seen in the legacy copy, resolved from the mirror.
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
# A handful of legacy URLs that the copy links to but that never existed here.
ALIAS = {
    "akrateia-ouron-gynaikeia": "akrateia-ouron",
    "proptosi-kolpou-mitras": "proptosi-mitras",
    "laser-plastiki-kolpou": "laser-kolpou",
}

CONDS = {c["slug"]: c for c in CONDITIONS}
TREATS = {t["slug"]: t for t in TREATMENTS}


def url_for(legacy_slug, depth):
    legacy_slug = ALIAS.get(legacy_slug, legacy_slug)
    target = URLMAP.get(legacy_slug)
    return None if target is None else rel(depth) + target


def rewrite_links(markup, depth):
    """Points the clinic's own copy at the new URLs; leaves outside links alone."""
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
    """Pulls a trailing FAQ section out of the copy so it can become an accordion."""
    m = FAQ_HEAD.search(markup)
    if not m:
        return markup, None, []
    before, rest = markup[:m.start()], markup[m.end():]
    pairs, pos = [], 0
    for h in re.finditer(r"<h3>(.*?)</h3>", rest, re.S):
        q = re.sub(r"<[^>]+>", "", h.group(1)).strip()
        nxt = re.search(r"<h3>", rest[h.end():], re.S)
        body = rest[h.end(): h.end() + (nxt.start() if nxt else len(rest))]
        if q and body.strip():
            pairs.append((q, body.strip()))
        pos = h.end()
    if not pairs:
        return markup, None, []
    return before, m.group(1).strip(), pairs


def faq_block(title, pairs, idx_prefix="faq"):
    if not pairs:
        return "", None
    items = "".join(f"""<div class="faq__item" id="{idx_prefix}-{i+1}">
      <button class="faq__q" type="button" aria-expanded="false" aria-controls="{idx_prefix}-{i+1}-a">
        <span>{html.escape(q)}</span><span class="faq__sign" aria-hidden="true"></span></button>
      <div class="faq__a" id="{idx_prefix}-{i+1}-a" aria-hidden="true"><div>{a}</div></div>
    </div>""" for i, (q, a) in enumerate(pairs))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", " ", a).strip()}}
        for q, a in pairs]}
    return f"""<section class="section section--tight section--mist">
  <div class="wrap wrap--narrow">
    <div class="sec-head"><p class="eyebrow">Ερωτήσεις</p><h2>{html.escape(title or 'Συχνές ερωτήσεις')}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>""", ld


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


def meta_desc(legacy_slug, fallback):
    rec = LEGACY.get(legacy_slug) or {}
    d = (rec.get("description") or "").strip()
    if not d:
        d = plain(legacy_slug, 155)
    return html.escape(d[:158], quote=True) or fallback


def write(path, markup):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(markup)


def page(*, path, title, desc, depth, body, active="", jsonld=None, lang="el",
         alt=None, og_image="assets/img/clinic-team.jpg", extra_js=""):
    markup = (head(title, desc, depth, path or "", lang=lang, alt=alt,
                   jsonld=jsonld, og_image=og_image)
              + f'\n<body>\n<div class="progress" aria-hidden="true"></div>\n'
              + header(depth, active, lang)
              + f'\n<main id="main">\n{body}\n</main>\n'
              + footer(depth, lang) + "\n" + book_dialog(depth, lang) + "\n" + overlays(depth, lang)
              + (f'\n<script>{extra_js}</script>' if extra_js else "")
              + f'\n<script src="{rel(depth)}assets/js/lvri.js" defer></script>\n</body>\n</html>\n')
    write(path + "index.html" if path.endswith("/") or path == "" else path, markup)
    return markup


def seo_title(text, suffix=" | LVRI Athens", cap=70):
    """Keeps the brand suffix only while the title still fits a search result."""
    return text if len(text) + len(suffix) > cap else text + suffix


def img(name, alt, w, h, depth, *, cls="", loading="lazy", priority=False):
    """Serves WebP with the original as fallback."""
    b = rel(depth) + "assets/img/"
    stem = name.rsplit(".", 1)[0]
    extra = ' fetchpriority="high"' if priority else ""
    load = "" if priority else f' loading="{loading}" decoding="async"'
    return (f'<picture><source srcset="{b}{stem}.webp" type="image/webp">'
            f'<img src="{b}{name}" alt="{alt}" width="{w}" height="{h}"'
            f'{load}{extra}{" class=" + chr(34) + cls + chr(34) if cls else ""}></picture>')


def crumbs(items, depth):
    """items: [(label, url_or_None)] — last one is the current page."""
    lis = [f'<li><a href="{rel(depth)}">Αρχική</a></li>']
    for label, url in items:
        lis.append(f'<li><a href="{url}">{label}</a></li>' if url else f"<li>{label}</li>")
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Αρχική", "item": SITE["domain"] + "/"}]}
    for n, (label, url) in enumerate(items, start=2):
        ld["itemListElement"].append({"@type": "ListItem", "position": n, "name": label})
    return f'<ol class="crumbs">{"".join(lis)}</ol>', ld


# ── Reusable blocks ─────────────────────────────────────────────────────────
def cta_band(depth, *, tone="navy"):
    return f"""<section class="section section--{'navy' if tone == 'navy' else 'mist'}">
  <div class="wrap">
    <div class="split" style="align-items:center">
      <div class="stack">
        <p class="eyebrow">Επόμενο βήμα</p>
        <h2>Μια συζήτηση δεν σας δεσμεύει σε τίποτα.</h2>
        <p class="lede">Θα σας εξετάσουμε, θα σας εξηγήσουμε τι βλέπουμε και θα σας πούμε
          ποιες είναι οι επιλογές σας — συμπεριλαμβανομένης της επιλογής να μην κάνετε τίποτα.</p>
      </div>
      <div class="stack" style="justify-items:stretch">
        <button class="btn btn--light btn--block" data-book-open>Ζητήστε ραντεβού</button>
        <a class="btn btn--outline-light btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
        <p class="tiny" style="color:#9aa3c8">{SITE['address']} · Δευτέρα – Παρασκευή 09:00 – 17:00</p>
      </div>
    </div>
  </div>
</section>"""


def guide_section(depth, *, heading=True):
    steps = json.dumps({
        "phone": SITE["phone"], "phoneHref": SITE["phone_href"],
        "steps": [{"id": s["id"], "type": s["type"], "q": s["q"], "help": s["help"],
                   "options": [[o[0], o[1], o[2]] for o in s["options"]]} for s in GUIDE_STEPS],
        "conditions": {c["slug"]: {
            "title": c["title"], "lead": c["lead"], "url": rel(depth) + f"pathiseis/{c['slug']}/",
            "treatments": [{"title": TREATS[t]["title"], "url": rel(depth) + f"therapeies/{t}/"}
                           for t in c["treatments"]]} for c in CONDITIONS},
    }, ensure_ascii=False, separators=(",", ":"))
    head_html = ""
    if heading:
        head_html = f"""<div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Οδηγός συμπτωμάτων</p>
        <h2>Πώς λέγεται αυτό που νιώθετε;</h2>
      </div>
      <p class="lede">Τέσσερις ερωτήσεις σε καθημερινή γλώσσα. Στο τέλος θα ξέρετε ποιον όρο
        να αναζητήσετε και τι συζητάμε συνήθως σε τέτοιες περιπτώσεις.</p>
    </div>"""
    return f"""<section class="section section--mist" id="odigos">
  <div class="wrap">
    {head_html}
    <div class="guide" id="guide" data-reveal>
      <div class="guide__head">
        <div style="display:flex;align-items:center;gap:.65rem">
          {I['shield']}<span class="small" style="font-weight:560;color:var(--navy)">Ιδιωτικός οδηγός</span>
        </div>
        <div class="guide__steps guide__dots" aria-hidden="true"></div>
      </div>
      <div class="guide__body"><p class="muted">Φόρτωση…</p></div>
    </div>
    <p class="tiny muted" style="margin-top:1rem;max-width:60ch">
      Ο οδηγός δεν αντικαθιστά την ιατρική εξέταση και δεν στέλνει τις απαντήσεις σας πουθενά.
      Αν έχετε {" ή ".join("<b>" + f.lower() + "</b>" for f in RED_FLAGS[:2])},
      μη χρησιμοποιήσετε τον οδηγό — καλέστε μας ή απευθυνθείτε σε γιατρό.</p>
  </div>
  <script>window.LVRI_GUIDE={steps};</script>
</section>"""


def anatomy_section(depth):
    by_organ = {}
    for c in CONDITIONS:
        by_organ.setdefault(c["organ"], []).append(c)
    labels = {"bladder": "Ουροδόχος κύστη", "uterus": "Μήτρα", "vagina": "Κόλπος", "rectum": "Ορθό"}
    info = {organ: {"organ": labels[organ], "conditions": [
        {"title": c["title"], "plain": c["plain"], "lead": c["lead"],
         "url": rel(depth) + f"pathiseis/{c['slug']}/",
         "treatments": [{"title": TREATS[t]["title"], "url": rel(depth) + f"therapeies/{t}/"}
                        for t in c["treatments"]]} for c in cs]}
            for organ, cs in by_organ.items()}
    return f"""<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Η ανατομία, χωρίς μυστήρια</p>
        <h2>Τέσσερα όργανα, ένα σύστημα στήριξης.</h2>
      </div>
      <p class="lede">Η ανατομική και λειτουργική ισορροπία του κόλπου στηρίζει το ουροποιητικό,
        το γεννητικό και το πεπτικό σύστημα. Δείτε τι επηρεάζει τι.</p>
    </div>
    {anatomy_block(depth)}
    <p class="anatomy__hint" style="margin-top:1.25rem">
      Επιλέξτε ένα όργανο στο διάγραμμα. Το «Με χαλάρωση» δείχνει σχηματικά την κάθοδο των οργάνων.</p>
  </div>
  <script>window.LVRI_ANATOMY={json.dumps(info, ensure_ascii=False, separators=(",", ":"))};</script>
</section>"""


def kegel_section(depth, *, compact=False):
    progs = json.dumps(KEGEL, ensure_ascii=False, separators=(",", ":"))
    buttons = "".join(
        f"""<button type="button" class="prog-btn" data-prog="{k['id']}" aria-pressed="{str(i == 0).lower()}">
      <span style="display:grid"><b>{k['name']}</b><span>{k['desc']}</span></span>
      <i>{k['contract']}″ σφίξιμο · {k['reps']} επαναλήψεις</i></button>""" for i, k in enumerate(KEGEL))
    return f"""<div class="kegel" id="kegel">
  <div>
    <div class="kegel__stage">
      <svg class="kegel__ring" viewBox="0 0 100 100" aria-hidden="true">
        <circle class="kegel__track" cx="50" cy="50" r="46"/>
        <circle class="kegel__prog" cx="50" cy="50" r="46"/>
      </svg>
      <div class="kegel__orb">
        <div style="display:grid;gap:.3rem;text-align:center">
          <span class="kegel__count" aria-live="off">3</span>
          <span class="kegel__phase" aria-live="polite">Έτοιμη;</span>
        </div>
      </div>
    </div>
  </div>
  <div class="stack" style="justify-items:stretch">
    <div class="kegel__progs">{buttons}</div>
    <div class="kegel__meta">
      <div><b data-kegel-rep>0</b><span class="tiny muted">επαναλήψεις τώρα</span></div>
      <div><b data-kegel-total>0</b><span class="tiny muted">ολοκληρωμένες συνεδρίες</span></div>
    </div>
    <button class="btn" data-kegel-start data-state="idle">Ξεκινήστε</button>
    <p class="tiny muted">Ο μετρητής μένει στη συσκευή σας. Οι ασκήσεις Kegel ενδυναμώνουν τους μύες
      της λεκάνης και βοηθούν κυρίως στην ακράτεια από προσπάθεια. Δεν αντικαθιστούν τη θεραπεία
      των κηλών — για αυτό μιλήστε με γιατρό.</p>
  </div>
  <script>window.LVRI_KEGEL={progs};</script>
</div>"""


def compare_section(depth, *, heading=True):
    rows = ""
    for t in TREATMENTS:
        m = t["matrix"]
        tag = {"non": ("Μη επεμβατική", "non"), "minor": ("Ελάχιστα επεμβατική", "minor"),
               "surgical": ("Χειρουργική", "surgical")}[t["invasive"]]
        rows += f"""<tr data-invasive="{t['invasive']}">
      <td><a href="{rel(depth)}therapeies/{t['slug']}/">{t['title']}</a>
        <div class="tiny muted" style="margin-top:.2rem">{t['short']}</div>
        <div style="margin-top:.5rem"><span class="tag tag--{tag[1]}">{tag[0]}</span></div></td>
      <td>{m['setting']}</td><td>{m['anesthesia']}</td><td>{m['sessions']}</td>
      <td>{m['duration']}</td><td>{m['recovery']}</td></tr>"""
    head_html = ""
    if heading:
        head_html = """<div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Σύγκριση</p><h2>Τι σημαίνει η κάθε θεραπεία στην πράξη.</h2></div>
      <p class="lede">Πόσο κρατάει, τι αναισθησία χρειάζεται, πότε επιστρέφετε στα δικά σας.
        Τα στοιχεία είναι όπως τα περιγράφουμε στους ασθενείς μας.</p>
    </div>"""
    return f"""<section class="section" id="compare">
  <div class="wrap">
    {head_html}
    <div class="compare">
      <div class="compare__filters" role="group" aria-label="Φίλτρα θεραπειών">
        <button class="filter" data-filter="all" aria-pressed="true">Όλες</button>
        <button class="filter" data-filter="non" aria-pressed="false">Μη επεμβατικές</button>
        <button class="filter" data-filter="minor" aria-pressed="false">Ελάχιστα επεμβατικές</button>
        <button class="filter" data-filter="surgical" aria-pressed="false">Χειρουργικές</button>
        <span class="tiny muted" data-compare-count style="align-self:center;margin-left:.5rem">{len(TREATMENTS)} θεραπείες</span>
      </div>
      <div class="compare__scroll">
        <table>
          <caption class="vh">Σύγκριση θεραπειών</caption>
          <thead><tr><th scope="col">Θεραπεία</th><th scope="col">Πού γίνεται</th>
            <th scope="col">Αναισθησία</th><th scope="col">Συνεδρίες</th>
            <th scope="col">Διάρκεια</th><th scope="col">Ανάρρωση</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="tiny muted" style="margin-top:1rem">Κάθε περιστατικό είναι διαφορετικό.
        Το τελικό πλάνο ορίζεται μετά από κλινική εξέταση.</p>
    </div>
  </div>
</section>"""


# ── Home ─────────────────────────────────────────────────────────────────────
def build_home():
    d = 0
    conds = "".join(f"""<a class="card" href="pathiseis/{c['slug']}/" data-reveal="{i*60}">
      <p class="card__kicker">{c['stat'][0]} · {c['stat'][1]}</p>
      <h3>{c['title']}</h3>
      <p>{c['lead']}</p>
      <p class="cond-card__voice">«{c['plain']}»</p>
    </a>""" for i, c in enumerate(CONDITIONS[:3]))

    treats = "".join(f"""<a class="card" href="therapeies/{t['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{t['short']}</p>
      <h3>{t['title']}</h3>
      <p>{t['lead']}</p>
      <p class="card__foot"><span class="link-more">Αναλυτικά</span></p>
    </a>""" for i, t in enumerate(TREATMENTS[:3]))

    latest = ARTICLES[:3]
    art = "".join(f"""<a class="card" href="arthra/{slug}/" data-reveal="{i*60}">
      <p class="card__kicker">{tag}</p>
      <h3>{html.escape(article_title(slug))}</h3>
      <p>{html.escape(plain(slug, 120))}…</p>
    </a>""" for i, (slug, tag) in enumerate(latest))

    creds = [("2008", "Ίδρυση του LVRI Athens μαζί με τον Dr. David Matlock"),
             ("2013", "Επιστημονική διεύθυνση πλαστικής κόλπου, μαιευτήριο ΡΕΑ"),
             ("ACOG · RCOG", "Μέλος Αμερικανικού &amp; Αγγλικού κολλεγίου γυναικολόγων"),
             ("CO₂ &amp; Erbium", "Επεμβατικό και μη επεμβατικό laser στον ίδιο χώρο")]
    creds_html = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in creds)

    body = f"""<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Laser Vaginal Rejuvenation Institute of Athens</p>
      <h1>Υπάρχουν πράγματα που <em>δεν λέγονται</em> εύκολα.</h1>
      <p class="lede">Ακράτεια. Ξηρότητα. Βάρος στην πύελο. Εδώ ακούγονται καθημερινά — και
        αντιμετωπίζονται. Αν δεν ξέρετε πώς να το περιγράψετε, ξεκινήστε από τον οδηγό.</p>
      <div class="hero__actions">
        <a class="btn" href="#odigos">Ξεκινήστε τον οδηγό</a>
        <a class="btn btn--ghost" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
      </div>
      <p class="hero__note">{I['lock']} Οι απαντήσεις σας μένουν στη συσκευή σας.</p>
    </div>
    <div class="hero__figure" data-reveal="120">
      {img("dr-myrillas.jpg", "Ο Dr. Κωνσταντίνος Μυρίλλας στο LVRI Athens", 500, 700, 0, priority=True)}
      <div class="hero__badge">
        <b>{SITE['founded']}</b>
        <span>Το πρώτο LVRI στην Ελλάδα, με τα πρωτόκολλα του LVRI Los Angeles</span>
      </div>
    </div>
  </div>
</section>

<section class="creds">
  <div class="wrap"><ul class="creds__list">{creds_html}</ul></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Παθήσεις</p>
        <h2>Τρία στα τέσσερα ραντεβού ξεκινούν από μία από αυτές.</h2>
      </div>
      <p class="lede">Διαβάστε τι είναι, γιατί συμβαίνει και τι γίνεται γι' αυτό —
        γραμμένο ώστε να το καταλάβετε πριν μπείτε στο ιατρείο.</p>
    </div>
    <div class="grid grid--3">{conds}</div>
    <p style="margin-top:2rem"><a class="link-more" href="pathiseis/">Όλες οι παθήσεις</a></p>
  </div>
</section>

{anatomy_section(d)}

{guide_section(d)}

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Θεραπείες</p>
        <h2>Από 15 λεπτά στο ιατρείο, μέχρι πλήρη ανάπλαση.</h2></div>
      <p class="lede">Δεν χρειάζονται όλες οι γυναίκες χειρουργείο. Ξεκινάμε πάντα από
        την πιο ήπια επιλογή που λύνει πραγματικά το πρόβλημα.</p>
    </div>
    <div class="grid grid--3">{treats}</div>
    <p style="margin-top:2rem"><a class="link-more" href="therapeies/">Συγκρίνετε όλες τις θεραπείες</a></p>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="split split--wide-left">
      <div class="frame" data-reveal>
        {img("clinic-team.jpg", "Η ομάδα του LVRI Athens", 1600, 1067, 0)}
      </div>
      <div class="stack">
        <p class="eyebrow">Η ομάδα</p>
        <h2>Γυναικολόγοι, πλαστικοί χειρουργοί και δερματολόγοι στο ίδιο τραπέζι.</h2>
        <p class="lede">Το γυναικείο γεννητικό σύστημα απασχολεί πολλές ειδικότητες.
          Το LVRI Athens δημιουργήθηκε για να μη χρειάζεται να τις κυνηγάτε μία-μία.</p>
        <div class="pill-row">
          <a class="chip" href="dr-mirillas/">Dr. Κωνσταντίνος Μυρίλλας</a>
          <a class="chip" href="dr-matlock/">Dr. David L. Matlock</a>
          <a class="chip" href="i-kliniki/">Η κλινική</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Πυελικό έδαφος</p>
        <h2>Ξεκινήστε από κάτι που μπορείτε να κάνετε απόψε.</h2></div>
      <p class="lede">Οι ασκήσεις Kegel είναι η πρώτη γραμμή για την ακράτεια από προσπάθεια.
        Ο μετρητής σας κρατά τον ρυθμό — δωρεάν, χωρίς εγγραφή.</p>
    </div>
    {kegel_section(d)}
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Άρθρα</p><h2>Από το ιατρείο, γραπτώς.</h2></div>
      <p class="lede">Ό,τι εξηγούμε συχνότερα, γραμμένο μία φορά καλά.</p>
    </div>
    <div class="grid grid--3">{art}</div>
    <p style="margin-top:2rem"><a class="link-more" href="arthra/">Όλα τα άρθρα</a></p>
  </div>
</section>

{cta_band(d)}"""

    ld = [{"@context": "https://schema.org", "@type": "MedicalClinic",
           "@id": SITE["domain"] + "/#clinic", "name": SITE["legal"], "alternateName": SITE["name"],
           "url": SITE["domain"] + "/", "telephone": "+30 210 7609109", "email": SITE["email"],
           "foundingDate": SITE["founded"],
           "image": SITE["domain"] + "/assets/img/clinic-team.jpg",
           "medicalSpecialty": ["Gynecologic", "PlasticSurgery", "Urologic"],
           "address": {"@type": "PostalAddress", "streetAddress": "Καραολή & Δημητρίου 41",
                       "addressLocality": "Βύρωνας", "postalCode": SITE["postcode"],
                       "addressRegion": "Αττική", "addressCountry": "GR"},
           "openingHoursSpecification": [
               {"@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "09:00", "closes": "17:00"},
               {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday",
                "opens": "09:00", "closes": "15:00"}],
           "sameAs": [SITE["social"]["facebook"], SITE["social"]["youtube"]]},
          {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
           "url": SITE["domain"] + "/", "inLanguage": "el"}]

    page(path="", title="LVRI Athens — Κοσμητική γυναικολογία & χειρουργική πυελικού εδάφους",
         desc="Ακράτεια ούρων, πρόπτωση, ξηρότητα κόλπου. Laser και χειρουργικές λύσεις στην Αθήνα, "
              "από το 2008. Ξεκινήστε από τον οδηγό συμπτωμάτων.",
         depth=0, body=body, jsonld=ld, alt=("en", "en/"),
         og_image="assets/img/dr-myrillas.jpg")


def article_title(slug):
    rec = LEGACY.get(slug) or {}
    t = (rec.get("h1") or rec.get("title") or slug).split(" | ")[0]
    return html.unescape(t).strip()


def article_date(slug):
    rec = LEGACY.get(slug) or {}
    d = rec.get("date")
    if not d:
        return "2022-01-01", "2022"
    mon, day, year = d
    return f"{year}-{MONTHS.get(mon, '01')}-{int(day):02d}", f"{day} {mon} {year}"


# ── Condition & treatment pages ─────────────────────────────────────────────
def related_strip(depth, treat_slugs, title="Σχετικές θεραπείες"):
    if not treat_slugs:
        return ""
    cards = "".join(f"""<a class="card" href="{rel(depth)}therapeies/{s}/">
      <p class="card__kicker">{TREATS[s]['short']}</p><h3>{TREATS[s]['title']}</h3>
      <p>{TREATS[s]['lead']}</p></a>""" for s in treat_slugs if s in TREATS)
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">{title}</p></div>
    <div class="grid grid--{min(len(treat_slugs), 3)}">{cards}</div>
  </div>
</section>"""


def doc_layout(depth, body_html, aside_html=""):
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="doc">
      <article class="prose">{body_html}</article>
      <aside class="doc__aside" data-toc-wrap>
        <div>
          <p class="eyebrow" style="margin-bottom:.9rem">Σε αυτή τη σελίδα</p>
          <nav class="toc" aria-label="Περιεχόμενα"></nav>
        </div>
        {aside_html}
      </aside>
    </div>
  </div>
</section>"""


def aside_cta(depth):
    return f"""<div class="card" style="background:var(--mist-2);border-color:transparent">
  <h3 style="font-size:1.05rem">Έχετε ερώτηση;</h3>
  <p class="small">Δεν χρειάζεται να ξέρετε τι να ρωτήσετε. Πείτε μας τι νιώθετε.</p>
  <button class="btn btn--sm btn--block" data-book-open>Ζητήστε ραντεβού</button>
  <a class="btn btn--ghost btn--sm btn--block" href="tel:{SITE['phone_href']}">{SITE['phone']}</a>
</div>"""


def build_condition(c):
    d, slug = 2, c["slug"]
    body, faq_title, pairs = prose(c["legacy"], d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Παθήσεις", rel(d) + "pathiseis/"), (c["title"], None)], d)
    head_block = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack">
        <p class="eyebrow">{c['stat'][0]} · {c['stat'][1]}</p>
        <h1>{c['title']}</h1>
      </div>
      <div class="stack">
        <p class="voice">{c['plain']}</p>
        <p class="lede" style="font-size:1rem">{c['lead']}</p>
      </div>
    </div>
  </div>
</section>"""
    ld = [crumb_ld, {"@context": "https://schema.org", "@type": "MedicalWebPage",
                     "name": c["title"], "inLanguage": "el",
                     "url": f"{SITE['domain']}/pathiseis/{slug}/",
                     "about": {"@type": "MedicalCondition", "name": c["title"]},
                     "publisher": {"@id": SITE["domain"] + "/#clinic"}}]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"pathiseis/{slug}/",
         title=seo_title(f"{c['title']} — συμπτώματα, αίτια & θεραπεία"),
         desc=meta_desc(c["legacy"], c["lead"][:150]), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html
              + related_strip(d, c["treatments"]) + cta_band(d),
         jsonld=ld)


def build_treatment(t):
    d, slug = 2, t["slug"]
    body, faq_title, pairs = prose(t["legacy"], d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Θεραπείες", rel(d) + "therapeies/"), (t["title"], None)], d)
    m = t["matrix"]
    facts = [("Πού γίνεται", m["setting"]), ("Αναισθησία", m["anesthesia"]),
             ("Συνεδρίες", m["sessions"]), ("Διάρκεια", m["duration"]),
             ("Ανάρρωση", m["recovery"]), ("Πόνος", m["pain"])]
    facts_html = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in facts)
    treats_html = "".join(f'<span class="chip">{x}</span>' for x in t["treats"])
    head_block = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack">
        <p class="eyebrow">{t['short']}</p>
        <h1>{t['title']}</h1>
      </div>
      <div class="stack">
        <p class="lede" style="font-size:1.06rem">{t['lead']}</p>
        <div class="pill-row">{treats_html}</div>
      </div>
    </div>
  </div>
</section>

<section class="creds">
  <div class="wrap"><ul class="creds__list" style="grid-template-columns:repeat(2,1fr)">{facts_html}</ul></div>
</section>"""
    ld = [crumb_ld, {"@context": "https://schema.org", "@type": "MedicalProcedure",
                     "name": t["title"], "description": t["lead"],
                     "url": f"{SITE['domain']}/therapeies/{slug}/",
                     "provider": {"@id": SITE["domain"] + "/#clinic"}}]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"therapeies/{slug}/",
         title=seo_title(f"{t['title']} — {t['short']}"),
         desc=meta_desc(t["legacy"], t["lead"][:150]), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html + cta_band(d),
         jsonld=ld)


def build_article(slug, tag):
    d = 2
    title = article_title(slug)
    iso, human = article_date(slug)
    body, faq_title, pairs = prose(slug, d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Άρθρα", rel(d) + "arthra/"), (title, None)], d)
    others = [(s, tg) for s, tg in ARTICLES if s != slug and tg == tag][:2] \
             or [(s, tg) for s, tg in ARTICLES if s != slug][:2]
    more = "".join(f"""<a class="card" href="{rel(d)}arthra/{s}/">
      <p class="card__kicker">{tg}</p><h3>{html.escape(article_title(s))}</h3></a>""" for s, tg in others)
    head_block = f"""<section class="page-head">
  <div class="wrap wrap--narrow">
    {crumb_html}
    <p class="eyebrow">{tag} · <time datetime="{iso}">{human}</time></p>
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.4vw,3rem);margin-top:.75rem">{html.escape(title)}</h1>
  </div>
</section>"""
    ld = [crumb_ld, {"@context": "https://schema.org", "@type": "Article",
                     "headline": title, "datePublished": iso, "dateModified": iso,
                     "inLanguage": "el", "articleSection": tag,
                     "author": {"@type": "Person", "name": "Dr. Κωνσταντίνος Μυρίλλας"},
                     "publisher": {"@id": SITE["domain"] + "/#clinic"},
                     "mainEntityOfPage": f"{SITE['domain']}/arthra/{slug}/"}]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"arthra/{slug}/", title=seo_title(title),
         desc=meta_desc(slug, title), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html + f"""
<section class="section section--tight section--mist">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Διαβάστε επίσης</p></div>
    <div class="grid grid--2">{more}</div>
  </div>
</section>""" + cta_band(d), jsonld=ld, active="articles")


# ── Hubs ─────────────────────────────────────────────────────────────────────
def build_conditions_hub():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}pathiseis/{c['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{c['stat'][0]} · {c['stat'][1]}</p>
      <h3>{c['title']}</h3><p>{c['lead']}</p>
      <p class="cond-card__voice">«{c['plain']}»</p></a>""" for i, c in enumerate(CONDITIONS))
    crumb_html, crumb_ld = crumbs([("Παθήσεις", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Παθήσεις</p>
        <h1>Πέντε καταστάσεις που μοιράζονται ένα σύστημα στήριξης.</h1></div>
      <p class="lede">Σπάνια έρχονται μόνες τους. Γι' αυτό εξετάζουμε ολόκληρο το πυελικό
        έδαφος, όχι μόνο το σύμπτωμα που σας έφερε εδώ.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="grid grid--3">{cards}</div></div></section>
{anatomy_section(d)}
{guide_section(d)}
{cta_band(d)}"""
    page(path="pathiseis/", title="Παθήσεις πυελικού εδάφους | LVRI Athens",
         desc="Ακράτεια ούρων, πρόπτωση μήτρας, ξηρότητα κόλπου, κυστεοκήλη, ορθοκήλη. "
              "Τι είναι, γιατί συμβαίνουν και πώς αντιμετωπίζονται.",
         depth=d, body=body, jsonld=[crumb_ld])


def build_treatments_hub():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}therapeies/{t['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{t['short']}</p><h3>{t['title']}</h3><p>{t['lead']}</p>
      <p class="card__foot"><span class="link-more">Αναλυτικά</span></p></a>"""
      for i, t in enumerate(TREATMENTS))
    crumb_html, crumb_ld = crumbs([("Θεραπείες", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Θεραπείες</p>
        <h1>Η πιο ήπια λύση που πραγματικά δουλεύει.</h1></div>
      <p class="lede">Ξεκινάμε από το ιατρείο και προχωράμε στο χειρουργείο μόνο όταν χρειάζεται.
        Δείτε τι σημαίνει η καθεμία σε χρόνο, αναισθησία και ανάρρωση.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="grid grid--3">{cards}</div></div></section>
{compare_section(d)}
{cta_band(d)}"""
    page(path="therapeies/", title="Θεραπείες — σύγκριση | LVRI Athens",
         desc="Laser αναζωογόνηση, G-Shot, αιδοιοπλαστική, laser πλαστική κόλπου, χειρουργική "
              "πυελικού εδάφους. Συγκρίνετε αναισθησία, διάρκεια και ανάρρωση.",
         depth=d, body=body, jsonld=[crumb_ld], active="treatments")


def build_articles_hub():
    d = 1
    tags = []
    for _s, t in ARTICLES:
        if t not in tags:
            tags.append(t)
    filters = '<button class="filter" data-tag-filter="all" aria-pressed="true">Όλα</button>' + "".join(
        f'<button class="filter" data-tag-filter="{t}" aria-pressed="false">{t}</button>' for t in tags)
    rows = ""
    for slug, tag in ARTICLES:
        title = article_title(slug)
        iso, human = article_date(slug)
        excerpt = html.escape(plain(slug, 150))
        needle = html.escape((title + " " + tag + " " + plain(slug, 400)).lower(), quote=True)
        rows += f"""<a class="article-row" href="{rel(d)}arthra/{slug}/" data-tag="{tag}" data-search="{needle}">
      <time datetime="{iso}">{human}</time>
      <div><h3>{html.escape(title)}</h3><p>{excerpt}…</p></div>
      <span class="chip">{tag}</span></a>"""
    crumb_html, crumb_ld = crumbs([("Άρθρα", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Άρθρα</p><h1>Από το ιατρείο, γραπτώς.</h1></div>
      <p class="lede">{len(ARTICLES)} κείμενα για ό,τι εξηγούμε συχνότερα. Χωρίς ιατρική ορολογία
        εκεί που δεν χρειάζεται.</p>
    </div>
  </div>
</section>
<section class="section section--tight" id="articles">
  <div class="wrap">
    <div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between;margin-bottom:2rem">
      <div class="compare__filters" style="margin:0">{filters}</div>
      <label class="searchbar">{I['search']}
        <span class="vh">Αναζήτηση στα άρθρα</span>
        <input type="search" placeholder="Αναζήτηση στα άρθρα…" data-article-search autocomplete="off"></label>
    </div>
    <div class="article-list">{rows}</div>
    <p class="empty" data-article-empty hidden>Δεν βρέθηκε άρθρο με αυτά τα κριτήρια.</p>
  </div>
</section>
{cta_band(d)}"""
    page(path="arthra/", title="Ιατρικά άρθρα | LVRI Athens",
         desc="Άρθρα για την ακράτεια ούρων, την πρόπτωση, την ξηρότητα κόλπου και τις "
              "σύγχρονες θεραπείες με laser, από το LVRI Athens.",
         depth=d, body=body, jsonld=[crumb_ld], active="articles")


# ── Clinic, doctors, guide, kegel, gallery, contact, terms ──────────────────
def build_clinic():
    d = 1
    body_html, _, _ = prose("h-kliniki", d)
    crumb_html, crumb_ld = crumbs([("Η κλινική", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Η κλινική</p>
        <h1>Ένα ιατρείο για όσα δεν χωρούν σε μία ειδικότητα.</h1></div>
      <p class="lede">Γυναικολόγοι, πλαστικοί χειρουργοί και δερματολόγοι δουλεύουν μαζί,
        ώστε η ασθενής να μη μεταφέρει η ίδια το ιστορικό της από ιατρείο σε ιατρείο.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="frame" data-reveal>
      {img("clinic-team.jpg", "Η ομάδα του LVRI Athens", 1600, 1067, d)}
    </div>
  </div>
</section>

{doc_layout(d, body_html, aside_cta(d))}

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Οι ιατροί</p><h2>Ποιοι θα σας δουν.</h2></div>
    <div class="grid grid--2">
      <a class="card" href="{rel(d)}dr-mirillas/">
        <p class="card__kicker">Επιστημονικός υπεύθυνος</p>
        <h3>Dr. Κωνσταντίνος Μυρίλλας</h3>
        <p>Μαιευτήρας γυναικολόγος. Ίδρυσε το LVRI Athens το 2008 μαζί με τον Dr. Matlock.
          Από το 2013 διευθύνει το τμήμα πλαστικής κόλπου στο μαιευτήριο ΡΕΑ.</p>
        <p class="card__foot"><span class="link-more">Βιογραφικό</span></p></a>
      <a class="card" href="{rel(d)}dr-matlock/">
        <p class="card__kicker">Συνιδρυτής</p>
        <h3>Dr. David L. Matlock</h3>
        <p>Ιδρυτής του Laser Vaginal Rejuvenation Institute® της Αμερικής και δημιουργός
          των τεχνικών LVR®, DLV® και G-Shot®.</p>
        <p class="card__foot"><span class="link-more">Βιογραφικό</span></p></a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap wrap--narrow">
    <a class="pdf-card" href="{rel(d)}assets/docs/lvri-athens.pdf" target="_blank" rel="noopener">
      {I['pdf']}<span><b>Laser κολπική ανανέωση — ενημερωτικό έντυπο</b>
      <span>PDF · ανοίγει σε νέα καρτέλα</span></span></a>
  </div>
</section>
{cta_band(d)}"""
    page(path="i-kliniki/", title="Η κλινική | LVRI Athens",
         desc=meta_desc("h-kliniki", "Το LVRI Athens, κέντρο κοσμητικής γυναικολογίας στην Αθήνα."),
         depth=d, body=body, jsonld=[crumb_ld], active="clinic")


def build_doctor(slug, legacy, name, role, photo, blurb):
    d = 1
    body_html, _, _ = prose(legacy, d)
    crumb_html, crumb_ld = crumbs([(name, None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="split split--wide-left" style="align-items:end">
      <div class="stack"><p class="eyebrow">{role}</p><h1>{name}</h1>
        <p class="lede">{blurb}</p></div>
      <div class="frame" style="max-width:340px">{img(photo, name, 500, 700, d)}</div>
    </div>
  </div>
</section>
{doc_layout(d, body_html, aside_cta(d))}
{cta_band(d)}"""
    ld = [crumb_ld, {"@context": "https://schema.org", "@type": "Physician", "name": name,
                     "url": f"{SITE['domain']}/{slug}/", "medicalSpecialty": "Gynecologic",
                     "worksFor": {"@id": SITE["domain"] + "/#clinic"}}]
    page(path=f"{slug}/", title=f"{name} | LVRI Athens",
         desc=meta_desc(legacy, blurb[:150]), depth=d, body=body, jsonld=ld)


def build_guide_page():
    d = 1
    crumb_html, crumb_ld = crumbs([("Οδηγός συμπτωμάτων", None)], d)
    flags = "".join(f"<li>{f}</li>" for f in RED_FLAGS)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Οδηγός συμπτωμάτων</p>
        <h1>Δεν χρειάζεται να ξέρετε πώς λέγεται.</h1></div>
      <p class="lede">Τέσσερις ερωτήσεις, γραμμένες όπως θα το λέγατε σε φίλη. Στο τέλος
        θα ξέρετε ποιον ιατρικό όρο να αναζητήσετε και ποιες είναι οι επιλογές.</p>
    </div>
  </div>
</section>
{guide_section(d, heading=False)}
<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Πότε να μην περιμένετε</p>
        <h2>Κάποια συμπτώματα θέλουν γιατρό σήμερα.</h2>
        <p class="lede">Ο οδηγός δεν είναι κατάλληλος αν έχετε:</p>
        <ul class="bullets">{flags}</ul>
        <a class="btn" href="tel:{SITE['phone_href']}">{I['phone']} Καλέστε μας</a>
      </div>
      <div class="stack">
        <p class="eyebrow">Πώς λειτουργεί</p>
        <ul class="timeline">
          <li><b>01</b><span>Επιλέγετε όσα σας ταιριάζουν, με καθημερινά λόγια.</span></li>
          <li><b>02</b><span>Ο οδηγός σταθμίζει τις απαντήσεις και δείχνει τις πιθανές αντιστοιχίες.</span></li>
          <li><b>03</b><span>Παίρνετε συνδέσμους στις σχετικές σελίδες και μπορείτε να ζητήσετε ραντεβού.</span></li>
        </ul>
        <p class="tiny muted">Τίποτα δεν φεύγει από τη συσκευή σας: ο υπολογισμός γίνεται
          τοπικά στον browser και δεν αποθηκεύεται πουθενά.</p>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    page(path="odigos-symptomaton/", title="Οδηγός συμπτωμάτων | LVRI Athens",
         desc="Τέσσερις ερωτήσεις σε καθημερινή γλώσσα για να καταλάβετε τι μπορεί να "
              "συμβαίνει και ποιες είναι οι επιλογές σας. Ιδιωτικό, χωρίς εγγραφή.",
         depth=d, body=body, jsonld=[crumb_ld], active="guide")


def build_kegel_page():
    d = 1
    crumb_html, crumb_ld = crumbs([("Ασκήσεις Kegel", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Πυελικό έδαφος</p>
        <h1>Ασκήσεις Kegel, με ρυθμό.</h1></div>
      <p class="lede">Οι ασκήσεις Kegel ενδυναμώνουν τους μύες της λεκάνης και φέρνουν
        θεαματικά αποτελέσματα στην ακράτεια ούρων από προσπάθεια. Το δύσκολο είναι ο ρυθμός —
        αυτό το αναλαμβάνει ο μετρητής.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap">{kegel_section(d)}</div></section>
<section class="section section--mist">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Πώς γίνονται σωστά</p>
        <h2>Σφίξτε σαν να συγκρατείτε ούρα — και τίποτε άλλο.</h2>
        <ul class="bullets">
          <li>Εντοπίστε τους σωστούς μύες: είναι αυτοί που θα σφίγγατε για να σταματήσετε τη ροή.</li>
          <li>Κοιλιά, γλουτοί και μηροί μένουν χαλαροί. Αν σφίγγονται, η άσκηση δεν πιάνει.</li>
          <li>Μην κρατάτε την αναπνοή σας. Αναπνέετε κανονικά σε όλη τη διάρκεια.</li>
          <li>Καλύτερα λίγες σωστές επαναλήψεις κάθε μέρα, παρά πολλές μία φορά την εβδομάδα.</li>
          <li>Μην τις κάνετε ενώ ουρείτε — αυτό είναι δοκιμή εντοπισμού, όχι άσκηση.</li>
        </ul>
      </div>
      <div class="stack">
        <p class="eyebrow">Πότε δεν αρκούν</p>
        <h2>Οι ασκήσεις δεν θεραπεύουν τις κήλες.</h2>
        <p class="lede">Σε πρόπτωση, κυστεοκήλη ή ορθοκήλη οι ασκήσεις βελτιώνουν τη μυϊκή
          σπαργή, αλλά δεν αποκαθιστούν την ανατομία. Αν νιώθετε βάρος ή προβολή, μιλήστε με γιατρό.</p>
        <div class="pill-row">
          <a class="chip" href="{rel(d)}pathiseis/akrateia-ouron/">Ακράτεια ούρων</a>
          <a class="chip" href="{rel(d)}pathiseis/proptosi-mitras/">Πρόπτωση</a>
          <a class="chip" href="{rel(d)}odigos-symptomaton/">Οδηγός συμπτωμάτων</a>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    page(path="askiseis-kegel/", title="Ασκήσεις Kegel — καθοδηγούμενος μετρητής | LVRI Athens",
         desc="Δωρεάν καθοδηγούμενες ασκήσεις Kegel με τρία προγράμματα, για την ενδυνάμωση "
              "του πυελικού εδάφους και την ακράτεια ούρων από προσπάθεια.",
         depth=d, body=body, jsonld=[crumb_ld])


def build_gallery():
    d = 1
    photos = [f"result-{i:02d}.jpg" for i in range(1, 18)]
    items = "".join(f"""<button class="gal__item is-sensitive" data-item data-kind="photo" data-sensitive
      data-full="{rel(d)}assets/img/{p}" data-alt="Αποτέλεσμα επέμβασης {i} — πριν και μετά">
      {img(p, f"Αποτέλεσμα επέμβασης {i} — πριν και μετά", 484, 176, d)}</button>""" for i, p in enumerate(photos, 1))
    items += "".join(f"""<button class="gal__item" data-item data-kind="video"
      data-video="{v}" data-alt="Βίντεο LVRI Athens {i}">
      <img src="https://i.ytimg.com/vi/{v}/mqdefault.jpg" alt="" loading="lazy" width="320" height="180">
      <span class="gal__play">{I['play']}</span></button>""" for i, v in enumerate(VIDEOS, 1))
    crumb_html, crumb_ld = crumbs([("Gallery", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Gallery</p><h1>Φωτογραφίες και βίντεο.</h1></div>
      <p class="lede">{len(photos)} περιστατικά και {len(VIDEOS)} βίντεο από τηλεοπτικές εκπομπές
        και συνέδρια. Τα αποτελέσματα διαφέρουν από περίπτωση σε περίπτωση.</p>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="compare__filters" role="group" aria-label="Φίλτρα gallery">
      <button class="filter" data-gal-filter="all" aria-pressed="true">Όλα</button>
      <button class="filter" data-gal-filter="photo" aria-pressed="false">Φωτογραφίες</button>
      <button class="filter" data-gal-filter="video" aria-pressed="false">Βίντεο</button>
    </div>

    <div class="reveal-gate" data-reveal-gate>
      <div>
        <p class="eyebrow">Κλινικό υλικό</p>
        <h3 style="margin-top:.5rem">Οι φωτογραφίες περιστατικών δείχνουν γυμνό.</h3>
        <p class="small muted" style="margin-top:.4rem;max-width:56ch">Είναι ιατρικές εικόνες πριν και
          μετά την επέμβαση. Εμφανίζονται μόνο αν το επιλέξετε — η επιλογή σας μένει σε αυτή τη συσκευή.</p>
      </div>
      <button class="btn btn--sm" data-reveal-photos>Εμφάνιση φωτογραφιών</button>
    </div>

    <div class="gal" data-gallery>{items}</div>
    <p class="tiny muted" style="margin-top:1.5rem;max-width:62ch">
      Οι εικόνες αφορούν πραγματικά περιστατικά και δημοσιεύονται με τη συγκατάθεση των ασθενών.
      Δεν αποτελούν υπόσχεση αποτελέσματος: κάθε ανατομία και κάθε επούλωση είναι διαφορετική.</p>
  </div>
</section>
{cta_band(d)}"""
    page(path="gallery/", title="Photo & Video Gallery | LVRI Athens",
         desc="Φωτογραφίες περιστατικών και βίντεο από το LVRI Athens.",
         depth=d, body=body, jsonld=[crumb_ld], active="gallery")


def build_contact():
    d = 1
    hours = "".join(f'<div style="display:flex;justify-content:space-between;gap:1rem;'
                    f'border-bottom:1px solid var(--line-soft);padding:.55rem 0">'
                    f'<span>{a}</span><b style="font-weight:560">{b}</b></div>'
                    for a, b in SITE["hours"])
    crumb_html, crumb_ld = crumbs([("Επικοινωνία", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Επικοινωνία</p>
        <h1>Καραολή &amp; Δημητρίου 41, Βύρωνας.</h1></div>
      <p class="lede">Τηλεφωνήστε, γράψτε μας ή στείλτε αίτημα ραντεβού. Απαντάμε την ίδια
        ή την επόμενη εργάσιμη.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="contact-grid">
      <div class="stack" style="justify-items:stretch">
        <ul class="info-list">
          <li>{I['pin']}<div><b>Διεύθυνση</b>
            <a href="{SITE['map']}" target="_blank" rel="noopener">{SITE['address']}, {SITE['postcode']}</a></div></li>
          <li>{I['phone']}<div><b>Τηλέφωνο</b><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></li>
          <li>{I['mail']}<div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
          <li>{I['clock']}<div style="width:100%"><b>Ωράριο</b><div style="margin-top:.35rem">{hours}</div></div></li>
        </ul>
        <button class="btn btn--block" data-book-open>Ζητήστε ραντεβού</button>
      </div>
      <div class="stack" style="justify-items:stretch">
        <iframe class="map" loading="lazy" title="Χάρτης — LVRI Athens"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q={SITE['address'].replace(' ', '+')}&amp;output=embed"></iframe>
        <div class="note">
          <b>Πριν το ραντεβού</b>
          <span>Αν έχετε πρόσφατο ουροδυναμικό έλεγχο, υπερηχογράφημα ή χειρουργικό ιστορικό,
          φέρτε τα μαζί σας. Κερδίζουμε χρόνο και αποφεύγουμε επαναλήψεις εξετάσεων.</span>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    page(path="epikoinonia/", title="Επικοινωνία & ραντεβού | LVRI Athens",
         desc=f"LVRI Athens — {SITE['address']}. Τηλέφωνο {SITE['phone']}. "
              "Δευτέρα – Παρασκευή 09:00 – 17:00, Σάββατο 09:00 – 15:00.",
         depth=d, body=body, jsonld=[crumb_ld], active="contact")


def build_terms():
    d = 1
    body_html, _, _ = prose("oroi-chrisis-politiki-aporritou", d)
    crumb_html, crumb_ld = crumbs([("Όροι χρήσης & απόρρητο", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap wrap--narrow">{crumb_html}
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.2vw,2.8rem)">Όροι χρήσης &amp; πολιτική απορρήτου</h1>
    <p class="lede" style="margin-top:.9rem">Τελευταία ενημέρωση: {TODAY}</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap wrap--narrow">
  <article class="prose">{body_html}</article></div></section>"""
    page(path="oroi-chrisis/", title="Όροι χρήσης & πολιτική απορρήτου | LVRI Athens",
         desc="Όροι χρήσης και πολιτική απορρήτου του ιστότοπου του LVRI Athens.",
         depth=d, body=body, jsonld=[crumb_ld])


def build_404():
    d = 0
    body = f"""<section class="section" style="min-height:56vh;display:grid;place-items:center">
  <div class="wrap wrap--narrow" style="text-align:center">
    <p class="eyebrow eyebrow--plain" style="justify-content:center">404</p>
    <h1 style="margin-block:.8rem 1.2rem">Αυτή η σελίδα δεν υπάρχει πια.</h1>
    <p class="lede" style="margin-inline:auto">Ο ιστότοπος ανανεώθηκε και κάποιοι σύνδεσμοι άλλαξαν.
      Ξεκινήστε από την αρχική ή αναζητήστε αυτό που ψάχνατε.</p>
    <div class="hero__actions" style="justify-content:center;margin-top:1.75rem">
      <a class="btn" href="/">Αρχική</a>
      <button class="btn btn--ghost" data-search-open>{I['search']} Αναζήτηση</button>
    </div>
  </div>
</section>"""
    page(path="404.html", title="Η σελίδα δεν βρέθηκε | LVRI Athens",
         desc="Η σελίδα που ζητήσατε δεν υπάρχει. Ο ιστότοπος του LVRI Athens ανανεώθηκε — "
              "ξεκινήστε από την αρχική ή χρησιμοποιήστε την αναζήτηση.", depth=d, body=body)


# ── English ─────────────────────────────────────────────────────────────────
from parts import EN_NAV


# hreflang is declared only where a page has a real 1:1 counterpart.
EN_PAIR = {"en/": "", "en/the-clinic/": "i-kliniki/"}


def en_shell(*, path, title, desc, depth, inner, crumb=None):
    b = rel(depth)
    nav = "".join(f'<a class="chip" href="{b}en/{s}/">{t}</a>' for s, t in EN_NAV)
    hours = "".join(f"<div><span>{a}</span><span>{c}</span></div>" for a, c in SITE["hours_en"])
    body = inner + f"""
<section class="section section--navy">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Visiting Athens</p>
        <h2>Consultations in English.</h2>
        <p class="lede">The full clinical site is in Greek. For an English consultation,
          call or email us — we will answer in English.</p>
        <div class="pill-row" style="margin-top:.5rem">{nav}</div>
      </div>
      <div class="stack" style="justify-items:stretch">
        <a class="btn btn--light btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
        <a class="btn btn--outline-light btn--block" href="tel:{SITE['phone_href']}">{I['phone']} +30 {SITE['phone']}</a>
        <p class="tiny" style="color:#9aa3c8">{SITE['address_en']}</p>
        <div class="footer__hours" style="color:#b6bdda">{hours}</div>
      </div>
    </div>
  </div>
</section>"""
    pair = EN_PAIR.get(path)
    page(path=path, title=title, desc=desc, depth=depth, body=body, lang="en",
         alt=("el", pair) if pair is not None else None, jsonld=[{
             "@context": "https://schema.org", "@type": "MedicalWebPage",
             "name": title, "inLanguage": "en",
             "url": f"{SITE['domain']}/{path}", "publisher": {"@id": SITE["domain"] + "/#clinic"}}])


def build_en_home():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}en/{s}/">
      <h3>{t}</h3><p>{html.escape(plain('en/' + s, 120))}…</p>
      <p class="card__foot"><span class="link-more">Read more</span></p></a>"""
      for s, t in EN_NAV if ("en/" + s) in LEGACY)
    inner = f"""<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Laser Vaginal Rejuvenation Institute of Athens</p>
      <h1>Cosmetic gynaecology and pelvic floor surgery, in Athens.</h1>
      <p class="lede">Founded in 2008 with Dr. David Matlock of LVRI Los Angeles.
        Urinary incontinence, prolapse, vaginal atrophy and laser vaginal rejuvenation.</p>
      <div class="hero__actions">
        <a class="btn" href="mailto:{SITE['email']}">Request a consultation</a>
        <a class="btn btn--ghost" href="{rel(d)}">Ελληνικά</a>
      </div>
    </div>
    <div class="hero__figure">
      {img("dr-myrillas.jpg", "Dr. Konstantinos Myrillas at LVRI Athens", 500, 700, d, priority=True)}
      <div class="hero__badge"><b>2008</b><span>Founded with the protocols of LVRI Los Angeles</span></div>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Treatments &amp; conditions</p>
    <h2>What we treat.</h2></div>
  <div class="grid grid--3">{cards}</div></div></section>"""
    en_shell(path="en/", title="LVRI Athens — Laser Vaginal Rejuvenation Institute",
             desc="Cosmetic gynaecology and pelvic floor surgery in Athens, Greece. "
                  "Urinary incontinence, vaginal atrophy, laser vaginal rejuvenation.",
             depth=1, inner=inner)


def build_en_page(slug, legacy, title):
    d = 2
    body_html, faq_title, pairs = prose(legacy, d)
    faq_html, _ = faq_block(faq_title, pairs, f"faq-{slug}")
    inner = f"""<section class="page-head">
  <div class="wrap wrap--narrow">
    <ol class="crumbs"><li><a href="{rel(d)}en/">LVRI Athens</a></li><li>{title}</li></ol>
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.4vw,3rem)">{title}</h1>
  </div>
</section>
{doc_layout(d, body_html)}{faq_html}"""
    en_shell(path=f"en/{slug}/", title=seo_title(title),
             desc=meta_desc(legacy, title), depth=d, inner=inner)


# ── Search index, sitemap, robots ───────────────────────────────────────────
def build_index_files():
    entries = []

    def add(url, title, blurb, keywords=""):
        entries.append({"u": url, "t": title,
                        "b": re.sub(r"\s+", " ", html.unescape(blurb))[:320], "k": keywords})

    add("", "Αρχική", "LVRI Athens — κοσμητική γυναικολογία και χειρουργική πυελικού εδάφους στην Αθήνα.")
    add("i-kliniki/", "Η κλινική", plain("h-kliniki", 300))
    add("dr-mirillas/", "Dr. Κωνσταντίνος Μυρίλλας", plain("dr-k-mirillas", 300), "βιογραφικό γιατρός")
    add("dr-matlock/", "Dr. David L. Matlock", plain("david-l-matlock", 300), "βιογραφικό")
    add("odigos-symptomaton/", "Οδηγός συμπτωμάτων",
        "Τέσσερις ερωτήσεις σε καθημερινή γλώσσα για να καταλάβετε τι μπορεί να συμβαίνει.", "τεστ συμπτώματα")
    add("askiseis-kegel/", "Ασκήσεις Kegel",
        "Καθοδηγούμενος μετρητής με τρία προγράμματα για την ενδυνάμωση του πυελικού εδάφους.", "kegel πύελος")
    add("pathiseis/", "Παθήσεις", "Ακράτεια, πρόπτωση, ξηρότητα, κυστεοκήλη, ορθοκήλη.")
    add("therapeies/", "Θεραπείες", "Σύγκριση θεραπειών: αναισθησία, διάρκεια, ανάρρωση.")
    add("gallery/", "Gallery", "Φωτογραφίες περιστατικών και βίντεο.")
    add("epikoinonia/", "Επικοινωνία", f"{SITE['address']} · {SITE['phone']} · {SITE['email']}", "ραντεβού")
    add("arthra/", "Άρθρα", "Ιατρικά άρθρα από το LVRI Athens.")
    add("oroi-chrisis/", "Όροι χρήσης & απόρρητο", "Όροι χρήσης και πολιτική απορρήτου.")
    for c in CONDITIONS:
        add(f"pathiseis/{c['slug']}/", c["title"], plain(c["legacy"], 320), c["plain"])
    for t in TREATMENTS:
        add(f"therapeies/{t['slug']}/", t["title"], plain(t["legacy"], 320), t["short"])
    for slug, tag in ARTICLES:
        add(f"arthra/{slug}/", article_title(slug), plain(slug, 320), tag)
    add("en/", "LVRI Athens — English", "Cosmetic gynaecology in Athens, in English.", "english")
    for slug, legacy, title in EN_PAGES:
        add(f"en/{slug}/", title, plain(legacy, 320), "english")

    write("search-index.json", json.dumps(entries, ensure_ascii=False, separators=(",", ":")))

    urls = [(e["u"], "1.0" if not e["u"] else "0.8" if "/" not in e["u"].rstrip("/") else "0.6")
            for e in entries]
    body = "".join(
        f"<url><loc>{SITE['domain']}/{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>monthly</changefreq><priority>{p}</priority></url>" for u, p in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")


# ── Legacy URL redirects ────────────────────────────────────────────────────
def build_redirects():
    """Keeps the old WordPress URLs alive so nothing that ranks today 404s."""
    rules = []
    for legacy, target in sorted(URLMAP.items()):
        if legacy in ("home",) or legacy.startswith("en/"):
            continue
        if legacy == target.rstrip("/"):
            continue
        rules.append((f"/{legacy}/", f"/{target}"))
    rules.append(("/photo-gallery/", "/gallery/"))
    rules.append(("/video-gallery/", "/gallery/"))

    write("_redirects", "".join(f"{a}  {b}  301\n" for a, b in rules))
    ht = ["RewriteEngine On"]
    ht += [f"RewriteRule ^{a.strip('/')}/?$ {b} [R=301,L]" for a, b in rules]
    ht.append("ErrorDocument 404 /404.html")
    write(".htaccess", "\n".join(ht) + "\n")

    # Vercel is the live host, and it reads neither of the files above.
    write("vercel.json", json.dumps({
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "trailingSlash": True,
        "cleanUrls": False,
        # trailingSlash normalises the path before redirects are matched, so the
        # source must carry the slash too.
        "redirects": [{"source": a, "destination": b, "permanent": True}
                      for a, b in rules],
        "headers": [
            {"source": "/assets/(img|docs)/(.*)",
             "headers": [{"key": "Cache-Control",
                          "value": "public, max-age=31536000, immutable"}]},
            {"source": "/assets/(css|js)/(.*)",
             "headers": [{"key": "Cache-Control",
                          "value": "public, max-age=86400, must-revalidate"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()"},
            ]},
        ],
    }, ensure_ascii=False, indent=2) + "\n")

    return len(rules)


def main():
    build_home()
    for c in CONDITIONS:
        build_condition(c)
    for t in TREATMENTS:
        build_treatment(t)
    for slug, tag in ARTICLES:
        build_article(slug, tag)
    build_conditions_hub(); build_treatments_hub(); build_articles_hub()
    build_clinic(); build_guide_page(); build_kegel_page()
    build_doctor("dr-mirillas", "dr-k-mirillas", "Dr. Κωνσταντίνος Μυρίλλας",
                 "Επιστημονικός υπεύθυνος", "dr-myrillas.jpg",
                 "Μαιευτήρας γυναικολόγος. Αποφοίτησε με άριστα από την Ιατρική Αθηνών το 1991 "
                 "και ειδικεύτηκε στη Μεγάλη Βρετανία. Ίδρυσε το LVRI Athens το 2008.")
    build_doctor("dr-matlock", "david-l-matlock", "Dr. David L. Matlock",
                 "Συνιδρυτής · LVRI Los Angeles", "dr-matlock.jpg",
                 "Πιστοποιημένος χειρουργός γυναικολόγος των Η.Π.Α. και δημιουργός των "
                 "κατοχυρωμένων τεχνικών LVR®, DLV® και G-Shot®.")
    build_gallery(); build_contact(); build_terms(); build_404()
    build_en_home()
    for slug, legacy, title in EN_PAGES:
        build_en_page(slug, legacy, title)
    build_index_files()
    n = build_redirects()
    pages = sum(len([f for f in fs if f.endswith((".html",))]) for _, _, fs in os.walk(OUT))
    print(f"built {pages} pages · {n} redirects · {OUT}")


if __name__ == "__main__":
    main()
