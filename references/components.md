# Component snippets

Copy-paste snippets for every slide class and component of the theme.
Design rules and Carbon tokens: [`style-guide.md`](style-guide.md) ·
rendered examples: [`examples/`](../examples/).

Image paths below are relative to a deck created with `scripts/new_deck.py`
(`assets/…`). Decks inside `examples/` use `../assets/…`.

## Two rules that prevent most broken slides

1. **Empty line after an opening `<div …>`** before any Markdown (`### title`, `- item`,
   `**bold**`), and before the closing `</div>`. Without it Marp prints the Markdown literally.
2. **One component per line** for `.node`, `.step`, `.kpi`, `.kpi-label` and `.toc-item`,
   with the tags in the order shown here.

`python scripts/lint_deck.py deck.md` (run by `export_deck.py`) checks both.

---

## Slide classes

```markdown
<!-- _class: lead -->        cover, Gray 10
<!-- _class: lead plain -->  cover, White
<!-- _class: lead dark -->   cover, Gray 100
<!-- _class: toc -->         contents
<!-- _class: section -->     section divider, Gray 100
<!-- _class: ruled -->       content slide with a Blue 60 left edge
<!-- _class: end -->         closing slide, Gray 100
<!-- _class: backup -->      backup opener, Gray 90
<!-- _class: bk -->          backup content slide
<!-- _class: compact -->     space-saving sizes on a dense slide (combines: bk compact)
<!-- _class: statement -->   one big number or one sentence, White
<!-- _class: statement dark --> the same on Gray 100
<!-- _class: quote -->       one quotation on the whole slide
```

Add `<!-- _paginate: false -->` to `lead`, `toc`, `section`, `end` and `backup`.
The footer and the header (breadcrumb) are hidden on those slides automatically.

### Cover

```markdown
<!-- _class: lead -->
<!-- _paginate: false -->

# Presentation title
## Subtitle — topic or theme

<div class="lead-author">
<strong>First Last</strong>
Role
<em>first.last@example.com</em>
</div>
```

### Contents

```html
<!-- _class: toc -->
<!-- _paginate: false -->

# Contents

<div class="toc-grid">
  <div class="toc-item"><span class="toc-num">01</span><span class="toc-title">First topic</span></div>
  <div class="toc-item"><span class="toc-num">02</span><span class="toc-title">Second topic</span></div>
  <div class="toc-item"><span class="toc-num">03</span><span class="toc-title">Third topic</span></div>
</div>
```

Items fill column by column, three rows per column (6 items = 3 + 3). For 7–8 items:
`<div class="toc-grid" style="grid-template-rows: repeat(4, auto)">` (rows = items ÷ 2,
rounded up). The PDF and the PPTX use the same value.

### Contents with the current section

In a deck with four or more sections, repeat the contents slide before each section instead
of a section divider and add `current` to the section that starts. It gets a grey fill, a
Blue 60 left edge and SemiBold text; the other items turn grey. One `current` per slide.

```html
<div class="toc-item current"><span class="toc-num">02</span><span class="toc-title">Results so far</span></div>
```

### Breadcrumb (header)

Marp's `header` directive puts a line at the top left of every slide after it, in the 12 px
footer style. Set it on the first slide of each section, with the levels separated by ` / `:

```markdown
<!-- header: Migration update / 02 Results so far -->
```

It stays until the next `header` directive (`<!-- header: "" -->` clears it) and is hidden
on `lead`, `toc`, `section`, `backup` and `end`. Use it in long decks only (about 20 slides
or more), and keep it short: it must not reach the title.

### Section divider

```markdown
<!-- _class: section -->
<!-- _paginate: false -->

# Section 01
## Section name
```

### Closing slide

```markdown
<!-- _class: end -->
<!-- _paginate: false -->

# Thank you
## Questions and discussion

<div class="lead-author">
<strong>First Last</strong>
Role
<em>first.last@example.com</em>
</div>
```

### Backup

