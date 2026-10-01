# -*- coding: utf-8 -*-
"""Site data for LVRI Athens.

Every clinical figure here is taken from the clinic's own published copy in
`legacy.json`; nothing is invented. Edit this file to change the site.
"""

SITE = {
    "name": "LVRI Athens",
    "legal": "Laser Vaginal Rejuvenation Institute of Athens",
    "domain": "https://lvriathens.com",
    "phone": "210 7609109",
    "phone_href": "+302107609109",
    "email": "info@lvriathens.com",
    "address": "Καραολή & Δημητρίου 41, Βύρωνας",
    "address_en": "Karaoli & Dimitriou 41, Vyronas, Athens",
    "postcode": "162 31",
    "map": "https://goo.gl/maps/G8ceMgUT5fFua3pm7",
    "map_full": ("https://www.google.com/maps/place/Karaoli+ke+Dimitriou+41,"
                 "+Vironas+162+31/@37.956885,23.761704,16z"),
    "lat": 37.9568854,
    "lng": 23.7617037,
    "region_iso": "GR-A1",          # Αττική, ISO 3166-2
    "locality": "Βύρωνας",
    "locality_en": "Vyronas",
    "region": "Αττική",
    "founded": "2008",
    "hours": [("Δευτέρα έως Παρασκευή", "09:00 έως 17:00"),
              ("Σάββατο", "09:00 έως 15:00"),
              ("Κυριακή", "Κλειστά")],
    "hours_en": [("Monday to Friday", "09:00 to 17:00"),
                 ("Saturday", "09:00 to 15:00"),
                 ("Sunday", "Closed")],
    # Where the clinic's work actually happens. Both facts come from the
    # clinic's own biography copy; confirm before changing.
    "venues": [
        ("Ιατρείο Βύρωνα", "Καραολή & Δημητρίου 41, Βύρωνας",
         "Ραντεβού, εξέταση, θεραπείες laser και ενέσιμες θεραπείες."),
        ("Μαιευτήριο ΡΕΑ", "Νότια προάστια Αθηνών",
         "Χειρουργικές επεμβάσεις. Ο Dr. Μυρίλλας διευθύνει εκεί από το 2013 "
         "το τμήμα πλαστικής κόλπου και επανορθωτικής χειρουργικής πυέλου με laser."),
    ],
    # Όμορες περιοχές που εξυπηρετούνται καθημερινά, δηλώνονται ως areaServed,
    # δεν φτιάχνουμε ξεχωριστή σελίδα για την καθεμία (doorway pages).
    "areas": ["Βύρωνας", "Καισαριανή", "Παγκράτι", "Ζωγράφου", "Υμηττός",
              "Ηλιούπολη", "Δάφνη", "Άγιος Αρτέμιος", "Νέος Κόσμος",
              "Κέντρο Αθήνας", "Αργυρούπολη", "Γλυφάδα"],
    "credit": {"name": "Astra", "url": "https://astramarketing.gr"},
    "social": {
        "facebook": "https://www.facebook.com/lvriathens/",
        "youtube": "https://www.youtube.com/user/KMyrillas",
    },
}

