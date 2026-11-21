# Pictogram library

1,429 pictograms from the open-source [`@carbon/pictograms`](https://www.npmjs.com/package/@carbon/pictograms)
package, version 12.88.0, licensed under **Apache-2.0** ([`LICENSE-CARBON`](LICENSE-CARBON)).
Browse them visually in the [Carbon pictogram library](https://carbondesignsystem.com/elements/pictograms/library/).

| Path | Content |
|---|---|
| `svg/<name>.svg` | one colourless SVG per pictogram; names are Carbon's (`cloud`, `cloud--analytics`) |
| `catalog.csv` | `name, friendly_name, categories, aliases` for every pictogram |
| `LICENSE-CARBON` | Apache-2.0 licence text of `@carbon/pictograms` |

**Left out:** deprecated pictograms, and pictograms that depict company products, brands,
third-party logos (Android, Docker, Java, Kubernetes, Linux, Python, Slack, Spring…), named
hardware or company sites. The list is [`tools/pictogram_exclude.txt`](../../tools/pictogram_exclude.txt);
aliases that name trademarked programmes are removed from the catalog as well.

## Find a pictogram

```bash
python scripts/pictograms.py search cloud security     # every word must match the name, label or an alias
python scripts/pictograms.py search --category Security
python scripts/pictograms.py categories
```

If a deck references a name that does not exist, `export_deck.py` stops and suggests the
closest names.

## Use it in a deck

Reference the file as `assets/pictograms/svg/<name>.svg` (`../assets/…` for decks in
`examples/`). `python scripts/export_deck.py deck.md` copies the pictograms a deck uses next to
it (`python scripts/pictograms.py sync deck.md` does only that), so the deck folder stays
self-contained.

```html
<img src="assets/pictograms/svg/cloud.svg" class="pictogram" alt="">          <!-- light slide: Gray 100 -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram blue" alt="">     <!-- light slide: Blue 60 accent -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram white" alt="">    <!-- dark slide -->
```

| Class | Colour | Use on |
|---|---|---|
| `pictogram` | Gray 100 `#161616` (icon-primary) | light slides (default) |
| `pictogram blue` | Blue 60 `#0f62fe` | light slides, as an accent |
| `pictogram white` | Gray 10 `#f4f4f4` (icon-primary on dark themes) | dark slides: `lead dark`, `section`, `end`, `backup` |
| `pictogram black` | Gray 100 | alias of the default, kept for older decks |

Carbon asks for pictograms that contrast with their background: never a dark pictogram on a
dark slide or a light one on a light slide. `scripts/lint_deck.py` flags both cases.

Sizes on the 8 px grid: `pictogram sm` 48 px (the minimum Carbon recommends) ·
`pictogram` 80 px · `pictogram lg` 120 px. Pictograms are decorative: always `alt=""`.

Inside a card or column, keep the empty lines so the Markdown after the image renders:

```html
<div class="card">

<img src="assets/pictograms/svg/cloud.svg" class="pictogram" alt="">

### Cloud
Short description.

</div>
```

## Technical notes

- Carbon pictograms sit in a 32 × 32 viewBox with a different amount of empty space on the
  left. `build_pictograms.py` wraps each glyph in `<g data-left-trim="X" transform="translate(-X 0)">`
  so that every pictogram starts at the text margin (`object-position: left center` in the CSS).
- The SVGs have no `fill`; the colour comes from a CSS filter.
- The PPTX export rasterises each SVG to a PNG in the rendered colour.

## Regenerate (maintainers)

```bash
python tools/build_pictograms.py              # downloads the pinned version with npm
python tools/build_pictograms.py --package DIR   # or use an extracted package
```

Requires `pip install pyyaml pymupdf` (maintainers only). To upgrade, change `CARBON_VERSION` in the script, run it, update
the version in this file, in `NOTICE` and in the README, and review the new names against the
exclusion list.

Attribution: pictograms © the Carbon Design System contributors, Apache License 2.0.
