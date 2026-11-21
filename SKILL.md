---
name: carbon-marp-deck
description: Create a presentation, slide deck or slides from a brief as Markdown (Marp) in the style of the open-source Carbon Design System, and export it to PDF and an editable PPTX. Use for informal decks such as team syncs, demos, drafts, knowledge sharing and internal updates. Do not use for decks that must follow a reviewed corporate or brand template.
license: Apache-2.0
compatibility: Needs shell access with Node.js 18+, Python 3.9+ (python-pptx, Pillow) and Google Chrome or Microsoft Edge; network access once to fetch Marp CLI and puppeteer-core from npm.
---

# Carbon-style Marp deck

Turn a content brief into a Marp deck styled with Carbon Design System tokens, then export
it to **PDF** and **editable PPTX** and check the result. The template is unofficial: it uses
only open-source Carbon material and is not endorsed by the Carbon project.

These instructions work in any agent that can read files and run shell commands
(Claude Code, IBM Bob, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI and others).
Where a step says "ask the user", use your agent's question tool if it has one,
otherwise ask in plain text.

## Locating `SKILL_DIR`

`SKILL_DIR` is the folder that contains this file (with `scripts/`, `references/`,
`themes/`, `assets/`, `pptx-export/`). It is usually the skills folder of your agent, for example
`~/.claude/skills/carbon-marp-deck`, `~/.bob/skills/carbon-marp-deck`,
`~/.codex/skills/carbon-marp-deck`, `.github/skills/carbon-marp-deck`, or a plain clone.
If unsure, find the folder that contains `scripts/new_deck.py`.

In the commands below replace `SKILL_DIR` with that absolute path, and `DECK_NAME`,
`DECK_TITLE`, `AUTHOR`, `SLUG` with real values (`SLUG` is `DECK_NAME` in lower case with
dashes). Use `python3` where `python` is not available.

## Step 0 — Check the fit

If the deck needs a brand compliance review or must follow an official corporate template,
**stop**: tell the user that this unofficial template is not suitable and a reviewed template
should be used. Otherwise continue.

## Step 1 — Gather the brief

You need: topic, audience, key messages or sections, **talk length in minutes**, author as
`Name — Role`, and the language of the slides. Ask only for what is missing. If the brief is
thin, propose an outline (slide titles written as takeaways) and wait for a go-ahead.

Content slides (excluding cover, contents, dividers, closing): about one per 1.5–2 minutes.

| Talk | Content slides |
|---|---|
| 5 min | 3–4 |
| 10 min | 5–7 |
| 20 min | 10–12 |
| 30 min | 15–18 |

Anything beyond that goes into backup slides after the closing slide.

## Step 2 — Check the machine and scaffold the deck

Check the prerequisites once per machine (the command prints the fix for anything missing;
missing Plex fonts are only a warning):

```bash
python SKILL_DIR/scripts/check_env.py
```

If Python packages are missing, run `pip install -r SKILL_DIR/pptx-export/requirements.txt`.
Ask the user before installing Node.js, a browser or fonts.

Then, from the user's working folder (not from `SKILL_DIR`):

```bash
python SKILL_DIR/scripts/new_deck.py "DECK_NAME" --title "DECK_TITLE" --author "AUTHOR"
```

Example author: `"Jane Smith — Staff Engineer"`. Optional: `--footer "Topic · Name"`,
`--out FOLDER`, `--force`.

This creates `SLUG/SLUG.md` and `SLUG/assets/`. The `.md` already holds the theme (generated
from `SKILL_DIR/themes/carbon.css`), the metadata and four starter slides: cover → contents →
placeholder → closing. **Never edit the `style: |` block.** Paths are relative to the `.md`.

## Step 3 — Write the slides

Edit `SLUG/SLUG.md` below the front matter. Read only what you need:

- `SKILL_DIR/references/components.md` — copy-paste snippets for every slide class and component
- `SKILL_DIR/examples/00-full-showcase.md` — every component in one deck
- `SKILL_DIR/references/style-guide.md` — the design rules and the Carbon tokens behind them
- Pictograms: `python SKILL_DIR/scripts/pictograms.py search KEYWORD` (names are Carbon's,
  e.g. `cloud--analytics`); reference them as `assets/pictograms/svg/<name>.svg`

