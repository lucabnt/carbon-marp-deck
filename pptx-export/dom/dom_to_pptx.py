#!/usr/bin/env python3
"""Marp deck -> editable PPTX, built from the geometry Chromium actually renders.

Pipeline:  deck.md --Marp CLI--> HTML --headless Chromium + page_extract.js--> positioned
           ops (boxes, text runs, images) --python-pptx--> .pptx. Speaker notes come from
           `marp --notes`. Because the layout is measured in the browser, any HTML/CSS the
           deck uses (custom components included) is reproduced, not just known patterns.

Usage:  python pptx-export/dom/dom_to_pptx.py deck.md --output deck.pptx
Needs:  Node >= 18 (its dependencies are installed automatically on first run),
        Chrome or Edge (CHROME_PATH overrides the search), python-pptx.
Options: --reflow     let PowerPoint wrap the text again (easier to edit; by default every
                      line ends where it ends in the PDF)
         --keep-html  keep the intermediate HTML next to the deck (debugging)
         --dy PX      extra vertical text offset in slide px
         --widen F    text box widening, fraction of the width (default 0.012)
"""
import argparse
import base64
import io
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import toolchain  # noqa: E402  (pinned Marp CLI, browser discovery, shared options)

PX = 9525  # EMU per slide px (slide = 1280 x 720 px = 13.333 x 7.5 in)
A = "http://schemas.openxmlformats.org/drawingml/2006/main"

WIDEN = 0.012  # text box widening (fraction): keeps PowerPoint from wrapping earlier than Chrome


def ppt_baseline(lh, size):
    """Where PowerPoint draws the first baseline of a text box with exact line spacing `lh`
    and zero insets, in px below the top, for a font of `size` px. It does not depend on the
    font. Below 1.2 em PowerPoint keeps the descent under the baseline; from 1.2 em it
    spreads the extra leading. Fitted on PowerPoint 365 renders (Segoe UI and its Light /
    SemiBold faces, Georgia, Consolas, Arial; 12-54 px; 1.0-1.65 em): mean error 0.3 px."""
    if lh < 1.2 * size:
        return 1.024 * lh - 0.248 * size
    return 0.760 * lh - 0.011 * size
ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}


def emu(v):
    return int(round(v * PX))


# -- Marp + Chromium -------------------------------------------------------
def render_html(md, html):
    r = toolchain.run_marp([str(md), "--template", "bare", "--output", str(html)], quiet=True)
    if r.returncode:
        sys.exit("error: marp failed:\n" + (r.stderr or r.stdout))


def render_notes(md):
    """Raw `marp --notes` output ("" when the deck has no notes, None if Marp failed)."""
    with tempfile.TemporaryDirectory() as tmp:
        txt = Path(tmp) / "notes.txt"
        r = toolchain.run_marp([str(md), "--notes", "--output", str(txt)], quiet=True)
        if r.returncode:
            return None
        # Marp writes an empty file (or none) when the deck has no notes at all
        return txt.read_text(encoding="utf-8").replace("\r\n", "\n") if txt.exists() else ""


def split_notes(text, slide_count):
    """Speaker notes per slide; None (+ warning) if they cannot be mapped to the slides."""
    if text is None:
        return None
    if not text.strip():
        return [""] * slide_count
    notes = [n.strip() for n in re.split(r"(?m)^---$", text)]
    # banner-only comments (<!-- ═══ -->, <!-- --- -->) carry no text: not speaker notes
    notes = ["\n\n".join(p for p in re.split(r"\n\s*\n", n) if re.search(r"\w", p)) for n in notes]
    if len(notes) != slide_count:
        print(f"warning: speaker notes not exported ({len(notes)} note blocks for "
              f"{slide_count} slides; a note probably contains a line with only '---')",
              file=sys.stderr)
        return None
    return notes


def ensure_node_deps():
    if (HERE / "node_modules" / "puppeteer-core").exists():
        return
    npm = toolchain.which("npm")
    if not toolchain.which("node") or not npm:
        sys.exit("error: Node.js >= 18 (node, npm) is required for PPTX export")
    print("first run: installing puppeteer-core in pptx-export/dom ...", file=sys.stderr)
    # `npm ci` installs exactly the versions recorded in package-lock.json
    verb = "ci" if (HERE / "package-lock.json").exists() else "install"
    r = subprocess.run([npm, verb, "--no-audit", "--no-fund"], cwd=HERE,
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"error: npm {verb} failed in pptx-export/dom:\n" + (r.stderr or r.stdout))