# ── Conditions ────────────────────────────────────────────────────────────────
# `organ` ties the entry to a hotspot in the pelvic-floor diagram.
CONDITIONS = [
    dict(slug="akrateia-ouron", legacy="akrateia-ouron", organ="bladder",
         title="Ακράτεια ούρων",
         image="cond-akrateia.jpg",
         meta="Ακράτεια ούρων στις γυναίκες: οι τέσσερις τύποι, τα αίτια, ο ουροδυναμικός έλεγχος και οι θεραπείες, από ασκήσεις Kegel μέχρι laser και χειρουργείο.",
         lead="Αφορά περίπου το 20% των γυναικών στην Ελλάδα. Είναι σύμπτωμα, όχι ασθένεια, και στις περισσότερες περιπτώσεις αντιμετωπίζεται ριζικά.",
         plain="Χάνω ούρα χωρίς να το θέλω.",
         stat=("20%", "των γυναικών στην Ελλάδα"),
         treatments=["anazoogonisi-kolpou", "laser-plastiki-kolpou"]),

    dict(slug="proptosi-mitras", legacy="proptosi-mitras", organ="uterus",
         title="Πρόπτωση μήτρας & κόλπου",
         image="cond-proptosi.jpg",
         meta="Πρόπτωση μήτρας και κόλπου: πώς αναγνωρίζεται, τα στάδια κατά POP-Q και οι θεραπείες που αποκαθιστούν την ανατομία του πυελικού εδάφους.",
         lead="Όταν το μυϊκό σύστημα που στηρίζει την πύελο χαλαρώσει, τα όργανα κατεβαίνουν. Ταξινομείται σε στάδια κατά POP-Q.",
         plain="Νιώθω βάρος ή κάτι να προβάλλει.",
         stat=("4", "στάδια κατά POP-Q"),
         treatments=["xeirourgiki-pyelikou-edafous", "laser-plastiki-kolpou"]),

    dict(slug="ksirotita-kolpou", legacy="kolpiki-ksirotita", organ="vagina",
         title="Ξηρότητα κόλπου",
         image="cond-ksirotita.jpg",
         meta="Ξηρότητα κόλπου: γιατί συμβαίνει, με ή χωρίς εμμηνόπαυση, και πώς την αντιμετωπίζουν το laser και οι ενέσιμες θεραπείες με υαλουρονικό.",
         lead="Δεν αφορά μόνο την εμμηνόπαυση. Ο κόλπος χάνει ελαστικότητα και κολλαγόνο, το pH αλκαλοποιείται και η χλωρίδα αλλάζει.",
         plain="Νιώθω ξηρότητα, κάψιμο ή πόνο στην επαφή.",
         stat=("pH 6 έως 7", "αλκαλοποίηση του κόλπου"),
         treatments=["anazoogonisi-kolpou"]),

    dict(slug="kysteokili", legacy="kysteokhlh", organ="bladder",
         title="Κυστεοκήλη",
         image="cond-kysteokili.jpg",
         meta="Κυστεοκήλη: όταν η ουροδόχος κύστη προβάλλει στο πρόσθιο τοίχωμα του κόλπου. Συμπτώματα, βαθμοί βαρύτητας και θεραπευτικές επιλογές.",
         lead="Η ουροδόχος κύστη προβάλλει προς το πρόσθιο τοίχωμα του κόλπου, συχνά μαζί με δυσκολία στην πλήρη κένωση.",
         plain="Δυσκολεύομαι να αδειάσω την κύστη μου.",
         stat=("Πρόσθιο", "τοίχωμα κόλπου"),
         treatments=["xeirourgiki-pyelikou-edafous", "laser-plastiki-kolpou"]),

    dict(slug="orthokili-enterokili", legacy="orthokili-enterokili", organ="rectum",
         title="Ορθοκήλη & εντεροκήλη",
         image="cond-orthokili.jpg",
         meta="Ορθοκήλη και εντεροκήλη: συμπτώματα, διαφορές και θεραπεία, από μη επεμβατικό laser στις αρχόμενες μορφές μέχρι πλήρη ανάπλαση κόλπου.",
         lead="Το ορθό ή το λεπτό έντερο πιέζει το οπίσθιο τοίχωμα του κόλπου. Προκαλεί δυσκοιλιότητα και επώδυνη επαφή.",
         plain="Δυσκολεύομαι στην κένωση, χρειάζομαι πίεση.",
         stat=("Οπίσθιο", "τοίχωμα κόλπου"),
         treatments=["anazoogonisi-kolpou", "xeirourgiki-pyelikou-edafous"]),
]

