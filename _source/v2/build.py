# -*- coding: utf-8 -*-
"""Builds LVRI Athens version 2 into version-2/site/.

    python3 version-2/build.py

Content comes from lvri-new/content/ (data.py + legacy.json), the same source
of truth as version 1, so copy is edited in one place only.
"""
import os, re, sys, json, html, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))

import content as C
import ui as U
from content import (SITE, CONDITIONS, TREATMENTS, ARTICLES, GUIDE_STEPS, RED_FLAGS,
                     KEGEL, VIDEO_GROUPS, VIDEO_LIBRARY, HOME_VIDEOS,
                     YOUTUBE_CHANNEL, EN_PAGES, CONDS, TREATS, LEGACY, TODAY, rel,
                     ARTICLE_IMAGES, EN_IMAGES, HUB_IMAGES)

OUT = os.path.abspath(os.environ.get("LVRI2_OUT") or os.path.join(HERE, "site"))
SRC = os.path.join(HERE, "src")
TOOLS, CONTENT = C.TOOLS, C.CONTENT
ASSETS_SRC = C._find(
    os.path.join(C.ROOT, "lvri-new", "site", "assets"),        # working tree
    os.path.join(os.path.dirname(C.ROOT), "assets"),           # deployment repo (_source/v2 → /)
    os.path.join(C.ROOT, "assets"))

PAGES = []          # (path, title, desc, priority, changefreq)
SEARCH = []         # search index rows


# ── output helpers ───────────────────────────────────────────────────────────
def write(path, markup):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(markup)


def index(url, *, title, desc, kind, hue=None, kw=""):
    SEARCH.append({"t": title, "d": desc, "u": url, "k": kind,
                   "h": hue if hue is not None else U.hue(url), "kw": kw})


def register(url, *, prio="0.6", freq="monthly"):
    PAGES.append((url, prio, freq))


# ── shared JSON-LD ───────────────────────────────────────────────────────────
def address_ld():
    return {"@type": "PostalAddress", "streetAddress": SITE["address"],
            "addressLocality": SITE["locality"], "postalCode": SITE["postcode"],
            "addressRegion": SITE["region"], "addressCountry": "GR"}


def clinic_ld():
    return {
        "@type": ["MedicalClinic", "LocalBusiness"],
        "@id": SITE["domain"] + "/#clinic",
        "name": SITE["name"], "legalName": SITE["legal"], "url": SITE["domain"] + "/",
        "telephone": "+" + SITE["phone_href"].lstrip("+"), "email": SITE["email"],
        "address": address_ld(),
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
        "hasMap": SITE["map_full"], "foundingDate": SITE["founded"],
        "priceRange": "€€", "knowsLanguage": ["el", "en"],
        "areaServed": [{"@type": "Place", "name": a} for a in SITE["areas"]]
                      + [{"@type": "AdministrativeArea", "name": SITE["region"]},
                         {"@type": "Country", "name": "Ελλάδα"}],
        "medicalSpecialty": ["Gynecologic", "PlasticSurgery"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek":
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "09:00", "closes": "17:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"],
             "opens": "09:00", "closes": "15:00"}],
        "availableService": [{"@type": "MedicalProcedure", "name": t["title"],
                              "url": f"{SITE['domain']}/therapeies/{t['slug']}/"}
                             for t in TREATMENTS],
        "sameAs": list(SITE["social"].values()),
    }


def doctor_ld():
    return {"@type": "Physician", "@id": SITE["domain"] + "/dr-mirillas/#physician",
            "name": "Dr. Κωνσταντίνος Μυρίλλας", "medicalSpecialty": "Gynecologic",
            "url": SITE["domain"] + "/dr-mirillas/",
            "worksFor": {"@id": SITE["domain"] + "/#clinic"}, "address": address_ld()}


def site_ld():
    return {"@type": "WebSite", "@id": SITE["domain"] + "/#website",
            "url": SITE["domain"] + "/", "name": SITE["name"], "inLanguage": "el",
            "publisher": {"@id": SITE["domain"] + "/#clinic"}}


def base_graph():
    return {"@context": "https://schema.org",
            "@graph": [clinic_ld(), doctor_ld(), site_ld()]}


# ── the anatomy diagram, restyled for the dark interface ─────────────────────
def anatomy_svg():
    src = open(os.path.join(TOOLS, "parts.py"), encoding="utf-8").read()
    svg = re.search(r'ANATOMY_SVG = """(.*?)"""', src, re.S).group(1)
    swap = {
        '<stop offset="0" stop-color="#dee3f3"/><stop offset="1" stop-color="#bcc5e4"/>':
            '<stop offset="0" stop-color="#39406b"/><stop offset="1" stop-color="#1b2140"/>',
        '#eaedf7': 'rgba(255,255,255,.30)', '#edeff8': 'rgba(255,255,255,.09)',
        '#dfe3f1': 'rgba(255,255,255,.20)', '#b7bfdd': 'rgba(160,180,255,.45)',
        '#c6cce7': 'rgba(200,215,255,.55)', '#a5accf': 'rgba(190,205,255,.45)',
        '#767c9c': 'rgba(190,205,255,.55)',
        'class="anatomy__svg"': 'class="an__svg"',
        'data-organ=': 'data-organ-hit=',
        '<g class="organ">': '<g class="organ organ--drop">',
    }
    for a, b in swap.items():
        svg = svg.replace(a, b)
    return svg


def organs_json():
    out = {}
    for key, (title, text) in U.ORGANS.items():
        links = [{"t": c["title"], "u": f"pathiseis/{c['slug']}/"}
                 for c in CONDITIONS if c["organ"] == key]
        out[key] = {"title": title, "text": text, "links": links}
    return out


def page_scripts(depth):
    return (f'<script id="scanner-data" type="application/json">'
            f'{json.dumps(U.scanner_data(), ensure_ascii=False, separators=(",", ":"))}</script>\n'
            f'<script>window.__ORGANS={json.dumps(organs_json(), ensure_ascii=False, separators=(",", ":"))}</script>')


# ── page shell ───────────────────────────────────────────────────────────────
def shell(*, path, title, desc, depth, body, active="", jsonld=None, lang="el",
          body_class=""):
    ld = [base_graph()] + list(jsonld or [])
    head = U.head(title=title, desc=desc, depth=depth, canonical=path, lang=lang,
                  jsonld=ld, body_class=body_class)
    return (head + U.topbar(depth, active) + body + U.footer(depth)
            + U.tail(depth, extra_js=page_scripts(depth), lang=lang))


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
def build_home():
    d = 0
    t_cards = [U.treatment_card(t, d, n=i + 1) for i, t in enumerate(TREATMENTS)]
    c_cards = [U.condition_card(c, d) for c in CONDITIONS]
    a_cards = [U.article_card(s, tag, d) for s, tag in ARTICLES[:12]]
    by_id = {v['id']: v for v in VIDEO_LIBRARY}
    v_cards = [U.video_card(by_id[i], d) for i in HOME_VIDEOS if i in by_id]

    body = U.billboard(d) + f"""
<main id="main">
  {U.row(rid="r-treat", title="Θεραπείες", eyebrow="Top 5", cards=t_cards,
         all_href="therapeies/", all_label="Όλες", kind="nf-row--top")}

  {U.row(rid="r-cond", title="Παθήσεις", cards=c_cards,
         all_href="pathiseis/", all_label="Όλες")}

  {U.row(rid="r-vid", title="Βίντεο", eyebrow="του ιατρείου", cards=v_cards,
         all_href="vinteo/", all_label="Όλα τα βίντεο", kind="nf-row--wide")}

  <div class="rv">{U.scanner_section(d)}</div>

  {U.row(rid="r-art", title="Άρθρα του ιατρείου", cards=a_cards,
         all_href="arthra/", all_label="Όλα")}

  <div class="rv">{U.compare_section(d)}</div>

  <section class="sec sec--edge rv">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Η κλινική</p>
        <h2>Ένα ιατρείο, μία ειδικότητα</h2>
        <p class="lede">Το LVRI Athens λειτουργεί από το {SITE['founded']} στον Βύρωνα ως κέντρο
          κοσμητικής γυναικολογίας και επανορθωτικής χειρουργικής πυέλου με laser. Τα ραντεβού,
          οι εξετάσεις και οι θεραπείες laser γίνονται στο ιατρείο· οι επεμβάσεις στο
          Μαιευτήριο ΡΕΑ, όπου ο Dr. Μυρίλλας διευθύνει το αντίστοιχο τμήμα από το 2013.</p>
        <ul class="figures" style="margin:2rem 0">
          <li><b>{SITE['founded']}</b><span>Ιατρείο στον Βύρωνα</span></li>
          <li><b>2013</b><span>Τμήμα στο ΡΕΑ</span></li>
          <li><b>{len(TREATMENTS)}</b><span>Θεραπείες</span></li>
        </ul>
        <p><a class="btn btn--ghost" href="i-kliniki/">Για την κλινική</a>
          <a class="btn btn--line" href="dr-mirillas/" style="margin-left:.4rem">Dr. Κ. Μυρίλλας</a></p>
      </div>
      <figure style="margin:0">{U.pic("dr-myrillas.jpg", "Dr. Κωνσταντίνος Μυρίλλας", 500, 700, d)}</figure>
    </div>
  </section>

  {U.cta_band(d)}
</main>"""
    desc = C.meta_desc("home", "Κέντρο κοσμητικής γυναικολογίας και επανορθωτικής χειρουργικής πυέλου στην Αθήνα.")
    write("index.html", shell(path="", title="Laser πλαστική κόλπου & πυελικό έδαφος, Αθήνα | LVRI Athens",
                              desc=desc, depth=d, body=body, active="", body_class="is-home"))
    register("", prio="1.0", freq="weekly")
    index("", title="Αρχική", desc="LVRI Athens: θεραπείες, παθήσεις και εργαλεία", kind="page",
          kw="αρχικη home lvri athens")