def extract(html, out_json):
    ensure_node_deps()
    r = subprocess.run([toolchain.which("node"), str(HERE / "extract.js"), str(html),
                        str(out_json), toolchain.find_browser() or ""],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit("error: extraction failed:\n" + (r.stderr or r.stdout))
    return json.loads(Path(out_json).read_text(encoding="utf-8"))


# -- XML helpers -----------------------------------------------------------
def rgb(c):
    return RGBColor(c[0], c[1], c[2])


def add_alpha(clr_el, alpha):
    if clr_el is not None and alpha is not None and alpha < 0.999:
        a = etree.SubElement(clr_el, f"{{{A}}}alpha")
        a.set("val", str(int(round(alpha * 100000))))


def apply_gradient(fill, grad):
    """Replace stops/angle of a python-pptx FillFormat with the CSS gradient."""
    fill.gradient()
    g = fill._xPr.find(f".//{{{A}}}gradFill")
    for ch in list(g):
        g.remove(ch)
    gs_lst = etree.SubElement(g, f"{{{A}}}gsLst")
    for st in grad["stops"]:
        gs = etree.SubElement(gs_lst, f"{{{A}}}gs")
        gs.set("pos", str(int(round(st["pos"] * 100000))))
        clr = etree.SubElement(gs, f"{{{A}}}srgbClr")
        clr.set("val", "%02X%02X%02X" % tuple(st["color"][:3]))
        add_alpha(clr, st["color"][3])
    lin = etree.SubElement(g, f"{{{A}}}lin")
    lin.set("ang", str(int(((grad["angle"] - 90) % 360) * 60000)))
    lin.set("scaled", "0")
    g.set("rotWithShape", "1")


def set_fill(fill, color, grad):
    if grad:
        apply_gradient(fill, grad)
    elif color:
        fill.solid()
        fill.fore_color.rgb = rgb(color)
        add_alpha(fill._xPr.find(f".//{{{A}}}solidFill/{{{A}}}srgbClr"), color[3])
    else:
        fill.background()


def strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


# -- shapes ----------------------------------------------------------------
def add_box(slide, op):
    x, y, w, h = op["x"], op["y"], op["w"], op["h"]
    if w <= 0.2 or h <= 0.2:
        return
    sides = [op["borders"].get(k) for k in "trbl"]
    uniform = all(sides) and len({(s["w"], tuple(s["color"]), s["style"]) for s in sides}) == 1
    radius = op["radius"]
    rounded = radius > 0.5
    ins = sides[0]["w"] / 2 if uniform else 0
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                 emu(x + ins), emu(y + ins),
                                 emu(max(w - 2 * ins, 0.5)), emu(max(h - 2 * ins, 0.5)))
    strip_style(shp)
    shp.name = op.get("name") or "box"
    if rounded:
        shp.adjustments[0] = min(0.5, radius / max(1.0, min(w, h) - 2 * ins))
    set_fill(shp.fill, op["fill"], op["grad"])
    if uniform:
        s = sides[0]
        shp.line.color.rgb = rgb(s["color"])
        shp.line.width = Emu(emu(s["w"]))
        add_alpha(shp.line._ln.find(f".//{{{A}}}srgbClr"), s["color"][3])
        if s["style"] in ("dashed", "dotted"):
            d = etree.SubElement(shp.line._ln, f"{{{A}}}prstDash")
            d.set("val", "dash" if s["style"] == "dashed" else "sysDot")
        return
    shp.line.fill.background()
    for key, s in zip("trbl", sides):
        if not s:
            continue
        bw = s["w"]
        geo = {"t": (x, y, w, bw), "b": (x, y + h - bw, w, bw),
               "l": (x, y, bw, h), "r": (x + w - bw, y, bw, h)}[key]
        side = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, *[emu(v) for v in geo])
        strip_style(side)
        side.name = (op.get("name") or "box") + f" border-{key}"
        set_fill(side.fill, s["color"], None)
        side.line.fill.background()


def is_fullbleed_opaque(op):
    """True for an image covering the whole slide with no transparency."""
    if op["x"] > 1 or op["y"] > 1 or op["w"] < 1278 or op["h"] < 718:
        return False
    im = Image.open(io.BytesIO(base64.b64decode(op["png"])))
    return im.mode != "RGBA" or im.getchannel("A").getextrema()[0] == 255