# ── Treatments ────────────────────────────────────────────────────────────────
# `matrix` powers the comparison tool. Values come straight from the clinic copy.
TREATMENTS = [
    dict(slug="anazoogonisi-kolpou", legacy="anazoogonisi-kolpou",
         title="Αναζωογόνηση κόλπου με laser",
         image="treat-anazoogonisi.jpg",
         short="Renovalaser / IntimaLase",
         meta="Αναζωογόνηση κόλπου με laser: 2 έως 3 ανώδυνες συνεδρίες των 15 λεπτών στο ιατρείο, χωρίς χρόνο ανάρρωσης, για ξηρότητα, ατροφία και ήπια χαλάρωση.",
         lead="Μη επεμβατικό laser στο ιατρείο. Αποκαθιστά την ελαστικότητα και την κολλαγόνωση του κόλπου.",
         invasive="non",
         matrix=dict(setting="Ιατρείο", anesthesia="Δεν απαιτείται",
                     sessions="2 έως 3 συνεδρίες", duration="15 λεπτά ανά συνεδρία",
                     recovery="Χωρίς ανάρρωση", pain="Ανώδυνο"),
         treats=["Ξηρότητα & ατροφία", "Ήπια χαλάρωση", "Ήπια ακράτεια", "Αρχόμενη ορθοκήλη"]),

    dict(slug="aidoioplastiki", legacy="plastiki-aidoiou",
         title="Αιδοιοπλαστική",
         image="treat-aidoioplastiki.jpg",
         short="Designer Laser Vaginoplasty®",
         meta="Αιδοιοπλαστική (Designer Laser Vaginoplasty®): αισθητική χειρουργική των αιδοιϊκών δομών, των χειλέων, του εφηβαίου και του περινέου.",
         lead="Αισθητική χειρουργική ενίσχυση των αιδοιϊκών δομών: μεγάλα και μικρά χείλη, εφηβαίο, περίνεο, είσοδος κόλπου.",
         invasive="surgical",
         matrix=dict(setting="Χειρουργείο ημέρας", anesthesia="Κατά προτίμηση τοπική",
                     sessions="1 επέμβαση", duration="Εξατομικευμένη",
                     recovery="Παυσίπονα κατά τις πρώτες ημέρες", pain="Χωρίς πόνο κατά την επέμβαση"),
         treats=["Μεγάλα & μικρά χείλη", "Εφηβαίο", "Περίνεο", "Είσοδος κόλπου"]),

    dict(slug="laser-plastiki-kolpou", legacy="laser-kolpou",
         title="Laser πλαστική κόλπου",
         image="treat-laser-plastiki.jpg",
         short="Laser Vaginal Rejuvenation®",
         meta="Laser πλαστική κόλπου (LVR®): χειρουργική σύσφιξη με CO₂ laser σε χειρουργείο ημέρας, χωρίς αφαίρεση ραμμάτων και με άμεση επιστροφή στα δικά σας.",
         lead="Χειρουργική σύσφιξη με CO₂ laser. Χειρουργείο ημέρας, χωρίς αφαίρεση ραμμάτων.",
         invasive="surgical",
         matrix=dict(setting="Χειρουργείο ημέρας", anesthesia="Εξατομικευμένη",
                     sessions="1 επέμβαση", duration="Εξιτήριο ίδια ή επόμενη ημέρα",
                     recovery="Επιστροφή σχεδόν άμεσα · αποχή επαφής 5 έως 6 εβδομάδες",
                     pain="Χωρίς αφαίρεση ραμμάτων"),
         treats=["Χαλάρωση κόλπου", "Μειωμένη αίσθηση", "Ήπια πρόπτωση"]),

    dict(slug="xeirourgiki-pyelikou-edafous", legacy="xeirourgiki-pyelikou-edafous",
         title="Χειρουργική πυελικού εδάφους",
         image="treat-xeirourgiki.jpg",
         short="Total Vaginal Reconstruction",
         meta="Χειρουργική πυελικού εδάφους: πλήρης ανάπλαση κόλπου με επεμβατικό CO₂ laser για βαρύτερη κυστεοκήλη, ορθοκήλη και πρόπτωση μήτρας.",
         lead="Πλήρης ανάπλαση του κόλπου με επεμβατικό CO₂ laser για βαρύτερες ή παραμελημένες κήλες.",
         invasive="surgical",
         matrix=dict(setting="Χειρουργείο", anesthesia="Εξατομικευμένη",
                     sessions="1 επέμβαση", duration="Εξατομικευμένη",
                     recovery="Κατά περίπτωση", pain="Υπό αναισθησία"),
         treats=["Κυστεοκήλη", "Ορθοκήλη & εντεροκήλη", "Πρόπτωση μήτρας"]),

    dict(slug="g-shot", legacy="g-shot",
         title="G-Shot®",
         image="treat-g-shot.jpg",
         short="Ενίσχυση σημείου G",
         meta="G-Shot®: ένεση υαλουρονικού υψηλού μοριακού βάρους στο σημείο G με τοπική αναισθησία. Επίσκεψη κάτω από 30 λεπτά, χωρίς χρόνο ανάρρωσης.",
         lead="Ένεση υαλουρονικού υψηλού μοριακού βάρους στο σημείο G, με τη βοήθεια ειδικού κολποσκοπίου.",
         invasive="minor",
         matrix=dict(setting="Ιατρείο", anesthesia="Τοπική",
                     sessions="1 συνεδρία", duration="Επίσκεψη κάτω από 30 λεπτά",
                     recovery="Χωρίς ανάρρωση", pain="Ανώδυνο"),
         treats=["Σεξουαλική διέγερση", "Ένταση οργασμού"]),
]