**Slide order:** `lead` cover → `toc` contents → content slides, with `section` dividers
between major topics → `end` closing → optional `backup` opener and `bk` slides.
Add `<!-- _paginate: false -->` to `lead`, `toc`, `section`, `end` and `backup` slides.
Replace every starter placeholder (`Subtitle`, `First topic`, `Replace this with a takeaway title`…).

**Content rules**

- One idea per slide; split rather than crowd.
- Titles are takeaways in sentence case: `## The platform cut costs by 40%`, not `## Cost analysis`.
- At most 5 bullets per column; use cards or `.cols3` for more items.
- End a complex slide with a `.band` that states the single takeaway; the band is the **last** element.
- Colour carries meaning, not decoration: keep text neutral, use the category colours
  (`cyan`, `teal`, `purple`, `magenta`, default blue) consistently for the same category
  across the deck, and give adjacent flow nodes or steps different colours.
  Filled `.node.hero`, `.node.dark` and `.step.hero` only to highlight a single item.
- Status bands: `.band` (info), `.band.warn`, `.band.success`, `.band.error`; the theme adds
  the status icon.
- Dense slide (three columns of cards with long titles, a table of 8–10 rows): first shorten,
  then add `compact` to the slide class (`<!-- _class: compact -->`, or e.g. `bk compact`),
  which uses the smaller Carbon sizes for `h3` and table rows; if it still does not fit, split
  the slide.
- Pictograms are decorative: `alt=""`. **Colour rule:** on light slides no class (Gray 100) or
  `blue`; on dark slides (`lead dark`, `section`, `end`, `backup`) always `white`.
