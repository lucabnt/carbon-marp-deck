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
```

Add `<!-- _paginate: false -->` to `lead`, `toc`, `section`, `end` and `backup`.
The footer is hidden on those slides automatically.

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