# ══════════════════════════════════════════════════════════════════════════════
# TREATMENTS
# ══════════════════════════════════════════════════════════════════════════════
def treatment_ld(t):
    return {"@context": "https://schema.org", "@type": "MedicalProcedure",
            "name": t["title"], "alternateName": t["short"],
            "url": f"{SITE['domain']}/therapeies/{t['slug']}/",
            "description": t["lead"], "bodyLocation": "Κόλπος / πυελικό έδαφος",
            "howPerformed": t["matrix"]["setting"] + " · " + t["matrix"]["anesthesia"],
            "followup": t["matrix"]["recovery"],
            "procedureType": {"non": "NoninvasiveProcedure", "minor": "PercutaneousProcedure",
                              "surgical": "SurgicalProcedure"}[t["invasive"]],
            "provider": {"@id": SITE["domain"] + "/#clinic"}}


def build_treatment(t):
    d, slug = 2, t["slug"]
    body_html, faq_title, faq_pairs = C.prose(t["legacy"], d)
    body_html = anchor_headings(body_html)
    faq_html, faq_ld = U.faq_block(faq_title, faq_pairs)
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Θεραπείες", "therapeies/"), (t["title"], None)], d)
    m = t["matrix"]
    facts = "".join(f'<li><span class="k">{k}</span><span class="v">{html.escape(v)}</span></li>'
                    for k, v in [("Πού γίνεται", m["setting"]), ("Αναισθησία", m["anesthesia"]),
                                 ("Συνεδρίες", m["sessions"]), ("Διάρκεια", m["duration"]),
                                 ("Ανάρρωση", m["recovery"]), ("Πόνος", m["pain"])])
    treats = "".join(f"<li>{html.escape(x)}</li>" for x in t["treats"])
    related = [c for c in CONDITIONS if slug in c["treatments"]]
    rel_cards = [U.condition_card(c, d) for c in related]
    toc = build_toc(body_html)
    aside = f'''{toc}
<div class="panel"><h3>Με μια ματιά</h3><ul class="facts">{facts}</ul></div>
<div class="panel"><h3>Αντιμετωπίζει</h3><ul class="card__chips" style="margin:0">{treats}</ul></div>
<div class="panel"><h3>Ταιριάζει σε εσάς;</h3>
  <p>Τέσσερα βήματα στη συσκευή σας, καμία αποστολή δεδομένων.</p>
  <button class="btn btn--cta btn--sm" type="button" data-open="scanner">Σαρωτής συμπτωμάτων</button></div>
<div class="panel"><h3>Ζητήστε εκτίμηση</h3><p>Απαντάμε την ίδια ή την επόμενη εργάσιμη.</p>
  <button class="btn btn--cta btn--sm" type="button" data-open="book" data-topic="{html.escape(t['title'])}">Ραντεβού</button></div>'''

    body = f'''
{U.hero_photo(t.get('image'), t['title'], d)}
  <div class="wrap">{crumb}
    <p class="hero__badge"><span class="k">{html.escape(t['short'])}</span>{U.lvl_badge(t['invasive'])}</p>
    <h1>{html.escape(t['title'])}</h1>
    <p class="lede">{html.escape(t['lead'])}</p>
    <ul class="hero__meta">
      <li>{U.I['pin']}{html.escape(m['setting'])}</li>
      <li>{U.I['clock']}{html.escape(m['duration'])}</li>
      <li>{U.I['check']}{html.escape(m['recovery'])}</li>
    </ul>
    <div class="hero__acts">
      <button class="btn btn--cta btn--lg" type="button" data-open="book" data-topic="{html.escape(t['title'])}">Ζητήστε ραντεβού</button>
      <a class="btn btn--glass btn--lg" href="tel:{SITE['phone_href']}">{U.I['phone']}{SITE['phone']}</a>
      {U.save_inline(slug, t['title'], f"therapeies/{slug}/", 'treatment')}
    </div>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside">{aside}</aside>
</div>
{faq_html}
{U.row(rid="r-rel", eyebrow="Σχετικά", title="Παθήσεις που αντιμετωπίζει", cards=rel_cards) if rel_cards else ""}
{U.cta_band(d, title="Μια ερώτηση δεν κοστίζει τίποτα")}
</main>'''
    write(f"therapeies/{slug}/index.html",
          shell(path=f"therapeies/{slug}/", title=C.seo_title(t["title"]), desc=html.escape(t["meta"][:158], quote=True),
                depth=d, body=body, active="therapeies",
                jsonld=[treatment_ld(t), crumb_ld] + ([faq_ld] if faq_ld else [])))
    register(f"therapeies/{slug}/", prio="0.9")
    index(f"therapeies/{slug}/", title=t["title"], desc=t["short"] + " · " + U.INVASIVE[t["invasive"]][0], kind="treatment",
          hue=U.hue(slug), kw=" ".join(t["treats"]) + " " + t["lead"] + " " + t["short"])


def build_treatments_hub():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Θεραπείες", None)], d)
    cards = [U.treatment_card(t, d, n=i + 1) for i, t in enumerate(TREATMENTS)]
    tiles = "".join(f'''<article class="tile">
      <span class="tile__n">{U.INVASIVE[t['invasive']][0]}</span>
      <h3><a href="{t['slug']}/">{html.escape(t['title'])}</a></h3>
      <p>{html.escape(t['lead'])}</p></article>''' for t in TREATMENTS)
    body = f'''
{U.hero_photo(HUB_IMAGES.get('therapeies/'), 'Θεραπείες', d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Πέντε διαδρομές</p>
    <h1>Θεραπείες</h1>
    <p class="lede">Από μια ανώδυνη συνεδρία laser στο ιατρείο μέχρι πλήρη ανάπλαση του κόλπου
      στο χειρουργείο. Δείτε τις δίπλα δίπλα και κρατήστε όσες σας αφορούν.</p>
    <div class="hero__acts">
      <a class="btn btn--cta" href="#compare">Σύγκριση</a>
      <button class="btn btn--glass" type="button" data-open="scanner">Ποια μου ταιριάζει;</button>
    </div>
  </div>
</section>
<main id="main">
  {U.row(rid="r-t", title="Όλες οι θεραπείες", cards=cards)}
  <div class="rv">{U.compare_section(d)}</div>
  <section class="sec rv"><div class="wrap">
    <div class="sec__head"><p class="eyebrow">Με λίγα λόγια</p><h2>Τι κάνει η καθεμία</h2></div>
    <div class="grid-3">{tiles}</div>
  </div></section>
  {U.cta_band(d)}
</main>'''
    write("therapeies/index.html", shell(path="therapeies/", title="Θεραπείες | LVRI Athens",
          desc="Οι πέντε θεραπείες του LVRI Athens για ακράτεια, πρόπτωση, ξηρότητα και χαλάρωση κόλπου: δίπλα δίπλα, με χώρο, αναισθησία, συνεδρίες και ανάρρωση.",
          depth=d, body=body, active="therapeies",
          jsonld=[crumb_ld]))
    register("therapeies/", prio="0.9", freq="weekly")
    index("therapeies/", title="Θεραπείες", desc="Και οι πέντε, με σύγκριση", kind="page",
          kw="θεραπειες laser χειρουργειο συγκριση")


# ══════════════════════════════════════════════════════════════════════════════
# CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════
def condition_ld(c):
    return {"@context": "https://schema.org", "@type": "MedicalCondition",
            "name": c["title"], "url": f"{SITE['domain']}/pathiseis/{c['slug']}/",
            "description": c["lead"],
            "possibleTreatment": [{"@type": "MedicalProcedure", "name": TREATS[s]["title"],
                                   "url": f"{SITE['domain']}/therapeies/{s}/"}
                                  for s in c["treatments"] if s in TREATS]}