- The closing slide is text: `# Thank you` (or a closing line in the deck's language), an
  optional `##` subtitle and the `.lead-author` contact block. No logos or marks.
- Do not invent facts, figures or sources; mark missing data as a placeholder for the user.
- Use only the pictograms in `SKILL_DIR/assets/pictograms/`; do not add logos or images whose
  licence is unknown.
- For anything not covered here, follow the [Carbon Design System](https://carbondesignsystem.com/)
  and [carbon-element-styles](https://github.com/carbon-design-system/carbon-element-styles).

**Speaker notes.** Put them in an HTML comment after the slide content:
`<!-- Say this out loud… -->`. Every comment that is not a Marp directive (`_class`,
`_paginate`, …) becomes the PowerPoint notes of that slide; it is not printed in the PDF.

### PPTX-safe syntax (follow it literally)

The PPTX is rebuilt from the layout Chrome renders, so documented components come out
faithfully and custom HTML/CSS is reproduced too. Content that cannot be exported
(`<video>`, `<iframe>`, text drawn with `::before`/`::after`, missing images) is reported
as a warning. The documented patterns remain the safest and the most editable:

1. **Copy snippets from `references/components.md`; do not invent HTML.** Allowed: Markdown headings
   (`#`, `##`, `###`), paragraphs, `-` lists, `1.` lists, pipe tables, `>` quotes, fenced code,
   `**bold**`, `*italic*`, `` `code` ``, links, and the components `.cols`/`.cols3`, `.card`,
   `.kpi`/`.kpi-label`, `.pill`, `.band`, `.small`, `.flow`/`.node`/`.arrow`, `.process`/`.step`,
   `img.pictogram`, `.toc-grid`, `.lead-author`, and the slide class `compact`.
2. **One component per line**, tags in the documented order:
   `<div class="node cyan"><b>Label</b><small>detail</small></div>`,
   `<div class="step teal"><span class="step-num">01</span><b>Title</b><small>detail</small></div>`,
   `<div class="kpi">42%</div>`, `<div class="kpi-label">Label</div>`.
3. **Empty line after an opening `<div …>`** before any Markdown (`### title`, `- item`,
   `**bold**`), and before the closing `</div>`. Otherwise Marp prints the Markdown literally —
   the most common mistake. Pure-HTML components (`.flow`, `.process`, `.toc-grid`, a one-line
   `.band`) need no empty lines.
4. **Images** on their own line: `![alt](assets/…)` or the `<img>` snippets.
5. **Tables**: Markdown pipe tables only.
6. **Contents slide**: one `.toc-item` per line; for more than 6 items add
   `style="grid-template-rows: repeat(N, auto)"` to `.toc-grid` (N = items ÷ 2, rounded up).
7. **Do not edit the theme.** A `<style scoped>` block is allowed only for sizes and spacing.

## Step 4 — Export, look, fix, repeat

```bash
python SKILL_DIR/scripts/export_deck.py SLUG/SLUG.md --strict --preview
```

It copies the pictograms the deck uses next to it, lints the deck (images that do not
resolve, Markdown inside HTML without an empty line, leftover placeholders, missing
`_paginate: false`, a `.band` that is not last, pictogram colour vs background) and reports
content that runs past the bottom margin (Marp would cut it off in the PDF), writes
`SLUG.pdf` and `SLUG.pptx` next to the `.md`, and with `--preview` one PNG per slide in
`SLUG-preview/` (PDF, PNG and PPTX are produced in parallel). `--strict` makes every warning
fail. The PPTX mirrors the PDF: same positions, the fonts Chrome used, the same line breaks.
Add `--reflow` only if the user says the PPTX will be heavily edited in PowerPoint (paragraphs
then re-wrap as they type, and line breaks may differ from the PDF). the Plex fonts are bundled,
so the PDF is always in Plex.

**The export is not finished while there are warnings or errors.** Loop:

1. Read each message (`slide N (line L): …`), fix the `.md` (split the slide, shorten text,
   use the documented snippet) and run the same command again.
2. If you can view images, open the PNGs (at least the cover, one slide per component type and
   every slide that was warned about). Check that no text is cut at the slide edge or overlaps,
   nothing is missing and the contrast is readable. Marp clips overflowing content silently.
   If you cannot view images, tell the user that the visual check was not done.

The first export downloads Marp CLI and `puppeteer-core` from npm (network needed once).

## Step 5 — Report

Check before reporting:

- [ ] `export_deck.py --strict` finished with no warnings or errors
- [ ] No placeholder text left; author, footer and closing slide are real
- [ ] Every title is a takeaway; complex slides end with a `.band`
- [ ] Slide count fits the talk length; extra material is in backup
- [ ] Numbers, names and sources come from the brief; gaps are marked for the user
- [ ] Speaker notes written where the brief asks for a script
- [ ] Previews checked, or the user told they were not

Then give the paths of the `.md`, `.pdf` and `.pptx`, and mention that:

- the deck is an unofficial Carbon-style template, for informal use;
- the PPTX matches the PDF and is fully editable (native shapes and text boxes); lines end
  where they end in the PDF unless `--reflow` was used; pictograms are PNG pictures and tables
  are made of individual shapes;
- the fonts: the PDF embeds Plex; the PPTX uses Plex Sans, Serif and Mono, which must be
  installed on the machines that open it (free, SIL OFL; `check_env.py` reports them).

## Troubleshooting

| Problem | Fix |
|---|---|
| Markdown shows literally (`**x**`, `###`) | Add the empty line after the opening `<div>` |
| Images missing in the PDF | `assets/` must sit next to the `.md`; the export already passes `--allow-local-files` |
| `python-pptx` missing | `pip install -r SKILL_DIR/pptx-export/requirements.txt` |
| `npx` not found | Install Node.js 18+ |
| No browser found | Install Chrome or Edge, or set `CHROME_PATH` |
| PPTX export fails in `pptx-export/dom/` | Run `npm ci` there and read the error (proxy, registry); `--pdf-only` still produces the PDF |
| HTML shows up as text on a slide | The tag or attribute is not in the allowlist (`themes/marp.config.json`): use the documented components instead |
| `remote resource not loaded` | Download the image next to the deck and reference the local file |
| Unknown pictogram | The export suggests the closest names; search with `scripts/pictograms.py search` |
