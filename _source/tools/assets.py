# -*- coding: utf-8 -*-
"""Copies the usable media out of the legacy mirror under ASCII filenames
and writes a manifest the build script reads."""
import os, json, shutil, glob, re

SRC = "lvriathens.com/wp-content/uploads"
DST = "lvri-new/site/assets/img"
MAP = "lvri-new/content/assets.json"

# legacy path -> new filename. Only media the new site actually uses.
RENAME = {
    "2023/02/Η-Κλινική-1-1.jpg":                "clinic-team.jpg",
    "2023/02/Dr-Myrilas.jpg":                   "dr-myrillas.jpg",
    "2020/11/mat.jpg":                          "dr-matlock.jpg",
    "2020/11/logo-resize-removebg-preview.png": "logo.png",
    "2020/11/favicon-144x144-1.png":            "favicon-144.png",
}


def main():
    os.makedirs(DST, exist_ok=True)
    manifest, missing = {}, []
    for legacy, name in RENAME.items():
        src = os.path.join(SRC, legacy)
        if not os.path.exists(src):
            missing.append(legacy)
            continue
        shutil.copy2(src, os.path.join(DST, name))
        manifest[legacy] = name

    # The before/after strip from the legacy photo gallery.
    ba = sorted(glob.glob(f"{SRC}/2020/11/vagina*la.jpg"),
                key=lambda p: int(re.search(r"vagina(\d+)la", p).group(1)))
    for i, p in enumerate(ba, 1):
        name = f"result-{i:02d}.jpg"
        shutil.copy2(p, os.path.join(DST, name))
        manifest[p.split("/uploads/")[-1]] = name

    os.makedirs("lvri-new/site/assets/docs", exist_ok=True)
    if os.path.exists(f"{SRC}/2022/04/lvr.pdf"):
        shutil.copy2(f"{SRC}/2022/04/lvr.pdf", "lvri-new/site/assets/docs/lvri-athens.pdf")

    json.dump(manifest, open(MAP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"copied {len(manifest)} files -> {DST}")
    if missing:
        print("MISSING:", *missing, sep="\n  ")


main()
