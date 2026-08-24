# LVRI Athens — νέος ιστότοπος

Στατικός ιστότοπος (HTML/CSS/JS χωρίς εξαρτήσεις) που παράγεται από τα κείμενα
του υπάρχοντος site. Καμία βάση δεδομένων, κανένα build tool πέρα από Python 3.

```
lvri-new/
├── site/                 ← το παραδοτέο. Ανεβάζετε ΑΥΤΟΝ τον φάκελο.
│   ├── index.html …      45 σελίδες + 404
│   ├── assets/{css,js,img,docs}
│   ├── search-index.json  ευρετήριο αναζήτησης (παράγεται)
│   ├── sitemap.xml · robots.txt
│   └── _redirects · .htaccess   ← 301 από τα παλιά URL
├── content/
│   ├── data.py           ← ΕΔΩ αλλάζετε περιεχόμενο, τιμές, μενού
│   ├── legacy.json       κείμενα που εξήχθησαν από το παλιό site
│   └── assets.json       αντιστοίχιση παλιών/νέων αρχείων εικόνας
└── tools/
    ├── extract.py        παλιό site  → legacy.json
    ├── assets.py         παλιό site  → assets/img
    ├── parts.py          header, footer, dialogs, ανατομικό διάγραμμα
    └── build.py          όλα τα παραπάνω → site/
```

## Ξαναχτίσιμο

```bash
python3 lvri-new/tools/build.py
```

Τρέχει σε ~1 δευτερόλεπτο και ξαναγράφει όλες τις σελίδες. Τα `extract.py` και
`assets.py` χρειάζονται μόνο αν αλλάξει το αρχικό υλικό.

## Τοπική προεπισκόπηση

```bash
cd lvri-new/site && python3 -m http.server 8899
```

## Τι αλλάζετε πού

| Θέλετε να αλλάξετε | Αρχείο |
|---|---|
| Τηλέφωνο, email, διεύθυνση, ωράριο | `content/data.py` → `SITE` |
| Παθήσεις, κείμενα καρτών, στατιστικά | `content/data.py` → `CONDITIONS` |
| Θεραπείες και ο πίνακας σύγκρισης | `content/data.py` → `TREATMENTS` |
| Ερωτήσεις του οδηγού συμπτωμάτων | `content/data.py` → `GUIDE_STEPS` |
| Προγράμματα Kegel | `content/data.py` → `KEGEL` |
| Λίστα άρθρων και κατηγορίες | `content/data.py` → `ARTICLES` |
| Βίντεο gallery (YouTube IDs) | `content/data.py` → `VIDEOS` |
| Χρώματα, γραμματοσειρές, αποστάσεις | `site/assets/css/lvri.css` → `:root` |
| Κείμενα μενού / κουμπιών (EL & EN) | `tools/parts.py` → `T` |

Το κυρίως κείμενο κάθε σελίδας ζει στο `content/legacy.json` (πεδίο `html`).
Είναι απλό HTML — μπορείτε να το επεξεργαστείτε απευθείας και να ξαναχτίσετε.

## Διαδραστικά στοιχεία

| Στοιχείο | Πού | Τι κάνει |
|---|---|---|
| Οδηγός συμπτωμάτων | αρχική, `/odigos-symptomaton/`, `/pathiseis/` | 4 βήματα σε καθημερινή γλώσσα → σταθμισμένη αντιστοίχιση με παθήσεις και θεραπείες. Υπολογίζεται τοπικά στον browser. |
| Ανατομικό διάγραμμα | αρχική, `/pathiseis/` | Custom SVG τομή πυέλου. Hotspots ανά όργανο + εναλλαγή «Φυσιολογική / Με χαλάρωση». Προσβάσιμο με πληκτρολόγιο. |
| Μετρητής Kegel | `/askiseis-kegel/`, αρχική | 3 προγράμματα, οπτικός ρυθμιστής σφίξιμο/κράτημα/χαλάρωση, μετρητής συνεδριών σε localStorage. |
| Σύγκριση θεραπειών | `/therapeies/` | Πίνακας με φίλτρα επεμβατικότητας. |
| Αίτημα ραντεβού | παντού | Modal με validation, επιλογή ώρας που σέβεται το ωράριο (κλειστά Κυριακή, Σάββατο ως 15:00), σύνθεση email. |
| Αναζήτηση ιστότοπου | παντού (`Ctrl/⌘ + K`) | Client-side, με απαλοιφή τόνων και τελικού σίγμα. |
| Gallery | `/gallery/` | Φίλτρα, lightbox με πλοήγηση πληκτρολογίου, **κλείδωμα κλινικών φωτογραφιών** μέχρι ρητή επιλογή του επισκέπτη. |
| Άρθρα | `/arthra/` | Ζωντανή αναζήτηση + φίλτρα κατηγορίας. |
| Άρθρα & σελίδες | παντού | Αυτόματος πίνακας περιεχομένων με scroll-spy, μπάρα προόδου ανάγνωσης, FAQ accordions με deep-link. |
| Cookies | παντού | Ξεχωριστή συγκατάθεση για στατιστικά, αποθήκευση επιλογής. |

Το αίτημα ραντεβού συνθέτει email — δεν υπάρχει server. Αν θέλετε φόρμα που
στέλνεται απευθείας, χρειάζεται endpoint (π.χ. Formspree) στο `booking()` του
`site/assets/js/lvri.js`.

## Τοπικό SEO (Βύρωνας / Αθήνα)

Το site είναι ένα ιατρείο σε μία διεύθυνση, οπότε τα τοπικά σήματα συγκεντρώνονται
αντί να διασπείρονται σε σελίδες-«κλώνους» ανά προάστιο (doorway pages — τις τιμωρεί
η Google). Τι υπάρχει:

