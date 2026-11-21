#!/usr/bin/env python3
"""Scaffold a new presentation from template.md.

Creates <out>/<slug>.md (front matter of template.md with the CSS of
themes/carbon.css, metadata replaced, starter slides) and <out>/assets/fonts/ (Plex).

Pictograms are copied into <out>/assets/pictograms/svg/ on demand by
scripts/pictograms.py sync (export_deck.py runs it for you).

Usage:
    python scripts/new_deck.py q3-review --title "Q3 Review" \\
        --author "Jane Smith — Engineering Manager"
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import sync_css  # noqa: E402

TEMPLATE = ROOT / "template.md"

STARTER_SLIDES = """
<!-- _class: lead -->
<!-- _paginate: false -->

# {title}
## Subtitle

<div class="lead-author">
<strong>{name}</strong>
{role}
</div>

---

<!-- _class: toc -->
<!-- _paginate: false -->

# Contents

<div class="toc-grid">
  <div class="toc-item"><span class="toc-num">01</span><span class="toc-title">First topic</span></div>
  <div class="toc-item"><span class="toc-num">02</span><span class="toc-title">Second topic</span></div>
</div>

---

## Replace this with a takeaway title

<!-- content slides go here -->

---

<!-- _class: end -->
<!-- _paginate: false -->

# Thank you

<div class="lead-author">
<strong>{name}</strong>
{role}
</div>
"""


def front_matter_lines(text: str) -> list:
    """Return the YAML front-matter block (including both '---' lines)."""
    text = sync_css.inject_css(text.replace("\r\n", "\n"), sync_css.read_css())
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "---")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "---")
    block = lines[start : end + 1]
    # drop the template's how-to comment (the lines before `marp: true`)
    first = next(i for i, ln in enumerate(block) if ln.startswith("marp:"))
    return [block[0]] + block[first:]


def set_field(lines: list, key: str, value: str) -> None:
    """Replace the first top-level `key: ...` line (before `style:`)."""
    pattern = re.compile(rf"^{key}:\s")
    for i, ln in enumerate(lines):
        if ln.startswith("style:"):
            break
        if pattern.match(ln):
            lines[i] = f"{key}: {json.dumps(value, ensure_ascii=False)}"
            return
    raise SystemExit(f"error: '{key}:' not found in template front-matter")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise SystemExit("error: name produces an empty slug")
    return slug


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("name", help="Deck name; used as folder and file name (slugified)")
    p.add_argument("--title", help="Presentation title (default: name)")
    p.add_argument("--author", default="Your Name — Your Role",
                   help='Format "Name — Role"')
    p.add_argument("--footer", help='Footer text (default: "<title> · <name>")')
    p.add_argument("--out", help="Output folder (default: ./<slug>)")
    p.add_argument("--force", action="store_true", help="Overwrite an existing deck file")
    args = p.parse_args()

    slug = slugify(args.name)
    title = args.title or args.name
    parts = re.split(r"\s+[–—-]\s+", args.author, maxsplit=1)
    person, role = parts[0], (parts[1] if len(parts) > 1 else "")
    footer = args.footer or f"{title} · {person.strip()}"

    out = Path(args.out) if args.out else Path.cwd() / slug
    deck = out / f"{slug}.md"
    if deck.exists() and not args.force:
        raise SystemExit(f"error: {deck} already exists (use --force to overwrite)")

    fm = front_matter_lines(TEMPLATE.read_text(encoding="utf-8-sig"))
    set_field(fm, "title", title)
    set_field(fm, "author", args.author)
    set_field(fm, "footer", footer)

    out.mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    sync_css.copy_fonts(out)
    body = STARTER_SLIDES.format(title=title, name=person.strip(), role=role.strip())
    deck.write_text("\n".join(fm) + "\n" + body, encoding="utf-8", newline="\n")

    print(f"Created {deck}")
    print(f"Assets  {out / 'assets'}  (Plex fonts; pictograms are added on export)")


if __name__ == "__main__":
    sys.exit(main())
