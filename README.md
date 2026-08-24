# LVRI Athens — στατικό site

Στατικό αντίγραφο του lvriathens.com (WordPress → static), έτοιμο για Vercel / GitHub Pages.

## Τοπική προεπισκόπηση
    python3 -m http.server 8080
    # http://localhost:8080

## Deploy
Push σε GitHub → import στο Vercel (Framework Preset: **Other**, Output Directory: `.`)

## Σημειώσεις
- Η φόρμα επικοινωνίας χρειάζεται εξωτερική υπηρεσία (Formspree / Web3Forms).
- Η αναζήτηση του WordPress δεν λειτουργεί σε στατικό site.