def build_condition(c):
    d, slug = 2, c["slug"]
    body_html, faq_title, faq_pairs = C.prose(c["legacy"], d)
    body_html = anchor_headings(body_html)
    faq_html, faq_ld = U.faq_block(faq_title, faq_pairs)
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Παθήσεις", "pathiseis/"), (c["title"], None)], d)
    n, unit = c["stat"]
    rel_cards = [U.treatment_card(TREATS[s], d) for s in c["treatments"] if s in TREATS]
    toc = build_toc(body_html)
    aside = f'''{toc}
<div class="panel"><h3>Με απλά λόγια</h3><p style="font-size:1rem;color:var(--ink)">«{html.escape(c['plain'])}»</p>
  <div class="stat"><b>{html.escape(n)}</b><span>{html.escape(unit)}</span></div></div>
<div class="panel"><h3>Δεν είστε σίγουρη;</h3><p>Ο σαρωτής συμπτωμάτων βάζει λέξεις σε αυτό που νιώθετε.</p>
  <button class="btn btn--cta btn--sm" type="button" data-open="scanner">Ξεκινήστε</button></div>
<div class="panel"><h3>Ζητήστε εκτίμηση</h3><p>Απαντάμε την ίδια ή την επόμενη εργάσιμη.</p>
  <button class="btn btn--cta btn--sm" type="button" data-open="book" data-topic="{html.escape(c['title'])}">Ραντεβού</button></div>'''
    body = f'''
{U.hero_photo(c.get('image'), c['title'], d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Πάθηση</p>
    <h1>{html.escape(c['title'])}</h1>
    <p class="lede">{html.escape(c['lead'])}</p>
    <div class="hero__acts">
      <button class="btn btn--cta btn--lg" type="button" data-open="scanner">Σαρωτής συμπτωμάτων</button>
      <button class="btn btn--glass btn--lg" type="button" data-open="book" data-topic="{html.escape(c['title'])}">Ζητήστε ραντεβού</button>
      {U.save_inline(slug, c['title'], f"pathiseis/{slug}/", 'condition')}
    </div>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside">{aside}</aside>
</div>
{faq_html}
{U.row(rid="r-rel", eyebrow="Επιλογές", title="Θεραπείες που συζητούνται", cards=rel_cards) if rel_cards else ""}
<div class="rv">{U.anatomy_section(d, anatomy_svg())}</div>
{U.cta_band(d)}
</main>'''
    write(f"pathiseis/{slug}/index.html",
          shell(path=f"pathiseis/{slug}/", title=C.seo_title(c["title"]),
                desc=html.escape(c["meta"][:158], quote=True), depth=d, body=body,
                active="pathiseis",
                jsonld=[condition_ld(c), crumb_ld] + ([faq_ld] if faq_ld else [])))
    register(f"pathiseis/{slug}/", prio="0.9")
    index(f"pathiseis/{slug}/", title=c["title"], desc=c["plain"], kind="condition",
          hue=U.hue(slug), kw=c["lead"] + " " + c["plain"])


def build_conditions_hub():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Παθήσεις", None)], d)
    cards = [U.condition_card(c, d) for c in CONDITIONS]
    body = f'''
{U.hero_photo(HUB_IMAGES.get('pathiseis/'), 'Παθήσεις', d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Πέντε καταστάσεις</p>
    <h1>Παθήσεις</h1>
    <p class="lede">Πέντε καταστάσεις που φέρνουν τις περισσότερες γυναίκες στο ιατρείο.
      Διαβάστε τι είναι, ή αφήστε τον σαρωτή να δείξει τι ταιριάζει με όσα νιώθετε.</p>
    <div class="hero__acts">
      <button class="btn btn--cta" type="button" data-open="scanner">Σαρωτής συμπτωμάτων</button>
      <a class="btn btn--glass" href="#anatomia">Χάρτης πυέλου</a>
    </div>
  </div>
</section>
<main id="main">
  {U.row(rid="r-c", title="Όλες οι παθήσεις", cards=cards)}
  <div class="rv">{U.anatomy_section(d, anatomy_svg())}</div>
  <div class="rv">{U.scanner_section(d)}</div>
  {U.cta_band(d)}
</main>'''
    write("pathiseis/index.html", shell(path="pathiseis/", title="Παθήσεις πυελικού εδάφους | LVRI Athens",
          desc="Ακράτεια ούρων, πρόπτωση μήτρας, κυστεοκήλη, ορθοκήλη και ξηρότητα κόλπου: τι είναι, πώς αναγνωρίζονται και ποιες θεραπείες τις αντιμετωπίζουν.",
          depth=d, body=body, active="pathiseis",
          jsonld=[crumb_ld]))
    register("pathiseis/", prio="0.9", freq="weekly")
    index("pathiseis/", title="Παθήσεις", desc="Πέντε καταστάσεις και ο χάρτης της πυέλου", kind="page",
          kw="παθησεις ακρατεια προπτωση ξηροτητα κυστεοκηλη ορθοκηλη")


# ══════════════════════════════════════════════════════════════════════════════
# ARTICLES
# ══════════════════════════════════════════════════════════════════════════════
def build_toc(body_html):
    """Auto table of contents. Runs on already-anchored markup, so it links to the
    ids that anchor_headings() put on the headings."""
    heads = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body_html, re.S)
    if len(heads) < 3:
        return ""
    items = ""
    for lvl, hid, raw in heads:
        txt = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if txt:
            items += f'<li class="lvl{lvl}"><a href="#{hid}">{html.escape(txt)}</a></li>'
    return f'<nav class="toc"><h2>Σε αυτή τη σελίδα</h2><ol>{items}</ol></nav>' if items else ""


def anchor_headings(body_html):
    n = [0]

    def repl(m):
        n[0] += 1
        return f'<h{m.group(1)} id="s{n[0]}">{m.group(2)}</h{m.group(1)}>'
    return re.sub(r"<h([23])>(.*?)</h\1>", repl, body_html, flags=re.S)


def build_article(slug, tag):
    d = 2
    title = C.article_title(slug)
    body_html, faq_title, faq_pairs = C.prose(slug, d)
    body_html = anchor_headings(body_html)
    toc = build_toc(body_html)
    faq_html, faq_ld = U.faq_block(faq_title, faq_pairs, prefix="faq")
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Άρθρα", "arthra/"), (title, None)], d)
    iso, pretty, mins = C.article_date(slug), C.article_pretty_date(slug), C.read_minutes(slug)
    others = [(s, t) for s, t in ARTICLES if t == tag and s != slug][:6]
    if len(others) < 4:
        others += [(s, t) for s, t in ARTICLES if s != slug and (s, t) not in others][:6 - len(others)]
    rel_cards = [U.article_card(s, t, d) for s, t in others]
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": title[:110],
          "datePublished": iso or None, "dateModified": iso or None,
          "inLanguage": "el", "url": f"{SITE['domain']}/arthra/{slug}/",
          "author": {"@id": SITE["domain"] + "/dr-mirillas/#physician"},
          "publisher": {"@id": SITE["domain"] + "/#clinic"},
          "mainEntityOfPage": f"{SITE['domain']}/arthra/{slug}/"}
    ld = {k: v for k, v in ld.items() if v is not None}
    body = f'''
{U.hero_photo(ARTICLE_IMAGES.get(slug), title, d)}
  <div class="wrap wrap--narrow">{crumb}
    <p class="eyebrow">{html.escape(tag)}</p>
    <h1>{html.escape(title)}</h1>
    <ul class="hero__meta">
      {f"<li>{U.I['clock']}{pretty}</li>" if pretty else ""}
      <li>{mins}′ ανάγνωση</li>
      <li>{U.save_inline(slug, title, f"arthra/{slug}/", "article")}</li>
    </ul>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside">{toc}
    <div class="panel"><h3>Ρωτήστε τον γιατρό</h3>
      <p>Ό,τι διαβάσατε εδώ αφορά τη γενική εικόνα. Το δικό σας περιστατικό θέλει εξέταση.</p>
      <button class="btn btn--cta btn--sm" type="button" data-open="book">Ζητήστε ραντεβού</button></div>
  </aside>
</div>
{faq_html}
{U.row(rid="r-more", eyebrow="Συνεχίστε", title="Σχετικά άρθρα", cards=rel_cards)}
{U.cta_band(d)}
</main>'''
    write(f"arthra/{slug}/index.html",
          shell(path=f"arthra/{slug}/", title=C.seo_title(title),
                desc=C.meta_desc(slug), depth=d, body=body, active="arthra",
                jsonld=[ld, crumb_ld] + ([faq_ld] if faq_ld else [])))
    register(f"arthra/{slug}/", prio="0.6")
    index(f"arthra/{slug}/", title=title, desc=f"{tag} · {pretty}" if pretty else tag,
          kind="article", hue=U.hue(slug), kw=C.plain(slug, 400))


