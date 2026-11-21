# Style guide

The design reference of the template: what each slide class and component looks like, and
which Carbon Design System token every value comes from. The implementation is
[`themes/carbon.css`](../themes/carbon.css); copy-paste snippets are in
[`components.md`](components.md).

The template is unofficial. Its values are taken from the open-source Carbon packages
(`@carbon/themes`, `@carbon/type`, `@carbon/colors`, `@carbon/layout`, `@carbon/pictograms`),
from [`@carbon/element-styles`](https://github.com/carbon-design-system/carbon-element-styles)
and from the guidance on [carbondesignsystem.com](https://carbondesignsystem.com/).

## Contents

1. [Principles](#1-principles)
2. [Themes](#2-themes)
3. [Colour tokens](#3-colour-tokens)
4. [Typography](#4-typography)
5. [Spacing, grid and shape](#5-spacing-grid-and-shape)
6. [Slide classes](#6-slide-classes)
7. [Markdown elements](#7-markdown-elements)
8. [Components](#8-components)
9. [Pictograms](#9-pictograms)
10. [Accessibility](#10-accessibility)
11. [Divergences from Carbon](#11-divergences-from-carbon)
12. [Changing the theme](#12-changing-the-theme)

---

## 1. Principles

- **Tokens, not hex values.** Every colour, size and space maps to a Carbon token; the CSS
  comments name it.
- **Neutral text.** Running text, headings and bold text use the text tokens. Colour is for
  links, a few brand accents, category coding and status — never decoration.
- **Light weight only for large type.** Plex Light (300) from 42 px up, Regular (400)
  below, SemiBold (600) for short labels and bold text.
- **Square and flat.** No rounded corners except tags, no shadows, no gradients.
- **One idea per slide**, title written as the takeaway, in sentence case.

## 2. Themes

Carbon defines two light themes (White, Gray 10) and two dark themes (Gray 90, Gray 100).
Each slide class uses one of them:

| Theme | Background | Slide classes |
|---|---|---|
| White | `#ffffff` | content slides, `toc`, `ruled`, `bk`, `lead plain` |
| Gray 10 | `#f4f4f4` | `lead` |
| Gray 90 | `#262626` | `backup` |
| Gray 100 | `#161616` | `lead dark`, `section`, `end` |

On dark slides the text tokens switch to their Gray 100 values: text-primary `#f4f4f4`,
text-secondary `#c6c6c6`, link-primary `#78a9ff`.

## 3. Colour tokens

Defined as custom properties in `:root` of the theme.

### Theme tokens (White theme)

| Custom property | Value | Carbon token | Used for |
|---|---|---|---|
| `--cds-background` | `#ffffff` | background | slide background |
| `--cds-layer-01` | `#f4f4f4` | layer-01 | cards, steps, code, table cells, `lead` background |
| `--cds-layer-accent-01` | `#e0e0e0` | layer-accent-01 | table header |
| `--cds-border-subtle-00` | `#e0e0e0` | border-subtle-00 | `hr`, contents rows |
| `--cds-border-subtle-01` | `#c6c6c6` | border-subtle-01 | table rows (on a layer) |
| `--cds-border-strong-01` | `#8d8d8d` | border-strong-01 | outlined flow nodes, `bk` top edge |
| `--cds-text-primary` | `#161616` | text-primary | all text, headings |
| `--cds-text-secondary` | `#525252` | text-secondary | subtitles, labels, footnotes, table cells |
| `--cds-text-on-color` | `#ffffff` | text-on-color | text on filled boxes |
| `--cds-icon-secondary` | `#525252` | icon-secondary | flow arrows |
| `--cds-link-primary` | `#0f62fe` | link-primary | links, contents numbers |
| `--cds-background-brand` | `#0f62fe` | background-brand | `ruled` edge, `.hero` fills |
| `--cds-background-inverse` | `#393939` | background-inverse | `.node.dark` |

### Dark theme values

| Custom property | Value | Carbon token |
|---|---|---|
| `--cds-g100-background` | `#161616` | background (Gray 100) |
| `--cds-g90-background` | `#262626` | background (Gray 90) |
| `--cds-dark-text-primary` | `#f4f4f4` | text-primary |
| `--cds-dark-text-secondary` | `#c6c6c6` | text-secondary |
| `--cds-dark-link-primary` | `#78a9ff` | link-primary |
| `--cds-dark-border-subtle` | `#525252` | border-subtle-01 (Gray 100) |

### Category accents

Cards, flow nodes and process steps code categories with a stroke and a tint of the same hue.
The strokes are Blue 60 (default) plus the first four colours of the Carbon categorical
data visualisation palette, which is ordered for maximum contrast between neighbours; the
tints are the 10 grade of each hue.

| Modifier | Stroke | Tint | Carbon colour |
|---|---|---|---|
| *(default)* / `.blue` | `#0f62fe` | `#edf5ff` | Blue 60 / Blue 10 |
| `.purple` | `#6929c4` | `#f6f2ff` | Purple 70 (categorical 01) / Purple 10 |
| `.cyan` | `#1192e8` | `#e5f6ff` | Cyan 50 (categorical 02) / Cyan 10 |
| `.teal` | `#005d5d` | `#d9fbfb` | Teal 70 (categorical 03) / Teal 10 |
| `.magenta` | `#9f1853` | `#fff0f7` | Magenta 70 (categorical 04) / Magenta 10 |

Strokes are graphics, never text colours. Use the same modifier for the same category
throughout a deck, and different modifiers for adjacent boxes.

### Status

| Variant | Background | Left border | Carbon tokens |
|---|---|---|---|
| `.band` (info) | `#edf5ff` | `#0043ce` | notification-background-info / support-info |
| `.band.warn` | `#fcf4d6` | `#f1c21b` | notification-background-warning / support-warning |
| `.band.success` | `#defbe6` | `#24a148` | notification-background-success / support-success |
| `.band.error` | `#fff1f1` | `#da1e28` | notification-background-error / support-error |

### Tags

| Modifier | Background | Text | Carbon tokens |
|---|---|---|---|
| *(default)* | `#d0e2ff` | `#0043ce` | tag-background-blue / tag-color-blue |
| `.cyan` | `#bae6ff` | `#00539a` | tag-*-cyan |
| `.teal` | `#9ef0f0` | `#005d5d` | tag-*-teal |
| `.purple` | `#e8daff` | `#6929c4` | tag-*-purple |
| `.magenta` | `#ffd6e8` | `#9f1853` | tag-*-magenta |
| `.green` | `#a7f0ba` | `#0e6027` | tag-*-green |
| `.red` | `#ffd7d9` | `#a2191f` | tag-*-red |
| `.gray` | `#e0e0e0` | `#161616` | tag-*-gray |

## 4. Typography

### Typefaces

| Role | Family | Carbon |
|---|---|---|
| Everything | `'Plex Sans', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif` | sans |
| Pull quotes | `'Plex Serif', Georgia, Times, serif` | serif (quotation styles) |
| Code | `'Plex Mono', Menlo, 'DejaVu Sans Mono', Consolas, Courier, monospace` | mono |

Plex is free under the SIL Open Font License. The faces the theme uses are bundled, unmodified,
in [`assets/fonts/`](../assets/fonts/) and declared with `@font-face` as Plex Sans, Plex Serif and
Plex Mono, so the PDF is always set in Plex. The PPTX names the installed Plex families, including
their Light and SemiBold faces: install the desktop fonts on the machines that open it.

### Type styles

Font sizes come from the Carbon type scale (12 · 14 · 16 · 20 · 24 · 28 · 32 · 42 · 54 px used
here). Letter spacing follows the type tokens: 0.32 px at 12 px (label-01) and in code blocks
(code-02), 0.16 px at 14 px (body-01, body-compact-01, heading-compact-01), 0 from 16 px up.

| Element | Size / line height | Weight | Colour | Carbon style |
|---|---|---|---|---|
| Cover, divider, closing title (`h1`) | 54 / 64 | Light 300 | text-primary | heading-07 |
| `h1` on other slides | 42 / 50 | Light 300 | text-primary | heading-06 |
| `h2` slide title | 32 / 40 | Regular 400 | text-primary | heading-05 |
| Cover, divider, closing subtitle (`h2`) | 28 / 36 | Regular 400 | text-secondary | heading-04 |
| `h3` | 28 / 36 (20 / 28 on `compact` slides) | Regular 400 | text-primary | heading-04 (heading-03) |
| `h4` | 20 / 28 | Regular 400 | text-primary | heading-03 |
| Body text | 20 / 28 | Regular 400 | text-primary | heading-03 metrics, Regular |
| Card, band, table, KPI label, tag | 16 / 22–24 | Regular 400 | as listed | body-02, body-compact-02 |
| Compact card, node detail, step text, footnote | 14 / 18–20, +0.16 px | Regular 400 | text-secondary for details | body-01, body-compact-01 |
| Footer, page number | 12 / 16, +0.32 px | Regular 400 | text-secondary | label-01 |
| KPI number | 54 / 64 | Light 300 | text-primary | heading-07 |
| Step number | 28 / 36 | Light 300 | text-primary | heading-04 size |
| Pull quote | 24 / 32 | Regular 400, serif | text-primary | quotation-01 at the lg breakpoint |
| `quote` slide | 42 / 50 | Regular 400, serif | text-primary | quotation-02 at the lg breakpoint (Regular: the Light serif is not bundled) |
| `statement` number | 120, leading 1 | Light 300 | text-primary | display-04 size |
| `statement` claim | 42 / 50 | Light 300 | text-primary | heading-06 |
| Breadcrumb (`header`) | 12 / 16, +0.32 px | Regular 400 | text-secondary | label-01 |
| Code block | 14 / 20, +0.32 px | Regular 400, mono | text-primary | code-02 |

**Bold** (`**text**`) is SemiBold 600 in the surrounding colour. *Italic* is reserved for
emphasis of titles of works, terms and captions, as in the Carbon typography guidance.

## 5. Spacing, grid and shape

| Aspect | Value | Carbon |
|---|---|---|
| Spacing scale | 2 · 4 · 8 · 12 · 16 · 24 · 32 · 40 · 48 · 64 px | spacing-01 … spacing-10 |
| Slide padding | 48 px top/bottom, 64 px left/right (cover and closing: 64 px top) | spacing-09, spacing-10 |
| `.cols` gutter | 32 px | 2x grid, wide gutter |
| `.cols3` gutter | 16 px | 2x grid, narrow gutter |
| Card and cell padding | 16 px horizontal | spacing-05 |
| Title width on cover, divider, closing | 75 % (12 of 16 columns) | 2x grid |
| Corners | 0; tags fully rounded | Carbon components |
| Elevation | none (no shadows) | |

Slides are 1280 × 720 px (16:9).

## 6. Slide classes

Set with `<!-- _class: name -->` at the top of the slide. Add `<!-- _paginate: false -->` to
`lead`, `toc`, `section`, `end` and `backup`; their footer is hidden automatically.

### `lead` — cover (Gray 10) · `lead plain` (White) · `lead dark` (Gray 100)

```
┌──────────────────────────────────────────────────────────┐
│ Presentation title                 54/64 Light, ≤ 75 %   │
│ Subtitle                           28/36 text-secondary  │
│                                                          │
│                                                          │
│ Name                               16/24 SemiBold        │
│ Role                               16/24                 │
│ contact                            16/24 text-secondary  │
└──────────────────────────────────────────────────────────┘
```

The author block (`.lead-author`) is pushed to the bottom edge.

### `toc` — contents (White)

Title 42/50 Light; items as a structured list: number in text-secondary, title in
text-primary, 20/28, 16 px vertical padding, 1 px border-subtle under each row. Items fill
column by column, three rows per column by default; for more than six items set
`style="grid-template-rows: repeat(N, auto)"` on `.toc-grid`.

`.toc-item.current` marks the section that starts when the contents slide is repeated before
each section, after the selected item of the Carbon side nav: layer-accent-01 fill, 3 px
Blue 60 left edge, SemiBold title; the other titles turn text-secondary and every item gets
16 px of left padding.

### `statement` — one number or one sentence (White) · `statement dark` (Gray 100)

Vertically centred. `#` is the number at 120 px Light (display-04 size), `##` the claim at
42/50 Light (heading-06), at most 75 % wide, `.small` the source 32 px below. A sentence alone
is written as `##` only. On `statement dark` text, footer and page number use the Gray 100
theme colours.

### `quote` — a quotation on a whole slide (White)

Vertically centred blockquote in Plex Serif 42/50 (quotation-02), at most 80 % wide; the
paragraph after it is the attribution, 20/28 text-secondary, 32 px below.

### `section` — divider (Gray 100) · `backup` — backup opener (Gray 90)

Vertically centred title 54/64 Light and subtitle 28/36 text-secondary. Paragraphs and `.small`
use text-secondary. Pictograms need the `white` class.

### Content slides (White) · `ruled` · `bk`

Content is anchored to the top so titles sit at the same height on every slide.
`ruled` adds an 8 px Blue 60 left edge. `bk` (backup content) adds a 4 px border-strong top
edge to mark appendix material.

### `end` — closing (Gray 100)

Same layout as the cover on Gray 100: a short closing line (`# Thank you` or its equivalent in
the deck's language), an optional subtitle and the `.lead-author` contact block. The closing
slide carries no logo or mark.

### `compact` — space-saving sizes (any slide)

Adds to any other class (`<!-- _class: compact -->`, `<!-- _class: bk compact -->`). On that
slide only, `h3` goes from 28/36 to 20/28 (heading-04 → heading-03) and table rows from 48 px
to 40 px (Carbon data table size lg → md). Use it for dense slides (three columns of cards
with long titles, tables of 8–10 rows) after shortening the text, before splitting the slide.
The PPTX export warns when content runs past the bottom margin, which is when `compact` or a
split is needed.

### Breadcrumb — the `header` directive

`<!-- header: Deck / 02 Section -->` writes a line at the top left (64 px from the left,
20 px from the top), label-01 12/16 text-secondary, like the footer. Hidden on `lead`, `toc`,
`section`, `backup` and `end`. Carbon's breadcrumb separates levels with `/`; on a slide the
levels are plain text, not links.

### Recommended order

`lead` → `toc` → content (with `section` dividers between major topics) → `end` →
optional `backup` → `bk` slides.

## 7. Markdown elements

Plain Markdown is styled after `@carbon/element-styles`:

| Element | Style |
|---|---|
| Unordered list | "–" marker, "▪" when nested, 8 px between marker and text |
| Ordered list | decimal, nested lower-alpha |
| Table | full width; header layer-accent-01, SemiBold, text-primary; cells layer-01, text-secondary; 1 px border-subtle-01 under each row; rows 48 px high (Carbon data table size lg, padding 12 × 16 px), 40 px on `compact` slides (size md, 8 × 16 px); left aligned |
| Blockquote | Plex Serif 24/32, indented 40 px, at most 50 characters wide, no rule or fill. Write the quotation marks in the text; put the attribution on the next line (e.g. `**— Name, role**`) |
| Inline code | Plex Mono at 0.875 em on layer-01 |
| Code block | 14/20 on layer-01, 16 px padding |
| Horizontal rule | 1 px border-subtle-00 |
| Link | link-primary, underlined |
| `<mark>` | Yellow 20 `#fddc69` background |

## 8. Components

### Columns — `.cols`, `.cols3`

Equal columns with 32 px (`.cols`) or 16 px (`.cols3`) gutters. Wrap each column in a `<div>`.

### Card — `.card`

A Carbon tile: layer-01 background, 16 px padding, square corners, 16/24 text, `h3` title
28/36 (20/28 on `compact` slides). A 4 px top stroke codes the category: Blue 60 by default, `.purple` `.cyan` `.teal`
`.magenta` for the others. `.sm` is the compact variant (14/20 text, 16/24 SemiBold title,
12 × 16 px padding) for three-column grids.

### KPI — `.kpi` + `.kpi-label`

Number 54/64 Light in text-primary; label 16/24 text-secondary below. Keep numbers short
(about 8 characters). Up to three pairs per column.

### Bar chart — `.bars` › `.bar`

A single-series bar chart after the Carbon simple bar chart, built from boxes and text so
the PPTX keeps native rectangles and editable text instead of a picture. Horizontal by
default: label column 160 px, 16/22 text-secondary; 24 px bars, 12 px apart; value 16/22
SemiBold text-primary, 8 px after the end of the bar. `.vertical`: columns half as wide as
their slot, up to 280 px high, over a 1 px border-strong baseline; value above, label below.
The values are written on the bars, so there are no axes or gridlines. Fill Blue 60 by
default, or one hue of the categorical palette (`.purple` `.cyan` `.teal` `.magenta`) for
the whole chart; `.gray` (Gray 30) mutes the bars around the one the title is about.
The bar length (`--v`, 0–100) is computed by the author: the chart does not scale itself,
and editing a value in the PPTX does not resize its bar.

`.stacked` follows the Carbon stacked bar chart: one segment per category, coloured with the
categorical palette strictly in its order (Purple 70, Cyan 50, Teal 70, Magenta 70, Red 50),
separated by a 1 px divider in the background colour, total after (or above) the bar. Up to
five segments. `.legend` names them: 12 px squares, 8 px from the name, 24 px between items,
14/18 text-secondary, above the chart.

`.diverging` puts a 1 px text-primary zero line in the middle of the plot; `--v` runs from
-100 to 100 and bars grow left or right from the line. Negative bars carry `.neg` and use
Red 50, the categorical red at the far end of the Carbon red–cyan diverging palette; positive
bars keep the chart colour. Values (with their sign) sit in a 72 px right-aligned column.

`.grouped` follows the Carbon grouped bar chart: two to four series per category, same
palette order as the stacked chart. Horizontal: 16 px bars 4 px apart, 14/22 SemiBold value
after each bar. Vertical: columns up to 48 px wide, value above.

### Meter — `.meter`

After the Carbon meter chart: title heading-compact-02 16/22 SemiBold, value 16/22
text-secondary on the right, then a 16 px track in layer-accent-01 filled to `--v`. The
target of a bullet chart is a 2 px text-primary mark that overhangs the track by 4 px.
Status fills use the support tokens (`.success` Green 50, `.warn` Yellow 30, `.error` Red 60),
as Carbon meters do for statuses. `.proportional` splits the fill into categorical colours
with 1 px dividers, like the Carbon proportional meter.

### Roadmap — `.roadmap`, `.scale`, `.task`

After the Carbon floating bar chart, laid out as a Gantt timeline. Scale 14/18
text-secondary over a 1 px border-strong line, periods separated by 1 px border-subtle;
label column 200 px, 16/22 text-primary; rows at least 40 px with a 1 px border-subtle rule
(as table rows); 16 px bars from `--from` to `--to`.

### Tag — `.pill`

A Carbon tag: tag background and text tokens, fully rounded, 16/24, 4 × 12 px padding.
Use for statuses, targets and categories, not for sentences.

### Band — `.band`

A low-contrast Carbon inline notification: notification background, 3 px support-colour
left border, the 20 px status icon of `@carbon/icons` (information, warning, checkmark, error)
16 px from the outer edge, 16/24 text from 52 px, left aligned. `<b>` is the notification title.
Place it **last** on the slide to state the takeaway. The icon is drawn by the theme
(`::before`); the PPTX export reproduces it as a picture.

### Flow diagram — `.flow`, `.node`, `.arrow`

Boxes in a row with 8 px gaps, equal widths and heights.

| Node | Look |
|---|---|
| `.node` | white, 1 px border-strong |
| `.node.cyan` `.teal` `.purple` `.magenta` | tint fill, 1 px stroke of the same hue |
| `.node.hero` | Blue 60 fill, white text — highlight one node only |
| `.node.dark` | background-inverse fill, white text — highlight one node only |

Label (`<b>`) 16/22 SemiBold text-primary; detail (`<small>`) 14/18 text-secondary.
Arrows: the characters `▸` (or `⇄`) at 24 px in icon-secondary. Colour modifiers use the
category accents: `.blue` `.cyan` `.teal` `.purple` `.magenta` (`.obs` is an alias of
`.magenta`, for monitoring paths).

### Process — `.process`, `.step`

Contiguous tiles separated by 1 px, each with a 4 px category stroke on top. Number
(`.step-num`) 28/36 Light, title (`<b>`) 14/18 SemiBold, detail (`<small>`) 14/18
text-secondary. Variants `.blue` `.cyan` `.teal` `.purple` `.magenta` add the tint;
`.hero` (Blue 60 fill) highlights one step. Five or six steps at most.

### Progress indicator — `.progress`

After the Carbon progress indicator, horizontal: one step per `<div>`, 8 px apart, each with a
2 px line on top (Blue 60 up to the current step, border-subtle-01 after it, support-error on
an `.error` step) and a 20 px status icon 16 px below it: checkmark outline (`.done`), ring
with a filled dot (`.current`), empty ring (not started), the error icon (`.error`). Label 20/28
text-primary, SemiBold on the current step; detail (`<small>`) 14/18 text-secondary.

### Do / Don't — `.do`, `.dont`

After the do/don't examples of the Carbon guidelines: layer-01 box, 16 px padding, a 4 px
top stroke in support-success (`.do`) or support-error (`.dont`), the matching 20 px status
icon (checkmark filled, error filled) before the SemiBold title, body 16/24.

### Contents — `.toc-grid`, `.toc-item`

See [`toc`](#toc--contents-white).

### Author block — `.lead-author`

Three lines at 16/24: `<strong>` name (SemiBold), role, `<em>` contact in text-secondary.

### Footnote — `.small`

14/20 text-secondary. For sources, disclaimers and notes; place it after the main content.

## 9. Pictograms

Carbon pictograms from `@carbon/pictograms` (Apache-2.0), stored as colourless SVG and
coloured by a CSS filter.

| Class | Colour | Use on |
|---|---|---|
| `pictogram` | Gray 100 (icon-primary) | light slides — the default |
| `pictogram blue` | Blue 60 | light slides, as a brand accent |
| `pictogram white` | Gray 10 (icon-primary on dark) | dark slides: `lead dark`, `section`, `end`, `backup` |
| `pictogram black` | Gray 100 | alias of the default, kept for older decks |

Sizes on the 8 px grid: `sm` 48 px (the minimum Carbon recommends) · default 80 px · `lg` 120 px.
Glyphs are trimmed on the left so they align with the text below. Pictograms are decorative:
always `alt=""`. Use one colour per slide and never a dark pictogram on a dark background
(the linter checks this).

## 10. Accessibility

- On White, text-primary reaches 18.1:1 and text-secondary 7.8:1 (16.5:1 and 7.1:1 on
  Gray 10). On Gray 100, text-primary reaches 16.5:1 and text-secondary 10.6:1 (8.9:1 on
  Gray 90). All are above the WCAG AA 4.5:1 minimum for text.
- Category strokes are graphics: Cyan 50, the lightest, reaches 3.3:1 on white (the minimum
  for non-text elements is 3:1). Do not use them for text.
- Do not rely on colour alone: label categories and statuses in words.
- Keep body text at 14 px or more; 12 px is for the footer only.

## 11. Divergences from Carbon

Carbon is a design system for product interfaces and web pages; it has no presentation
layouts. Where the template departs from Carbon, or builds something Carbon does not define,
the reason is given here. Everything else follows the Carbon tokens and guidance cited above.

### Kept on purpose: Carbon values that do not work on slides

Each of these was compared with the strict Carbon version on rendered slides and in PowerPoint.

| Element | Carbon | Template | Why |
|---|---|---|---|
| Inline code size | Fixed code-01 / code-02 (12 / 14 px) | 0.875 em of the surrounding text (17.5 px in body text, 14 px in cards) | Carbon pairs 14 px code with 14–16 px UI text. Slide body text is 20 px: fixed 14 px code would be 30 % smaller than the words around it, and commands are often what the audience must read. |
| Tag size | md: 24 px high, label-01 12 px text | 32 px high (the lg height), 16 px text | 12 px is under 1 % of the slide width: a status such as "On track" cannot be read when projected or shared in a call, and reading it at a glance is the tag's job. |
| Flow arrows | Icons from `@carbon/icons` (`arrow--right`) | The characters `▸` and `⇄` | A character keeps the markup to one line, can take any colour from a class (`.arrow.cyan`…), and stays editable text in the PPTX. An icon needs an `<img>` per arrow and one file per colour, and becomes a picture in the PPTX. |
| Pictogram colour | Exact colour values | A CSS filter on colourless SVGs: Blue 60 renders as `#0060fe` instead of `#0f62fe` | The difference cannot be seen side by side. Exact colours need one copy of the 1,429 pictograms per colour, or SVG pasted into the Markdown. |
| Font fallbacks | `'Plex Sans', system-ui, -apple-system, BlinkMacSystemFont, '.SFNSText-Regular', sans-serif` (Carbon names the typeface by its full family name) | `'Plex Sans', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif` | Only matters when Plex cannot load. `system-ui` is a generic name PowerPoint cannot use: with the Carbon stack the PDF would fall back to Segoe UI and the PPTX to Arial. Named fallbacks keep PDF and PPTX in the same font. |
| Light weight from 42 px | Light (300) for the large headings | Also for the 28 px step numbers | Numbers in Light read as labels rather than headings and keep the step tiles quiet; the 28 px size matches heading-04. |

### Optional: the space-saving sizes

| Element | Carbon default here | `compact` slide class | Why it exists |
|---|---|---|---|
| `h3` | heading-04, 28/36 | heading-03, 20/28 | At 28 px, card titles in three columns wrap and the cards grow; a card title also gets close to the 32 px slide title. |
| Table rows | data table size lg, 48 px | size md, 40 px | Eight or more rows at 48 px run past the bottom of a 720 px slide. |

Both options are Carbon sizes; only the choice of size per slide is the template's.

### Compositions: built from Carbon tokens, not defined by Carbon

| Element | What Carbon has | Why the template adds it |
|---|---|---|
| Slide layouts (cover, contents, section divider, closing, backup) | Themes, type and grid, no slide layouts | A deck needs them. Each uses one Carbon theme (White, Gray 10, Gray 90, Gray 100) and the type scale. |
| Body text at 20/28 | Body styles at 14 and 16 px | Slides are read from a distance; 20/28 uses the size and leading of heading-03 in Regular weight. |
| Category stroke on cards and steps (4 px) | Tiles without strokes | Marks the category of a tile at a glance; the colours are the first entries of the Carbon categorical palette, which is designed for telling categories apart. |
| Category tints on flow nodes and steps | The 10 grade of each hue | Same coding as the strokes, as a fill. |
| Flow diagrams, process steps, KPIs | No equivalent components (the progress indicator, now `.progress`, is closest to the steps) | Common slide content; built from tiles, borders and type tokens. |
| Bar chart from boxes (`.bars`) | Carbon Charts, an SVG/JavaScript library | Marp decks allow no scripts or SVG markup, and a chart drawn with boxes stays native shapes and editable text in the PPTX. It follows the simple bar chart: one series, categorical colours, labelled values. |
| Chart sizes: 16 px meter track, 24 px bars, 16 px labels | Carbon Charts: thinner tracks and 12 px axis labels, values in tooltips | Slides are read from a distance and are not interactive, so values are written on the chart and text uses the body sizes of the deck. |
| Diverging bars (`.bars.diverging`) | Bar charts with negative values on a shared axis | Same box construction as `.bars`; the values replace the axis, and the zero line is the only rule. |
| `statement` and `quote` slides, breadcrumb in the header | Display and quotation type tokens; a breadcrumb component for page navigation | Slide layouts built from those tokens. |
| Current step and do/don't in SemiBold | Progress labels in Regular; do/don't captions under the example | On a slide the current step and the verdict must be found at a glance. |
| `.gray` bars and tasks (Gray 30) | No muted series colour in the palettes | Lets one bar or task carry the message; done work in a roadmap reads as finished. |
| `ruled` (8 px Blue 60 left edge) and `bk` (4 px Gray 50 top edge) | No such borders | Optional markers: emphasis for a slide, and appendix slides that must not be mistaken for the main talk. |
| Default pictogram colour Gray 100, sizes 80 and 120 px | Pictograms in a colour that contrasts with the background, 48 px minimum | Gray 100 keeps colour for meaning; the sizes stay on the 8 px grid. |
| Band icon position and spacing | Inline notification with an optional close button and actions | Slides are not interactive: no close button or actions; the icon and text positions follow the notification layout. |
| `.cols` / `.cols3` | 2x grid of 16 columns | Equal columns with the 2x grid gutters; slides are a fixed 1280 px, not a Carbon breakpoint. |

### Content rules

Takeaway titles, one idea per slide, five bullets per column, slides per minute of talk and a
band as the last element are presentation practice, not Carbon guidance. From Carbon come
sentence case, neutral text colour and the rule that colour carries meaning.

## 12. Changing the theme

1. Edit [`themes/carbon.css`](../themes/carbon.css), taking the value from a Carbon token and
   naming the token in a comment.
2. Run `python scripts/sync_css.py` to embed it into `template.md` and `examples/*.md`
   (new decks get it from `scripts/new_deck.py`).
3. Run `python tools/check_examples.py`, look at the renders, and accept intended converter
   changes with `--update`.
