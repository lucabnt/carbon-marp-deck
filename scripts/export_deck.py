#!/usr/bin/env python3
"""Lint a Marp deck, then export it to PDF, PNG previews and editable PPTX.

    python scripts/export_deck.py my-deck/my-deck.md --strict --preview
    python scripts/export_deck.py my-deck/my-deck.md --pdf-only
    python scripts/export_deck.py my-deck/my-deck.md --pptx-only
    python scripts/export_deck.py my-deck/my-deck.md --pptx-only --reflow

Steps: copy the Plex fonts and the pictograms the deck uses next to it, lint (errors stop the export),
then PDF, PNG previews and PPTX, run in parallel.

--strict       every warning (lint or PPTX export) makes the command fail
--preview      one PNG per slide in <deck>-preview/, to look at before finishing
--pdf-notes    speaker notes as PDF annotations (the PPTX always has them)
--reflow       PPTX text re-wraps in PowerPoint (easier to edit); by default every
               line ends where it ends in the PDF

Requires Node.js 18+, Chrome or Edge, and `pip install -r pptx-export/requirements.txt`.
Run `python scripts/check_env.py` to check them.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_deck  # noqa: E402
import pictograms  # noqa: E402
import sync_css  # noqa: E402
import toolchain  # noqa: E402

CONVERTER = toolchain.ROOT / "pptx-export" / "dom" / "dom_to_pptx.py"


# Each export step returns (ok, report lines, warnings). The steps are independent, so
# export_deck runs them at the same time and prints the reports in a fixed order.
Step = "tuple[bool, list[str], list[str]]"


def _failure(proc: subprocess.CompletedProcess) -> list[str]:
    return [f"      {ln}" for ln in (proc.stderr or proc.stdout or "").strip().splitlines()[-8:]]


def export_pdf(md: Path, outdir: Path, notes: bool) -> Step:
    target = outdir / f"{md.stem}.pdf"
    args = [str(md), "--pdf", "--output", str(target)] + (["--pdf-notes"] if notes else [])
    proc = toolchain.run_marp(args, quiet=True)
    ok = proc.returncode == 0
    return ok, [f"PDF  -> {target}"] + ([] if ok else _failure(proc)), []


def export_preview(md: Path, outdir: Path) -> Step:
    folder = outdir / f"{md.stem}-preview"
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob(f"{md.stem}.*.png"):
        old.unlink()
    proc = toolchain.run_marp([str(md), "--images", "png",
                               "--output", str(folder / f"{md.stem}.png")], quiet=True)
    ok = proc.returncode == 0
    shots = sorted(folder.glob(f"{md.stem}.*.png"))
    lines = [f"PNG  -> {folder}"]
    if ok and shots:
        lines.append(f"      {len(shots)} slide image(s): {shots[0].name} ... {shots[-1].name}")
    return ok, lines + ([] if ok else _failure(proc)), []


def export_pptx(md: Path, outdir: Path, reflow: bool) -> Step:
    if not toolchain.has_python_pptx():
        return False, ["PPTX -> error: python-pptx missing - run: "
                       "pip install -r pptx-export/requirements.txt"], []
    target = outdir / f"{md.stem}.pptx"
    cmd = [sys.executable, str(CONVERTER), str(md), "--output", str(target)]
    if reflow:
        cmd.append("--reflow")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    warnings = [ln.strip() for ln in proc.stderr.splitlines() if re.match(r"\s*warning:", ln, re.I)]
    lines = [f"PPTX -> {target}"]
    lines += [f"      {ln}" for ln in proc.stdout.strip().splitlines()]
    lines += [f"      {ln}" for ln in proc.stderr.strip().splitlines()]
    return proc.returncode == 0, lines, warnings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("deck", help="path to the Marp .md file")
    p.add_argument("--outdir", help="output folder (default: next to the .md file)")
    p.add_argument("--strict", action="store_true", help="fail on any warning")
    p.add_argument("--preview", action="store_true", help="also write one PNG per slide")
    p.add_argument("--pdf-notes", action="store_true",
                   help="add the speaker notes to the PDF as annotations")
    p.add_argument("--reflow", action="store_true",
                   help="PPTX text re-wraps in PowerPoint (easier to edit) instead of keeping "
                        "the line breaks of the PDF")
    only = p.add_mutually_exclusive_group()
    only.add_argument("--pdf-only", action="store_true")
    only.add_argument("--pptx-only", action="store_true")
    args = p.parse_args()

    md = Path(args.deck).resolve()
    if not md.is_file():
        print(f"error: {md} not found", file=sys.stderr)
        return 1
    outdir = Path(args.outdir).resolve() if args.outdir else md.parent
    outdir.mkdir(parents=True, exist_ok=True)

    sync_css.copy_fonts(md.parent)
    unknown = pictograms.sync(md)
    for name in unknown:
        close = ", ".join(pictograms.suggest(name)) or "none"
        print(f"error: unknown pictogram '{name}' (closest: {close}). "
              "Find names with: python scripts/pictograms.py search <word>", file=sys.stderr)
    if unknown:
        return 1

    issues = lint_deck.lint(md)
    lint_deck.report(issues)
    errors = sum(1 for lvl, *_ in issues if lvl == "error")
    if errors:
        print(f"Stopped: {errors} error(s) in the deck. Fix them and re-run.", file=sys.stderr)
        return 1
    warnings = [f"lint: slide {s} (line {ln}): {m}" for lvl, s, ln, m in issues if lvl == "warning"]

    toolchain.require_marp()                         # stop early if Node or the browser is missing

    steps = []
    if not args.pptx_only:
        steps.append((export_pdf, (md, outdir, args.pdf_notes)))
        if args.preview:
            steps.append((export_preview, (md, outdir)))
    if not args.pdf_only:
        steps.append((export_pptx, (md, outdir, args.reflow)))
    print(f"Exporting {md.name}: " + ", ".join(
        {"export_pdf": "PDF", "export_preview": "PNG previews", "export_pptx": "PPTX"}[f.__name__]
        for f, _ in steps) + " ...")
    with ThreadPoolExecutor(max_workers=len(steps)) as pool:
        results = [f.result() for f in [pool.submit(fn, *a) for fn, a in steps]]

    ok = True
    for step_ok, lines, step_warnings in results:
        ok &= step_ok
        print("\n".join(lines))
        warnings += step_warnings

    if warnings:
        print(f"\n{len(warnings)} warning(s): content may be missing, clipped or mis-styled.",
              file=sys.stderr)
        if args.strict:
            print("Strict mode: fix the .md and re-run the same command until there are "
                  "no warnings.", file=sys.stderr)
            ok = False
    print("Done." if ok else "Finished with errors.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