- **Structured data**: ένα `@graph` με `MedicalClinic` + `LocalBusiness` και `Physician`
  σε κάθε σελίδα, με `geo` (37.9568854, 23.7617037 — από το ίδιο το pin του πελάτη),
  `hasMap`, `areaServed` (12 όμορες περιοχές + Αττική + Ελλάδα), `openingHoursSpecification`,
  `availableService` με τις πέντε θεραπείες, `knowsLanguage`, `priceRange`.
- **Ανά σελίδα**: `MedicalCondition` με `possibleTreatment`, `MedicalProcedure` με
  `howPerformed` / `preparation` / `followup`, `FAQPage`, `BreadcrumbList`, `ContactPage`.
- **Geo meta**: `geo.region` (GR-A1), `geo.placename`, `geo.position`, `ICBM`,
  Open Graph `place:location:*` και `business:contact_data:*`.
- **NAP**: ίδια ακριβώς γραφή σε footer, σελίδα επικοινωνίας και schema. Ο ΤΚ είναι
  **162 31** — επιβεβαιωμένος από το Google Maps pin του πελάτη.
- **Σελίδα τοποθεσίας**: το `/epikoinonia/` έχει χάρτη με συντεταγμένες, τους δύο
  χώρους (ιατρείο Βύρωνα / μαιευτήριο ΡΕΑ), τις περιοχές προέλευσης ασθενών και έξι
  τοπικές ερωτήσεις με `FAQPage` schema.
- **Titles & descriptions**: ειδικότητα + περιοχή όπου διαβάζεται φυσικά. Όλες οι
  περιγραφές ξαναγράφτηκαν — οι παλιές ήταν keyword stuffing («Super Αποτελέσματα —
  Χαμηλό Κόστος! Τηλ. Ραντεβού: 2107609109»), που ρίχνει το CTR και τη σοβαρότητα.

### Τι μένει εκτός κώδικα

Το μεγαλύτερο μέρος του τοπικού SEO δεν παίζεται στον ιστότοπο:

1. **Google Business Profile** — αν δεν υπάρχει, φτιάξτε το· αν υπάρχει, ταιριάξτε
   ακριβώς NAP, ωράριο, κατηγορία («Γυναικολόγος» / «Ιατρικό κέντρο»), φωτογραφίες.
   Είναι ο #1 παράγοντας για το local pack.
2. **Κριτικές** — δεν μπήκε `aggregateRating` στο schema, γιατί θα ήταν κατασκευασμένο.
   Μόλις υπάρχουν πραγματικές κριτικές, συνδέονται.
3. **Τοπικές καταχωρήσεις** με ίδιο NAP: Χρυσός Οδηγός, Doctoranytime, Vrisko, iatronet.
4. **Λεπτομέρειες πρόσβασης** που δεν επινοήσαμε: γραμμές λεωφορείων, στάση, parking,
   όροφος, κουδούνι. Δώστε τα και μπαίνουν στο `/epikoinonia/`.

## SEO & μετάβαση

- 301 ανακατευθύνσεις για **όλα** τα παλιά URL: `_redirects` (Netlify/Cloudflare)
  και `.htaccess` (Apache). Σε Nginx μεταφράστε τις γραμμές του `_redirects`.
- `sitemap.xml`, `robots.txt`, canonical, hreflang el/en σε κάθε σελίδα.
- Structured data: `MedicalClinic`, `Physician`, `MedicalCondition`,
  `MedicalProcedure`, `Article`, `FAQPage`, `BreadcrumbList`.
- Open Graph + Twitter cards.

## Ποιότητα

- Εικόνες σε WebP με fallback (`<picture>`), lazy loading, ρητά width/height.
- Προσβασιμότητα: skip link, landmarks, ορατό focus, ARIA στα widgets,
  σεβασμός στο `prefers-reduced-motion`.
- Γραμματοσειρές: **GFS Didot** (Greek Font Society) για τους τίτλους,
  **Commissioner** (Κώστας Μπαρτσώκας) για το κείμενο — και οι δύο με πλήρη
  ελληνική κάλυψη, από Google Fonts.
- Καμία εξωτερική εξάρτηση JavaScript.
- Credit «Made by ClinicBrain» → https://clinicbrain.gr στο κάτω μέρος κάθε σελίδας
  (`SITE["credit"]` στο `content/data.py`).

## Πριν τη δημοσίευση

1. Ελέγξτε τα στοιχεία επικοινωνίας και το ωράριο στο `content/data.py`.
2. Ενημερώστε το κείμενο στο `/oroi-chrisis/` με τα πραγματικά στοιχεία του
   υπευθύνου επεξεργασίας δεδομένων.
3. Επιβεβαιώστε ότι υπάρχει γραπτή συγκατάθεση ασθενών για κάθε φωτογραφία
   στο `/gallery/`.
4. Ανεβάστε το `site/` και επιβεβαιώστε ότι οι ανακατευθύνσεις δουλεύουν.
5. Δηλώστε ξανά το `sitemap.xml` στο Google Search Console.

### Προαιρετικό

Πέντε τίτλοι άρθρων ξεπερνούν τους 70 χαρακτήρες και η Google θα τους κόψει στα
αποτελέσματα αναζήτησης. Είναι οι αρχικοί τίτλοι του πελάτη — δεν τους αλλάξαμε.
Αν θέλετε συντομότερους, επεξεργαστείτε το πεδίο `h1` του άρθρου στο
`content/legacy.json` και ξαναχτίστε.