def build_articles_hub():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Άρθρα", None)], d)
    tags = []
    for _s, t in ARTICLES:
        if t not in tags:
            tags.append(t)
    chips = '<button class="chip is-on" type="button" data-art="all">Όλα</button>' + "".join(
        f'<button class="chip" type="button" data-art="{html.escape(t)}">{html.escape(t)}</button>' for t in tags)
    items = "".join(U.photo_tile(
        ARTICLE_IMAGES.get(s), C.article_title(s), d,
        kicker=f'{html.escape(t)} · {C.article_pretty_date(s) or "Άρθρο"}',
        heading=f'<h3><a href="{s}/">{html.escape(C.article_title(s))}</a></h3>',
        body=f'<p>{html.escape(C.plain(s, 150))}…</p>',
        extra_attrs=f' data-tag="{html.escape(t)}" data-title="{html.escape(C.article_title(s), quote=True)}"',
    ) for s, t in ARTICLES)
    body = f'''
{U.hero_photo(HUB_IMAGES.get('arthra/'), 'Άρθρα', d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Αρχείο</p>
    <h1>Άρθρα</h1>
    <p class="lede">{len(ARTICLES)} κείμενα του ιατρείου για την ακράτεια, την πρόπτωση,
      την ξηρότητα και το laser. Φιλτράρετε ή γράψτε για να βρείτε.</p>
    <div class="fld" style="max-width:420px;margin-top:1.4rem">
      <label for="art-q">Αναζήτηση στα άρθρα</label>
      <input id="art-q" type="search" placeholder="π.χ. εμμηνόπαυση" autocomplete="off"></div>
    <div class="chips" style="margin-top:1rem">{chips}</div>
  </div>
</section>
<main id="main"><section class="sec"><div class="wrap">
  <div class="grid-3" id="art-grid">{items}</div>
  <p id="art-empty" hidden style="color:var(--dim);margin-top:2rem">Καμία αντιστοιχία.</p>
</div></section>{U.cta_band(d)}</main>
<script>
(function(){{var q=document.getElementById('art-q'),g=document.getElementById('art-grid'),
e=document.getElementById('art-empty'),chips=[].slice.call(document.querySelectorAll('[data-art]')),tag='all';
function n(s){{return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/ς/g,'σ');}}
function run(){{var v=n(q.value.trim()),shown=0;
[].forEach.call(g.children,function(c){{var okT=tag==='all'||c.dataset.tag===tag;
var okQ=!v||n(c.textContent).indexOf(v)>-1;c.hidden=!(okT&&okQ);if(!c.hidden)shown++;}});
e.hidden=shown>0;}}
q.addEventListener('input',run);
chips.forEach(function(c){{c.addEventListener('click',function(){{chips.forEach(function(x){{x.classList.toggle('is-on',x===c);}});tag=c.dataset.art;run();}});}});}})();
</script>'''
    write("arthra/index.html", shell(path="arthra/", title="Άρθρα | LVRI Athens",
          desc="Κείμενα του ιατρείου για την ακράτεια ούρων, την πρόπτωση, την ξηρότητα κόλπου και τη θεραπεία με laser.",
          depth=d, body=body, active="arthra", jsonld=[crumb_ld]))
    register("arthra/", prio="0.7", freq="weekly")
    index("arthra/", title="Άρθρα", desc=f"{len(ARTICLES)} κείμενα του ιατρείου", kind="page",
          kw="αρθρα blog κειμενα")


# ══════════════════════════════════════════════════════════════════════════════
# TOOL PAGES
# ══════════════════════════════════════════════════════════════════════════════
def build_guide_page():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Σαρωτής συμπτωμάτων", None)], d)
    steps = "".join(f'''<article class="tile"><span class="tile__n">Βήμα {i+1}</span>
      <h3>{html.escape(s['q'])}</h3><p>{html.escape(s['help'] or '')}</p></article>'''
                    for i, s in enumerate(GUIDE_STEPS))
    flags = "".join(f"<li>{html.escape(f)}</li>" for f in RED_FLAGS)
    body = f'''
{U.hero_photo(HUB_IMAGES.get('odigos-symptomaton/'), 'Σαρωτής συμπτωμάτων', d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Διαδραστικό εργαλείο</p>
    <h1>Σαρωτής συμπτωμάτων</h1>
    <p class="lede">Τέσσερα βήματα σε καθημερινή γλώσσα. Στο τέλος βλέπετε με ποιες παθήσεις
      ταιριάζει αυτό που περιγράψατε και ποιες θεραπείες συζητούνται συνήθως.</p>
    <div class="hero__acts">
      <button class="btn btn--cta btn--lg" type="button" data-open="scanner">{U.I['play']}Ξεκινήστε</button>
    </div>
  </div>
</section>
<main id="main">
  <section class="sec"><div class="wrap">
    <div class="sec__head"><p class="eyebrow">Τι θα σας ρωτήσει</p><h2>Τέσσερα βήματα</h2></div>
    <div class="grid-3">{steps}</div>
  </div></section>
  <section class="sec sec--edge"><div class="wrap wrap--narrow">
    <div class="sc__flags"><h3>Ζητήστε εκτίμηση σύντομα αν έχετε</h3><ul>{flags}</ul></div>
    <p style="margin-top:1.6rem;color:var(--dim);font-size:.9rem">Ο υπολογισμός γίνεται εξ ολοκλήρου
      στον browser σας. Καμία απάντηση δεν αποστέλλεται και τίποτα δεν αποθηκεύεται.
      Το αποτέλεσμα είναι προσανατολισμός, όχι διάγνωση.</p>
  </div></section>
  <div class="rv">{U.anatomy_section(d, anatomy_svg())}</div>
  {U.cta_band(d)}
</main>'''
    write("odigos-symptomaton/index.html", shell(path="odigos-symptomaton/",
          title="Σαρωτής συμπτωμάτων | LVRI Athens",
          desc="Τέσσερα βήματα σε καθημερινή γλώσσα δείχνουν με ποιες παθήσεις του πυελικού εδάφους ταιριάζουν τα συμπτώματά σας. Υπολογισμός τοπικά στη συσκευή σας.",
          depth=d, body=body, active="odigos",
          jsonld=[crumb_ld]))
    register("odigos-symptomaton/", prio="0.8")
    index("odigos-symptomaton/", title="Σαρωτής συμπτωμάτων", desc="Διαδραστικό εργαλείο 4 βημάτων",
          kind="page", kw="οδηγος συμπτωματα quiz τεστ scanner")


def build_kegel_page():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Ασκήσεις Kegel", None)], d)
    body = f'''
<section class="page-hero">
  <div class="wrap">{crumb}
    <p class="eyebrow">Προπόνηση</p>
    <h1>Ασκήσεις Kegel</h1>
    <p class="lede">Οι ασκήσεις Kegel αναφέρονται στα κείμενα του ιατρείου ως πρώτη, μη επεμβατική
      επιλογή για την ακράτεια ούρων. Αυτός ο μετρητής κρατά μόνο τον ρυθμό.</p>
  </div>
</section>
<main id="main">
  {U.kegel_section(d, heading=False)}
  <section class="sec sec--edge"><div class="wrap wrap--narrow">
    <div class="sec__head"><h2>Πώς γίνονται σωστά</h2></div>
    <div class="prose">
      <ul>
        <li>Σφίξτε τους μυς που θα χρησιμοποιούσατε για να συγκρατήσετε τα ούρα, όχι την κοιλιά,
          τους γλουτούς ή τους μηρούς.</li>
        <li>Αναπνέετε κανονικά σε όλη τη διάρκεια. Αν κρατάτε την αναπνοή, σφίγγετε λάθος μυς.</li>
        <li>Η χαλάρωση μετράει όσο και το σφίξιμο. Αφήστε τον μυ να ξεκουραστεί πλήρως.</li>
        <li>Καθημερινά, όχι εντατικά. Η βελτίωση φαίνεται σε εβδομάδες, όχι σε ημέρες.</li>
        <li>Αν νιώσετε πόνο ή δεν βρίσκετε τους σωστούς μυς, ζητήστε καθοδήγηση.</li>
      </ul>
      <p>Οι ασκήσεις βοηθούν σε ήπιες μορφές. Σε εγκατεστημένη πρόπτωση ή σε ακράτεια που
        επηρεάζει την καθημερινότητα, χρειάζεται εκτίμηση:
        <a href="../pathiseis/akrateia-ouron/">διαβάστε για την ακράτεια ούρων</a>.</p>
    </div>
  </div></section>
  {U.cta_band(d)}
</main>'''
    write("askiseis-kegel/index.html", shell(path="askiseis-kegel/", title="Ασκήσεις Kegel: προπονητής | LVRI Athens",
          desc="Τρία προγράμματα Kegel με οπτικό ρυθμιστή για σφίξιμο, κράτημα και χαλάρωση και μετρητή συνεδριών. Οδηγίες για σωστή εκτέλεση.",
          depth=d, body=body, active="", jsonld=[crumb_ld]))
    register("askiseis-kegel/", prio="0.7")
    index("askiseis-kegel/", title="Ασκήσεις Kegel", desc="Προπονητής με 3 προγράμματα", kind="page",
          kw="kegel ασκησεις πυελικο εδαφος προπονηση")


def build_mylist_page():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Η λίστα μου", None)], d)
    body = f'''
<section class="page-hero">
  <div class="wrap">{crumb}
    <p class="eyebrow">Στη συσκευή σας</p>
    <h1>Η λίστα μου</h1>
    <p class="lede">Ό,τι κρατήσατε με το <b>+</b>. Μένει μόνο σε αυτόν τον browser:
      δεν συνδέεται με λογαριασμό και δεν φεύγει από τη συσκευή σας.</p>
  </div>
</section>
<main id="main"><section class="sec"><div class="wrap">
  <div data-mylist></div>
</div></section>{U.cta_band(d)}</main>'''
    write("i-lista-mou/index.html", shell(path="i-lista-mou/", title="Η λίστα μου | LVRI Athens",
          desc="Οι θεραπείες, παθήσεις και άρθρα που κρατήσατε. Αποθηκεύονται τοπικά στη συσκευή σας.",
          depth=d, body=body, active="", jsonld=[crumb_ld]))
    register("i-lista-mou/", prio="0.3")