```markdown
<!-- _class: backup -->
<!-- _paginate: false -->

# Backup
## Supporting material

<span class="small">Topic A · Topic B · Topic C</span>

---

<!-- _class: bk -->

## Backup · The figures behind the cost estimate
```

### Dense slide: `compact`

```markdown
<!-- _class: compact -->

## Release readiness by service

| Service | Owner | Tests | Status |
|---|---|---|---|
| Identity | Platform team | 1,240 | Ready |
```

On a `compact` slide `h3` is 20 px instead of 28 px and table rows are 40 px instead of 48 px
(both Carbon sizes). Use it when a slide is still too full after shortening the text; if the
export still reports content past the bottom margin, split the slide.

### Statement: one number or one sentence

```markdown
<!-- _class: statement -->

# 3.2×

## faster from merge to production since the move to the new pipeline

<p class="small">Median lead time, April – September 2025 · source: CI data</p>
```

`#` is the number (120 px Light), `##` the claim (42 px Light, three lines at most), `.small`
the source. For a sentence alone, write only the `##`. `statement dark` puts it on Gray 100.
At most one or two per deck: the slide works because it is rare.

### Quote

```markdown
<!-- _class: quote -->

> “The new close process saved us two days at every month end.”

— Head of finance, pilot customer
```

The quotation in Plex Serif 42 px, the attribution under it in grey. Write the typographic
quotes (“ ”) yourself, keep the quotation under about 25 words, and quote only what the
person really said: mark a paraphrase as such in the attribution.

---

## Layout

### Two columns

```html
<div class="cols">
<div>

**Left column**
- Point one
- Point two

</div>
<div>

**Right column**
- Point three
- Point four

</div>
</div>
```

### Three columns

```html
<div class="cols3">
<div>

### First
Short text.

</div>
<div>

### Second
Short text.

</div>
<div>

### Third
Short text.

</div>
</div>
```

---

## Components

### Card

```html
<div class="card cyan">

### Card title
Body text — at most three lines, **bold** for key terms.

</div>
```

Accent: *(none)* Blue 60 · `cyan` · `teal` · `purple` · `magenta`. Compact: add `sm`
(e.g. `class="card teal sm"`), for six cards in a `.cols3` grid.
For a 2 × 2 grid put four cards in one `.cols` block.

### KPI

```html
<div class="kpi">94%</div>
<div class="kpi-label">customer satisfaction — <strong>2024</strong></div>
```

### Bar chart

One series, one `.bar` per line, values written on the bars (no axes). `--v` is the bar
length from 0 to 100: **value ÷ largest value × 100, rounded**, so the largest bar is 100.
The empty `<span></span>` draws the bar; `<small>` is the value as the audience reads it.

```html
<div class="bars">
<div class="bar" style="--v: 100"><b>Europe</b><span></span><small>412</small></div>
<div class="bar" style="--v: 62"><b>North America</b><span></span><small>256</small></div>
<div class="bar" style="--v: 35"><b>Asia Pacific</b><span></span><small>144</small></div>
</div>

<p class="small">New customers by region, 2024 · source: …</p>
```

Vertical columns, for a time series (labels at most two lines, up to about 8 columns):

```html
<div class="bars vertical">
<div class="bar" style="--v: 100"><b>Q1</b><span></span><small>1,840</small></div>
<div class="bar" style="--v: 71"><b>Q2</b><span></span><small>1,300</small></div>
</div>
```

Colour: *(none)* Blue 60 · `purple` · `cyan` · `teal` · `magenta`, on `.bars` for the whole
chart or on one `.bar`; `gray` mutes the bars that are not the point
(`<div class="bar gray" …>` next to one `<div class="bar magenta" …>`). Long labels: widen
the label column with `<div class="bars" style="--label: 240px">` (default 160px).
Sort horizontal bars by value unless the categories have a natural order; up to about 8 bars.
Always add a `.small` line with what is measured and the source.

### Stacked bar chart

Parts of a whole per category: one `<span style="--v: N">` per segment, with a `.legend`
above the chart that names the segments in the same order. Each `--v` is **segment value ÷
largest bar total × 100, rounded**, so the longest bar totals 100; for a percentage chart
every bar totals 100 and `<small>` (the total) can be left out. Every bar has the same
segments in the same order (`--v: 0` for an empty one); at most five segments.