def set_background_picture(slide, op):
    """Full-bleed picture as slide background: not selectable, never covers other shapes."""
    _, rid = slide.part.get_or_add_image_part(io.BytesIO(base64.b64decode(op["png"])))
    slide.background.fill.solid()
    bg_pr = slide._element.cSld.find(qn("p:bg")).find(qn("p:bgPr"))
    for ch in list(bg_pr):
        bg_pr.remove(ch)
    blip_fill = etree.SubElement(bg_pr, f"{{{A}}}blipFill")
    blip_fill.set("dpi", "0")
    blip_fill.set("rotWithShape", "1")
    blip = etree.SubElement(blip_fill, f"{{{A}}}blip")
    blip.set(qn("r:embed"), rid)
    etree.SubElement(etree.SubElement(blip_fill, f"{{{A}}}stretch"), f"{{{A}}}fillRect")
    etree.SubElement(bg_pr, f"{{{A}}}effectLst")


def add_image(slide, op):
    pic = slide.shapes.add_picture(io.BytesIO(base64.b64decode(op["png"])),
                                   emu(op["x"]), emu(op["y"]), emu(op["w"]), emu(op["h"]))
    pic.name = "image"


# -- text ------------------------------------------------------------------
GENERIC = ("sans-serif", "serif", "monospace", "system-ui", "ui-monospace")

def installed_name(family):
    """'Plex Sans Light' -> the installed family PowerPoint knows; other names unchanged."""
    for alias, name in toolchain.INSTALLED_FONT_NAMES.items():
        if family == alias or family.startswith(alias + " "):
            return name + family[len(alias):]
    return family


def first_family(css):
    for fam in css.split(","):
        fam = fam.strip().strip("'\"")
        if fam and fam.lower() not in GENERIC:
            return fam
    return "Arial"


def font_for(run):
    """(family, bold) for PowerPoint: the face Chrome actually used (page_extract.js)."""
    face = run.get("face")
    if face:
        return installed_name(face["family"]), face["bold"]
    return installed_name(first_family(run["font"])), run["weight"] >= 600


def merge_runs(runs):
    out = []
    for r in runs:
        if not r.get("br") and out and not out[-1].get("br") and \
                all(out[-1].get(k) == r.get(k) for k in r if k != "t"):
            out[-1]["t"] += r["t"]
        else:
            out.append(dict(r))
    return out


def soft_breaks_to_spaces(runs):
    """--reflow: the line breaks Chrome made by wrapping become spaces again."""
    out = []
    for r in runs:
        if r.get("soft"):
            if out and not out[-1].get("br") and not out[-1]["t"].endswith(" "):
                out.append(dict(out[-1], t=" "))
        else:
            out.append(r)
    return out