# ══════════════════════════════════════════════════════════════════════════════
# GALLERY
# ══════════════════════════════════════════════════════════════════════════════
def build_gallery():
    d = 1
    photos = [f"result-{i:02d}.jpg" for i in range(1, 18)]
    photo_items = "".join(f'''<button class="gal__i" type="button" data-cat="photo"
      data-full="{rel(d)}assets/img/{p}" data-alt="Αποτέλεσμα επέμβασης {i}, πριν και μετά"
      data-cap="Περιστατικό {i}">{U.pic(p, f"Αποτέλεσμα επέμβασης {i}, πριν και μετά", 484, 176, d)}
      <span class="gal__lock">{U.I['lock']}<span>Κλινική φωτογραφία</span></span></button>'''
                         for i, p in enumerate(photos, 1))
    by_id = {v["id"]: v for v in VIDEO_LIBRARY}
    g_cards = [U.video_card(by_id[i], d) for i in HOME_VIDEOS if i in by_id]
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Gallery", None)], d)
    body = f'''
{U.hero_photo(HUB_IMAGES.get('gallery/'), 'Gallery', d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Αρχείο</p>
    <h1>Gallery</h1>
    <p class="lede">{len(photos)} περιστατικά πριν και μετά. Τα αποτελέσματα διαφέρουν
      από περίπτωση σε περίπτωση. Τα {len(VIDEO_LIBRARY)} βίντεο του ιατρείου βρίσκονται
      πλέον στη <a class="linky" href="{rel(d)}vinteo/">σελίδα Βίντεο</a>.</p>
  </div>
</section>
<main id="main">
  <section class="sec"><div class="wrap">
    <div class="consent">
      <p><b>Οι φωτογραφίες περιστατικών δείχνουν γυμνό.</b> Είναι ιατρικές εικόνες πριν και μετά
        την επέμβαση. Εμφανίζονται μόνο αν το επιλέξετε. Η επιλογή μένει σε αυτή τη συσκευή.</p>
      <button class="btn btn--cta btn--sm" type="button" data-unlock>Εμφάνιση φωτογραφιών</button>
    </div>
    <div class="gal is-locked">{photo_items}</div>
    <p style="margin-top:1.6rem;color:var(--dim-2);font-size:.8rem;max-width:64ch">
      Οι εικόνες αφορούν πραγματικά περιστατικά και δημοσιεύονται με τη συγκατάθεση των ασθενών.
      Δεν αποτελούν υπόσχεση αποτελέσματος: κάθε ανατομία και κάθε επούλωση είναι διαφορετική.</p>
  </div></section>
  <div id="video"></div>
  {U.row(rid="r-gv", eyebrow="του ιατρείου", title="Βίντεο", cards=g_cards,
         all_href=f"{rel(d)}vinteo/", all_label="Όλα τα βίντεο", kind="nf-row--wide")}
  {U.cta_band(d)}
</main>'''
    write("gallery/index.html", shell(path="gallery/", title="Gallery: φωτογραφίες & βίντεο | LVRI Athens",
          desc="Φωτογραφίες περιστατικών πριν και μετά και βίντεο από τηλεοπτικές εκπομπές και ιατρικά συνέδρια. LVRI Athens, Βύρωνας, Αθήνα.",
          depth=d, body=body, active="gallery", jsonld=[crumb_ld]))
    register("gallery/", prio="0.6")
    index("gallery/", title="Gallery", desc="Φωτογραφίες περιστατικών και βίντεο", kind="page",
          kw="gallery φωτογραφιες βιντεο πριν μετα")


# ══════════════════════════════════════════════════════════════════════════════
# VIDEO
# ══════════════════════════════════════════════════════════════════════════════
def video_ld(v):
    """VideoObject ανά βίντεο. Όλα τα πεδία βγαίνουν από τα μεταδεδομένα του
    ίδιου του καναλιού, τίποτα δεν συμπληρώνεται στο περίπου."""
    what = ("Καταγραφή επέμβασης" if v["group"] == "epemvaseis"
            else "Ενημερωτικό βίντεο ή συνέντευξη")
    return {"@type": "VideoObject", "name": v["title"],
            "description": f"{what} από το κανάλι του Dr. Κωνσταντίνου Μυρίλλα: {v['title']}.",
            "uploadDate": v["date"],
            "duration": f"PT{v['secs'] // 60}M{v['secs'] % 60}S",
            "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg",
            "embedUrl": f"https://www.youtube.com/embed/{v['id']}",
            "url": f"https://www.youtube.com/watch?v={v['id']}",
            "publisher": {"@id": SITE["domain"] + "/#clinic"}}


def build_videos():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Βίντεο", None)], d)
    chips = "".join(
        f'<button class="chip{" is-on" if i == 0 else ""}" type="button" data-vt="{g["slug"]}"'
        f' aria-controls="vt-{g["slug"]}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'{html.escape(g["title"])} <span class="chip__n">{len(g["items"])}</span></button>'
        for i, g in enumerate(VIDEO_GROUPS))

    panels = ""
    for i, g in enumerate(VIDEO_GROUPS):
        cards = "".join(U.video_card(v, d) for v in g["items"])
        warn = (f'<div class="consent" style="margin-bottom:1.6rem"><p><b>{html.escape(g["warn"])}</b> '
                f'Το υλικό προορίζεται για ενημέρωση ασθενών και συναδέλφων και μπορεί να '
                f'φανεί δυσάρεστο. Η αναπαραγωγή ξεκινά μόνο αν πατήσετε μια κάρτα.</p></div>'
                if g["warn"] else "")
        panels += f'''
  <section class="vt__panel" id="vt-{g["slug"]}" data-vt-panel="{g["slug"]}">
    <h2>{html.escape(g["title"])}</h2>
    <p class="vt__lead">{html.escape(g["lead"])}</p>
    {warn}
    <div class="vt__grid">{cards}</div>
  </section>'''

    total = len(VIDEO_LIBRARY)
    body = f'''
{U.hero_photo(HUB_IMAGES.get("vinteo/"), "Βίντεο", d)}
  <div class="wrap">{crumb}
    <p class="eyebrow">Αρχείο</p>
    <h1>Βίντεο</h1>
    <p class="lede">{total} βίντεο από το κανάλι του Dr. Κωνσταντίνου Μυρίλλα:
      {len(VIDEO_GROUPS[0]["items"])} καταγραφές επεμβάσεων και
      {len(VIDEO_GROUPS[1]["items"])} συνεντεύξεις, ομιλίες και ενημερωτικά βίντεο.
      Παίζουν από το YouTube, χωρίς να φορτώνει τίποτα πριν πατήσετε.</p>
    <div class="fld" style="max-width:420px;margin-top:1.4rem">
      <label for="vt-q">Αναζήτηση στα βίντεο</label>
      <input id="vt-q" type="search" placeholder="π.χ. ινομυώματα" autocomplete="off"></div>
    <div class="chips" style="margin-top:1rem">{chips}</div>
  </div>
</section>
<main id="main"><section class="sec"><div class="wrap">
  {panels}
  <p class="vt__empty" id="vt-empty" hidden>Καμία αντιστοιχία.</p>
  <p style="margin-top:2.4rem;color:var(--dim-2);font-size:.8rem;max-width:64ch">
    Τα βίντεο φιλοξενούνται στο YouTube και παίζουν μέσα από το youtube-nocookie.com.
    Δεν υποκαθιστούν την ιατρική εξέταση: κάθε περιστατικό κρίνεται ξεχωριστά.
    <a class="linky" href="{YOUTUBE_CHANNEL}" rel="noopener" target="_blank"
       style="text-decoration:underline">Το κανάλι στο YouTube</a>.</p>
</div></section>{U.cta_band(d)}</main>
<script>
(function(){{var q=document.getElementById('vt-q'),
e=document.getElementById('vt-empty'),
chips=[].slice.call(document.querySelectorAll('[data-vt]')),
panels=[].slice.call(document.querySelectorAll('[data-vt-panel]')),tab=chips[0].dataset.vt;
function n(s){{return (s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ς/g,'σ');}}
function run(){{var v=n(q.value.trim()),shown=0;
panels.forEach(function(p){{var open=v?true:p.dataset.vtPanel===tab,hits=0;
[].forEach.call(p.querySelector('.vt__grid').children,function(c){{
var ok=!v||n(c.textContent).indexOf(v)>-1;c.hidden=!ok;if(ok)hits++;}});
p.hidden=!open||(!!v&&!hits);if(!p.hidden)shown+=hits;}});
e.hidden=shown>0;}}
chips.forEach(function(c){{c.addEventListener('click',function(){{
chips.forEach(function(x){{x.classList.toggle('is-on',x===c);
x.setAttribute('aria-pressed',x===c?'true':'false');}});tab=c.dataset.vt;run();}});}});
q.addEventListener('input',run);run();}})();
</script>'''
    write("vinteo/index.html", shell(
        path="vinteo/", title="Βίντεο: επεμβάσεις, συνεντεύξεις και ενημέρωση | LVRI Athens",
        desc=f"{total} βίντεο του Dr. Κωνσταντίνου Μυρίλλα: καταγραφές λαπαροσκοπικών και "
             f"υστεροσκοπικών επεμβάσεων, τηλεοπτικές συνεντεύξεις, ομιλίες και ενημέρωση "
             f"για παθήσεις και θεραπείες.",
        depth=d, body=body, active="vinteo",
        jsonld=[crumb_ld,
                {"@context": "https://schema.org", "@type": "ItemList",
                 "name": "Βίντεο LVRI Athens", "numberOfItems": total,
                 "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                      "item": video_ld(v)}
                                     for i, v in enumerate(VIDEO_LIBRARY)]}]))
    register("vinteo/", prio="0.7")
    index("vinteo/", title="Βίντεο", desc=f"{total} βίντεο: επεμβάσεις, συνεντεύξεις, ενημέρωση",
          kind="page", kw="βιντεο video youtube επεμβασεις συνεντευξεις ομιλιες καναλι")
    for g in VIDEO_GROUPS:
        index(f"vinteo/#vt-{g['slug']}", title=f"Βίντεο: {g['title']}",
              desc=f"{len(g['items'])} βίντεο από το κανάλι του ιατρείου", kind="page",
              kw=f"βιντεο video {g['title'].lower()}")