# ── Symptom guide ─────────────────────────────────────────────────────────────
# Plain-language statements, weighted towards the conditions above. This is
# orientation, not diagnosis: the result screen says so explicitly.
GUIDE_STEPS = [
    dict(id="main", type="multi",
         q="Τι σας απασχολεί περισσότερο;",
         help="Διαλέξτε όσα σας ταιριάζουν. Δεν υπάρχει σωστή απάντηση.",
         options=[
             ("leak-effort", "Χάνω ούρα όταν βήχω, φταρνίζομαι ή γελάω", {"akrateia-ouron": 3}),
             ("leak-urgent", "Με πιάνει ξαφνική, επιτακτική ανάγκη για ούρηση", {"akrateia-ouron": 3}),
             ("night", "Ξυπνώ τη νύχτα για να πάω στην τουαλέτα", {"akrateia-ouron": 2}),
             ("heavy", "Νιώθω βάρος ή πίεση χαμηλά στην κοιλιά", {"proptosi-mitras": 3, "kysteokili": 1}),
             ("bulge", "Αισθάνομαι κάτι να προβάλλει από τον κόλπο", {"proptosi-mitras": 4}),
             ("empty", "Δυσκολεύομαι να αδειάσω τελείως την κύστη μου", {"kysteokili": 4}),
             ("uti", "Έχω συχνές ουρολοιμώξεις", {"kysteokili": 2}),
             ("bowel", "Δυσκολεύομαι στην κένωση ή χρειάζομαι πίεση", {"orthokili-enterokili": 4}),
             ("dry", "Νιώθω ξηρότητα, κάψιμο ή ερεθισμό", {"ksirotita-kolpou": 4}),
             ("pain-sex", "Η επαφή είναι επώδυνη ή δυσάρεστη",
              {"ksirotita-kolpou": 3, "orthokili-enterokili": 1}),
             ("laxity", "Νιώθω χαλάρωση ή μειωμένη αίσθηση στην επαφή",
              {"proptosi-mitras": 1, "ksirotita-kolpou": 1}),
             ("look", "Με ενοχλεί η εμφάνιση της περιοχής", {}),
         ]),
    dict(id="since", type="single",
         q="Από πότε το παρατηρείτε;",
         help="Μας βοηθά να καταλάβουμε πόσο επείγει.",
         options=[("weeks", "Λίγες εβδομάδες", {}), ("months", "Μερικούς μήνες", {}),
                  ("years", "Πάνω από έναν χρόνο", {}), ("unsure", "Δεν θυμάμαι ακριβώς", {})]),
    dict(id="context", type="multi",
         q="Ισχύει κάτι από τα παρακάτω;",
         help="Προαιρετικό. Επηρεάζει ποια θεραπεία ταιριάζει καλύτερα.",
         options=[
             ("birth", "Έχω γεννήσει με φυσιολογικό τοκετό", {"proptosi-mitras": 1, "orthokili-enterokili": 1}),
             ("meno", "Βρίσκομαι σε ή μετά την εμμηνόπαυση", {"ksirotita-kolpou": 2}),
             ("surgery", "Έχω κάνει επέμβαση στην πύελο", {"proptosi-mitras": 1}),
             ("none", "Τίποτα από αυτά", {}),
         ]),
    dict(id="impact", type="single",
         q="Πόσο επηρεάζει την καθημερινότητά σας;",
         help="",
         options=[("low", "Ελάχιστα, απλώς με προβληματίζει", {}),
                  ("mid", "Αρκετά, αποφεύγω κάποια πράγματα", {}),
                  ("high", "Πολύ, αλλάζω τον τρόπο που ζω", {})]),
]

RED_FLAGS = [
    "Αιμορραγία εκτός περιόδου ή μετά την εμμηνόπαυση",
    "Έντονος, επίμονος πόνος στην πύελο",
    "Πυρετός μαζί με ενοχλήσεις στην ούρηση",
]

# ── Kegel programmes ─────────────────────────────────────────────────────────
# Kegel exercises are named in the clinic's incontinence copy as a first-line,
# non-invasive option; the trainer just paces them.
KEGEL = [
    dict(id="start", name="Εισαγωγικό", desc="Για την πρώτη εβδομάδα",
         contract=3, hold=3, release=5, reps=10),
    dict(id="build", name="Ενδυνάμωση", desc="Όταν οι 3 δευτ. γίνονται εύκολες",
         contract=5, hold=5, release=5, reps=12),
    dict(id="hold", name="Αντοχή", desc="Για μεγαλύτερη διάρκεια συγκράτησης",
         contract=8, hold=8, release=8, reps=10),
]

# ── Articles ─────────────────────────────────────────────────────────────────
MONTHS = {"Ιαν": "01", "Φεβ": "02", "Μάρ": "03", "Απρ": "04", "Μάιος": "05", "Μάι": "05",
          "Ιούν": "06", "Ιούλ": "07", "Αύγ": "08", "Σεπ": "09", "Οκτ": "10",
          "Νοέ": "11", "Δεκ": "12"}