def add_text(slide, op, dy_px, reflow=False):
    raw = soft_breaks_to_spaces(op["runs"]) if reflow else op["runs"]
    runs = merge_runs(raw)
    if not any(not r.get("br") and r["t"].strip() for r in runs):
        return
    # Exact mode (default): every line ends where Chrome ended it, so PowerPoint must not
    # wrap again. Reflow mode: PowerPoint wraps, as in the PDF as long as fonts match.
    wrap = bool(op["wrap"]) and reflow
    w, align = op["w"], op["align"]
    extra = w * WIDEN + (0 if wrap else 6)
    x = op["x"] - (extra / 2 if align == "center" else extra if align == "right" else 0)
    y = op["y"] + dy_px
    lh = op["lh"]
    if lh and op.get("base") is not None:
        first_line = next((i for i, r in enumerate(runs) if r.get("br")), len(runs))
        size = max((r["size"] for r in runs[:first_line] if not r.get("br")), default=lh / 1.4)
        if first_line == len(runs) and not wrap:
            # one line: the line pitch is irrelevant, so use 1.5 em, where PowerPoint's
            # baseline is predictable for every font (±0.5 px) instead of the CSS value,
            # which may fall near PowerPoint's font-dependent switch at about 1.2 em
            lh = 1.5 * size
        # put the first baseline where Chrome drew it (see ppt_baseline)
        y += op["base"] - ppt_baseline(lh, size)
    tb = slide.shapes.add_textbox(emu(x), emu(y), emu(w + extra), emu(max(op["h"], lh or 0, 4)))
    tb.name = op.get("name") or "text"
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = ALIGN.get(align, PP_ALIGN.LEFT)
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    if lh:
        p.line_spacing = Pt(lh * 0.75)
    for r in runs:
        if r.get("br"):
            p.add_line_break()
            continue
        run = p.add_run()
        run.text = r["t"]
        f = run.font
        fam, bold = font_for(r)
        f.name = "Segoe UI Emoji" if r.get("emoji") else fam
        f.size = Pt(round(r["size"] * 0.75 * 2) / 2)
        f.bold = True if bold else None
        f.italic = True if r["italic"] else None
        if r["underline"]:
            f.underline = True
        if r["color"]:
            f.color.rgb = rgb(r["color"])
        rPr = run._r.get_or_add_rPr()
        if r["color"]:
            add_alpha(rPr.find(f".//{{{A}}}solidFill/{{{A}}}srgbClr"), r["color"][3])
        if r["strike"]:
            rPr.set("strike", "sngStrike")
        if r["sup"]:
            rPr.set("baseline", "30000")
        elif r["sub"]:
            rPr.set("baseline", "-25000")
        if r["spc"]:
            rPr.set("spc", str(int(round(r["spc"] * 0.75 * 100))))
        if r["bg"]:
            hl = etree.Element(f"{{{A}}}highlight")
            etree.SubElement(hl, f"{{{A}}}srgbClr").set("val", "%02X%02X%02X" % tuple(r["bg"][:3]))
            latin = rPr.find(f"{{{A}}}latin")
            latin.addprevious(hl) if latin is not None else rPr.append(hl)
        if r["href"]:
            run.hyperlink.address = r["href"]


# -- main ------------------------------------------------------------------
def build(data, out, dy_px=0.0, notes=None, reflow=False):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(1280 * PX), Emu(720 * PX)
    blank = prs.slide_layouts[6]
    for si, sd in enumerate(data["slides"]):
        slide = prs.slides.add_slide(blank)
        if notes and notes[si]:
            slide.notes_slide.notes_text_frame.text = notes[si]
        bg = sd["bg"] or {}
        if bg.get("fill") or bg.get("grad"):
            set_fill(slide.background.fill, bg.get("fill"), bg.get("grad"))
        for i, op in enumerate(sd["ops"]):
            if op["t"] == "image" and i == 0 and is_fullbleed_opaque(op):
                set_background_picture(slide, op)
            elif op["t"] == "box":
                add_box(slide, op)
            elif op["t"] == "text":
                add_text(slide, op, dy_px, reflow)
            elif op["t"] == "image":
                add_image(slide, op)
    prs.save(out)


def main():
    global WIDEN
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("--output", "-o", required=True)
    ap.add_argument("--keep-html", action="store_true", help="keep the intermediate HTML/JSON")
    ap.add_argument("--dy", type=float, default=0.0, help="vertical text offset in slide px (calibration)")
    ap.add_argument("--widen", type=float, default=WIDEN, help="text box widening fraction")
    ap.add_argument("--reflow", action="store_true",
                    help="let PowerPoint wrap the text (easier to edit) instead of keeping "
                         "the line breaks of the PDF")
    args = ap.parse_args()
    WIDEN = args.widen

    md = Path(args.deck).resolve()
    if not md.is_file():
        sys.exit(f"error: {md} not found")
    html = md.with_name(f".{md.stem}.dom.html")   # next to the deck: relative assets resolve
    # the speaker notes need their own Marp run: do it while the slides are measured
    with ThreadPoolExecutor(max_workers=1) as pool, tempfile.TemporaryDirectory() as tmp:
        notes_text = pool.submit(render_notes, md)
        try:
            render_html(md, html)
            data = extract(html, Path(tmp) / "ops.json")
        finally:
            if not args.keep_html and html.exists():
                html.unlink()
        notes = split_notes(notes_text.result(), len(data["slides"]))
    for msg in data["warnings"]:
        print("warning:", msg, file=sys.stderr)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    build(data, args.output, args.dy, notes, args.reflow)
    n = sum(len(sd["ops"]) for sd in data["slides"])
    print(f"wrote {args.output}: {len(data['slides'])} slides, {n} objects, "
          f"{len(data['warnings'])} warnings")


if __name__ == "__main__":
    main()
