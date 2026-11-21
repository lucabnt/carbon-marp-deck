#!/usr/bin/env python3
"""Find Carbon pictograms and copy the ones a deck uses into the deck folder.

    python scripts/pictograms.py search cloud security     # find names
    python scripts/pictograms.py search --category Security
    python scripts/pictograms.py categories
    python scripts/pictograms.py sync my-deck/my-deck.md    # copy used SVGs

Pictograms come from the open-source @carbon/pictograms package (Apache-2.0),
stored in assets/pictograms/svg/ and listed in assets/pictograms/catalog.csv.
The claude.ai upload build packs the SVGs into one file, assets/pictograms/svg.json
({file name: SVG text}), because claude.ai accepts at most 200 files per skill and no
nested archives; this script reads either form.
A deck refers to them as `assets/pictograms/svg/<name>.svg`; `sync` copies the
referenced files next to the deck so the deck folder stays self-contained.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import shutil
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "assets" / "pictograms"
SVG_DIR = LIB / "svg"
SVG_PACK = LIB / "svg.json"
# Only deck-local references; "../assets/..." (examples) points at the library itself.
REF = re.compile(r"""(?<![./\w])assets/pictograms/svg/([A-Za-z0-9_.\-]+\.svg)""")


def load_catalog() -> list[dict]:
    with (LIB / "catalog.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def search(terms: list[str], category: str | None, limit: int) -> list[dict]:
    rows = load_catalog()
    if category:
        rows = [r for r in rows if category.lower() in r["categories"].lower()]
    if not terms:
        return rows[:limit]
    scored = []
    for r in rows:
        name, friendly = r["name"].lower(), r["friendly_name"].lower()
        aliases = r["aliases"].lower()
        score = 0
        for t in (x.lower() for x in terms):
            if t == name:
                score += 10
            elif t in name or t in friendly:
                score += 5
            elif t in aliases:
                score += 2
            else:
                score -= 100
        if score > 0:
            scored.append((-score, len(name), r))
    return [r for _, _, r in sorted(scored, key=lambda x: x[:2])][:limit]


def _pack() -> dict[str, str]:
    if not SVG_PACK.is_file():
        return {}
    return json.loads(SVG_PACK.read_text(encoding="utf-8"))


def svg_names() -> set[str]:
    """File names of the available pictograms, from svg/ or the packed svg.json."""
    if SVG_DIR.is_dir():
        return {p.name for p in SVG_DIR.glob("*.svg")}
    return set(_pack())


def copy_svg(fname: str, dest: Path) -> bool:
    """Copy one pictogram to dest; False if it does not exist."""
    src = SVG_DIR / fname
    if src.is_file():
        shutil.copy2(src, dest)
        return True
    text = _pack().get(fname)
    if text is None:
        return False
    dest.write_text(text, encoding="utf-8", newline="")
    return True


def referenced(deck: Path) -> list[str]:
    return sorted(set(REF.findall(deck.read_text(encoding="utf-8-sig"))))


def sync(deck: Path) -> list[str]:
    """Copy referenced SVGs into <deck dir>/assets/pictograms/svg/. Return unknown names."""
    dest = deck.parent / "assets" / "pictograms" / "svg"
    if dest.resolve() == SVG_DIR.resolve():
        return []
    available = svg_names()
    unknown = []
    for fname in referenced(deck):
        if fname not in available:
            unknown.append(fname)
            continue
        dest.mkdir(parents=True, exist_ok=True)
        if not (dest / fname).exists():
            copy_svg(fname, dest / fname)
    return unknown


def suggest(fname: str) -> list[str]:
    names = [Path(n).stem for n in svg_names()]
    return difflib.get_close_matches(Path(fname).stem, names, n=3, cutoff=0.5)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="find pictograms by name, label or alias")
    s.add_argument("terms", nargs="*")
    s.add_argument("--category")
    s.add_argument("--limit", type=int, default=20)
    sub.add_parser("categories", help="list categories")
    y = sub.add_parser("sync", help="copy the pictograms a deck uses next to the deck")
    y.add_argument("deck", type=Path)
    args = ap.parse_args()

    if args.cmd == "search":
        for r in search(args.terms, args.category, args.limit):
            print(f"{r['name']:<40} {r['friendly_name']}  [{r['categories']}]")
        return 0
    if args.cmd == "categories":
        cats: dict[str, int] = {}
        for r in load_catalog():
            for c in filter(None, (x.strip() for x in r["categories"].split(";"))):
                cats[c] = cats.get(c, 0) + 1
        for c, n in sorted(cats.items()):
            print(f"{c:<28} {n}")
        return 0

    unknown = sync(args.deck)
    for fname in unknown:
        close = ", ".join(suggest(fname)) or "none"
        print(f"error: unknown pictogram '{fname}' (closest: {close})", file=sys.stderr)
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(main())
