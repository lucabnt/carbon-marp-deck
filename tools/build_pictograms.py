#!/usr/bin/env python3
"""Rebuild assets/pictograms/ from the open-source @carbon/pictograms package.

Maintainer tool - deck authors do not need to run it.

    python tools/build_pictograms.py              # download pinned version, rebuild
    python tools/build_pictograms.py --package DIR  # use an already extracted package

Outputs (all under assets/pictograms/):
  svg/<name>.svg         Carbon pictogram, left-trimmed (see below); names listed in
                         tools/pictogram_exclude.txt are skipped (names or globs)
  catalog.csv            name, friendly_name, categories, aliases
  LICENSE-CARBON         Apache-2.0 licence text of @carbon/pictograms

Left trim: every Carbon pictogram lives in a 32x32 viewBox with a variable amount
of empty space on the left. The glyph is wrapped in a <g> translated left by that
amount so that `object-position: left center` aligns all of them on one edge.
The amount is stored in `data-left-trim` (informational only).

Requires: PyYAML, PyMuPDF, npm (only when --package is not given).
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import yaml

CARBON_VERSION = "12.88.0"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "pictograms"
EXCLUDE_FILE = Path(__file__).with_name("pictogram_exclude.txt")
SCALE = 8  # raster scale used to measure the glyph bounding box
# Aliases that name trademarked programmes or products; dropped from catalog.csv.
ALIAS_DROP = {"EDT", "enterprise design thinking team", "z17", "LinuxONE", "Z"}


def _pymupdf():
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    return pymupdf


def fetch_package(dest: Path) -> Path:
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        sys.exit("error: npm not found; pass --package DIR with an extracted @carbon/pictograms")
    subprocess.run([npm, "pack", f"@carbon/pictograms@{CARBON_VERSION}", "--silent"],
                   cwd=dest, check=True, capture_output=True)
    tgz = next(dest.glob("carbon-pictograms-*.tgz"))
    with tarfile.open(tgz) as tf:
        tf.extractall(dest)
    return dest / "package"


def left_trim(pymupdf, svg_text: str) -> float:
    """Empty space (in viewBox units) between the left edge and the first inked pixel."""
    page = pymupdf.open(stream=svg_text.encode(), filetype="svg")[0]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), alpha=True)
    w, h, n = pix.width, pix.height, pix.n
    data = pix.samples
    for x in range(w):
        for y in range(h):
            if data[(y * w + x) * n + n - 1] > 16:
                return round(x / w * 32, 2)
    return 0.0


def wrap(svg_text: str, trim: float) -> str:
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg_text, re.S).group(1).strip()
    t = f"{trim:g}"
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            f'<g data-left-trim="{t}" transform="translate(-{t} 0)">{inner}</g></svg>\n')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--package", help="path to an extracted @carbon/pictograms package")
    args = ap.parse_args()
    pymupdf = _pymupdf()

    tmp = Path(tempfile.mkdtemp(prefix="carbon-pictograms-"))
    try:
        pkg = Path(args.package) if args.package else fetch_package(tmp)
        load = lambda f: yaml.safe_load((pkg / f).read_text(encoding="utf-8"))
        meta = {p["name"]: p for p in load("pictograms.yml")}
        deprecated = {d["name"] for d in load("deprecated.yml")["deprecated"]}
        patterns = [ln.strip() for ln in EXCLUDE_FILE.read_text(encoding="utf-8").splitlines()
                    if ln.strip() and not ln.startswith("#")]
        excluded = lambda n: any(fnmatch.fnmatchcase(n, p) for p in patterns)
        cats: dict[str, list[str]] = {}
        for c in load("categories.yml")["categories"]:
            for m in c.get("members") or []:
                cats.setdefault(m, []).append(c["name"])

        if OUT.joinpath("svg").exists():
            shutil.rmtree(OUT / "svg")
        (OUT / "svg").mkdir(parents=True)

        rows = []
        for src in sorted((pkg / "svg").glob("*.svg")):
            name = src.stem
            if name in deprecated or excluded(name):
                continue
            text = src.read_text(encoding="utf-8")
            (OUT / "svg" / f"{name}.svg").write_text(wrap(text, left_trim(pymupdf, text)),
                                                       encoding="utf-8", newline="\n")
            m = meta.get(name, {})
            rows.append([name, m.get("friendly_name", name.replace("-", " ")),
                         "; ".join(cats.get(name, [])), "; ".join(a for a in (m.get("aliases") or []) if a not in ALIAS_DROP)])

        with (OUT / "catalog.csv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["name", "friendly_name", "categories", "aliases"])
            w.writerows(rows)
        shutil.copyfile(pkg / "LICENSE", OUT / "LICENSE-CARBON")
        print(f"{len(rows)} pictograms from @carbon/pictograms {CARBON_VERSION} -> {OUT}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
