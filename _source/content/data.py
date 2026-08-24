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
    "hours": [("Δευτέρα – Παρασκευή", "09:00 – 17:00"),
              ("Σάββατο", "09:00 – 15:00"),
              ("Κυριακή", "Κλειστά")],
    "hours_en": [("Monday – Friday", "09:00 – 17:00"),
                 ("Saturday", "09:00 – 15:00"),
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
    # Όμορες περιοχές που εξυπηρετούνται καθημερινά — δηλώνονται ως areaServed,
    # δεν φτιάχνουμε ξεχωριστή σελίδα για την καθεμία (doorway pages).
    "areas": ["Βύρωνας", "Καισαριανή", "Παγκράτι", "Ζωγράφου", "Υμηττός",
              "Ηλιούπολη", "Δάφνη", "Άγιος Αρτέμιος", "Νέος Κόσμος",
              "Κέντρο Αθήνας", "Αργυρούπολη", "Γλυφάδα"],
    "credit": {"name": "ClinicBrain", "url": "https://clinicbrain.gr"},
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
         meta="Ακράτεια ούρων στις γυναίκες: οι τέσσερις τύποι, τα αίτια, ο ουροδυναμικός έλεγχος και οι θεραπείες — από ασκήσεις Kegel μέχρι laser και χειρουργείο.",
         lead="Αφορά περίπου το 20% των γυναικών στην Ελλάδα. Είναι σύμπτωμα, όχι ασθένεια — και στις περισσότερες περιπτώσεις αντιμετωπίζεται ριζικά.",
         plain="Χάνω ούρα χωρίς να το θέλω.",
         stat=("20%", "των γυναικών στην Ελλάδα"),
         treatments=["anazoogonisi-kolpou", "laser-plastiki-kolpou"]),

    dict(slug="proptosi-mitras", legacy="proptosi-mitras", organ="uterus",
         title="Πρόπτωση μήτρας & κόλπου",
         meta="Πρόπτωση μήτρας και κόλπου: πώς αναγνωρίζεται, τα στάδια κατά POP-Q και οι θεραπείες που αποκαθιστούν την ανατομία του πυελικού εδάφους.",
         lead="Όταν το μυϊκό σύστημα που στηρίζει την πύελο χαλαρώσει, τα όργανα κατεβαίνουν. Ταξινομείται σε στάδια κατά POP-Q.",
         plain="Νιώθω βάρος ή κάτι να προβάλλει.",
         stat=("4", "στάδια κατά POP-Q"),
         treatments=["xeirourgiki-pyelikou-edafous", "laser-plastiki-kolpou"]),

    dict(slug="ksirotita-kolpou", legacy="kolpiki-ksirotita", organ="vagina",
         title="Ξηρότητα κόλπου",
         meta="Ξηρότητα κόλπου: γιατί συμβαίνει, με ή χωρίς εμμηνόπαυση, και πώς την αντιμετωπίζουν το laser και οι ενέσιμες θεραπείες με υαλουρονικό.",
         lead="Δεν αφορά μόνο την εμμηνόπαυση. Ο κόλπος χάνει ελαστικότητα και κολλαγόνο, το pH αλκαλοποιείται και η χλωρίδα αλλάζει.",
         plain="Νιώθω ξηρότητα, κάψιμο ή πόνο στην επαφή.",
         stat=("pH 6–7", "αλκαλοποίηση του κόλπου"),
         treatments=["anazoogonisi-kolpou"]),

    dict(slug="kysteokili", legacy="kysteokhlh", organ="bladder",
         title="Κυστεοκήλη",
         meta="Κυστεοκήλη: όταν η ουροδόχος κύστη προβάλλει στο πρόσθιο τοίχωμα του κόλπου. Συμπτώματα, βαθμοί βαρύτητας και θεραπευτικές επιλογές.",
         lead="Η ουροδόχος κύστη προβάλλει προς το πρόσθιο τοίχωμα του κόλπου, συχνά μαζί με δυσκολία στην πλήρη κένωση.",
         plain="Δυσκολεύομαι να αδειάσω την κύστη μου.",
         stat=("Πρόσθιο", "τοίχωμα κόλπου"),
         treatments=["xeirourgiki-pyelikou-edafous", "laser-plastiki-kolpou"]),

    dict(slug="orthokili-enterokili", legacy="orthokili-enterokili", organ="rectum",
         title="Ορθοκήλη & εντεροκήλη",
         meta="Ορθοκήλη και εντεροκήλη: συμπτώματα, διαφορές και θεραπεία — από μη επεμβατικό laser στις αρχόμενες μορφές μέχρι πλήρη ανάπλαση κόλπου.",
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
         short="Renovalaser / IntimaLase",
         meta="Αναζωογόνηση κόλπου με laser: 2–3 ανώδυνες συνεδρίες των 15 λεπτών στο ιατρείο, χωρίς χρόνο ανάρρωσης, για ξηρότητα, ατροφία και ήπια χαλάρωση.",
         lead="Μη επεμβατικό laser στο ιατρείο. Αποκαθιστά την ελαστικότητα και την κολλαγόνωση του κόλπου.",
         invasive="non",
         matrix=dict(setting="Ιατρείο", anesthesia="Δεν απαιτείται",
                     sessions="2–3 συνεδρίες", duration="15 λεπτά ανά συνεδρία",
                     recovery="Χωρίς ανάρρωση", pain="Ανώδυνο"),
         treats=["Ξηρότητα & ατροφία", "Ήπια χαλάρωση", "Ήπια ακράτεια", "Αρχόμενη ορθοκήλη"]),

    dict(slug="g-shot", legacy="g-shot",
         title="G-Shot®",
         short="Ενίσχυση σημείου G",
         meta="G-Shot®: ένεση υαλουρονικού υψηλού μοριακού βάρους στο σημείο G με τοπική αναισθησία. Επίσκεψη κάτω από 30 λεπτά, χωρίς χρόνο ανάρρωσης.",
         lead="Ένεση υαλουρονικού υψηλού μοριακού βάρους στο σημείο G, με τη βοήθεια ειδικού κολποσκοπίου.",
         invasive="minor",
         matrix=dict(setting="Ιατρείο", anesthesia="Τοπική",
                     sessions="1 συνεδρία", duration="Επίσκεψη κάτω από 30 λεπτά",
                     recovery="Χωρίς ανάρρωση", pain="Ανώδυνο"),
         treats=["Σεξουαλική διέγερση", "Ένταση οργασμού"]),

    dict(slug="aidoioplastiki", legacy="plastiki-aidoiou",
         title="Αιδοιοπλαστική",
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
         short="Laser Vaginal Rejuvenation®",
         meta="Laser πλαστική κόλπου (LVR®): χειρουργική σύσφιξη με CO₂ laser σε χειρουργείο ημέρας, χωρίς αφαίρεση ραμμάτων και με άμεση επιστροφή στα δικά σας.",
         lead="Χειρουργική σύσφιξη με CO₂ laser. Χειρουργείο ημέρας, χωρίς αφαίρεση ραμμάτων.",
         invasive="surgical",
         matrix=dict(setting="Χειρουργείο ημέρας", anesthesia="Εξατομικευμένη",
                     sessions="1 επέμβαση", duration="Εξιτήριο ίδια ή επόμενη ημέρα",
                     recovery="Επιστροφή σχεδόν άμεσα · αποχή επαφής 5–6 εβδομάδες",
                     pain="Χωρίς αφαίρεση ραμμάτων"),
         treats=["Χαλάρωση κόλπου", "Μειωμένη αίσθηση", "Ήπια πρόπτωση"]),

    dict(slug="xeirourgiki-pyelikou-edafous", legacy="xeirourgiki-pyelikou-edafous",
         title="Χειρουργική πυελικού εδάφους",
         short="Total Vaginal Reconstruction",
         meta="Χειρουργική πυελικού εδάφους: πλήρης ανάπλαση κόλπου με επεμβατικό CO₂ laser για βαρύτερη κυστεοκήλη, ορθοκήλη και πρόπτωση μήτρας.",
         lead="Πλήρης ανάπλαση του κόλπου με επεμβατικό CO₂ laser για βαρύτερες ή παραμελημένες κήλες.",
         invasive="surgical",
         matrix=dict(setting="Χειρουργείο", anesthesia="Εξατομικευμένη",
                     sessions="1 επέμβαση", duration="Εξατομικευμένη",
                     recovery="Κατά περίπτωση", pain="Υπό αναισθησία"),
         treats=["Κυστεοκήλη", "Ορθοκήλη & εντεροκήλη", "Πρόπτωση μήτρας"]),
]

