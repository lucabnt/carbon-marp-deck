#!/usr/bin/env python3
"""Check that this machine can export decks, and say how to fix what is missing.

    python scripts/check_env.py

Checks Node.js, npx, Chrome/Edge, Marp CLI (pinned version), the Python packages of
the PPTX export and the Plex fonts. Exit code 1 if anything required is missing;
missing fonts are only a warning (the export works, with a substitute font).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toolchain  # noqa: E402

FONTS = tuple(toolchain.INSTALLED_FONT_NAMES)      # Plex Sans, Plex Serif, Plex Mono


def _version(cmd: list[str]) -> str | None:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return (r.stdout or r.stderr).strip().splitlines()[0] if r.returncode == 0 else None


def _font_dirs() -> list[Path]:
    home = Path.home()
    if os.name == "nt":
        return [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
                Path(os.environ.get("LOCALAPPDATA", home)) / "Microsoft" / "Windows" / "Fonts"]
    if sys.platform == "darwin":
        return [home / "Library" / "Fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts")]
    return [home / ".fonts", home / ".local" / "share" / "fonts", Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts")]


def installed_fonts() -> set[str]:
    """Families from FONTS found as installed font files (by file name)."""
    names = set()
    for d in _font_dirs():
        if d.is_dir():
            names.update(p.name.lower().replace("-", "").replace("_", "")
                         for p in d.rglob("*") if p.suffix.lower() in (".ttf", ".otf"))
    found = set()
    for fam in FONTS:
        key = toolchain.INSTALLED_FONT_NAMES[fam].lower().replace(" ", "")
        if any(n.startswith(key) for n in names):
            found.add(fam)
    return found


def main() -> int:
    problems, notes = [], []

    def report(ok: bool, label: str, detail: str, fix: str = "", required: bool = True):
        print(f"{'ok  ' if ok else ('FAIL' if required else 'warn')}  {label:<14} {detail}")
        if not ok:
            (problems if required else notes).append(f"{label}: {fix}")

    node = _version([toolchain.which("node") or "node", "--version"])
    major = int(re.sub(r"\D", "", node.split(".")[0]) or 0) if node else 0
    report(major >= 18, "Node.js", node or "not found", "install Node.js 18 or later")
    report(bool(toolchain.which("npx")), "npx", toolchain.which("npx") or "not found",
           "comes with Node.js")
    browser = toolchain.find_browser()
    report(bool(browser), "browser", browser or "not found",
           "install Google Chrome or Microsoft Edge, or set CHROME_PATH")

    marp = toolchain.marp_base()
    version = _version(marp + ["--version"]) if marp else None
    report(bool(version), "Marp CLI", version or f"@{toolchain.marp_version()} not runnable",
           "needs Node.js and network access once (npx downloads it)")

    for module, pkg in (("pptx", "python-pptx"), ("PIL", "Pillow")):
        try:
            __import__(module)
            ok = True
        except ImportError:
            ok = False
        report(ok, pkg, "installed" if ok else "missing",
               "pip install -r pptx-export/requirements.txt")

    dom = toolchain.ROOT / "pptx-export" / "dom" / "node_modules" / "puppeteer-core"
    report(dom.exists(), "puppeteer-core", "installed" if dom.exists() else
           "not installed yet (installed by the first PPTX export)", required=False,
           fix="run the export once with network access, or `npm ci` in pptx-export/dom")

    fonts = installed_fonts()
    for fam in FONTS:
        report(fam in fonts, fam, "installed" if fam in fonts else "not found",
               "the PDF uses the bundled copy; for the PPTX install the desktop fonts "
               "(TTF or OTF) from the official Plex releases (SIL OFL)", required=False)

    print()
    for line in problems:
        print("required:", line)
    for line in notes:
        print("optional:", line)
    print("Ready to export." if not problems else "Not ready: fix the required items above.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