ARTICLES = [
    ("poies-afora-i-ksirotita-kolpou-kai-pos-tin-antimetopizei-i-sygchroni-iatriki", "Ξηρότητα"),
    ("mathete-ta-panta-gia-tin-proptosi-mitras", "Πρόπτωση"),
    ("aidoioplastiki-tonoste-tin-aftopepoithisi-sas-allakste-tin-poiotita-tis-zois-sas", "Αιδοιοπλαστική"),
    ("apolafste-tin-kathe-mera-kratiste-makria-tin-kolpiki-ksirotita", "Ξηρότητα"),
    ("akrateia-ouron-aitia-diagnosi-therapeia", "Ακράτεια"),
    ("therapeia-akrateias-ouron-ksirotitas-sysfixis-kolpou", "Ακράτεια"),
    ("ygieini-kata-tis-kolpitidas", "Πρόληψη"),
    ("proto-pagosmio-synedrio-laha-laser", "Επιστήμη"),
    ("to-laser-stin-sygxroni-epoxi", "Laser"),
    ("plastiki-kolpou-o-dr-myrillas-apanta", "Πλαστική κόλπου"),
    ("plastiki-kolpou-vlaves-pou-diorthonei", "Πλαστική κόλπου"),
    ("arthro-gia-tin-kolpiki-proptosi", "Πρόπτωση"),
    ("arthro-gia-tin-akrateia-ouron", "Ακράτεια"),
    ("akrateia-ouron-prospatheias", "Ακράτεια"),
    ("akrateia-ouron-aitia-kai-therapeia", "Ακράτεια"),
    ("ksirotita-kolpou-kata-tin-emminopausi-to-laser-einai-h-lysi", "Ξηρότητα"),
]

# ── Images ───────────────────────────────────────────────────────────────────
# Each article's own featured image on lvriathens.com, re-cropped to 4:3.
# A slug missing here falls back to the typographic title poster.
ARTICLE_IMAGES = {
    "poies-afora-i-ksirotita-kolpou-kai-pos-tin-antimetopizei-i-sygchroni-iatriki": "art-ksirotita-moderni.jpg",
    "mathete-ta-panta-gia-tin-proptosi-mitras": "art-proptosi-panta.jpg",
    "aidoioplastiki-tonoste-tin-aftopepoithisi-sas-allakste-tin-poiotita-tis-zois-sas": "art-aidoioplastiki.jpg",
    "apolafste-tin-kathe-mera-kratiste-makria-tin-kolpiki-ksirotita": "art-ksirotita-kathimera.jpg",
    "akrateia-ouron-aitia-diagnosi-therapeia": "art-akrateia-diagnosi.jpg",
    "therapeia-akrateias-ouron-ksirotitas-sysfixis-kolpou": "art-akrateia-therapeia.jpg",
    "ygieini-kata-tis-kolpitidas": "art-ygieini.jpg",
    "proto-pagosmio-synedrio-laha-laser": "art-synedrio.jpg",
    "to-laser-stin-sygxroni-epoxi": "art-laser-epoxi.jpg",
    "plastiki-kolpou-o-dr-myrillas-apanta": "art-myrillas-apanta.jpg",
    "plastiki-kolpou-vlaves-pou-diorthonei": "art-vlaves.jpg",
    "arthro-gia-tin-kolpiki-proptosi": "art-kolpiki-proptosi.jpg",
    "arthro-gia-tin-akrateia-ouron": "art-akrateia-arthro.jpg",
    "akrateia-ouron-prospatheias": "art-akrateia-prospatheias.jpg",
    "akrateia-ouron-aitia-kai-therapeia": "art-akrateia-aitia.jpg",
    "ksirotita-kolpou-kata-tin-emminopausi-to-laser-einai-h-lysi": "art-emminopausi.jpg",
}

# English pages reuse the image of their Greek counterpart.
EN_IMAGES = {
    "the-clinic": "clinic-team.jpg",
    "urinary-incontinence": "cond-akrateia.jpg",
    "vaginal-atrophy": "en-atrophy.jpg",
    "vaginal-dryness": "cond-ksirotita.jpg",
    "vaginal-tightening-laser": "treat-laser-plastiki.jpg",
    "designer-laser-vaginoplasty": "treat-aidoioplastiki.jpg",
}

# Hub pages (photographic hero behind the title).
HUB_IMAGES = {
    "therapeies/": "hub-therapeies.jpg",
    "pathiseis/": "hub-pathiseis.jpg",
    "arthra/": "hub-arthra.jpg",
    "gallery/": "hub-gallery.jpg",
    "odigos-symptomaton/": "hub-odigos.jpg",
}

# ── Βίντεο ────────────────────────────────────────────────────────────────────
# Το κανάλι YouTube του ιατρού, χωρισμένο στις δύο ενότητες που δείχνει η σελίδα
# /vinteo/. Τίποτα δεν φιλοξενείται εδώ: το iframe του youtube-nocookie φορτώνει
# μόνο αφού πατηθεί η κάρτα, οπότε η σελίδα ξεκινά με μηδέν αιτήματα προς το
# YouTube. Το `secs` είναι η διάρκεια σε δευτερόλεπτα και το `date` η ημερομηνία
# ανεβάσματος, όπως τα δίνει το ίδιο το κανάλι.
YOUTUBE_CHANNEL = "https://www.youtube.com/@KMyrillas"


