#!/usr/bin/env python3
"""Regression check for the template, the examples and the PPTX converter.

    python tools/check_examples.py            # run all checks
    python tools/check_examples.py --update   # accept the current converter output as the new baseline
    python tools/check_examples.py --no-pptx  # skip the converter (no Node.js / browser / python-pptx)

Checks:
  1. template.md and examples/*.md pass scripts/lint_deck.py without errors or warnings.
  2. The CSS in those files equals themes/carbon.css (scripts/sync_css.py --check).
  3. Every example, plus tests/converter-cases.md, converts with
     pptx-export/dom/dom_to_pptx.py (needs Node.js, Chrome or Edge, python-pptx).
     Per slide, the shape count, the speaker notes and the warnings must match
     tests/baseline.json. Examples and no-notes.md must have no warnings; converter-cases.md warns
     on purpose (unsupported constructs must be reported, not dropped silently).
     A difference is either a regression or an intended converter change; in the
     second case review the output, then use --update.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import lint_deck  # noqa: E402
import sync_css  # noqa: E402

CONVERTER = ROOT / "pptx-export" / "dom" / "dom_to_pptx.py"
BASELINE = ROOT / "tests" / "baseline.json"
DECKS = [ROOT / "template.md", *sorted((ROOT / "examples").glob("*.md"))]
CONVERTED = [*sorted((ROOT / "examples").glob("*.md")), ROOT / "tests" / "converter-cases.md",
             ROOT / "tests" / "no-notes.md"]


def check_lint(failures: list) -> None:
    for md in DECKS:
        for lvl, slide, line, msg in lint_deck.lint(md):
            failures.append(f"lint {md.name}: slide {slide} (line {line}): {lvl}: {msg}")


def check_css(failures: list) -> None:
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_css.py"), "--check"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        failures.append("css: files differ from themes/carbon.css - run scripts/sync_css.py\n"
                        + (r.stdout + r.stderr).strip())


def convert_all() -> dict:
    """{name: {"shapes": [...], "notes": [...], "warnings": [...]}} per converted deck."""
    from pptx import Presentation
    result = {}
    with tempfile.TemporaryDirectory() as tmp:
        for md in CONVERTED:
            out = Path(tmp) / f"{md.stem}.pptx"
            r = subprocess.run([sys.executable, str(CONVERTER), str(md), "-o", str(out)],
                               capture_output=True, text=True, encoding="utf-8")
            entry = {"returncode": r.returncode,
                     "warnings": [ln for ln in r.stderr.splitlines() if ln.startswith("warning:")]}
            if r.returncode == 0 and out.exists():
                prs = Presentation(str(out))
                entry["shapes"] = [len(s.shapes) for s in prs.slides]
                entry["notes"] = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
                                  for s in prs.slides]
            result[md.stem] = entry
    return result


def check_crlf(current: dict, failures: list) -> None:
    """A CRLF copy of the regression deck must convert exactly like the LF original."""
    from pptx import Presentation
    src = ROOT / "tests" / "converter-cases.md"
    crlf = src.with_name("_crlf-cases.md")   # same folder: relative image paths still resolve
    out = None
    try:
        text = src.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\n", "\r\n")
        crlf.write_bytes(text.encode("utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "crlf.pptx"
            r = subprocess.run([sys.executable, str(CONVERTER), str(crlf), "-o", str(out)],
                               capture_output=True, text=True, encoding="utf-8")
            if r.returncode != 0 or not out.exists():
                failures.append(f"crlf: converter exited with {r.returncode}")
                return
            prs = Presentation(str(out))
            shapes = [len(s.shapes) for s in prs.slides]
            warnings = [ln for ln in r.stderr.splitlines() if ln.startswith("warning:")]
    finally:
        crlf.unlink(missing_ok=True)
    ref = current["converter-cases"]
    if shapes != ref["shapes"]:
        failures.append(f"crlf: shapes {shapes} differ from the LF deck {ref['shapes']}")
    if len(warnings) != len(ref["warnings"]):
        failures.append(f"crlf: {len(warnings)} warnings, the LF deck has {len(ref['warnings'])}")


def check_pptx(failures: list, update: bool) -> None:
    if not CONVERTER.exists():
        failures.append(f"pptx: converter not found at {CONVERTER}")
        return
    try:
        import pptx  # noqa: F401
    except ImportError:
        failures.append("pptx: python-pptx missing (pip install -r pptx-export/requirements.txt, or use --no-pptx)")
        return
    for folder in {md.parent for md in CONVERTED}:
        sync_css.copy_fonts(folder)
    current = convert_all()
    if current.get("converter-cases", {}).get("returncode") == 0:
        check_crlf(current, failures)
    snapshot = {}
    for name, e in current.items():
        if e["returncode"] != 0:
            failures.append(f"pptx {name}: converter exited with {e['returncode']}")
            continue
        snapshot[name] = {k: e[k] for k in ("shapes", "notes", "warnings")}
        if name != "converter-cases":           # only this deck warns on purpose
            failures += [f"pptx {name}: {w}" for w in e["warnings"]]
    if update and failures:
        print("baseline NOT updated: fix the problems below first", file=sys.stderr)
        return
    if update:
        BASELINE.parent.mkdir(exist_ok=True)
        BASELINE.write_text(json.dumps(snapshot, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"baseline updated: {BASELINE}")
        return
    if not BASELINE.exists():
        failures.append("pptx: tests/baseline.json missing (run with --update once)")
        return
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    for name in sorted(set(base) | set(snapshot)):
        a, b = base.get(name), snapshot.get(name)
        if a is None or b is None:
            if b is not None or name in current:   # a failed conversion is reported above
                failures.append(f"pptx {name}: deck added/removed vs baseline")
            continue
        if len(a["shapes"]) != len(b["shapes"]):
            failures.append(f"pptx {name}: {len(b['shapes'])} slides, "
                            f"baseline has {len(a['shapes'])}")
            continue
        diff = [f"slide {i + 1}: {x}->{y}"
                for i, (x, y) in enumerate(zip(a["shapes"], b["shapes"])) if x != y]
        if diff:
            failures.append(f"pptx {name}: shapes differ from baseline ({', '.join(diff)})")
        if a["notes"] != b["notes"]:
            failures.append(f"pptx {name}: speaker notes differ from baseline")
        new, gone = _warning_diff(a["warnings"], b["warnings"])
        failures += [f"pptx {name}: new {w}" for w in new]
        failures += [f"pptx {name}: expected warning no longer issued: {w}" for w in gone]


# Overflow amounts are measured in the browser and shift by a few pixels with the
# Chrome/Edge version and font rasterisation (e.g. 730px locally, 728px on CI).
_PX = re.compile(r"(\d+)px")
PX_TOLERANCE = 8


def _warning_diff(base: list, cur: list) -> tuple[list, list]:
    """(new, gone) warnings; pixel amounts within PX_TOLERANCE count as equal."""
    def split(w):
        return _PX.sub("Npx", w), [int(n) for n in _PX.findall(w)]
    pending = [split(w) + (w,) for w in base]
    new = []
    for w in cur:
        key, nums = split(w)
        for i, (bkey, bnums, _) in enumerate(pending):
            if bkey == key and all(abs(x - y) <= PX_TOLERANCE for x, y in zip(nums, bnums)):
                del pending[i]
                break
        else:
            new.append(w)
    return sorted(new), sorted(w for _, _, w in pending)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", action="store_true", help="rewrite tests/baseline.json")
    ap.add_argument("--no-pptx", action="store_true", help="skip the converter checks")
    args = ap.parse_args()

    failures: list = []
    check_lint(failures)
    check_css(failures)
    if not args.no_pptx:
        check_pptx(failures, args.update)

    if failures:
        print(f"{len(failures)} problem(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"OK: {len(DECKS)} decks linted, CSS in sync"
          + ("" if args.no_pptx else ", converter output matches baseline"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