```html
<div class="legend"><span><i></i>Compute</span><span><i></i>Storage</span><span><i></i>Network</span></div>

<div class="bars stacked">
<div class="bar"><b>Q1</b><span style="--v: 42"></span><span style="--v: 21"></span><span style="--v: 7"></span><small>€ 200k</small></div>
<div class="bar"><b>Q4</b><span style="--v: 61"></span><span style="--v: 28"></span><span style="--v: 11"></span><small>€ 285k</small></div>
</div>

<p class="small">Quarterly cloud spend by service · source: …</p>
```

Vertical columns: `<div class="bars vertical stacked">`; the first segment sits on the
baseline. The colours are fixed: the Carbon categorical palette in order (Purple 70, Cyan 50,
Teal 70, Magenta 70, Red 50); colour modifiers and `gray` do not apply to stacked charts.

### Grouped bar chart

Two to four series side by side per category (e.g. 2023 vs 2024), with a `.legend`. One span
per series with its value inside; the **largest single bar** is `--v: 100`. Same series in
the same order in every bar; same palette as the stacked chart.

```html
<div class="legend"><span><i></i>2023</span><span><i></i>2024</span></div>

<div class="bars grouped">
<div class="bar"><b>Europe</b><span style="--v: 92"><small>380</small></span><span style="--v: 100"><small>412</small></span></div>
<div class="bar"><b>North America</b><span style="--v: 46"><small>190</small></span><span style="--v: 62"><small>256</small></span></div>
</div>
```

Vertical columns per period: `<div class="bars vertical grouped">`, up to about 5 periods
with 3 series.

### Diverging bar chart

Gains and losses around a zero line in the middle (change vs last year, variance to plan).
`--v` goes from -100 to 100: the **largest change, of either sign, is 100 or -100**, the others
are change / largest change × 100. Negative bars also take `neg` (Red 50). The values sit in
a column on the right.

```html
<div class="bars diverging">
<div class="bar" style="--v: 100"><b>Europe</b><span></span><small>+14%</small></div>
<div class="bar" style="--v: 57"><b>Asia Pacific</b><span></span><small>+8%</small></div>
<div class="bar neg" style="--v: -50"><b>Americas</b><span></span><small>−7%</small></div>
</div>
```

Sort the bars from the largest gain to the largest loss. Write the sign in every value
(+14%, −7%). Horizontal only.

### Meter and target (bullet)

One measure against its full scale: title, value text, and a track filled to `--v` (0–100).
Add `--t` and `<u></u>` for a target mark. Colour: *(none)* Blue 60 · `purple` · `cyan` ·
`teal` · `magenta`, or status `success` · `warn` · `error` when the meter shows a status.

```html
<div class="meter" style="--v: 72"><b>Budget used</b><small>€ 720k of € 1 M · 72%</small><span><span></span></span></div>
<div class="meter error" style="--v: 64; --t: 85"><b>Billing</b><small>64 · target 85</small><span><span></span><u></u></span></div>
```

Say in the `.small` line under the meters what the mark means.

### Proportional meter

Parts of a capacity in one track (the grey rest is unused), with a `.legend`. Each part's
`--v` is part ÷ capacity × 100; the parts take the categorical palette in order.

```html
<div class="legend"><span><i></i>Logs</span><span><i></i>Backups</span></div>

<div class="meter proportional"><b>Storage used</b><small>96 TB of 200 TB · 48%</small><span><span style="--v: 31"></span><span style="--v: 17"></span></span></div>
```

### Roadmap (floating bars)

A timeline: `.scale` names equal periods, each `.task` is a bar from `--from` to `--to`,
both 0–100 of the whole timeline (one quarter of a year = 25, one month ≈ 8.33). Use one colour
per workstream (`purple` `cyan` `teal` `magenta`) and `gray` for work that is done; up to
about 8 tasks. Widen the label column with `style="--label: 260px"` on `.roadmap`.