# ══════════════════════════════════════════════════════════════════════════════
# CLINIC · DOCTORS · CONTACT · TERMS
# ══════════════════════════════════════════════════════════════════════════════
def build_clinic():
    d = 1
    body_html, faq_title, faq_pairs = C.prose("h-kliniki", d)
    body_html = anchor_headings(body_html)
    faq_html, faq_ld = U.faq_block(faq_title, faq_pairs)
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Η κλινική", None)], d)
    venues = "".join(f'''<article class="tile"><span class="tile__n">{html.escape(n)}</span>
      <h3>{html.escape(a)}</h3><p>{html.escape(t)}</p></article>'''
                     for n, a, t in SITE["venues"])
    body = f'''
<section class="page-hero">
  <div class="wrap">{crumb}
    <p class="eyebrow">Από το {SITE['founded']}</p>
    <h1>Η κλινική</h1>
    <p class="lede">{SITE['legal']}: κέντρο κοσμητικής γυναικολογίας και επανορθωτικής
      χειρουργικής πυέλου με laser, στον Βύρωνα.</p>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside">{build_toc(body_html)}
    <div class="panel"><h3>Πού θα μας βρείτε</h3>
      <ul class="facts">
        <li><span class="k">Ιατρείο</span><span class="v">{SITE['address']}, {SITE['postcode']}</span></li>
        <li><span class="k">Τηλέφωνο</span><span class="v"><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></span></li>
        <li><span class="k">Email</span><span class="v"><a href="mailto:{SITE['email']}">{SITE['email']}</a></span></li>
      </ul>
      <a class="btn btn--ghost btn--sm" href="../epikoinonia/" style="margin-top:1rem">Χάρτης & ωράριο</a></div>
    <div class="panel"><h3>Ο γιατρός</h3><p>Dr. Κωνσταντίνος Μυρίλλας, μαιευτήρας χειρουργός γυναικολόγος.</p>
      <a class="btn btn--cta btn--sm" href="../dr-mirillas/">Βιογραφικό</a></div>
  </aside>
</div>
<section class="sec sec--edge"><div class="wrap">
  <div class="sec__head"><p class="eyebrow">Δύο χώροι</p><h2>Πού γίνεται τι</h2></div>
  <div class="grid-3">{venues}</div>
</div></section>
{faq_html}
{U.cta_band(d)}</main>'''
    write("i-kliniki/index.html", shell(path="i-kliniki/", title="Η κλινική | LVRI Athens",
          desc=C.meta_desc("h-kliniki", "Το LVRI Athens στον Βύρωνα: κοσμητική γυναικολογία και επανορθωτική χειρουργική πυέλου με laser."),
          depth=d, body=body, active="kliniki",
          jsonld=[crumb_ld] + ([faq_ld] if faq_ld else [])))
    register("i-kliniki/", prio="0.8")
    index("i-kliniki/", title="Η κλινική", desc="Ποιοι είμαστε, από το 2008", kind="page",
          kw="κλινικη ιατρειο lvri athens βυρωνας")


def build_doctor(slug, legacy, name, role, photo, blurb):
    d = 1
    body_html, faq_title, faq_pairs = C.prose(legacy, d)
    body_html = anchor_headings(body_html)
    faq_html, faq_ld = U.faq_block(faq_title, faq_pairs)
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), (name, None)], d)
    body = f'''
<section class="page-hero">
  <div class="wrap">{crumb}
    <p class="eyebrow">{html.escape(role)}</p>
    <h1>{html.escape(name)}</h1>
    <p class="lede">{html.escape(blurb)}</p>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">
    <figure style="margin:0 0 2rem">{U.pic(photo, name, 500, 700, d)}</figure>
    {body_html}
  </article>
  <aside class="doc__aside">{build_toc(body_html)}
    <div class="panel"><h3>Ραντεβού</h3><p>Ζητήστε μια εκτίμηση. Δεν δεσμεύει σε τίποτα.</p>
      <button class="btn btn--cta btn--sm" type="button" data-open="book">Ζητήστε ραντεβού</button></div>
  </aside>
</div>{faq_html}{U.cta_band(d)}</main>'''
    write(f"{slug}/index.html", shell(path=f"{slug}/", title=C.seo_title(name),
          desc=C.meta_desc(legacy, blurb), depth=d, body=body, active="", jsonld=[crumb_ld] + ([faq_ld] if faq_ld else [])))
    register(f"{slug}/", prio="0.7")
    index(f"{slug}/", title=name, desc=role, kind="page", kw=name + " " + role + " " + blurb)


def build_contact():
    d = 1
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Επικοινωνία", None)], d)
    hours = "".join(f"<li><span>{a}</span><b>{b}</b></li>" for a, b in SITE["hours"])
    areas = "".join(f"<li>{html.escape(a)}</li>" for a in SITE["areas"])
    venues = "".join(f'''<article class="tile"><span class="tile__n">{html.escape(n)}</span>
      <h3>{html.escape(a)}</h3><p>{html.escape(t)}</p></article>''' for n, a, t in SITE["venues"])
    faqs = [
        ("Πού ακριβώς βρίσκεται το ιατρείο;",
         f"<p>{SITE['address']}, {SITE['postcode']}, {SITE['locality']}. Το pin στον χάρτη είναι "
         f"στις συντεταγμένες {SITE['lat']}, {SITE['lng']}.</p>"),
        ("Ποιες ώρες λειτουργεί;",
         "<p>Δευτέρα έως Παρασκευή 09:00 έως 17:00 και Σάββατο 09:00 έως 15:00. Την Κυριακή είμαστε κλειστά.</p>"),
        ("Χρειάζεται ραντεβού;",
         "<p>Ναι. Καλέστε στο " + SITE["phone"] + " ή στείλτε αίτημα από τη φόρμα· απαντάμε "
         "την ίδια ή την επόμενη εργάσιμη.</p>"),
        ("Πού γίνονται οι επεμβάσεις;",
         "<p>Στο Μαιευτήριο ΡΕΑ, όπου ο Dr. Μυρίλλας διευθύνει από το 2013 το τμήμα πλαστικής "
         "κόλπου και επανορθωτικής χειρουργικής πυέλου με laser. Τα ραντεβού, οι εξετάσεις και "
         "οι θεραπείες laser γίνονται στο ιατρείο του Βύρωνα.</p>"),
        ("Από ποιες περιοχές έρχονται ασθενείς;",
         "<p>Κυρίως από τον Βύρωνα και τις όμορες περιοχές: Καισαριανή, Παγκράτι, Ζωγράφου, "
         "Υμηττό, Ηλιούπολη, Δάφνη, αλλά και από όλη την Αττική και την υπόλοιπη Ελλάδα.</p>"),
        ("Μιλάτε αγγλικά;",
         '<p>Ναι. Οι βασικές σελίδες υπάρχουν και <a href="../en/">στα αγγλικά</a>.</p>'),
    ]
    faq_html, faq_ld = U.faq_block("Συχνές ερωτήσεις για την επίσκεψη", faqs, prefix="faq")
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage",
                  "url": f"{SITE['domain']}/epikoinonia/",
                  "mainEntity": {"@id": SITE["domain"] + "/#clinic"}}
    body = f'''
<section class="page-hero">
  <div class="wrap">{crumb}
    <p class="eyebrow">Επικοινωνία</p>
    <h1>Ελάτε να τα πούμε</h1>
    <p class="lede">Ένα τηλέφωνο, ένα email, ή η φόρμα. Ό,τι σας βολεύει.</p>
    <div class="hero__acts">
      <a class="btn btn--cta btn--lg" href="tel:{SITE['phone_href']}">{U.I['phone']}{SITE['phone']}</a>
      <button class="btn btn--glass btn--lg" type="button" data-open="book">Φόρμα ραντεβού</button>
    </div>
  </div>
</section>
<main id="main">
  <section class="sec"><div class="wrap">
    <div class="grid-3">
      <article class="tile"><span class="tile__n">Διεύθυνση</span>
        <h3>{SITE['address']}</h3><p>{SITE['postcode']}, {SITE['locality']}, {SITE['region']}</p>
        <p><a class="btn btn--ghost btn--sm" href="{SITE['map']}" rel="noopener" target="_blank">Άνοιγμα στους χάρτες</a></p></article>
      <article class="tile"><span class="tile__n">Τηλέφωνο & email</span>
        <h3><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></h3>
        <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p></article>
      <article class="tile"><span class="tile__n">Ωράριο</span>
        <ul class="ft__hours" style="margin:0;list-style:none;padding:0">{hours}</ul></article>
    </div>
  </div></section>
  <section class="sec sec--edge"><div class="wrap">
    <div class="sec__head"><p class="eyebrow">Χάρτης</p><h2>Βρείτε μας</h2></div>
    <div style="border:1px solid var(--line);border-radius:var(--r-l);overflow:hidden">
      <iframe title="Χάρτης: {SITE['address']}" width="100%" height="420" style="border:0;display:block;filter:grayscale(.3) invert(.92) hue-rotate(180deg)"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q={SITE['lat']},{SITE['lng']}&hl=el&z=16&output=embed"></iframe>
    </div>
  </div></section>
  <section class="sec"><div class="wrap">
    <div class="sec__head"><p class="eyebrow">Δύο χώροι</p><h2>Ιατρείο και χειρουργείο</h2></div>
    <div class="grid-3">{venues}</div>
    <div class="sec__head" style="margin-top:clamp(28px,4vw,52px)"><p class="eyebrow">Εξυπηρετούμε</p>
      <h2>Περιοχές</h2></div>
    <ul class="card__chips" style="gap:.4rem">{areas}</ul>
  </div></section>
  {faq_html}
  {U.cta_band(d)}
</main>'''
    write("epikoinonia/index.html", shell(path="epikoinonia/", title="Επικοινωνία: Βύρωνας, Αθήνα | LVRI Athens",
          desc=f"LVRI Athens: {SITE['address']}, {SITE['postcode']} {SITE['locality']}. Τηλέφωνο {SITE['phone']}, Δευτέρα έως Παρασκευή 09:00 έως 17:00 και Σάββατο 09:00 έως 15:00.",
          depth=d, body=body, active="epikoinonia",
          jsonld=[contact_ld, crumb_ld] + ([faq_ld] if faq_ld else [])))
    register("epikoinonia/", prio="0.9")
    index("epikoinonia/", title="Επικοινωνία", desc=f"{SITE['address']} · {SITE['phone']}", kind="page",
          kw="επικοινωνια τηλεφωνο διευθυνση χαρτης ωραριο ραντεβου")


