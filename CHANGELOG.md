# Changelog

All notable changes to this project. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Bar chart component (`.bars` › `.bar`, `.bars.vertical`): one series after the Carbon simple
  bar chart, drawn with boxes so the PPTX keeps native shapes and editable text; colour
  modifiers from the categorical palette and `.gray` to mute bars. Stacked variant
  (`.bars.stacked`, horizontal and vertical) with the categorical palette in order and a
  `.legend`. Grouped variant (`.bars.grouped`, horizontal and vertical) for two to four
  series per category.
- Meter component (`.meter`) after the Carbon meter chart, with a target mark (bullet chart),
  status colours and a proportional variant (`.meter.proportional`).
- Roadmap component (`.roadmap` › `.scale` + `.task`): floating bars on a timeline.
- Snippets, style guide, `SKILL.md` guidance on charts, examples `08-bar-charts.md` and
  `09-meters-and-roadmaps.md`, and lint warnings for chart values out of range, missing
  bar, track or target elements, charts not scaled to 100, bars with different numbers of
  series, missing legends and roadmap tasks that end before they start.

## [1.0.0] — 2026-11-21

First public release.

### Added

- Agent skill usable with Claude Code, IBM Bob, OpenAI Codex, GitHub Copilot and any agent
  that reads files and runs commands (`SKILL.md`, with `license` and `compatibility`).
- Marp theme built on Carbon tokens (`themes/carbon.css`): White, Gray 10, Gray 90 and Gray 100
  themes; Carbon type scale and letter spacing; neutral text with Blue 60 for links; category
  accents from the Carbon categorical palette; Markdown elements after
  `@carbon/element-styles`; tables as Carbon data tables (size lg).
- Plex Sans, Serif and Mono bundled (SIL OFL) and loaded by the theme, so every PDF is set in
  the Carbon typeface.
- Slide classes (`lead`, `section`, `toc`, `ruled`, `compact`, `backup`, `end`) and components
  for columns, cards, KPIs, flow and process diagrams, tables and quotes.
- Notification bands with status icons from `@carbon/icons` (`.band.success`, `.band.error`
  and more); Carbon tag colours for `.pill`; colour modifiers for flow arrows.
- 1,429 Carbon pictograms with a keyword search (`scripts/pictograms.py`).
- Editable PPTX export: fonts as rendered by Chrome, line breaks of the PDF (`--reflow` to
  re-wrap), baselines aligned to the PDF, string and roman list markers, absolutely
  positioned `::before`/`::after` drawings, warnings for content past the bottom margin and
  for decorations that cannot be exported.
- Raw HTML goes through an allowlist (`themes/marp.config.json`) instead of `--html`; the
  measuring browser loads local files only and keeps its sandbox; `puppeteer-core` pinned
  and installed with `npm ci`.
- Scripts for the agent: `new_deck.py`, `lint_deck.py`, `export_deck.py` (PDF, PNG previews
  and PPTX in parallel), `check_env.py`, `sync_css.py`.
- Maintainer tools: `build_examples.py`, `check_examples.py`, `check_fidelity.py` (PPTX vs
  PDF with PowerPoint), `build_pictograms.py`.
- Example decks with their PDF and PPTX renders, `SECURITY.md`, `CONTRIBUTING.md`, CI workflow.

[Unreleased]: https://github.com/lucabnt/carbon-marp-deck/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/lucabnt/carbon-marp-deck/releases/tag/v1.0.0