```html
<div class="roadmap">
<div class="scale"><span>Q1 2025</span><span>Q2 2025</span><span>Q3 2025</span><span>Q4 2025</span></div>
<div class="task gray" style="--from: 0; --to: 15"><b>Discovery</b><span></span></div>
<div class="task" style="--from: 10; --to: 55"><b>Platform build</b><span></span></div>
<div class="task teal" style="--from: 65; --to: 100"><b>Migration</b><span></span></div>
</div>
```

### Custom chart (`.plot`)

For the chart the message needs when no component above draws it: lines, areas, scatter,
dumbbells, lollipops, slopes, ranges, annotated series. Pick the chart first (SKILL.md,
*Custom charts*), then build it here; follow the rules in the style guide, *Custom charts*.

Everything is placed in the plot area at `--x` (0 = left, 100 = right) and `--y` (0 =
bottom, 100 = top). Map your data yourself: **(value − axis minimum) ÷ (axis maximum −
axis minimum) × 100**, rounded to two decimals. Choose round axis limits (0–500, not
0–463) and four to six gridlines.

| Element | Draws | Variables |
|---|---|---|
| `<div class="y" style="--y: N">label</div>` | gridline + y-axis label; add `zero` to the baseline | `--y` |
| `<span class="x" style="--x: N">label</span>` | x-axis label under the plot | `--x` |
| `<img class="layer" src="charts/….svg" alt="">` | lines, areas, curves: the SVG layer | — |
| `<span class="dot" style="--x: N; --y: N"></span>` | 8 px point; `lg` = 14 px for scatter and dumbbells | `--x` `--y` |
| `<span class="range" style="--x: A; --x2: B; --y: N"></span>` | horizontal segment (dumbbell, range); `vertical` with `--y` `--y2` (lollipop stem) | `--t` thickness, 2px |
| `<span class="zone" style="--x: A; --x2: B"></span>` | Gray 10 area: a forecast, a period, a target band (`--y` `--y2` to limit it) | — |
| `<span class="note" style="--x: N; --y: N">text</span>` | label right of the point; `left`, `above`, `above left`, `above right`: place it on the side the lines do not cross | — |

Colours on `.dot`, `.range` and `.note`: *(none)* Blue 60 for one series; `purple` `cyan`
`teal` `magenta` `red` in this order for several series; `gray` for context. On `.plot`:
`--h` plot height (default 320px), `--axis` width of the y-label column (default 56px,
160px or more for category names), `--end` right gutter for labels at the end of the lines.
Order inside `.plot`: zones, gridlines, x labels, the layer, ranges, dots, notes (later
elements are drawn on top).

Line chart, labelled at the end of each line (no legend):

```html
<div class="plot" style="--h: 340px; --end: 150px">
<div class="y zero" style="--y: 0">0</div>
<div class="y" style="--y: 50">250</div>
<div class="y" style="--y: 100">500</div>
<span class="x" style="--x: 0">2019</span>
<span class="x" style="--x: 50">2022</span>
<span class="x" style="--x: 100">2025</span>
<img class="layer" src="charts/accounts.svg" alt="">
<span class="dot purple" style="--x: 100; --y: 90"></span>
<span class="note purple" style="--x: 100; --y: 90">Enterprise 450</span>
</div>

<p class="small">Active accounts by plan, thousands · source: …</p>
```

**The SVG layer** (`charts/accounts.svg`, next to the deck) holds only shapes, in the same
0–100 space with y pointing down, so a point at `--x: 50; --y: 62` is `50,38`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
<polyline points="0,80 16.67,72 33.33,65 50,53 66.67,42 83.33,28 100,10" fill="none"
  stroke="#6929c4" stroke-width="2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
