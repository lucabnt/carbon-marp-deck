# carbon-marp-deck

**An agent skill and a Marp template for slide decks in the style of the [Carbon Design System](https://carbondesignsystem.com/).**
Repository: [github.com/lucabnt/carbon-marp-deck](https://github.com/lucabnt/carbon-marp-deck)
Write the deck in Markdown, or let your coding agent write it from a brief, and get a **PDF** and an **editable PowerPoint** file.

> [!IMPORTANT]
> **Unofficial.** This is a community project built only on open-source Carbon material
> (design tokens, guidelines, pictograms, the Plex typeface). It is not affiliated with,
> endorsed or supported by the Carbon Design System project. Use it for informal decks
> (team syncs, demos, drafts, knowledge sharing), not for material that must follow a
> reviewed corporate template.

---

## Contents

- [What you get](#what-you-get)
- [Use it as an agent skill](#use-it-as-an-agent-skill)
- [Use it as a template, without an agent](#use-it-as-a-template-without-an-agent)
- [Requirements](#requirements)
- [The design](#the-design)
- [Slide classes and components](#slide-classes-and-components)
- [Pictograms](#pictograms)
- [Export](#export)
- [Examples](#examples)
- [Repository layout](#repository-layout)
- [Maintaining the template](#maintaining-the-template)
- [Sources](#sources)
- [Security](#security)
- [Contributing](#contributing)
- [Licence and trademarks](#licence-and-trademarks)

---

## What you get

- **A Carbon-style Marp theme** ([`themes/carbon.css`](themes/carbon.css)) whose values all come from Carbon tokens: the White, Gray 10, Gray 90 and Gray 100 themes, the Carbon type scale in Plex, the spacing scale and 2x grid gutters, Carbon tag and notification colours, and the Markdown element styles of [`@carbon/element-styles`](https://github.com/carbon-design-system/carbon-element-styles).
- **Slide layouts**: cover (three themes), contents (also with the current section), section divider, content, statement, quote, closing, backup.
- **Components**: two and three column grids, cards (Carbon tiles), KPIs, bar charts (also diverging), custom charts (lines, areas, scatter, dumbbells, slopes, donuts, heatmaps), meters, roadmaps, progress indicators, do / don't boxes, breadcrumbs, tags, notification bands, flow diagrams, process diagrams, data tables, pull quotes.
- **Plex bundled** (SIL OFL): every PDF renders in the Carbon typeface, installed or not.
- **1,429 Carbon pictograms** (Apache-2.0) with a keyword search.
- **An agent skill** ([`SKILL.md`](SKILL.md)): an agent turns a brief into a finished deck, lints it, exports it and checks the previews.
- **Exporters**: PDF and PNG previews through Marp CLI, and an editable PPTX made of native shapes and text boxes, measured from the browser layout.
- **Guard rails**: a linter for the mistakes that break Marp slides silently, and a regression test for the examples and the PPTX converter.

## Use it as an agent skill

[`SKILL.md`](SKILL.md) follows the **Agent Skills** format: a folder with a `SKILL.md` file whose
front matter holds a `name` and a `description`. Agents that support the format load the skill
when a request matches the description ("make a deck about…"); the rest of the folder
(scripts, theme, pictograms, docs) is read only when needed.

### 1. Install

Clone the repository **as a folder named `carbon-marp-deck`** (the folder name must match the
`name` in `SKILL.md`) into the skills folder of your agent:

| Agent | Personal skill (all projects) | Project skill (one repository) |
|---|---|---|
| **Claude Code** (CLI, desktop app, IDE extensions) | `~/.claude/skills/carbon-marp-deck` | `.claude/skills/carbon-marp-deck` |
| **IBM Bob** | `~/.bob/skills/carbon-marp-deck` | `.bob/skills/carbon-marp-deck` |
| **OpenAI Codex CLI** | `~/.codex/skills/carbon-marp-deck` | see the Codex documentation |
| **GitHub Copilot** (agent mode, Copilot CLI) | `~/.copilot/skills/carbon-marp-deck` | `.github/skills/carbon-marp-deck` |
| **Any other agent** that reads files and runs shell commands (Cursor, Gemini CLI, Windsurf, Cline…) | anywhere | anywhere, then point the agent at `SKILL.md` (see below) |

Skill folder locations are defined by each agent and can change; if the skill is not picked
up, check your agent's documentation for its current skills folder.

```bash
# example: personal skill for Claude Code
git clone https://github.com/lucabnt/carbon-marp-deck.git ~/.claude/skills/carbon-marp-deck
pip install -r ~/.claude/skills/carbon-marp-deck/pptx-export/requirements.txt
python ~/.claude/skills/carbon-marp-deck/scripts/check_env.py      # verify the prerequisites
```

On Windows PowerShell `~` is `$HOME` (for example `$HOME\.bob\skills\carbon-marp-deck`).
Start a new session or task after installing: most agents scan their skills at start-up.
Update later with `git pull` inside the skill folder.

**Agents without skill support.** Add one line to the agent's rules or instructions file
(`AGENTS.md`, `.cursor/rules`, `GEMINI.md`, a custom prompt…):

```text
To create a presentation or slide deck, follow <path-to>/carbon-marp-deck/SKILL.md.
```

**Web chat apps.** The export needs Node.js, Python and Chrome or Edge on the machine that runs
the commands, so use an agent that works on your computer (or in a sandbox with those tools).

**claude.ai.** Upload the skill as a .zip in **Settings > Capabilities > Skills** (with code
execution turned on). claude.ai accepts at most 200 files and no archives inside the zip, so
build it with the packaging script rather than zipping the folder:

```bash
python tools/build_skill_zip.py      # -> dist/carbon-marp-deck-<version>.zip
```

The script packs the pictogram SVGs into one file (`assets/pictograms/svg.json`, read by
`scripts/pictograms.py`) and tests the zip; CI runs the same test. The claude.ai sandbox
usually has no Chrome or Edge, so expect the agent to write the deck there but not export it.

### 2. Ask for a deck

Describe the deck in plain language, or call the skill by name where your agent supports it
(for example `/carbon-marp-deck` in Claude Code or IBM Bob):

> Create a 10-minute deck about our Q3 platform migration for the engineering team.
> Author: Jane Smith — Staff Engineer. Export PDF and PPTX.

### 3. What the agent does

1. **Checks the fit**: informal decks only; anything that needs a reviewed corporate template is declined.
2. **Gathers the brief**: topic, audience, key messages, talk length, author, language. It proposes an outline if the brief is thin.
3. **Scaffolds** the deck with [`scripts/new_deck.py`](scripts/new_deck.py).
4. **Writes the slides** with the documented components ([`references/components.md`](references/components.md)), takeaway titles, one idea per slide, speaker notes.
5. **Exports and checks** with [`scripts/export_deck.py`](scripts/export_deck.py) `--strict --preview`: lint, PDF, PPTX and one PNG per slide, then it looks at the previews and fixes the deck until there are no warnings.
6. **Reports** the paths of the `.md`, `.pdf` and `.pptx`.

## Use it as a template, without an agent

```bash
git clone https://github.com/lucabnt/carbon-marp-deck.git carbon-marp-deck
cd carbon-marp-deck
pip install -r pptx-export/requirements.txt          # only for the PPTX export

python scripts/new_deck.py "Q3 review" --title "Q3 review" --author "Jane Smith — Staff Engineer"
# edit q3-review/q3-review.md
python scripts/export_deck.py q3-review/q3-review.md --strict --preview
```

`new_deck.py` creates `q3-review/q3-review.md` with the theme already embedded, the metadata
filled in and four starter slides (cover, contents, one content slide, closing).
You can also copy [`template.md`](template.md) by hand: it is a complete reference deck.

**Rules that keep a deck working**

- Edit only `title`, `author` and `footer` in the front matter. Never edit the `style: |` block:
  it is generated from [`themes/carbon.css`](themes/carbon.css).
- Copy component snippets from [`references/components.md`](references/components.md).
- Leave an empty line between an opening `<div …>` and any Markdown inside it.
- Reference pictograms as `assets/pictograms/svg/<name>.svg`; the export copies the files next to the deck.

**Live preview in VS Code.** Install [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
and set `"markdown.marp.html": "all"` in the workspace settings, so that the preview keeps the
inline `style` attributes as the export does. Use that setting for your own decks only: the export
filters raw HTML through an allowlist (see [Security](#security)), the preview does not.

## Requirements

| Tool | Needed for |
|---|---|
| **Node.js 18+** | Marp CLI (fetched by `npx`, version pinned in [`package.json`](package.json)) and the PPTX exporter (`puppeteer-core`, installed on first use) |
| **Google Chrome or Microsoft Edge** | Rendering PDF/PNG and measuring the layout for the PPTX. Set `CHROME_PATH` if it is not found. |
| **Python 3.9+** with `pip install -r pptx-export/requirements.txt` | The scripts and the PPTX export (`python-pptx`, `Pillow`) |
| **Plex Sans, Serif and Mono, installed** (recommended) | The PPTX: PowerPoint uses installed fonts only. The PDF does not need them: the fonts are bundled in [`assets/fonts/`](assets/fonts/) and loaded by the theme. Free under the SIL Open Font License (desktop fonts from the official Plex releases); `python scripts/check_env.py` reports whether they are installed. |

Check everything at once, with the fix for each missing item:

```bash
python scripts/check_env.py
```

The first run of Marp CLI and of the PPTX exporter downloads packages from npm (network needed once).

## The design

The full reference, with every token and its Carbon source, is [`references/style-guide.md`](references/style-guide.md);
where the template departs from Carbon, and why, is listed in its
[Divergences from Carbon](references/style-guide.md#11-divergences-from-carbon) section.
In short:

| Aspect | Rule | Carbon source |
|---|---|---|
| **Themes** | Content slides White · cover Gray 10 (or White, or Gray 100) · section divider and closing Gray 100 · backup Gray 90 | `@carbon/themes` |
| **Typeface** | Plex Sans; Plex Serif for quotes; Plex Mono for code | `@carbon/type` |
| **Type scale** | 12 · 14 · 16 · 20 · 24 · 28 · 32 · 42 · 54 px. Light (300) only from 42 px; SemiBold (600) for short labels and bold text | `@carbon/type` |
| **Headings** | `h1` 42/50 Light · `h2` (slide title) 32/40 · `h3` 28/36 (20/28 on `compact` slides) · cover and divider titles 54/64 Light. Sentence case, neutral colour | productive headings 06, 05, 04, 07 |
| **Colour** | Text stays neutral (text-primary `#161616`, text-secondary `#525252`). Blue 60 `#0f62fe` is for links and a few brand accents | Carbon colour and typography guidance |
| **Category accents** | Blue 60 and the first four colours of the categorical palette: Purple 70, Cyan 50, Teal 70, Magenta 70, with their 10-grade tints | data visualisation palette |
| **Status** | Notification colours: info, warning, success, error | `support-*`, `notification-background-*` |
| **Spacing** | 2 · 4 · 8 · 12 · 16 · 24 · 32 · 40 · 48 · 64 px; slide padding 48 × 64; gutters 32 (wide) and 16 (narrow) | `@carbon/layout`, 2x grid |
| **Shape** | Square corners; only tags are rounded | Carbon components |
| **Markdown elements** | "–" bullets, data-table tables, serif pull quotes, 1 px rules, code on `layer` | `@carbon/element-styles` |

## Slide classes and components

Set a slide class with `<!-- _class: name -->` at the top of the slide.

| Class | Theme | Use |
|---|---|---|
| `lead` | Gray 10 | Cover: title, subtitle, author block at the bottom |
| `lead plain` | White | Cover, white variant |
| `lead dark` | Gray 100 | Cover, dark variant |
| `toc` | White | Contents: numbered structured list |
| `section` | Gray 100 | Section divider |
| *(none)* | White | Content slide |
| `ruled` | White | Content slide with an 8 px Blue 60 left edge |
| `end` | Gray 100 | Closing: short line ("Thank you") and contact block |
| `backup` | Gray 90 | Opens the backup section, after `end` |
| `bk` | White | Backup content slide, 4 px Gray 50 top edge |
| `compact` | (any) | Adds to another class: on a dense slide, `h3` 20 px and table rows 40 px (Carbon sizes md) |
| `statement` | White (`statement dark`: Gray 100) | One big number (120 px Light) or one sentence, with its source |
| `quote` | White | One quotation in Plex Serif 42 px, with its attribution |

| Component | Markup | Based on |
|---|---|---|
| Two / three columns | `.cols` / `.cols3` | 2x grid, 32 / 16 px gutters |
| Card | `.card` + `.cyan` `.teal` `.purple` `.magenta`, `.sm` | Tile with a category stroke |
| KPI | `.kpi` + `.kpi-label` | 54 px Light number, secondary label |
| Bar chart | `.bars` › `.bar` (`--v` 0–100), `.vertical`, `.stacked` / `.grouped` + `.legend`, `.diverging` (`--v` −100–100, `.neg`), colour modifiers, `.gray` | Carbon simple, stacked and grouped bar charts, as native shapes |
| Meter | `.meter` (`--v`), target `--t` + `<u>`, `.proportional`, status `.success` `.warn` `.error` | Carbon meter and bullet charts |
| Roadmap | `.roadmap` › `.scale` + `.task` (`--from`, `--to`) | Carbon floating bar chart, as a Gantt timeline |
| Custom chart | `.plot` › `.y` `.x` gridlines and labels, `.dot` `.range` `.zone` `.note` at `--x` / `--y` 0–100, one text-free SVG `.layer` for lines and areas | Carbon line, area, scatter and other charts, for the chart no component draws |
| Donut | `.donut` (SVG ring + centre value) + `.legend.vertical` | Carbon donut chart |
| Heatmap | `<span class="heat s1">` … `s9` in table cells | Carbon heatmap, Blue sequential scale |
| Tag | `.pill` + `.cyan` `.teal` `.purple` `.magenta` `.green` `.red` `.gray` | Carbon Tag |
| Band | `.band` + `.warn` `.success` `.error` | Inline notification (low contrast) with its status icon |
| Flow diagram | `.flow` › `.node` + `.arrow` (colour modifiers) | Outlined boxes, category tints |
| Process | `.process` › `.step` | Numbered tiles with a category stroke |
| Progress indicator | `.progress` › `div` + `.done` `.current` `.error` | Carbon progress indicator |
| Do / Don't | `.do`, `.dont` | Do and don't examples of the Carbon guidelines |
| Current section | `.toc-item.current` on a repeated contents slide | Carbon side nav, selected item |
| Breadcrumb | `<!-- header: Deck / 02 Section -->` | Carbon breadcrumb, as plain text |
| Contents | `.toc-grid` › `.toc-item` | Structured list |
| Author block | `.lead-author` | Cover and closing slides |
| Footnote | `.small` | Helper text |
| Table, quote, code, rule | plain Markdown | `@carbon/element-styles` |

Snippets: [`references/components.md`](references/components.md) · rendered examples: [`examples/`](examples/).

## Pictograms

[`assets/pictograms/`](assets/pictograms/) holds 1,429 pictograms from the open-source
[`@carbon/pictograms`](https://www.npmjs.com/package/@carbon/pictograms) package (Apache-2.0),
as colourless SVG. Pictograms of company products, brands, third-party logos and named sites
are left out ([`tools/pictogram_exclude.txt`](tools/pictogram_exclude.txt)).

```bash
python scripts/pictograms.py search cloud security      # find names
python scripts/pictograms.py categories
```

```html
<img src="assets/pictograms/svg/cloud.svg" class="pictogram" alt="">         <!-- light slide: Gray 100 -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram blue" alt="">    <!-- light slide: Blue 60 accent -->
<img src="assets/pictograms/svg/cloud.svg" class="pictogram white" alt="">   <!-- dark slide -->
```

Sizes: `sm` 48 px (the Carbon minimum) · default 80 px · `lg` 120 px. Details:
[`assets/pictograms/README.md`](assets/pictograms/README.md).

## Export

```bash
python scripts/export_deck.py my-deck/my-deck.md --strict --preview
```

| Step | Output |
|---|---|
| Copy the pictograms the deck uses | `my-deck/assets/pictograms/svg/` |
| Lint ([`scripts/lint_deck.py`](scripts/lint_deck.py)) | errors and warnings with slide and line numbers |
| PDF (Marp CLI) | `my-deck/my-deck.pdf` |
| PPTX ([`pptx-export/dom/`](pptx-export/)) | `my-deck/my-deck.pptx` |
| `--preview` | `my-deck/my-deck-preview/*.png`, one per slide |

PDF, previews and PPTX are produced in parallel (a few seconds for a typical deck).
Options: `--pdf-only` (alias `--no-pptx`), `--pptx-only`, `--outdir DIR`, `--pdf-notes` (speaker notes as PDF
annotations), `--reflow` (PPTX text re-wraps in PowerPoint, see below).
With `--strict` every warning fails the export.

**The PPTX mirrors the PDF.** It is rebuilt from the layout Chrome renders: every box becomes a
native shape and every text a native, editable text box at the same position, in the font
Chrome actually used, with the first baseline aligned to Chrome's and each line ending where it
ends in the PDF. Measured against the PDF, the examples differ by 0.18–0.65 % of pixels on
average ([details](pptx-export/README.md#fidelity)). Pictograms become PNG pictures and
`<!-- … -->` comments become speaker notes. Tables are rectangles and text boxes, not PowerPoint
tables. Video, iframes and text drawn with CSS `::before`/`::after` are not exported and are
reported as warnings.

Two things to know:

- **Fonts.** The PDF is always in Plex (the fonts are bundled). The PPTX names the installed Plex
  families, so the machines that open it need the Plex fonts installed, otherwise PowerPoint substitutes
  another font. `python scripts/check_env.py` reports whether they are installed.
- **Line breaks are fixed by default**, so the PPTX looks exactly like the PDF. For a deck that
  will be heavily edited in PowerPoint, export with `--reflow` so paragraphs re-wrap as you type.

**Only the PDF**, without Python:

```bash
npx --yes @marp-team/marp-cli@4.5.1 --no-stdin my-deck.md --pdf --config-file themes/marp.config.json --allow-local-files
```

(run from the repository, or give the full path of `themes/marp.config.json`).
Do not leave out `--config-file`: without the allowlist Marp drops the `style` attributes
without a warning, and bars, meters, roadmaps and custom charts render empty.

## Examples

| Deck | Shows | Renders |
|---|---|---|
| [`00-full-showcase.md`](examples/00-full-showcase.md) | every layout and component | [PDF](examples/pdf/00-full-showcase.pdf) · [PPTX](examples/pptx/00-full-showcase.pptx) |
| [`01-title-slides.md`](examples/01-title-slides.md) | covers, contents, dividers, backup, closing | [PDF](examples/pdf/01-title-slides.pdf) · [PPTX](examples/pptx/01-title-slides.pptx) |
| [`02-two-column.md`](examples/02-two-column.md) | `.cols`, `.cols3` | [PDF](examples/pdf/02-two-column.pdf) · [PPTX](examples/pptx/02-two-column.pptx) |
| [`03-cards.md`](examples/03-cards.md) | cards and accents | [PDF](examples/pdf/03-cards.pdf) · [PPTX](examples/pptx/03-cards.pptx) |
| [`04-kpi-and-metrics.md`](examples/04-kpi-and-metrics.md) | KPIs, tags, bands | [PDF](examples/pdf/04-kpi-and-metrics.pdf) · [PPTX](examples/pptx/04-kpi-and-metrics.pptx) |
| [`05-flow-diagrams.md`](examples/05-flow-diagrams.md) | flows, nodes, arrows | [PDF](examples/pdf/05-flow-diagrams.pdf) · [PPTX](examples/pptx/05-flow-diagrams.pptx) |
| [`06-tables-and-quotes.md`](examples/06-tables-and-quotes.md) | tables, quotes, `ruled`, footnotes | [PDF](examples/pdf/06-tables-and-quotes.pdf) · [PPTX](examples/pptx/06-tables-and-quotes.pptx) |
| [`07-process-diagrams.md`](examples/07-process-diagrams.md) | process steps, pictograms | [PDF](examples/pdf/07-process-diagrams.pdf) · [PPTX](examples/pptx/07-process-diagrams.pptx) |
| [`08-bar-charts.md`](examples/08-bar-charts.md) | bar charts: simple, stacked and grouped, horizontal and vertical | [PDF](examples/pdf/08-bar-charts.pdf) · [PPTX](examples/pptx/08-bar-charts.pptx) |
| [`09-meters-and-roadmaps.md`](examples/09-meters-and-roadmaps.md) | meters, targets, proportional meter, roadmap | [PDF](examples/pdf/09-meters-and-roadmaps.pdf) · [PPTX](examples/pptx/09-meters-and-roadmaps.pptx) |
| [`10-progress-and-statements.md`](examples/10-progress-and-statements.md) | contents with the current section, breadcrumb, progress indicator, statement and quote slides, diverging bars, do / don't | [PDF](examples/pdf/10-progress-and-statements.pdf) · [PPTX](examples/pptx/10-progress-and-statements.pptx) |
| [`11-custom-charts.md`](examples/11-custom-charts.md) | custom charts: line, area with forecast, scatter, dumbbell, slope, donut, heatmap | [PDF](examples/pdf/11-custom-charts.pdf) · [PPTX](examples/pptx/11-custom-charts.pptx) |

Regenerate them with `python tools/build_examples.py` (or `npm run build`).

## Repository layout

The layout follows the Agent Skills conventions: `SKILL.md` at the root, the commands an agent
runs in `scripts/`, documents it reads on demand in `references/`, files it uses in `assets/`.
Everything a deck author or agent does not need lives in `tools/` and `tests/`.

```
carbon-marp-deck/
├── SKILL.md                    the skill: workflow, content rules, PPTX-safe syntax
├── README.md                   this file
├── template.md                 reference deck; copy it to start by hand
├── CHANGELOG.md · CONTRIBUTING.md · SECURITY.md · LICENSE · NOTICE
├── themes/
│   ├── carbon.css              the theme (single source; embedded into every deck)
│   └── marp.config.json        allowlist of the raw HTML a deck may use
├── references/
│   ├── components.md           copy-paste snippets for every component
│   └── style-guide.md          design reference: tokens, layouts, Carbon sources
├── assets/fonts/               Plex woff2 files (OFL), copied next to every deck
├── assets/pictograms/          Carbon pictograms (svg/), catalog.csv, licence
├── scripts/                    what the agent runs
│   ├── check_env.py            check the prerequisites and say how to fix them
│   ├── new_deck.py             scaffold a deck
│   ├── export_deck.py          pictograms + lint + PDF + PPTX + PNG previews
│   ├── lint_deck.py            static checks (also run by export_deck.py)
│   ├── pictograms.py           search pictograms, copy the ones a deck uses
│   ├── sync_css.py             embed the theme into decks
│   └── toolchain.py            shared: pinned Marp CLI, browser discovery
├── pptx-export/                PPTX converter (dom/: Chrome layout → PowerPoint objects)
├── examples/                   example decks with pdf/ and pptx/ renders
├── tools/                      maintainers only
│   ├── build_examples.py       regenerate examples/pdf and examples/pptx
│   ├── check_examples.py       regression test
│   ├── check_fidelity.py       PPTX vs PDF visual comparison (Windows + PowerPoint)
│   ├── build_pictograms.py     rebuild assets/pictograms/ from @carbon/pictograms
│   └── pictogram_exclude.txt   pictograms left out of the library
├── tests/                      converter cases, fixtures, PPTX baseline
└── .github/workflows/ci.yml    lint and PPTX regression on Ubuntu and Windows
```

## Maintaining the template

```bash
python scripts/sync_css.py                # after editing themes/carbon.css
python tools/build_examples.py            # regenerate the example PDFs and PPTX files
python tools/check_examples.py            # lint, CSS in sync, PPTX output vs tests/baseline.json
python tools/check_examples.py --update   # accept an intended converter or content change
python tools/check_fidelity.py            # PPTX vs PDF, slide by slide (Windows + PowerPoint)
python tools/build_pictograms.py          # rebuild the pictograms from the pinned @carbon/pictograms
```

`npm run build`, `npm run check` and `npm run doctor` are shortcuts for the same commands.
When you change the theme, take the values from Carbon tokens and say which token in a comment.

## Sources

| Source | Used for |
|---|---|
| [carbondesignsystem.com](https://carbondesignsystem.com/) | colour, typography, 2x grid, pictogram and data visualisation guidance |
| [github.com/carbon-design-system/carbon](https://github.com/carbon-design-system/carbon) | token values: `@carbon/themes`, `@carbon/type`, `@carbon/colors`, `@carbon/layout`, `@carbon/pictograms` |
| [github.com/carbon-design-system/carbon-element-styles](https://github.com/carbon-design-system/carbon-element-styles) | styles of native HTML / Markdown elements |
| the official Plex releases (versions in [`NOTICE`](NOTICE)) | the Plex typeface |
| [marp.app](https://marp.app/) | the slide engine |

## Security

Exporting renders the deck in a browser, so the export limits what a deck can do. Raw HTML is
filtered through an allowlist ([`themes/marp.config.json`](themes/marp.config.json)): the tags
and attributes of the components stay, `<script>`, `<iframe>` and event handlers are removed. The
browser that measures the slides for the PPTX loads local files only and keeps its sandbox. The
converter's Node dependency is pinned and installed from a lockfile. Local images referenced by a
deck do end up in the outputs: export decks you trust. Details and how to report a problem:
[`SECURITY.md`](SECURITY.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md): where each kind of change goes, the checks to run and
how the example renders and test baseline are kept up to date. Changes are listed in
[`CHANGELOG.md`](CHANGELOG.md).

## Licence and trademarks

This repository is released under the [Apache License 2.0](LICENSE); see also [`NOTICE`](NOTICE).

| Material | Licence |
|---|---|
| Theme, scripts, exporters, template, examples, docs | Apache-2.0 |
| Carbon pictograms (`assets/pictograms/svg/`) | Apache-2.0, © the Carbon Design System contributors ([`LICENSE-CARBON`](assets/pictograms/LICENSE-CARBON)) |
| Carbon token values used in the theme | Apache-2.0 (Carbon Design System) |
| Plex fonts (`assets/fonts/`) | SIL Open Font License 1.1 ([`LICENSE-OFL.txt`](assets/fonts/LICENSE-OFL.txt)), Reserved Font Name "Plex"; bundled unmodified, copyright notice in [`NOTICE`](NOTICE) |
| Marp CLI, puppeteer-core, python-pptx | their own licences; installed, not bundled |

Carbon, Plex, IBM Bob, Claude, Claude Code, OpenAI Codex, GitHub Copilot and other names are trademarks of
their respective owners. They are mentioned only to describe compatibility; no affiliation or
endorsement is implied.
