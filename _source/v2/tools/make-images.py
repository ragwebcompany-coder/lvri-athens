#!/usr/bin/env python3
"""Crops the clinic's own published photographs to the 4:3 the cards use and
writes a .jpg + .webp pair into site/assets/img/.

Sources are the images already live on lvriathens.com, mirrored under
../lvriathens.com/wp-content/uploads/. Run from the repository root:

    python3 version-2/tools/make-images.py && python3 version-2/build.py

To swap a photograph: point its entry in M at the new file, re-run, rebuild.
Add the stem to GRAVITY when the subject is not centred.
"""
import os
from PIL import Image
SRC="lvriathens.com/wp-content/uploads/"
# Canonical asset source. build.py copies this into version-2/site/ on a
# clean build, so generated images must live here, not only in the output.
OUT="lvri-new/site/assets/img/"

# dest stem -> source file, from the clinic's own published images
M = {
 # conditions
 "cond-akrateia":            "2022/05/232.jpg",
 "cond-proptosi":            "2022/07/προπτωση-μητρας.jpg",
 "cond-ksirotita":           "2021/02/eikona-3.jpg",
 "cond-kysteokili":          "2020/12/κυστεοκήλη.jpeg",
 "cond-orthokili":           "2022/07/Ορθοκήλη-εντεροκήλη.jpg",
 # treatments
 "treat-anazoogonisi":       "2021/03/eikona2.png",
 "treat-g-shot":             "2021/02/eikona1.jpg",
 "treat-aidoioplastiki":     "2020/11/aidioplastiki.jpg",
 "treat-laser-plastiki":     "2020/11/laser-plastiki-kolpou-1.jpg",
 "treat-xeirourgiki":        "2020/11/Venus.jpg",
 # articles
 "art-ksirotita-moderni":    "2022/07/shutterstock_1067815811.jpg",
 "art-proptosi-panta":       "2022/06/προπτωση-μητρας.jpg",
 "art-aidoioplastiki":       "2022/05/αιδιο-1.jpg",
 "art-ksirotita-kathimera":  "2022/05/3333.jpg",
 "art-akrateia-diagnosi":    "2020/11/shutterstock_1048505722.jpg",
 "art-akrateia-therapeia":   "2018/10/akrateia.jpg",
 "art-akrateia-arthro":      "2018/10/ακρατεια-ουρων-768x1024-1.jpg",
 "art-akrateia-prospatheias":"2021/03/εικονα4.png",
 "art-akrateia-aitia":       "2018/10/antimetopisi-provlimaton-slider-3.jpg",
 "art-ygieini":              "2018/10/Υγιεινή-κατα-της-Κολπίτιδας-1024x474-1.jpg",
 "art-synedrio":             "2018/10/13383412_1174380722592328_1225273210_o-768x576-1.jpg",
 "art-laser-epoxi":          "2018/10/14596167828103.jpg",
 "art-myrillas-apanta":      "2018/10/Πλαστική-κόλπου-Ο-Dr-K.-Μυρίλλας-απαντά-σε-σημαντικά-ερωτήματα.jpg",
 "art-vlaves":               "2018/10/Πλαστική-κόλπου-ποιες-είναι-συνοπτικά-οι-κυριότερες-βλάβες-που-διορθώνει.jpg",
 "art-kolpiki-proptosi":     "2018/10/Κολπική-Πρόπτωση.jpg",
 "art-emminopausi":          "2018/10/Ανάπλαση-κόλπου.jpg",
 # english + hubs
 "en-atrophy":               "2020/11/shutterstock_1229202016.jpg",
 "hub-therapeies":           "2020/11/shutterstock_1115302421.jpg",
 "hub-pathiseis":            "2020/11/shutterstock_776591572.jpg",
 "hub-arthra":               "2020/11/shutterstock_1373047118.jpg",
 "hub-gallery":             "2021/03/eikona1.png",
 "hub-odigos":              "2020/11/VDiagram.jpg",
}
# Horizontal crop anchor for images whose subject is not centred.
# 0.0 keeps the left edge, 0.5 centres (default), 1.0 keeps the right edge.
GRAVITY = {
    "hub-arthra": 0.0,   # subject sits in the left third of a 2560x952 banner
    "art-vlaves": 1.0,   # the "Laser Vaginal Rejuvenation" wordmark is on the right
}
# Artwork supplied by the clinic, cropped out of a composite sheet.
# box = (left, top, right, bottom) in the source; the badge and the baked-in
# caption are cropped away because the card renders both from data.py.
SUPPLIED_ROOT = "version-2/src/img-src/"
SUPPLIED = {
    "treat-aidoioplastiki": ("treatments-3-4-5.png", (36, 169, 486, 769)),
    "treat-laser-plastiki": ("treatments-3-4-5.png", (542, 169, 992, 769)),
    "treat-xeirourgiki":    ("treatments-3-4-5.png", (1048, 169, 1498, 769)),
}

TARGET_W, TARGET_H = 1200, 900          # 4:3, matches .nf-card__img
os.makedirs(OUT, exist_ok=True)
made = []
for stem, rel in sorted(M.items()):
    if stem in SUPPLIED:
        continue
    p = SRC + rel
    if not os.path.exists(p):
        print("MISSING SOURCE", p); continue
    im = Image.open(p)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    else:
        im = im.convert("RGB")
    # cover-crop to 4:3, centred
    sw, sh = im.size
    scale = max(TARGET_W / sw, TARGET_H / sh)
    if scale > 1:                        # never upscale past source: shrink target instead
        w, h = sw, int(sw * TARGET_H / TARGET_W)
        if h > sh: h, w = sh, int(sh * TARGET_W / TARGET_H)
    else:
        w, h = TARGET_W, TARGET_H
        im = im.resize((max(1, round(sw * scale)), max(1, round(sh * scale))), Image.LANCZOS)
        sw, sh = im.size
    g = GRAVITY.get(stem, 0.5)
    left, top = int(round((sw - w) * g)), (sh - h) // 2
    im = im.crop((left, top, left + w, top + h))
    if im.size != (TARGET_W, TARGET_H) and im.size[0] > TARGET_W:
        im = im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    im.save(OUT + stem + ".jpg", "JPEG", quality=82, optimize=True, progressive=True)
    im.save(OUT + stem + ".webp", "WEBP", quality=80, method=6)
    made.append((stem, im.size, os.path.getsize(OUT+stem+".jpg"), os.path.getsize(OUT+stem+".webp")))
for stem, (fname, box) in sorted(SUPPLIED.items()):
    p = SUPPLIED_ROOT + fname
    if not os.path.exists(p):
        print("MISSING SUPPLIED", p); continue
    im = Image.open(p).convert("RGB").crop(box)
    im.save(OUT + stem + ".jpg", "JPEG", quality=88, optimize=True, progressive=True)
    im.save(OUT + stem + ".webp", "WEBP", quality=86, method=6)
    made.append((stem, im.size, os.path.getsize(OUT+stem+".jpg"), os.path.getsize(OUT+stem+".webp")))

for s, size, j, w in made:
    print(f"{s:28} {size[0]:>4}x{size[1]:<4} jpg {j//1024:>4}K  webp {w//1024:>4}K")
print(f"\n{len(made)} images written to {OUT}")
