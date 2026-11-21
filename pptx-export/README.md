# PPTX export

Turns a Marp deck into an **editable** PowerPoint file that matches the PDF: same positions,
same fonts, same line breaks, native shapes and text boxes.

The converter is [`dom/dom_to_pptx.py`](dom/dom_to_pptx.py): Marp renders HTML, headless Chrome
measures every element, python-pptx rebuilds the slide.

## Usage

Through the wrapper (lint, PDF, previews and PPTX in parallel):

```bash
python scripts/export_deck.py my-deck.md                # PDF + PPTX
python scripts/export_deck.py my-deck.md --pptx-only
python scripts/export_deck.py my-deck.md --pptx-only --reflow
```

Directly:

```bash
python pptx-export/dom/dom_to_pptx.py my-deck.md --output my-deck.pptx
```

| Option | Meaning |
|---|---|
| `--output`, `-o` | Output `.pptx` (required) |
| `--reflow` | Let PowerPoint wrap the text again. Easier to edit; line breaks may then differ from the PDF |
| `--keep-html` | Keep the intermediate `.<name>.dom.html` next to the deck (debugging) |
| `--dy PX` | Extra vertical text offset in slide pixels (default 0; normally not needed) |
| `--widen F` | Text box widening as a fraction of the width (default 0.012) |

Warnings go to stderr as `warning: slide N: ...`; `export_deck.py --strict` turns them into a failure.

## Prerequisites

- Python 3.9+ and `pip install -r pptx-export/requirements.txt`
- Node.js 18+. The first run installs `puppeteer-core` in `pptx-export/dom/node_modules` by itself,
  with `npm ci` at the exact version recorded in `package-lock.json`.
- Chrome or Edge, found by [`scripts/toolchain.py`](../scripts/toolchain.py) (`CHROME_PATH` overrides it).
- **The fonts.** Plex is bundled ([`assets/fonts/`](../assets/fonts/)) and loaded by the theme,
  so the PDF and the measurement always use it. The PPTX names the installed Plex families,
  including their Light and SemiBold faces: the machines that open it need the Plex fonts
  installed. `python scripts/check_env.py` tells you whether it is.

## Security

The HTML Marp produces is already filtered by the allowlist in
[`themes/marp.config.json`](../themes/marp.config.json) (no scripts, no event handlers). The
headless Chrome that measures it loads only local files (`file:`, `data:`, `blob:`): every other
request is refused and reported as a warning, and the twemoji images Marp would fetch are
answered locally. Chrome keeps its sandbox unless it runs as root or `CHROME_NO_SANDBOX=1` is
set. See [`SECURITY.md`](../SECURITY.md).

## Pipeline

```
deck.md --marp--> .deck.dom.html --extract.js + page_extract.js (Chrome)--> ops --dom_to_pptx.py--> deck.pptx
        --marp --notes (in parallel)--> speaker notes ------------------------------------------^
```

1. Marp renders the deck to HTML next to the deck (relative assets resolve), and, at the same
   time, the speaker notes.
2. [`extract.js`](dom/extract.js) opens the HTML in headless Chrome; [`page_extract.js`](dom/page_extract.js)
   walks each slide and records, in slide pixels (1280 × 720): boxes (fill, gradient, border, radius,
   opacity), text runs, list markers, images, CSS `url()` backgrounds, the page number and the
   `![bg]` layers.
3. [`dom_to_pptx.py`](dom/dom_to_pptx.py) turns each record into a PowerPoint shape, text box or picture.

Because the geometry is measured, custom HTML and CSS in a deck are reproduced as well as the
built-in components.

## How the PPTX matches the PDF

