#!/usr/bin/env python3
"""Single source of truth for the deck CSS: themes/carbon.css.

Marp decks must be self-contained, so the CSS is embedded in the front matter
(`style: |`) of every deck. This script keeps those copies identical:

    python scripts/sync_css.py            # rewrite template.md and examples/*.md
    python scripts/sync_css.py --check    # exit 1 if any copy has diverged

`new_deck.py` uses the same function, so scaffolded decks always carry the
current CSS. Edit the CSS only in themes/carbon.css, then run this script.
"""
import argparse
import difflib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_FILE = ROOT / "themes" / "carbon.css"
TARGETS = [ROOT / "template.md"] + sorted((ROOT / "examples").glob("*.md"))
FONTS_DIR = ROOT / "assets" / "fonts"          # Plex woff2 files + OFL licence


def copy_fonts(deck_dir: Path) -> None:
    """Copy the bundled Plex files to <deck_dir>/assets/fonts/ (the theme loads them
    from there with a path relative to the deck). Unchanged files are not copied again."""
    dest = Path(deck_dir) / "assets" / "fonts"
    if not FONTS_DIR.is_dir() or dest.resolve() == FONTS_DIR.resolve():
        return
    dest.mkdir(parents=True, exist_ok=True)
    for src in FONTS_DIR.iterdir():
        if src.suffix in (".woff2", ".txt"):
            target = dest / src.name
            if not target.exists() or target.stat().st_size != src.stat().st_size:
                shutil.copy2(src, target)

STYLE_RE = re.compile(r"^style: \|[ \t]*\n.*?(?=\n---[ \t]*\n)", re.S | re.M)


def style_block(css: str) -> str:
    """CSS text -> the `style: |` YAML block (2-space indent)."""
    body = "\n".join(("  " + ln) if ln.strip() else "" for ln in css.rstrip().split("\n"))
    return "style: |\n" + body


def read_css() -> str:
    return CSS_FILE.read_text(encoding="utf-8").replace("\r\n", "\n")


def inject_css(text: str, css: str) -> str:
    """Return `text` (LF newlines) with its style block replaced by `css`."""
    block = style_block(css)
    new, count = STYLE_RE.subn(lambda _m: block, text, count=1)
    if count != 1:
        raise ValueError("no `style: |` block found in front matter")
    return new


def read_lf(path: Path):
    raw = path.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    return raw.replace("\r\n", "\n"), crlf


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--check", action="store_true", help="Only report divergences")
    args = p.parse_args()

    css = read_css()
    if not args.check:
        copy_fonts(ROOT / "examples")       # examples/ sits one level below assets/
    diverged = 0
    for path in TARGETS:
        text, crlf = read_lf(path)
        try:
            new = inject_css(text, css)
        except ValueError as exc:
            print(f"SKIP {path.relative_to(ROOT)}: {exc}")
            continue
        if new == text:
            print(f"ok       {path.relative_to(ROOT)}")
            continue
        diverged += 1
        if args.check:
            print(f"DIVERGED {path.relative_to(ROOT)}")
            diff = difflib.unified_diff(text.split("\n"), new.split("\n"),
                                        "current", "themes/carbon.css", n=0, lineterm="")
            for ln in list(diff)[2:12]:
                print("   ", ln)
        else:
            data = new.replace("\n", "\r\n") if crlf else new
            path.write_bytes(data.encode("utf-8"))
            print(f"updated  {path.relative_to(ROOT)}")
    if args.check and diverged:
        print(f"\n{diverged} file(s) differ from themes/carbon.css - run: "
              "python scripts/sync_css.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
