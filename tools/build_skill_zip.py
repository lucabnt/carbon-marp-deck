#!/usr/bin/env python3
"""Package the skill as a .zip for upload to claude.ai (Settings > Capabilities > Skills).

Maintainer tool - deck authors do not need to run it.

    python tools/build_skill_zip.py                 # -> dist/carbon-marp-deck-<version>.zip
    python tools/build_skill_zip.py --out FILE.zip
    python tools/build_skill_zip.py --check         # build in a temp folder and test it (CI)

claude.ai accepts at most 200 files per skill, so the ~1,400 pictogram SVGs are packed
into one JSON file, assets/pictograms/svg.json (it rejects nested archives;
scripts/pictograms.py reads either form). Files that the
skill never uses at run time (CI, git settings) are left out. Only files tracked by git
are packaged, as they are in the working tree.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def skill_name() -> str:
    """The `name:` in the SKILL.md front matter, so a fork only renames it there."""
    m = re.search(r"^name:\s*[\"']?([\w.-]+)", (ROOT / "SKILL.md").read_text(encoding="utf-8"), re.M)
    if not m:
        sys.exit("error: no `name:` in the SKILL.md front matter")
    return m.group(1)


NAME = skill_name()
MAX_FILES = 200
SVG_PREFIX = "assets/pictograms/svg/"
SKIP_PREFIXES = (".github/", ".gitattributes", ".gitignore")
ARCHIVES = (".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".jar")


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True,
                         capture_output=True).stdout.decode("utf-8")
    return sorted(f for f in out.split("\0") if f and (ROOT / f).is_file())


def check(zpath: Path) -> list[str]:
    """Test a built zip the way claude.ai and the skill use it. Return the problems."""
    problems = []
    with zipfile.ZipFile(zpath) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        if len(names) > MAX_FILES:
            problems.append(f"{len(names)} files (claude.ai accepts at most {MAX_FILES})")
        problems += [f"nested archive: {n}" for n in names if n.lower().endswith(ARCHIVES)]
        if f"{NAME}/SKILL.md" not in names:
            problems.append(f"{NAME}/SKILL.md missing")
        with tempfile.TemporaryDirectory() as tmp:
            zf.extractall(tmp)
            skill = Path(tmp) / NAME
            deck = Path(tmp) / "deck" / "deck.md"
            deck.parent.mkdir()
            deck.write_text("![](assets/pictograms/svg/cloud--analytics.svg)\n", encoding="utf-8")
            pic = [sys.executable, str(skill / "scripts" / "pictograms.py")]
            if "cloud--analytics" not in subprocess.run(pic + ["search", "cloud--analytics"], capture_output=True,
                                                        text=True).stdout:
                problems.append("pictograms.py search finds nothing in the packaged skill")
            subprocess.run(pic + ["sync", str(deck)], capture_output=True)
            copied = deck.parent / "assets" / "pictograms" / "svg" / "cloud--analytics.svg"
            original = ROOT / SVG_PREFIX / "cloud--analytics.svg"
            if not copied.is_file() or copied.read_bytes() != original.read_bytes():
                problems.append("pictograms.py sync does not copy pictograms from the packaged skill")
    return problems


def main() -> int:
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8")).get("version", "dev")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / f"{NAME}-{version}.zip")
    ap.add_argument("--check", action="store_true", help="build in a temp folder and test the zip")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / f"{NAME}.zip" if args.check else args.out
        if build(out):
            return 1
        problems = check(out)
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    print("claude.ai zip check: " + ("FAILED" if problems else "ok"))
    return 1 if problems else 0


def build(out: Path) -> int:
    """Write the zip to out. Return 1 if it cannot be built."""
    files = [f for f in tracked_files() if not f.startswith(SKIP_PREFIXES)]
    svgs = [f for f in files if f.startswith(SVG_PREFIX)]
    rest = [f for f in files if not f.startswith(SVG_PREFIX)]

    pack = {f[len(SVG_PREFIX):]: (ROOT / f).read_bytes().decode("utf-8") for f in svgs}

    count = len(rest) + 1
    if count > MAX_FILES:
        print(f"error: {count} files, claude.ai accepts at most {MAX_FILES}", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in rest:
            zf.write(ROOT / f, f"{NAME}/{f}")
        zf.writestr(f"{NAME}/assets/pictograms/svg.json",
                    json.dumps(pack, ensure_ascii=False, separators=(",", ":")))

    size = out.stat().st_size / 1e6
    print(f"{out}  {count} files ({len(svgs)} pictograms packed), {size:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