# ── Symptom guide ─────────────────────────────────────────────────────────────
# Plain-language statements, weighted towards the conditions above. This is
# orientation, not diagnosis — the result screen says so explicitly.
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
         options=[("low", "Ελάχιστα — απλώς με προβληματίζει", {}),
                  ("mid", "Αρκετά — αποφεύγω κάποια πράγματα", {}),
                  ("high", "Πολύ — αλλάζω τον τρόπο που ζω", {})]),
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

VIDEOS = ["-SC1i2CREU4", "1xj1ngz2kAk", "3o-3ZxK0Lu0", "6q84Aew3qzc", "7SD3zuPclxU",
          "Bg40rl4uLJs", "CWBUzBTY9Ds", "DXTZMDa9ktY", "GNLicz9-bKI", "H2ZTHGWiWWo",
          "IN7QScg2asQ", "JAjdyYS8WNc", "LXxzwIUyJxE", "QJb-8_KTkTQ", "TogV_N-yK6k",
          "V5m06f__-fQ", "Z6CR-BathFM", "a-H8o1hcU2I", "aiWCtJKY7-k", "d3Vn4NYxx8Q",
          "d6sCNMdVAJo", "fHYs0WhivBk", "laGmpqXs_U0", "nFouvGCASEA", "ohQqUD25Ey8",
          "oqNHCo-P8x0", "pgWN-S56Djo", "q5PxY4sgaWk", "xHTLQfCdqm0", "yO010TX9JKk",
          "z2IStToynCM"]

# ── English pages ────────────────────────────────────────────────────────────
EN_PAGES = [
    ("the-clinic", "en/the-clinic", "The Clinic"),
    ("urinary-incontinence", "en/urinary-incontinence", "Urinary Incontinence"),
    ("vaginal-atrophy", "en/vaginal-atrophy", "Vaginal Atrophy"),
    ("vaginal-dryness", "en/vaginal-dryness", "Vaginal Dryness"),
    ("vaginal-tightening-laser", "en/vaginal-tightening-laser", "Vaginal Tightening Laser"),
    ("designer-laser-vaginoplasty", "en/designer-laser-vaginoplasty", "Designer Laser Vaginoplasty"),
]