def build_terms():
    d = 1
    body_html, _t, _p = C.prose("oroi-chrisis-politiki-aporritou", d, drop_faq=False)
    body_html = anchor_headings(body_html)
    crumb, crumb_ld = U.crumbs([("Αρχική", ""), ("Όροι χρήσης & απόρρητο", None)], d)
    body = f'''
<section class="page-hero"><div class="wrap wrap--narrow">{crumb}
  <p class="eyebrow">Νομικά</p><h1>Όροι χρήσης & απόρρητο</h1></div></section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}
    <h2 id="local">Τι κρατά αυτός ο ιστότοπος στη συσκευή σας</h2>
    <ul>
      <li><b>Η λίστα μου</b>: όσα κρατήσατε με το «+».</li>
      <li><b>Συνεδρίες Kegel</b>: ο μετρητής ολοκληρωμένων συνεδριών.</li>
      <li><b>Επιλογές εμφάνισης</b>: κίνηση, αντίθεση, εναλλαγή hero.</li>
      <li><b>Συγκατάθεση</b>: για τα cookies και για τις κλινικές φωτογραφίες.</li>
    </ul>
    <p>Όλα αυτά μένουν στον browser σας (localStorage). Δεν αποστέλλονται πουθενά, δεν συνδέονται
      με λογαριασμό και μπορείτε να τα σβήσετε από το εικονίδιο ρυθμίσεων στην κορυφή.</p>
  </article>
  <aside class="doc__aside">{build_toc(body_html)}</aside>
</div></main>'''
    write("oroi-chrisis/index.html", shell(path="oroi-chrisis/", title="Όροι χρήσης & πολιτική απορρήτου | LVRI Athens",
          desc="Όροι χρήσης, πολιτική απορρήτου και τι αποθηκεύει ο ιστότοπος τοπικά στη συσκευή σας.",
          depth=d, body=body, active="", jsonld=[crumb_ld]))
    register("oroi-chrisis/", prio="0.2", freq="yearly")


# ══════════════════════════════════════════════════════════════════════════════
# ENGLISH
# ══════════════════════════════════════════════════════════════════════════════
EN_NAV = [("en/", "Home")] + [(f"en/{new}/", title) for new, _legacy, title in EN_PAGES]


def topbar_en(depth, active=""):
    r = rel(depth)
    links = "".join(f'<a class="tb__link{" is-on" if href == active else ""}" href="{r}{href}">{t}</a>'
                    for href, t in EN_NAV[:5])
    return f'''<header class="tb" id="topbar" data-at-top="1">
  <div class="tb__in">
    <a class="tb__logo" href="{r}en/" aria-label="LVRI Athens, home">
      <span class="tb__word">LVRI<em>Athens</em></span></a>
    <nav class="tb__nav" aria-label="Main navigation">{links}</nav>
    <div class="tb__right">
      <a class="tb__ic" href="{r}" aria-label="Ελληνικά" title="Ελληνικά"
         style="width:auto;padding:0 .8em;border-radius:100px;font-size:.8rem;font-weight:700">ΕΛ</a>
      <a class="tb__call" href="tel:{SITE['phone_href']}">{U.I['phone']}<span>{SITE['phone']}</span></a>
      <button class="btn btn--cta tb__cta" type="button" data-open="book">Book</button>
      <button class="tb__ic tb__burger" type="button" data-open="drawer" aria-label="Menu">{U.I['burger']}</button>
    </div>
  </div>
  <div class="tb__scan" aria-hidden="true"></div>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="drawer__sheet" role="dialog" aria-modal="true" aria-label="Menu">
    <button class="drawer__x" type="button" data-close aria-label="Close">{U.I['close']}</button>
    <nav class="drawer__nav">{"".join(f'<a class="tb__link" href="{r}{h}">{t}</a>' for h, t in EN_NAV)}</nav>
    <a class="btn btn--ghost" href="{r}">Ελληνική έκδοση</a>
    <button class="btn btn--cta" type="button" data-open="book">Request an appointment</button>
  </div>
</div>'''


def footer_en(depth):
    r = rel(depth)
    links = "".join(f'<li><a href="{r}{h}">{t}</a></li>' for h, t in EN_NAV[1:])
    return f'''<footer class="ft"><div class="ft__glow" aria-hidden="true"></div>
  <div class="wrap ft__grid" style="grid-template-columns:1.4fr 1fr 1.2fr">
    <div class="ft__brand"><a class="tb__logo" href="{r}en/">
      <span class="tb__word">LVRI<em>Athens</em></span></a>
      <p class="ft__tag">{SITE['legal']}. Cosmetic gynaecology and pelvic floor reconstruction in Athens, since {SITE['founded']}.</p></div>
    <div><h3>Pages</h3><ul>{links}</ul></div>
    <div class="ft__nap"><h3>Contact</h3><ul class="ft__contact">
      <li>{U.I['pin']}<span>{SITE['address_en']}<br>{SITE['postcode']}</span></li>
      <li>{U.I['phone']}<a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
      <li>{U.I['mail']}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li></ul>
      <ul class="ft__hours">{"".join(f"<li><span>{a}</span><b>{b}</b></li>" for a, b in SITE['hours_en'])}</ul></div>
  </div>
  <div class="wrap ft__base"><p>© {TODAY[:4]} {SITE['name']}</p>
    <p><a href="{r}">Ελληνικά</a> · Made by <a href="{SITE['credit']['url']}" rel="noopener" target="_blank">{SITE['credit']['name']}</a></p></div>
</footer>'''


def en_shell(*, path, title, desc, depth, body, active=""):
    head = U.head(title=title, desc=desc, depth=depth, canonical=path, lang="en",
                  jsonld=[base_graph()])
    return head + topbar_en(depth, active) + body + footer_en(depth) + \
        U.tail(depth, extra_js=page_scripts(depth), lang="en")


