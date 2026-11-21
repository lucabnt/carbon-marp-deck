#!/usr/bin/env python3
"""Regenerate the rendered examples: examples/pdf/*.pdf and examples/pptx/*.pptx.

    python tools/build_examples.py              # PDF and PPTX for every example
    python tools/build_examples.py --pdf-only
    python tools/build_examples.py 03-cards     # only the decks whose name contains "03-cards"

Run it after changing themes/carbon.css (and running scripts/sync_css.py) or an example.
The decks are built in parallel.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_css  # noqa: E402
import toolchain  # noqa: E402

EXAMPLES = toolchain.ROOT / "examples"
CONVERTER = toolchain.ROOT / "pptx-export" / "dom" / "dom_to_pptx.py"


def build(md: Path, pdf: bool, pptx: bool) -> list[tuple[str, str]]:
    """[(status line, problem or "")] for one deck."""
    out = []
    if pdf:
        target = EXAMPLES / "pdf" / f"{md.stem}.pdf"
        r = toolchain.run_marp([str(md), "--pdf", "--output", str(target)], quiet=True)
        out.append((f"{'ok  ' if r.returncode == 0 else 'FAIL'} {target.relative_to(toolchain.ROOT)}",
                    "" if r.returncode == 0 else f"{md.name} (PDF): {r.stderr.strip()[-300:]}"))
    if pptx:
        target = EXAMPLES / "pptx" / f"{md.stem}.pptx"
        r = subprocess.run([sys.executable, str(CONVERTER), str(md), "--output", str(target)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        warnings = [ln for ln in r.stderr.splitlines() if ln.startswith("warning:")]
        ok = r.returncode == 0 and not warnings
        out.append((f"{'ok  ' if ok else 'FAIL'} {target.relative_to(toolchain.ROOT)}"
                    + (f" ({len(warnings)} warning(s))" if warnings else ""),
                    "" if ok else f"{md.name} (PPTX): " + "; ".join(warnings or [r.stderr.strip()[-300:]])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("filter", nargs="?", default="", help="part of the deck name")
    only = ap.add_mutually_exclusive_group()
    only.add_argument("--pdf-only", action="store_true")
    only.add_argument("--pptx-only", action="store_true")
    args = ap.parse_args()

    decks = [md for md in sorted(EXAMPLES.glob("*.md")) if args.filter in md.stem]
    if not decks:
        print(f"no example matches '{args.filter}'", file=sys.stderr)
        return 1
    if not args.pdf_only and not toolchain.has_python_pptx():
        sys.exit("error: python-pptx missing - pip install -r pptx-export/requirements.txt")
    toolchain.require_marp()
    sync_css.copy_fonts(EXAMPLES)
    (EXAMPLES / "pdf").mkdir(exist_ok=True)
    (EXAMPLES / "pptx").mkdir(exist_ok=True)

    workers = max(1, min(len(decks), (os.cpu_count() or 2) // 2, 4))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda md: build(md, not args.pptx_only, not args.pdf_only), decks))
    problems = []
    for deck in results:
        for line, problem in deck:
            print(line)
            if problem:
                problems.append(problem)
    for p in problems:
        print("  -", p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
