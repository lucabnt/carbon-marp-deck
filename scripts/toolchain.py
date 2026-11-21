#!/usr/bin/env python3
"""Shared toolchain helpers: Marp CLI, the browser and the Python dependencies.

Every script that renders a deck (export_deck.py, build_examples.py, the PPTX
converter, check_env.py) goes through this module, so that all of them use the same
pinned Marp CLI, the same browser and the same Marp options.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Options every Marp call needs. Raw HTML is part of the component syntax, but only
# through the allowlist in themes/marp.config.json: the tags and attributes the
# components use (class, style, src…) are kept, while <script>, <iframe>, event
# handlers (onerror=…) and anything else are removed before the deck is rendered.
# Images are local files, hence --allow-local-files.
MARP_CONFIG = ROOT / "themes" / "marp.config.json"
MARP_OPTIONS = ["--no-stdin", "--config-file", str(MARP_CONFIG), "--allow-local-files"]

# The theme declares the bundled Plex files under short family names. Installed copies
# (needed by PowerPoint) carry the typeface's full official family name, so the PPTX export
# and check_env.py translate with this table; it is the one place that name is needed.
INSTALLED_FONT_NAMES = {
    "Plex Sans": "IBM Plex Sans",
    "Plex Serif": "IBM Plex Serif",
    "Plex Mono": "IBM Plex Mono",
}

_BROWSER_NAMES = ("google-chrome", "google-chrome-stable", "chrome", "chromium",
                  "chromium-browser", "msedge", "microsoft-edge", "microsoft-edge-stable")
_BROWSER_PATHS = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
)


def which(name: str) -> str | None:
    """shutil.which that also finds the .cmd shims npm installs on Windows."""
    return shutil.which(name) or (shutil.which(name + ".cmd") if os.name == "nt" else None)


@lru_cache(maxsize=None)
def marp_version() -> str:
    """The Marp CLI version pinned in package.json."""
    try:
        spec = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        return spec["devDependencies"]["@marp-team/marp-cli"].lstrip("^~")
    except (OSError, KeyError, ValueError):
        return "latest"


@lru_cache(maxsize=None)
def find_browser() -> str | None:
    """Chrome, Edge or Chromium: CHROME_PATH first, then PATH, then the usual locations."""
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for name in _BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return next((p for p in _BROWSER_PATHS if Path(p).exists()), None)


def marp_base() -> list[str] | None:
    """The Marp CLI executable: a local install, else the pinned version through npx.

    Returns None when neither a local install nor npx is available.
    """
    local = ROOT / "node_modules" / ".bin" / ("marp.cmd" if os.name == "nt" else "marp")
    if local.exists():
        return [str(local)]
    npx = which("npx")
    return [npx, "--yes", f"@marp-team/marp-cli@{marp_version()}"] if npx else None


def marp_command() -> list[str] | None:
    """marp_base() plus the common options and the browser found by find_browser()."""
    cmd = marp_base()
    if cmd is None:
        return None
    browser = find_browser()
    return cmd + MARP_OPTIONS + (["--browser-path", browser] if browser else [])


def require_marp() -> list[str]:
    """marp_command(), or exit with an actionable message."""
    if not find_browser():
        sys.exit("error: no browser found - install Google Chrome or Microsoft Edge, "
                 "or set CHROME_PATH to its executable")
    cmd = marp_command()
    if not cmd:
        sys.exit("error: npx not found - install Node.js 18 or later")
    return cmd


def run_marp(args: list[str], quiet: bool = False) -> subprocess.CompletedProcess:
    """Run Marp CLI with the common options followed by `args`."""
    return subprocess.run(require_marp() + args, text=True, encoding="utf-8",
                          errors="replace", capture_output=quiet)


def has_python_pptx() -> bool:
    try:
        import pptx  # noqa: F401
    except ImportError:
        return False
    return True
