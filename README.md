# LVRI Athens

Στατικός ιστότοπος για το **Laser Vaginal Rejuvenation Institute of Athens**.
Το περιεχόμενο του repo **είναι** το ανεβασμένο site: ό,τι βρίσκεται στο root σερβίρεται
από το Vercel. Ο κώδικας που το παράγει ζει στο `_source/` και δεν ανεβαίνει
(`.vercelignore`).

## Δομή

```
/                    ← το site που σερβίρεται (HTML, assets, sitemap, redirects)
/_source/content/    ← η μοναδική πηγή περιεχομένου: data.py + legacy.json
/_source/tools/      ← generator έκδοσης 1
/_source/v2/         ← generator έκδοσης 2
```

Και οι δύο generators διαβάζουν το **ίδιο** `_source/content/`. Αλλάζετε το κείμενο μία
φορά και ξαναχτίζετε όποια έκδοση θέλετε.

## Ξαναχτίσιμο

```bash
# έκδοση 2 (τρέχουσα σχεδίαση)
LVRI2_OUT="$PWD" python3 _source/v2/build.py

# έκδοση 1
LVRI_OUT="$PWD" python3 _source/tools/build.py
```

Τρέχει σε ~2 δευτερόλεπτα, χωρίς εξαρτήσεις πέρα από Python 3, και ξαναγράφει και τις
46 σελίδες μαζί με `sitemap.xml`, `robots.txt`, `vercel.json`, `_redirects` και `.htaccess`.

## Τοπική προεπισκόπηση

```bash
python3 -m http.server 8899
```

## Τι αλλάζετε πού

| Θέλετε να αλλάξετε | Αρχείο |
|---|---|
| Τηλέφωνο, διεύθυνση, ωράριο | `_source/content/data.py` → `SITE` |
| Θεραπείες, παθήσεις, στατιστικά | `_source/content/data.py` |
| Κείμενο σελίδας | `_source/content/legacy.json` (πεδίο `html`) |
| Χρώματα, γραμματοσειρές (v2) | `_source/v2/src/assets/css/v2.css` → `:root` |
| Φωτογραφία θεραπείας/πάθησης | `_source/content/data.py` → πεδίο `image` |

Αναλυτικά για την έκδοση 2: [`_source/v2/README.md`](_source/v2/README.md).
Για την έκδοση 1: [`_source/BUILD.md`](_source/BUILD.md).