def build_en_home():
    d = 1
    # The legacy "en/home" record is the Greek homepage mirrored by mistake, with
    # broken markup, so this page is written, not extracted. Every fact below
    # already appears on the clinic's own English pages.
    body_html = f"""
<h2 id="s1">What we do</h2>
<p>LVRI Athens is a centre for cosmetic gynaecology and reconstructive pelvic floor
surgery, working with CO<sub>2</sub> laser. It has been open in Athens since {SITE['founded']}.
Consultations, examinations and in-office laser sessions take place at the practice in
Vyronas; operations take place at REA Maternity Hospital, where Dr. Myrillas has directed
the department of vaginal plastic and reconstructive pelvic laser surgery since 2013.</p>
<h2 id="s2">What we treat</h2>
<p>Urinary incontinence, uterine and vaginal prolapse, cystocele, rectocele and enterocele,
vaginal dryness and atrophy, and vaginal laxity, with options that run from a painless
in-office laser session to full vaginal reconstruction.</p>
<h2 id="s3">Techniques</h2>
<p>The practice works with Laser Vaginal Rejuvenation<sup>&reg;</sup> and Designer Laser
Vaginoplasty<sup>&reg;</sup>, the techniques developed by
<a href="../dr-matlock/">Dr. David L. Matlock</a>, alongside non-invasive laser rejuvenation
and injectable treatments.</p>
<h2 id="s4">Languages</h2>
<p>Consultations are held in Greek and English. The pages below cover the main procedures
and conditions in English; the full site is in
<a href="../">Greek</a>.</p>
"""
    tiles = "".join(U.photo_tile(
        EN_IMAGES.get(new), title, 1, kicker="English",
        heading=f'<h3><a href="{new}/">{html.escape(title)}</a></h3>',
    ) for new, _legacy, title in EN_PAGES)
    body = f'''
{U.hero_photo('clinic-team.jpg', 'LVRI Athens', 1)}
  <div class="wrap">
    <p class="eyebrow">Athens, Greece</p>
    <h1>Laser Vaginal Rejuvenation Institute of Athens</h1>
    <p class="lede">Cosmetic gynaecology and pelvic floor reconstruction with CO₂ laser,
      in Athens since {SITE['founded']}.</p>
    <div class="hero__acts">
      <button class="btn btn--cta btn--lg" type="button" data-open="book">Request an appointment</button>
      <a class="btn btn--glass btn--lg" href="tel:{SITE['phone_href']}">{U.I['phone']}{SITE['phone']}</a>
    </div>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside"><div class="panel"><h3>Contact</h3>
    <ul class="facts">
      <li><span class="k">Address</span><span class="v">{SITE['address_en']}</span></li>
      <li><span class="k">Phone</span><span class="v"><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></span></li>
      <li><span class="k">Email</span><span class="v"><a href="mailto:{SITE['email']}">{SITE['email']}</a></span></li>
    </ul></div></aside>
</div>
<section class="sec sec--edge"><div class="wrap">
  <div class="sec__head"><p class="eyebrow">In English</p><h2>Procedures & conditions</h2></div>
  <div class="grid-3">{tiles}</div>
</div></section></main>'''
    write("en/index.html", en_shell(path="en/", title="LVRI Athens: Laser Vaginal Rejuvenation Institute",
          desc=C.meta_desc("en/home", "Cosmetic gynaecology and pelvic floor reconstruction with CO2 laser in Athens."),
          depth=d, body=body, active="en/"))
    register("en/", prio="0.7")


def build_en_page(new, legacy, title):
    d = 2
    body_html, faq_title, faq_pairs = C.prose(legacy, d)
    body_html = anchor_headings(body_html)
    faq_html, _ld = U.faq_block(faq_title, faq_pairs)
    body = f'''
{U.hero_photo(EN_IMAGES.get(new), title, 2)}
  <div class="wrap wrap--narrow">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">English</a></li>
      <li aria-current="page">{html.escape(title)}</li></ol></nav>
    <h1>{html.escape(title)}</h1>
  </div>
</section>
<main id="main"><div class="wrap doc">
  <article class="doc__main prose">{body_html}</article>
  <aside class="doc__aside">{build_toc(body_html)}
    <div class="panel"><h3>Request an appointment</h3>
      <p>We reply the same or next working day.</p>
      <button class="btn btn--cta btn--sm" type="button" data-open="book">Book</button></div>
  </aside>
</div>{faq_html}</main>'''
    write(f"en/{new}/index.html", en_shell(path=f"en/{new}/", title=f"{title} | LVRI Athens",
          desc=C.meta_desc(legacy, title + " at LVRI Athens."), depth=d, body=body, active=f"en/{new}/"))
    register(f"en/{new}/", prio="0.6")


# ══════════════════════════════════════════════════════════════════════════════
# 404 · INDEX FILES · REDIRECTS
# ══════════════════════════════════════════════════════════════════════════════
def build_404():
    d = 0
    body = f'''
<section class="page-hero" style="text-align:center">
  <div class="wrap wrap--narrow">
    <p class="eyebrow">404</p>
    <h1>Η σελίδα άλλαξε διεύθυνση</h1>
    <p class="lede" style="margin-inline:auto">Ο ιστότοπος ανανεώθηκε. Αν ήρθατε από παλιό σύνδεσμο,
      ψάξτε από εδώ, ή πατήστε <kbd>⌘</kbd><kbd>K</kbd>.</p>
    <div class="hero__acts" style="justify-content:center">
      <button class="btn btn--cta btn--lg" type="button" data-open="palette">Αναζήτηση</button>
      <a class="btn btn--glass btn--lg" href="/">Αρχική</a>
    </div>
  </div>
</section>
<main id="main">
  {U.row(rid="r-404t", title="Θεραπείες", cards=[U.treatment_card(t, d) for t in TREATMENTS])}
  {U.row(rid="r-404c", title="Παθήσεις", cards=[U.condition_card(c, d) for c in CONDITIONS])}
</main>'''
    write("404.html", shell(path="", title="Δεν βρέθηκε | LVRI Athens",
          desc="Η σελίδα δεν βρέθηκε.", depth=d, body=body, active=""))


def _redirect_pairs():
    """Every legacy URL that must keep working, resolved to its new home."""
    pairs = []
    for legacy, target in sorted(C.URLMAP.items()):
        if legacy == "home":
            continue
        pairs.append((f"/{legacy}/", "/" + target))
    seen, out = set(), []
    for a, b in pairs:
        if a not in seen and a.strip("/") != b.strip("/"):
            seen.add(a)
            out.append((a, b))
    return out


def build_index_files():
    write("search-index.json", json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")))
    urls = "".join(
        f"  <url><loc>{SITE['domain']}/{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{f}</changefreq><priority>{p}</priority></url>\n"
        for u, p, f in PAGES)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")

    # Vercel: same conventions as version 1: 301s, immutable asset caching, security headers.
    cfg = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "trailingSlash": True, "cleanUrls": False,
        "redirects": [{"source": a, "destination": b, "permanent": True}
                      for a, b in _redirect_pairs()],
        "headers": [
            {"source": "/assets/(img|docs)/(.*)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/assets/(css|js)/(.*)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=86400, must-revalidate"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()"}]},
        ],
    }
    write("vercel.json", json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    write(".vercelignore", "# Build sources, not part of the deployed site.\n"
                           "_source/\n.htaccess\n_redirects\n")


def build_redirects():
    pairs = list(_redirect_pairs())
    for pid, legacy in sorted(C.PID.items(), key=lambda x: int(x[0])):
        t = C.URLMAP.get(C.ALIAS.get(legacy, legacy))
        if t is not None:
            pairs.append((f"/?p={pid}", "/" + t))
    lines = "".join(f"{a}  {b}  301\n" for a, b in pairs)
    write("_redirects", lines)
    ht = ["RewriteEngine On", "RewriteBase /", "",
          "# 301s from the previous site structure"]
    for a, b in pairs:
        if a.startswith("/?p="):
            continue
        ht.append(f"RedirectMatch 301 ^{re.escape(a).replace(chr(92) + '/', '/')}?$ {b}")
    ht += ["", "ErrorDocument 404 /404.html",
           "<IfModule mod_deflate.c>",
           "  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml",
           "</IfModule>",
           "<IfModule mod_expires.c>", "  ExpiresActive On",
           "  ExpiresByType text/css \"access plus 1 year\"",
           "  ExpiresByType application/javascript \"access plus 1 year\"",
           "  ExpiresByType image/webp \"access plus 1 year\"", "</IfModule>", ""]
    write(".htaccess", "\n".join(ht))


# ══════════════════════════════════════════════════════════════════════════════
def copy_assets():
    for sub in ("css", "js"):
        src = os.path.join(SRC, "assets", sub)
        dst = os.path.join(OUT, "assets", sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    # images and docs come from the version-1 asset pipeline
    for sub in ("img", "docs"):
        s = os.path.join(ASSETS_SRC, sub)
        d = os.path.join(OUT, "assets", sub)
        if os.path.isdir(s) and not os.path.isdir(d):
            shutil.copytree(s, d)


def main():
    os.makedirs(OUT, exist_ok=True)
    copy_assets()
    build_home()
    build_treatments_hub()
    for t in TREATMENTS:
        build_treatment(t)
    build_conditions_hub()
    for c in CONDITIONS:
        build_condition(c)
    build_articles_hub()
    for slug, tag in ARTICLES:
        build_article(slug, tag)
    build_gallery()
    build_videos()
    build_guide_page()
    build_kegel_page()
    build_mylist_page()
    build_clinic()
    build_doctor("dr-mirillas", "dr-k-mirillas", "Dr. Κωνσταντίνος Μυρίλλας",
                 "Μαιευτήρας χειρουργός γυναικολόγος",
                 "dr-myrillas.jpg",
                 "Ιδρυτής του LVRI Athens. Διευθύνει από το 2013 το τμήμα πλαστικής κόλπου και "
                 "επανορθωτικής χειρουργικής πυέλου με laser στο Μαιευτήριο ΡΕΑ.")
    build_doctor("dr-matlock", "david-l-matlock", "Dr. David L. Matlock",
                 "Δημιουργός των LVR® και DLV®",
                 "dr-matlock.jpg",
                 "Ο Αμερικανός γυναικολόγος που ανέπτυξε τις τεχνικές Laser Vaginal Rejuvenation® "
                 "και Designer Laser Vaginoplasty®.")
    build_contact()
    build_terms()
    build_en_home()
    for new, legacy, title in EN_PAGES:
        build_en_page(new, legacy, title)
    build_404()
    build_index_files()
    build_redirects()
    n = sum(len(files) for _r, _d, files in os.walk(OUT) if _r.find("assets") < 0)
    print(f"✓ {len(PAGES)} σελίδες · {len(SEARCH)} εγγραφές ευρετηρίου → {OUT}")


if __name__ == "__main__":
    main()
