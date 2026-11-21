#!/usr/bin/env python3
"""Static checks for a Marp deck written with this template.

Catches the mistakes that break a slide silently, before the PDF / PPTX export:

  error    image path that does not resolve
  error    Markdown inside an HTML block without a blank line (Marp renders it
           literally: `**bold**`, `### title`, `- item` appear as plain text)
  warning  placeholder text from the starter deck still present
  warning  `lead` / `toc` / `section` / `backup` / `end` slide without
           `<!-- _paginate: false -->`
  warning  `.band` that is not the last element of its slide
  warning  pictogram colour that does not fit the slide background
           (default or `blue` on light slides, `white` on dark slides:
           `lead dark`, `section`, `backup`, `end`)
  warning  leftover end-mark image (the closing slide is now text on Gray 100)
  warning  bar chart `.bar` without `style="--v: N"` (N from 0 to 100), without its
           `<span></span>` fill, or a `.bars` chart whose largest bar is not 100;
           stacked and grouped charts: a span without `--v`, bars with different
           numbers of spans, a largest bar that is not 100, no `.legend` on the slide
  warning  `.meter` without `--v` 0-100 or its track, a target (`--t`) without
           `<u></u>` or the reverse, proportional parts over 100 or without a legend
  warning  roadmap `.task` without `--from` < `--to` (0-100) or its `<span></span>`

Usage:
    python scripts/lint_deck.py my-deck/my-deck.md
    python scripts/lint_deck.py my-deck/my-deck.md --strict   # warnings fail too

Exit code: 1 if there are errors (or warnings with --strict), otherwise 0.
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDERS = (
    "Replace this with a takeaway title",
    "content slides go here",
    "First topic",
    "Second topic",
    "Your Name",
    "Your Role",
)
PLACEHOLDER_SUBTITLE = re.compile(r"^##\s+Subtitle\s*$", re.M)

NO_PAGINATE = {"lead", "toc", "section", "backup", "end"}
DARK = {"section", "backup", "end"}          # plus `lead dark`

IMG_RE = re.compile(r"""src=["']([^"']+)["']|!\[[^\]]*\]\(([^)\s]+)""")
IMG_TAG_RE = re.compile(r"<img\b[^>]*>")
HTML_BLOCK_START = re.compile(
    r"^\s{0,3}</?(?:div|table|thead|tbody|tr|td|th|section|ul|ol|li|p|details|"
    r"summary|figure|figcaption|header|footer|article|aside|nav|h[1-6]|hr|"
    r"blockquote|center|dl|dt|dd|form|main)\b", re.I)
MARKDOWN_LINE = re.compile(r"^(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\|)")
BOLD_RE = re.compile(r"\*\*[^*\s][^*]*\*\*")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
SEPARATOR_RE = re.compile(r"^\s{0,3}(-{3,}|\*{3,}|_{3,})\s*$")
BARS_RE = re.compile(r'<div\s+class="bars\b')
BAR_RE = re.compile(r'<div\s+class="bar(?:\s[^"]*)?"')
LEGEND_RE = re.compile(r'<div\s+class="legend\b')
METER_RE = re.compile(r'<div\s+class="meter\b')
ROADMAP_RE = re.compile(r'<div\s+class="roadmap\b')
TASK_RE = re.compile(r'<div\s+class="task\b')


def read_text(md: Path) -> str:
    return md.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def split_slides(text: str):
    """Return [(first_line_number, [lines])] for every slide after the front matter.

    Fence-aware: a `---` inside a fenced code block does not split the deck.
    """
    lines = text.split("\n")
    i = 0
    # optional leading comment, then the YAML front matter
    j = 0
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j < len(lines) and lines[j].lstrip().startswith("<!--"):
        while j < len(lines) and "-->" not in lines[j]:
            j += 1
        j += 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j < len(lines) and lines[j].strip() == "---":
        k = j + 1
        while k < len(lines) and lines[k].strip() != "---":
            k += 1
        i = k + 1

    slides, cur, start, fence = [], [], i + 1, None
    for n in range(i, len(lines)):
        line = lines[n]
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
        elif fence is None and SEPARATOR_RE.match(line):
            slides.append((start, cur))
            cur, start = [], n + 2
            continue
        cur.append(line)
    slides.append((start, cur))
    return [(s, ls) for s, ls in slides if any(x.strip() for x in ls)]


def code_free(lines):
    """Lines with fenced code replaced by blanks (keeps line numbers)."""
    out, fence = [], None
    for line in lines:
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            out.append("")
        else:
            out.append("" if fence else line)
    return out


def blank_comments(lines):
    """Lines with HTML comments (also multi-line) emptied, keeping line numbers."""
    text = "\n".join(lines)
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return text.split("\n")


def slide_classes(lines):
    text = "\n".join(re.sub(r"`[^`\n]*`", "", ln) for ln in lines)
    classes = set()
    for m in re.finditer(r"<!--\s*_class:\s*(.*?)\s*-->", text):
        classes.update(m.group(1).split())
    paginate_off = bool(re.search(r"<!--\s*_paginate:\s*false\s*-->", text))
    return classes, paginate_off


def check_slide(md: Path, number: int, first_line: int, lines, issues):
    def add(level, offset, msg):
        issues.append((level, number, first_line + offset, msg))

    body = code_free(lines)
    classes, paginate_off = slide_classes(body)

    # -- images ---------------------------------------------------------------
    for off, line in enumerate(body):
        plain = re.sub(r"`[^`\n]*`", "", line)
        for m in IMG_RE.finditer(plain):
            ref = m.group(1) or m.group(2)
            if re.match(r"^(https?:|data:|//)", ref):
                continue
            if not (md.parent / ref).exists():
                add("error", off, f"image not found: {ref}")

    # -- Markdown inside an HTML block ---------------------------------------
    in_html, in_comment, in_style = False, False, False
    for off, raw in enumerate(body):
        line = raw.strip()
        if in_comment:
            in_comment = "-->" not in line
            continue
        if in_style:
            in_style = "</style>" not in line
            continue
        if line.startswith("<!--"):
            in_comment = "-->" not in line
            continue
        if re.match(r"<style\b", line):
            in_style = "</style>" not in line
            continue
        if not line:
            in_html = False
            continue
        plain = re.sub(r"`[^`\n]*`", "", line)
        if HTML_BLOCK_START.match(raw):
            in_html = True
            if BOLD_RE.search(re.sub(r"<[^>]*>", "", plain)) and "</" in plain:
                add("error", off, "`**bold**` inside an HTML block is not rendered; "
                                  "use <b>...</b> or put the text after a blank line")
            continue
        if in_html and (MARKDOWN_LINE.match(plain) or BOLD_RE.search(plain)):
            add("error", off, f"Markdown inside an HTML block needs a blank line "
                              f"before it: `{line[:50]}`")

    # -- placeholders ----------------------------------------------------------
    joined = "\n".join(body)
    for ph in PLACEHOLDERS:
        if ph in joined:
            off = next(i for i, ln in enumerate(body) if ph in ln)
            add("warning", off, f"placeholder text left: \"{ph}\"")
    if PLACEHOLDER_SUBTITLE.search(joined):
        off = next(i for i, ln in enumerate(body) if PLACEHOLDER_SUBTITLE.match(ln.strip()))
        add("warning", off, "placeholder text left: \"## Subtitle\"")

    # -- pagination ------------------------------------------------------------
    if classes & NO_PAGINATE and not paginate_off:
        add("warning", 0, "add `<!-- _paginate: false -->` to this slide")

    # -- band position -------------------------------------------------------------
    depth, band_end = 0, None
    for off, raw in enumerate(blank_comments(body)):
        line = raw.strip()
        if band_end is None:
            if depth == 0 and re.match(r'<div\s+class="band\b', line):
                opens, closes = len(re.findall(r"<div\b", line)), len(re.findall(r"</div>", line))
                if opens - closes <= 0:
                    band_end = off
                else:
                    depth += opens - closes
                    band_end = -1                      # multi-line band, find its end
                continue
        elif band_end == -1:
            depth += len(re.findall(r"<div\b", line)) - len(re.findall(r"</div>", line))
            if depth <= 0:
                depth, band_end = 0, off
            continue
        elif band_end >= 0:
            if (line and not line.startswith("<!--") and not line.startswith("</")
                    and not re.match(r'<div\s+class="small\b', line)
                    and not re.match(r"<span\s+class=\"small\"", line)):
                add("warning", band_end, "`.band` should be the last element of the slide")
                break
            continue
        depth += len(re.findall(r"<div\b", line)) - len(re.findall(r"</div>", line))

    # -- charts: bars, meters, roadmaps -----------------------------------------
    check_charts(body, add)

    # -- removed end mark --------------------------------------------------------
    for off, line in enumerate(body):
        if "end-mark" in line:
            add("warning", off, "the end-mark image is no longer part of the template; "
                                "write the closing slide as `# Thank you` (see references/components.md)")
            break

    # -- pictogram colour vs background ----------------------------------------
    dark = bool(classes & DARK) or {"lead", "dark"} <= classes
    for off, line in enumerate(body):
        for tag in IMG_TAG_RE.findall(line):
            cm = re.search(r'class="([^"]*)"', tag)
            cls = cm.group(1).split() if cm else []
            if "pictogram" not in cls:
                continue
            if dark and "white" not in cls:
                add("warning", off, "pictogram on a dark slide must use the `white` class")
            elif not dark and "white" in cls:
                add("warning", off, "white pictogram on a light slide is invisible; "
                                    "drop the `white` class")


def _num(pattern: str, text: str):
    m = re.search(pattern + r":\s*(-?\d+(?:\.\d+)?)\s*[;\"']", text)
    return float(m.group(1)) if m else None


def check_charts(body, add):
    """Bar charts (`.bars`: simple, `stacked`, `grouped`), meters and roadmaps."""
    lines = blank_comments(body)
    has_legend = any(LEGEND_RE.search(ln) for ln in lines)
    chart, kind, totals, segments = None, "", [], set()
    roadmap = None
    for off, raw in enumerate(lines):
        line = raw.strip()

        # meters (one line each)
        if METER_RE.match(line):
            cls = re.search(r'class="([^"]*)"', line).group(1).split()
            if "proportional" in cls:
                inner = re.findall(r"<span\b[^>]*>", line)[1:]
                parts = [_num("--v", s) for s in inner]
                if not inner or None in parts:
                    add("warning", off, "each part of a proportional `.meter` needs "
                                        "`<span style=\"--v: N\"></span>` inside the track")
                elif sum(parts) > 101:
                    add("warning", off, f"the parts of this meter add up to {sum(parts):g}; "
                                        "they can fill at most 100")
                if not has_legend:
                    add("warning", off, "a proportional meter needs a `.legend` on the slide")
            else:
                v = _num("--v", line)
                if v is None or not 0 <= v <= 100:
                    add("warning", off, "each `.meter` needs `style=\"--v: N\"` with N from 0 to 100")
                if "<span><span></span>" not in line.replace(" ", ""):
                    add("warning", off, "`.meter` needs its track: `<span><span></span></span>` "
                                        "after the value")
            t = _num("--t", line)
            if ("<u></u>" in line) != (t is not None):
                add("warning", off, "a target needs both `--t: N` in the style and `<u></u>` "
                                    "in the track")
            elif t is not None and not 0 <= t <= 100:
                add("warning", off, "`--t` must be from 0 to 100")
            continue

        # roadmaps
        if ROADMAP_RE.match(line):
            roadmap = off
            continue
        if roadmap is not None:
            if TASK_RE.match(line):
                a, b = _num("--from", line), _num("--to", line)
                if a is None or b is None or not 0 <= a < b <= 100:
                    add("warning", off, "each `.task` needs `style=\"--from: A; --to: B\"` with "
                                        "0 <= A < B <= 100 (share of the whole timeline)")
                if "<span></span>" not in line.replace(" ", ""):
                    add("warning", off, "`.task` needs an empty `<span></span>` after its label "
                                        "(it draws the bar)")
            elif line.startswith("</div>"):
                roadmap = None
            continue

        # bar charts
        if BARS_RE.match(line):
            cls = re.search(r'class="([^"]*)"', line).group(1).split()
            kind = "stacked" if "stacked" in cls else "grouped" if "grouped" in cls else ""
            chart, totals, segments = off, [], set()
            if kind and not has_legend:
                add("warning", off, f"a {kind} chart needs a `.legend` on the slide "
                                    "(one `<span><i></i>Name</span>` per series)")
            continue
        if chart is None:
            continue
        if BAR_RE.match(line):
            if kind:
                spans = re.findall(r"<span\b[^>]*>", line)
                parts = [_num("--v", s) for s in spans]
                if not spans or None in parts:
                    add("warning", off, f"each span of a {kind} `.bar` needs "
                                        "`style=\"--v: N\"` with N from 0 to 100")
                    continue
                segments.add(len(spans))
                totals.append(sum(parts) if kind == "stacked" else max(parts))
                if totals[-1] > 101:
                    add("warning", off, f"this bar reaches {totals[-1]:g}; "
                                        "the largest bar must be 100")
                if kind == "grouped" and line.count("<small>") not in (0, len(spans)):
                    add("warning", off, "put one `<small>` value inside every span, or none")
            else:
                v = _num("--v", line)
                if v is None or not 0 <= v <= 100:
                    add("warning", off, "each `.bar` needs `style=\"--v: N\"` with N from 0 to 100 "
                                        "(value / largest value x 100)")
                else:
                    totals.append(v)
                if "<span></span>" not in line.replace(" ", ""):
                    add("warning", off, "`.bar` needs an empty `<span></span>` between label "
                                        "and value (it draws the bar)")
        elif line.startswith("</div>"):
            top = max(totals) if totals else None
            if top is not None and not (99 <= top <= 101 if kind == "stacked" else top == 100):
                add("warning", chart, f"the largest bar is {top:g}; "
                                      "scale the chart so the largest value is 100")
            if len(segments) > 1:
                add("warning", chart, f"every bar of a {kind} chart needs the same number of "
                                      "spans (use `--v: 0` for an empty one)")
            chart = None


def lint(md: Path):
    """Return a list of (level, slide_number, line_number, message)."""
    issues = []
    for n, (first, lines) in enumerate(split_slides(read_text(md)), start=1):
        check_slide(md, n, first, lines, issues)
    return issues


def report(issues, stream=sys.stderr):
    for level, slide, line, msg in issues:
        print(f"{level}: slide {slide} (line {line}): {msg}", file=stream)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("deck", help="Path to the Marp .md file")
    p.add_argument("--strict", action="store_true", help="Warnings fail too")
    args = p.parse_args()
    md = Path(args.deck).resolve()
    if not md.is_file():
        print(f"error: {md} not found", file=sys.stderr)
        return 1
    issues = lint(md)
    report(issues)
    errors = sum(1 for i in issues if i[0] == "error")
    warnings = len(issues) - errors
    print(f"lint: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
