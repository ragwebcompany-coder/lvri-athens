# LVRI Athens

Ιστότοπος του Laser Vaginal Rejuvenation Institute of Athens.
Στατικό site — HTML/CSS/JS χωρίς εξαρτήσεις, χωρίς build step στο deploy.

**Live:** https://lvri-athens.vercel.app

## Δομή

```
/                  το site όπως σερβίρεται (45 σελίδες + 404)
  assets/{css,js,img,docs}
  vercel.json      301 από τα παλιά URL, cache & security headers
  sitemap.xml · robots.txt · search-index.json
_source/           ο generator — δεν γίνεται deploy (.vercelignore)
  content/data.py  ΕΔΩ αλλάζετε περιεχόμενο, στοιχεία, μενού
  tools/build.py   ξαναχτίζει όλες τις σελίδες
  BUILD.md         αναλυτικές οδηγίες
```

## Αλλαγές στο site

```bash
# 1. επεξεργασία _source/content/data.py ή _source/content/legacy.json
# 2. ξαναχτίσιμο στο root του repo
LVRI_OUT=. python3 _source/tools/build.py
# 3. commit & push — το Vercel κάνει deploy μόνο του
```

## Τοπική προεπισκόπηση

```bash
python3 -m http.server 8080   # http://localhost:8080
```

## Deploy

Vercel · Framework Preset **Other** · Output Directory `.`
Το `vercel.json` κρατά `trailingSlash: true` και τις 36 ανακατευθύνσεις 301
από τα παλιά WordPress URL. Τα `_redirects` (Netlify) και `.htaccess` (Apache)
υπάρχουν για φορητότητα αν αλλάξει hosting.

## Σημειώσεις

- Η φόρμα ραντεβού συνθέτει email — δεν υπάρχει backend. Για απευθείας αποστολή
  χρειάζεται endpoint (Formspree / Web3Forms) στο `booking()` του `assets/js/lvri.js`.
- Η αναζήτηση είναι client-side πάνω στο `search-index.json`.
- Οι κλινικές φωτογραφίες στο `/gallery/` εμφανίζονται μόνο μετά από ρητή
  επιλογή του επισκέπτη.