| Aspect | What the converter does |
|---|---|
| **Fonts** | For every run it detects which family of the CSS stack Chrome really drew with and names that family, including the weight faces of static fonts (the Light and SemiBold faces of Plex, `Segoe UI Semibold`). The bundled Plex web fonts, declared as Plex Sans / Serif / Mono, are mapped to the installed family names (`INSTALLED_FONT_NAMES` in `scripts/toolchain.py`). It also works, and when a custom deck uses other fonts. |
| **Line breaks** | Every line ends where Chrome ended it: the wrap points are measured character by character and written as line breaks, and the text boxes do not wrap. `--reflow` keeps wrapping on instead. |
| **Baselines** | Chrome and PowerPoint place text differently inside a line. The converter measures Chrome's first baseline and moves each text box so that PowerPoint's baseline lands on it. PowerPoint's rule was fitted on PowerPoint 365 renders of Plex Sans (Light, Regular, SemiBold), Serif and Mono, Segoe UI, Georgia, Consolas and Arial at 12–54 px: from 1.2 em the first baseline sits `0.760·L − 0.011·size` below the top (within 0.5 px for every font at 1.5 em), below about 1.2 em `1.024·L − 0.248·size`; the switch between the two depends slightly on the font. Single-line text therefore gets 1.5 em spacing (the pitch does not matter for one line); multi-line text keeps the CSS line height. |
| **List markers** | Placed against the border box (outside markers) with Chrome's spacing; `disc`, `circle`, `square`, string markers such as `"–"`, numbers, letters and roman numerals. |
| **Inline code** | Its padding becomes a highlighted space of the same width; the real space after it is kept. |
| **Pseudo-element drawings** | An empty, absolutely positioned `::before` / `::after` that draws a background image or colour (the status icons of `.band`) is exported as a picture or rectangle at the same place. Text in pseudo-elements, and drawings whose position cannot be computed, are reported. |
| **Overflow** | Content that runs past the slide's bottom margin, which Marp cuts off silently, is reported with the number of pixels (`--strict` then fails). |
| **Emoji** | Rendered as text in Segoe UI Emoji; during measurement they take the same 1 em box as Marp's twemoji images, without network access. |
| **Colours** | Semi-transparent text is flattened against its background (PowerPoint drops text alpha in PDF export). |

## What you get

- Real, editable text boxes, shapes and pictures (SVG images are rasterised at 2×).
- `![bg]`, `![bg right]` and similar layouts; a full-page opaque image becomes the slide background.
- Gradients, borders, rounded corners and opacity.
- Speaker notes (also for decks where only some slides have notes), hyperlinks, inline code highlighting.

## Limits

- **Tables are not native PowerPoint tables.** Each cell is a rectangle plus a text box.
- `<video>`, `<audio>`, `<iframe>`, `<canvas>`, `<object>` and `<embed>` are not exported; a warning names the slide.
- Text in CSS pseudo-elements is not exported (the page number and list markers are); empty
  pseudo-elements that draw are exported when absolutely positioned.
- With exact line breaks, editing a line does not re-wrap the paragraph; use `--reflow` for decks
  that will be edited heavily in PowerPoint.

## Fidelity

Measured with [`tools/check_fidelity.py`](../tools/check_fidelity.py) (Windows with PowerPoint):
Marp renders each slide to PNG, PowerPoint renders the converted PPTX to PNG, and the score is
the mean pixel difference after a 1 px blur, in % of full scale (0 = identical; anti-aliasing and
PowerPoint's dithering of light fills do not count).

| Deck | Mean | Worst slide |
|---|---|---|
| `template.md` | 0.25 % | 0.45 % |
| `examples/00-full-showcase.md` (32 slides) | 0.37 % | 1.00 % |
| all eight examples | 0.18–0.65 % | ≤ 1.00 % |

Measured in Plex. Slides that look identical can still score up to about 1 % because
PowerPoint dithers light fills (table cells, tiles) when it exports PNG; `check_fidelity.py` fails
a slide above 1.25 %. Before the font, line-break and baseline work above, `template.md` scored
0.83 % (worst slide 1.55 %).

## Checking a change

```bash
python tools/check_examples.py              # lint, CSS sync, PPTX structure vs tests/baseline.json
python tools/check_examples.py --update     # accept an intended change
python tools/check_fidelity.py --keep out/  # visual comparison with the PDF (Windows + PowerPoint)
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `No Chrome/Edge found` | Install one or set `CHROME_PATH` |
| `npm ci` fails | Run `npm ci` in `pptx-export/dom` and read the error (proxy, registry) |
| `remote resource not loaded` warning | The deck uses an image or font from the web; the export loads local files only. Download it next to the deck and reference the local file |
| Chrome does not start on Linux | Chrome needs its sandbox: allow unprivileged user namespaces, or set `CHROME_NO_SANDBOX=1` (containers running as root get it automatically) |
| The PPTX shows another font than Plex | The Plex fonts are not installed on the machine that opens the PPTX: install the desktop fonts from the official Plex releases |
| A line overflows its box after editing | Export with `--reflow`, or widen the text box in PowerPoint |
| Something looks wrong only in the PPTX | Run with `--keep-html`, open the HTML in Chrome and compare |
