#!/usr/bin/env python3
"""Measure how closely the PPTX export reproduces the PDF, slide by slide.

    python tools/check_fidelity.py                      # every example
    python tools/check_fidelity.py examples/03-cards.md --keep out/

For each deck: Marp renders the slides to PNG (what the PDF shows), the deck is converted
to PPTX, PowerPoint renders that PPTX to PNG, and the two images are compared. The score
is the mean pixel difference after a 1 px blur (so anti-aliasing and the dithering
PowerPoint applies to light fills do not count), in % of full scale. A slide above
--max (default 1.25 %) fails.

Needs Windows with Microsoft PowerPoint (driven through COM, read-only), plus everything
the export needs. With --keep, writes side-by-side images (PDF | PPTX | difference).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_css  # noqa: E402
import toolchain  # noqa: E402

CONVERTER = toolchain.ROOT / "pptx-export" / "dom" / "dom_to_pptx.py"
PS_EXPORT = r"""
param([string]$Pptx, [string]$OutDir)
$ErrorActionPreference = "Stop"
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($Pptx, -1, 0, 0)   # read-only, no window
    try {
        $i = 1
        foreach ($s in $pres.Slides) {
            $s.Export((Join-Path $OutDir ("ppt.{0:D3}.png" -f $i)), "PNG", 1280, 720); $i++
        }
    } finally { $pres.Close() }
} finally {
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
"""


def render(md: Path, work: Path) -> str | None:
    """Marp PNGs + PowerPoint PNGs of the converted deck in `work`; an error message or None."""
    r = toolchain.run_marp([str(md), "--images", "png", "--output", str(work / "marp.png")], quiet=True)
    if r.returncode:
        return "marp failed: " + r.stderr.strip()[-300:]
    pptx = work / "deck.pptx"
    r = subprocess.run([sys.executable, str(CONVERTER), str(md), "-o", str(pptx)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        return "conversion failed: " + r.stderr.strip()[-300:]
    script = work / "export.ps1"
    script.write_text(PS_EXPORT, encoding="utf-8")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(script), str(pptx), str(work)], capture_output=True, text=True)
    return None if r.returncode == 0 else "PowerPoint export failed: " + r.stderr.strip()[-300:]


def compare(work: Path, keep: Path | None) -> list[float]:
    from PIL import Image, ImageChops, ImageFilter, ImageStat
    scores = []
    for i, a_path in enumerate(sorted(work.glob("marp.*.png")), 1):
        b_path = work / f"ppt.{i:03d}.png"
        if not b_path.exists():
            scores.append(100.0)
            continue
        a = Image.open(a_path).convert("RGB")
        b = Image.open(b_path).convert("RGB").resize(a.size)
        blur = lambda im: im.convert("L").filter(ImageFilter.BoxBlur(1))  # noqa: E731
        d = ImageChops.difference(blur(a), blur(b))
        scores.append(ImageStat.Stat(d).mean[0] / 255 * 100)
        if keep:
            side = Image.new("RGB", (a.width * 3, a.height), "white")
            side.paste(a, (0, 0))
            side.paste(b, (a.width, 0))
            side.paste(ImageChops.difference(a, b).point(lambda v: min(255, v * 3)), (a.width * 2, 0))
            side.save(keep / f"side.{i:03d}.png")
    return scores


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("decks", nargs="*", type=Path)
    # 1.25 %: slides that look identical can reach ~1 % because PowerPoint dithers light
    # fills (table cells, tiles) when it exports PNG; real layout problems score higher
    ap.add_argument("--max", type=float, default=1.25, help="highest acceptable slide score (%%)")
    ap.add_argument("--keep", type=Path, help="folder for the side-by-side images")
    args = ap.parse_args()
    if os.name != "nt":
        sys.exit("error: needs Windows with Microsoft PowerPoint")
    toolchain.require_marp()
    decks = args.decks or sorted((toolchain.ROOT / "examples").glob("*.md"))

    failed = 0
    for md in decks:
        md = md.resolve()
        sync_css.copy_fonts(md.parent)
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            error = render(md, work)
            if error:
                print(f"FAIL {md.name}: {error}")
                failed += 1
                continue
            keep = None
            if args.keep:
                keep = args.keep / md.stem
                keep.mkdir(parents=True, exist_ok=True)
            scores = compare(work, keep)
        worst = max(range(len(scores)), key=scores.__getitem__) if scores else 0
        bad = [i + 1 for i, s in enumerate(scores) if s > args.max]
        status = "FAIL" if bad else "ok  "
        failed += bool(bad)
        print(f"{status} {md.name:<28} mean {sum(scores) / max(1, len(scores)):.2f}%  "
              f"worst slide {worst + 1} {scores[worst] if scores else 0:.2f}%"
              + (f"  over {args.max}%: slides {bad}" if bad else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
