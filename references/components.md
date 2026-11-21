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