def V(vid, title, secs, date):
    return dict(id=vid, title=title, secs=secs, date=date)


VIDEO_GROUPS = [
    dict(slug="epemvaseis", title="Επεμβάσεις",
         lead="Καταγραφές από το χειρουργείο: λαπαροσκοπικές και υστεροσκοπικές "
              "τεχνικές, όπως βιντεοσκοπήθηκαν κατά τη διάρκεια της επέμβασης.",
         warn="Τα βίντεο αυτής της ενότητας δείχνουν πραγματικό χειρουργείο.",
         items=[
        V("Ztf3aAmVnl8", "Εκτεταμένη λύση συμφύσεων", 176, "2023-12-12"),
        V("O-j--kculzA", "Αφαίρεση ινομυωμάτων", 354, "2021-08-30"),
        V("NrCe2Q3l4xk", "Λαπαροσκοπική υστερεκτομία", 235, "2021-08-23"),
        V("3d_PkwJBlhU", "Επεμβατική υστεροσκόπηση", 134, "2021-05-26"),
        V("h6kXAEQw4ho", "Αφαίρεση εξωμήτριου κύησης", 125, "2021-05-06"),
        V("0sn-0fyhVPs", "Αφαίρεση δερμοειδούς κύστης", 229, "2021-04-28"),
        V("V4dnTzpiyE4", "Αφαίρεση σαλπίγγων και ωοθηκών", 183, "2021-03-07"),
        V("cgjOsb9lbSA", "Λαπαροσκοπική υπερτραχηλική υστερεκτομία", 208, "2021-02-09"),
        V("BDkqraHX6bc", "Λαπαροσκοπική υφολική υστερεκτομία", 191, "2021-01-26"),
        V("wcxrn0bL2f0", "Λαπαροσκοπική υστερεκτομία, πλήρες περιστατικό", 393, "2020-12-15"),
        V("WHNq7l7vS5E", "Εξωμήτριος εγκυμοσύνη στη σάλπιγγα", 65, "2020-12-14"),
        V("TNGlmgOoccs", "Υστεροσκοπική αφαίρεση πολύποδα", 182, "2020-12-14"),
        V("bLT0sjTVHy4", "Λύση συμφύσεων", 236, "2020-12-14"),
        V("OM1c7x3ZwdM", "Λαπαροσκοπική ολική υστερεκτομή", 184, "2018-11-14"),
        V("r0bjdoeFty4", "Κύστη ενδομητρίωσης ωοθήκης", 178, "2018-10-16"),
        V("9HSIG18nmf4", "Λαπαροσκοπική αφαίρεση δερμοειδούς κύστης", 159, "2018-01-10"),
        V("UlkqdHo8DFI", "Λαπαροσκοπική αφαίρεση ινομυωμάτων", 152, "2016-06-22"),
        V("SLJnO8Nn44E", "Λαπαροσκοπική αφαίρεση ινομυωμάτων, περιστατικό Α", 166, "2013-03-12"),
        V("GazeN9lDgS8", "Λαπαροσκοπική αφαίρεση ινομυωμάτων, περιστατικό Β", 245, "2013-03-12"),
        V("Y0Au-835oSs", "Τεχνική συρραφής ινομυωμάτων", 676, "2011-02-26"),
         ]),
    dict(slug="enimerosi", title="Συνεντεύξεις και ενημέρωση",
         lead="Τηλεοπτικές εμφανίσεις, ομιλίες σε συνέδρια και σύντομα ενημερωτικά "
              "βίντεο για παθήσεις, θεραπείες και πρόληψη.",
         warn="",
         items=[
        V("258HlPMsHnQ", "Εμμηνόπαυση, ξηρότητα κόλπου και Erbium laser: όσα δεν σου είπε κανείς", 3289, "2025-11-19"),
        V("Eg1q9phhklk", "Ενδομητρίωση: τι είναι, πού εντοπίζεται και πώς θεραπεύεται", 159, "2021-04-03"),
        V("WrXrhO9063c", "Κωνσταντίνος Μυρίλλας, μαιευτήρας χειρουργός γυναικολόγος", 149, "2021-04-01"),
        V("NjDBP5ciyq8", "HPV: τι είναι, τι προβλήματα δημιουργεί και πώς αντιμετωπίζεται", 282, "2021-04-01"),
        V("AsA3RQ8XmsA", "Τι είναι η υστεροσκόπηση και πότε χρησιμοποιείται", 113, "2021-04-01"),
        V("EiRfs1SgpSE", "Ποια είναι η δράση του PRP στην εμμηνόπαυση", 86, "2021-04-01"),
        V("Zupbo3Ume_Y", "Τι είναι τα ινομυώματα και πώς αντιμετωπίζονται", 172, "2021-04-01"),
        V("DqMU1oGjiYI", "Σε ένα λεπτό: αναζωογόνηση κόλπου με laser στο ιατρείο", 99, "2018-12-13"),
        V("44M7wSk0Tec", "Σε ένα λεπτό: πόνος στην επαφή και ενέσιμο υαλουρονικό οξύ", 98, "2018-12-11"),
        V("IgQ9-sOmHEQ", "Σε ένα λεπτό: αναδόμηση κόλπου με ενέσιμη θεραπεία PRP", 86, "2018-12-11"),
        V("gJenGRkZhf4", "Στην εκπομπή της Ελένης Μενεγάκη", 100, "2018-11-06"),
        V("nFouvGCASEA", "«Το Πρωινό»: συνέντευξη Κωνσταντίνου Μυρίλλα", 816, "2018-02-27"),
        V("DG7sv_O_szQ", "«Εδώ»: ο Κωνσταντίνος Μυρίλλας για τον ιό HPV", 403, "2018-01-08"),
        V("a-H8o1hcU2I", "Ομιλία στο Derma Beauty Lounge 2017", 1380, "2017-06-23"),
        V("DXTZMDa9ktY", "Λειτουργικά και αισθητικά προβλήματα κόλπου στην εμμηνόπαυση", 94, "2017-05-04"),
        V("aiWCtJKY7-k", "Erbium laser για τη θεραπεία ακράτειας ούρων", 48, "2017-05-04"),
        V("CWBUzBTY9Ds", "Erbium laser για σύσφιξη κόλπου", 37, "2017-05-04"),
        V("xHTLQfCdqm0", "«Επιτέλους Σαββατοκύριακο»: ο Κωνσταντίνος Μυρίλλας", 520, "2017-03-21"),
        V("msSCFVDZcxc", "Προβλήματα γονιμότητας", 265, "2017-01-31"),
        V("d6sCNMdVAJo", "Γυναικολογικές θεραπείες με τη χρήση laser", 532, "2017-01-18"),
        V("8tdaRja_DTc", "Forever Skin Laser, σύντομη παρουσίαση", 77, "2016-12-01"),
        V("6q84Aew3qzc", "Διόρθωση χαλάρωσης κόλπου και αρχόμενων κηλών", 210, "2016-12-01"),
        V("Z6CR-BathFM", "Υπάρχει υποειδικότητα χειρουργικής για τον κόλπο;", 69, "2016-12-01"),
        V("TogV_N-yK6k", "Χρειάζονται μη επεμβατικές τεχνικές επιδιόρθωσης του κόλπου;", 80, "2016-12-01"),
        V("7SD3zuPclxU", "Το μέλλον του ατραυματικού laser στην Ελλάδα", 203, "2016-12-01"),
        V("QJb-8_KTkTQ", "Τι περιλαμβάνει η πλαστική κόλπου και τι σημαίνουν LVR και TVR", 107, "2016-12-01"),
        V("oqNHCo-P8x0", "Πρακτικές πληροφορίες για τις συνεδρίες laser", 100, "2016-12-01"),
        V("ohQqUD25Ey8", "Ποια είναι η φυσιολογική λειτουργία του κόλπου;", 52, "2016-12-01"),
        V("LXxzwIUyJxE", "Διόρθωση ξηρότητας και ατροφίας κόλπου με laser", 311, "2016-12-01"),
        V("GNLicz9-bKI", "Σε τι διαφέρει το laser erbium από τους άλλους τύπους laser", 89, "2016-12-01"),
        V("3o-3ZxK0Lu0", "Διόρθωση ακράτειας ούρων με laser", 212, "2016-12-01"),
        V("pgWN-S56Djo", "Ποιες βλάβες διορθώνει το ατραυματικό laser", 80, "2016-12-01"),
        V("Bg40rl4uLJs", "Θεραπείες κόλπου στην εμμηνόπαυση", 866, "2016-11-22"),
        V("d3Vn4NYxx8Q", "Πλαστική κόλπου, αναλυτική παρουσίαση", 974, "2016-11-22"),
        V("-SC1i2CREU4", "Ακράτεια ούρων, αναλυτική παρουσίαση", 976, "2016-11-22"),
        V("TtoXVyIoD5U", "Forever Skin Laser", 235, "2016-06-10"),
        V("q5PxY4sgaWk", "Πλαστική κόλπου, ομιλία", 1110, "2016-04-21"),
        V("H2ZTHGWiWWo", "Συμβουλές υγιεινής της ευαίσθητης περιοχής", 135, "2015-11-07"),
        V("z2IStToynCM", "Συμβουλές για σωστή υγιεινή", 556, "2014-06-13"),
        V("yO010TX9JKk", "Πού οφείλονται οι κολπικές λοιμώξεις;", 558, "2014-06-03"),
        V("1xj1ngz2kAk", "Φυσική ισορροπία της ευαίσθητης περιοχής", 541, "2014-06-03"),
        V("IN7QScg2asQ", "Σωστή ατομική υγιεινή", 471, "2014-06-03"),
        V("JAjdyYS8WNc", "Στην εκπομπή «Το Πρωινό» του ΑΝΤ1", 480, "2014-05-08"),
        V("V5m06f__-fQ", "Συνέντευξη στο Mega Channel", 481, "2014-05-08"),
        V("laGmpqXs_U0", "Τι είναι το G shot", 422, "2012-11-14"),
        V("fHYs0WhivBk", "Τεχνικές πλαστικής κόλπου", 562, "2012-11-14"),
        V("AxqM0BT6XIE", "Τι είναι τα ινομυώματα", 311, "2012-11-14"),
        V("iGFBuU3COOY", "Μαιευτήριο ΡΕΑ", 666, "2011-05-14"),
        V("qGRrNZOA2Ek", "Ρομποτική χειρουργική", 619, "2011-05-14"),
        V("XCrgU4_S950", "Ρομποτική γυναικολογία, τηλεπαρουσίαση", 845, "2011-05-13"),
        V("1jduxMcgNcs", "Παθολογία μήτρας και ινομυώματα", 851, "2011-02-26"),
        V("hebumP1RasI", "Ρομποτική και γυναικολογία", 558, "2010-11-18"),
        V("cAh-5sH2lV0", "Ρομποτική χειρουργική στη γυναικολογία", 412, "2010-10-24"),
        V("EPHbT_-9GkI", "Ρομποτική χειρουργική στη γυναικολογία, μέρος Β", 536, "2010-10-21"),
        V("RGLafhTXWwo", "Ρομποτική γυναικολογία", 526, "2010-10-21"),
         ]),
]