</svg>
```

Keep `viewBox="0 0 100 100"`, `preserveAspectRatio="none"` and
`vector-effect="non-scaling-stroke"` on every stroke (the layer is stretched to the plot,
strokes stay 2px). Areas: a `<polygon>` closed along `y = 100` with `fill-opacity="0.2"`
under the line. Forecasts: `stroke-dasharray="6 4"`. **No `<text>` in the SVG**: put every
label in a `.note` or an axis label, so it uses IBM Plex and stays editable in the PPTX.
Draw circles as `.dot`, not in the SVG (the stretch would make them ellipses). The layer
becomes one picture in the PPTX.

Scatter (one highlighted point, the others `gray`), dumbbell and slope: see
`examples/11-custom-charts.md`. A dumbbell puts the category names in `.y` labels with
`--axis: 160px`, one row per `--y` (10, 30, 50 …), a `range` from the lower to the higher
value and two `dot lg` at its ends; a slope chart uses `--axis` and `--end` as label gutters,
two x labels, one line per item in the layer and `.note left` / `.note` at both ends.

### Donut

Parts of a whole, at most five, with the main share in the middle. The ring is an SVG file;
the text and the legend are HTML.

```html
<div class="donut" style="--size: 300px"><img src="charts/renewals.svg" alt=""><b>62%</b><small>renewed</small></div>
```

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 42">
<circle cx="21" cy="21" r="15.9155" fill="none" stroke="#6929c4" stroke-width="6"
  stroke-dasharray="61.6 38.4" stroke-dashoffset="25"/>
<circle cx="21" cy="21" r="15.9155" fill="none" stroke="#1192e8" stroke-width="6"
  stroke-dasharray="23.6 76.4" stroke-dashoffset="-37"/>
</svg>
```