VIDEO_LIBRARY = [dict(v, group=g["slug"]) for g in VIDEO_GROUPS for v in g["items"]]

# Βίντεο ανά θεραπεία: μόνο όσα μιλούν για τη συγκεκριμένη θεραπεία, με τη σειρά
# που εμφανίζονται στη σελίδα της. Θεραπεία χωρίς σχετικό βίντεο δεν έχει σειρά.
TREATMENT_VIDEOS = {
    "anazoogonisi-kolpou": ["258HlPMsHnQ", "DqMU1oGjiYI", "LXxzwIUyJxE", "CWBUzBTY9Ds",
                            "aiWCtJKY7-k", "3o-3ZxK0Lu0", "6q84Aew3qzc", "pgWN-S56Djo",
                            "oqNHCo-P8x0", "GNLicz9-bKI", "TogV_N-yK6k", "Bg40rl4uLJs"],
    "g-shot": ["laGmpqXs_U0"],
    "laser-plastiki-kolpou": ["QJb-8_KTkTQ", "d3Vn4NYxx8Q", "fHYs0WhivBk", "q5PxY4sgaWk",
                              "Z6CR-BathFM"],
    "xeirourgiki-pyelikou-edafous": ["QJb-8_KTkTQ", "fHYs0WhivBk", "Z6CR-BathFM"],
}

# Ό,τι δείχνει η σειρά βίντεο της αρχικής: τα θεματικά κοντινότερα στο ιατρείο.
HOME_VIDEOS = ["258HlPMsHnQ", "DqMU1oGjiYI", "44M7wSk0Tec", "IgQ9-sOmHEQ", "3o-3ZxK0Lu0", "LXxzwIUyJxE",
               "6q84Aew3qzc", "QJb-8_KTkTQ", "pgWN-S56Djo", "CWBUzBTY9Ds", "aiWCtJKY7-k",
               "laGmpqXs_U0", "nFouvGCASEA", "xHTLQfCdqm0", "Bg40rl4uLJs"]

# Κρατιέται για το version 1, που περιμένει σκέτη λίστα με κωδικούς YouTube.
VIDEOS = [v["id"] for v in VIDEO_LIBRARY]

# ── English pages ────────────────────────────────────────────────────────────
EN_PAGES = [
    ("the-clinic", "en/the-clinic", "The Clinic"),
    ("urinary-incontinence", "en/urinary-incontinence", "Urinary Incontinence"),
    ("vaginal-atrophy", "en/vaginal-atrophy", "Vaginal Atrophy"),
    ("vaginal-dryness", "en/vaginal-dryness", "Vaginal Dryness"),
    ("vaginal-tightening-laser", "en/vaginal-tightening-laser", "Vaginal Tightening Laser"),
    ("designer-laser-vaginoplasty", "en/designer-laser-vaginoplasty", "Designer Laser Vaginoplasty"),
]