The circumference is 100, so each part is its percentage: `stroke-dasharray="P−0.4 100−P+0.4"`
(the 0.4 leaves a white gap), `stroke-dashoffset` = 25 − the sum of the parts before it
(25 starts at twelve o'clock). Colours in the categorical order, matched by a
`<div class="legend vertical">` with one `<span><i></i>Name · 62%</span>` per part.

### Heatmap

Two categories crossed (day × hour, team × month): a pipe table whose cells hold
`<span class="heat sN">value</span>`, N from 1 (Blue 10) to 9 (Blue 90). Bucket the values
into five to seven steps of equal width; text turns white from `s6`.

```markdown
| | 8–10 | 10–12 |
|---|---|---|
| Monday | <span class="heat s7">142</span> | <span class="heat s6">118</span> |
| Tuesday | <span class="heat s5">96</span> | <span class="heat s4">71</span> |
```

### Tag

```html
<span class="pill">On track</span>
<span class="pill green">Done</span>
<span class="pill red">Blocked</span>
```

Colours: *(none)* blue · `cyan` · `teal` · `purple` · `magenta` · `green` · `red` · `gray`.

### Band (takeaway or status)

Put the band **last** on the slide. The status icon (info, warning, done, error) is added by
the theme: do not add one in the markup.

```html
<div class="band"><b>Takeaway:</b> one-line summary of the slide</div>
<div class="band warn"><b>Note:</b> caution or caveat</div>
<div class="band success"><b>Done:</b> positive outcome</div>
<div class="band error"><b>Risk:</b> blocking issue</div>
```

### Flow diagram

```html
<div class="flow">
  <div class="node"><b>Source</b><small>detail</small></div>
  <div class="arrow">▸</div>
  <div class="node cyan"><b>Platform</b><small>detail</small></div>
  <div class="arrow">▸</div>
  <div class="node teal"><b>Output</b><small>detail</small></div>
</div>
```

Nodes: *(none)* outlined · `cyan` · `teal` · `purple` · `magenta` (tinted) — a different one for
each adjacent node. `hero` (Blue 60) and `dark` are filled: one highlighted node at most.
Arrows: `▸` forward · `⇄` both ways. Colour: *(none)* grey · `blue` · `cyan` · `teal` ·
`purple` · `magenta` (e.g. `<div class="arrow magenta">▸</div>` for a monitoring path; the older
`obs` is an alias of `magenta`). Up to five nodes per row.

### Process

```html
<div class="process">
  <div class="step blue"><span class="step-num">01</span><b>Discover</b><small>detail</small></div>
  <div class="step cyan"><span class="step-num">02</span><b>Design</b><small>detail</small></div>
  <div class="step teal"><span class="step-num">03</span><b>Build</b><small>detail</small></div>
</div>
```

Steps: `blue` · `cyan` · `teal` · `purple` · `magenta` — a different one for each step.
`hero` (filled Blue 60) highlights one step. Five or six steps at most.

### Progress indicator

Where a project stands: the phases in order, each with its state. Use it instead of
`.process` when the point is *how far along* the work is, not how it is done.

```html
<div class="progress">
  <div class="done"><b>Discovery</b><small>January – February</small></div>
  <div class="done"><b>Design</b><small>March</small></div>
  <div class="current"><b>Build</b><small>Sprint 4 of 6</small></div>
  <div><b>Pilot</b><small>Two teams, July</small></div>
</div>
```

States: `done` (checkmark) · `current` (filled dot, SemiBold label; one per indicator) ·
no class = not started (empty circle) · `error` (red, blocked). The line on top is Blue 60
up to the current step. Three to six steps; the `<small>` detail is optional.

### Do / Don't

Guidelines, standards and onboarding: a good and a bad example side by side.

```html
<div class="cols">
<div class="do"><b>Do</b>Report one problem per ticket, with the steps to reproduce it.</div>
<div class="dont"><b>Don't</b>Write “nothing works” without the service name or a log.</div>
</div>
```

Start each box with its title in `<b>`; the green or red icon is added by the theme. Up to
two pairs per slide (a second `.cols` with `style="margin-top: 32px"`). A box can hold an
image or a code block instead of text: put an empty line after the line with the `<b>`
title and before `</div>`, as for any Markdown inside a `<div>`.

### Footnote

```html
<span class="small">Source: name of the document, year.</span>
```

---

## Markdown elements

### Table

```markdown
| Criterion | Option A | Option B |
|---|---|---|
| Cost | Low | Medium |
| Time to value | 2 weeks | 6 weeks |
```

At most 4–5 columns and 6–8 rows per slide.

### Pull quote

```markdown
> "The quoted sentence, with its quotation marks."

**— Name, role, organisation**
```

### Code

````markdown
```bash
python scripts/export_deck.py deck.md --strict
```
````

### Rule

```markdown
---
```

Inside a slide `---` starts a new slide; use `<hr>` for a divider line.

---

## Pictograms

```html
<img src="assets/pictograms/svg/cloud.svg" class="pictogram" alt="">          <!-- light slide: Gray 100 -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram blue" alt="">     <!-- light slide: Blue 60 -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram white" alt="">    <!-- dark slide -->
```

- Find names: `python scripts/pictograms.py search cloud security`.
- Sizes: `sm` 48 px · default 80 px · `lg` 120 px.
- Dark slides (`lead dark`, `section`, `end`, `backup`) need `white`; light slides must not use it.
- Always `alt=""`: pictograms are decorative.
- Inside a card, put the pictogram first, then an empty line, then the Markdown:

```html
<div class="card">

<img src="assets/pictograms/svg/cloud.svg" class="pictogram sm" alt="">

### Cloud
Short description.

</div>
```

---

## Speaker notes

```markdown
<!-- Say this out loud. Not shown on the slide. -->
```

Every comment that is not a Marp directive becomes the PowerPoint notes of its slide.
`export_deck.py --pdf-notes` also adds them to the PDF as annotations.

## What the PPTX export produces

Each slide is rebuilt from the layout Chrome renders, so the PPTX mirrors the PDF: boxes
become native rectangles with their fill and borders; text becomes native editable text boxes
in the font Chrome used, with the same size, colour, line height, baseline and line breaks
(`--reflow` lets PowerPoint re-wrap instead); pictograms and images become PNG pictures;
comments become notes. Tables are rectangles and text boxes, not PowerPoint tables. Video,
iframes and text drawn with CSS `::before`/`::after` are not exported and are reported as
warnings. The Plex fonts are bundled, so the PDF is always in Plex; the machines that open the
PPTX need Plex Sans, Serif and Mono installed, otherwise PowerPoint substitutes another font.
