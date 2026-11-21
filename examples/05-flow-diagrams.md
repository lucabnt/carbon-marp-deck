---
marp: true
title: "Carbon Marp Template — Example 05: Flow Diagrams"
author: "Carbon Marp Template"
paginate: false
theme: default
size: 16:9
footer: "Carbon Marp Template · examples/05-flow-diagrams"
style: |
  /* ══════════════════════════════════════════════════════════════════════════ */
  /* Carbon-style Marp theme (unofficial)                                       */
  /* Every value below is a token of the open-source Carbon Design System       */
  /* (@carbon/colors, @carbon/themes, @carbon/type, @carbon/layout, Apache-2.0). */
  /* Not affiliated with or endorsed by the Carbon Design System project.        */
  /*                                                                            */
  /* Themes   White (content) · Gray 10 (cover) · Gray 100 (cover dark,         */
  /*          section, end) · Gray 90 (backup)                                  */
  /* Type     Plex Sans; Carbon type scale 12·14·16·20·24·28·32·42·54 px;      */
  /*          Light 300 only from 42 px, SemiBold 600 for short labels.         */
  /* Spacing  Carbon spacing scale 2·4·8·12·16·24·32·40·48·64 px (2x grid).     */
  /* Colour   neutral text; Blue 60 for links and the brand accent; category    */
  /*          accents from the Carbon categorical palette; tags and             */
  /*          notifications use the matching Carbon component tokens.            */
  /* Elements Markdown elements (lists, tables, quotes, code, rules) follow     */
  /*          @carbon/element-styles (Apache-2.0).                              */
  /* Shape    square corners; only tags (.pill) are rounded.                    */
  /* ══════════════════════════════════════════════════════════════════════════ */
  /* ── Plex typeface (SIL Open Font License, assets/fonts/LICENSE-OFL.txt) ───── */
  /* The bundled, unmodified font files, declared as Plex Sans / Serif / Mono.   */
  /* scripts/new_deck.py and scripts/export_deck.py copy assets/fonts/ next to   */
  /* the deck, because the paths are relative to it. The PPTX export maps these  */
  /* names to the installed font families (pptx-export/dom/dom_to_pptx.py).     */
  @font-face { font-family: 'Plex Sans'; font-weight: 300; font-style: normal;
    src: url('assets/fonts/PlexSans-Light.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Sans'; font-weight: 300; font-style: italic;
    src: url('assets/fonts/PlexSans-LightItalic.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Sans'; font-weight: 400; font-style: normal;
    src: url('assets/fonts/PlexSans-Regular.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Sans'; font-weight: 400; font-style: italic;
    src: url('assets/fonts/PlexSans-Italic.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Sans'; font-weight: 600; font-style: normal;
    src: url('assets/fonts/PlexSans-SemiBold.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Sans'; font-weight: 600; font-style: italic;
    src: url('assets/fonts/PlexSans-SemiBoldItalic.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Serif'; font-weight: 400; font-style: normal;
    src: url('assets/fonts/PlexSerif-Regular.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Serif'; font-weight: 400; font-style: italic;
    src: url('assets/fonts/PlexSerif-Italic.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Serif'; font-weight: 600; font-style: normal;
    src: url('assets/fonts/PlexSerif-SemiBold.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Mono'; font-weight: 400; font-style: normal;
    src: url('assets/fonts/PlexMono-Regular.woff2') format('woff2'); }
  @font-face { font-family: 'Plex Mono'; font-weight: 600; font-style: normal;
    src: url('assets/fonts/PlexMono-SemiBold.woff2') format('woff2'); }

  :root {
    /* White theme (@carbon/themes) */
    --cds-background:        #ffffff;   /* background                         */
    --cds-layer-01:          #f4f4f4;   /* layer-01: tiles, steps, code       */
    --cds-layer-accent-01:   #e0e0e0;   /* layer-accent-01: table header      */
    --cds-border-subtle-00:  #e0e0e0;   /* border-subtle-00: dividers         */
    --cds-border-subtle-01:  #c6c6c6;   /* border-subtle-01: rules on layer   */
    --cds-border-strong-01:  #8d8d8d;   /* border-strong-01: outlined boxes   */
    --cds-text-primary:      #161616;   /* text-primary                       */
    --cds-text-secondary:    #525252;   /* text-secondary                     */
    --cds-text-on-color:     #ffffff;   /* text-on-color                      */
    --cds-icon-secondary:    #525252;   /* icon-secondary: connectors         */
    --cds-link-primary:      #0f62fe;   /* link-primary                       */
    --cds-background-brand:  #0f62fe;   /* background-brand (Blue 60)         */
    --cds-background-inverse:#393939;   /* background-inverse                 */

    /* Gray 100 / Gray 90 themes */
    --cds-g100-background:   #161616;
    --cds-g90-background:    #262626;
    --cds-dark-text-primary: #f4f4f4;
    --cds-dark-text-secondary:#c6c6c6;
    --cds-dark-link-primary: #78a9ff;
    --cds-dark-border-subtle:#525252;

    /* Category accents: Blue 60 + Carbon categorical palette 01-04 (strokes) */
    --cds-accent-blue:       #0f62fe;   /* Blue 60                            */
    --cds-accent-purple:     #6929c4;   /* Purple 70 (categorical 01)         */
    --cds-accent-cyan:       #1192e8;   /* Cyan 50   (categorical 02)         */
    --cds-accent-teal:       #005d5d;   /* Teal 70   (categorical 03)         */
    --cds-accent-magenta:    #9f1853;   /* Magenta 70 (categorical 04)        */
    /* …and the 10-grade tint of the same hue (fills) */
    --cds-tint-blue:         #edf5ff;   /* Blue 10                            */
    --cds-tint-purple:       #f6f2ff;   /* Purple 10                          */
    --cds-tint-cyan:         #e5f6ff;   /* Cyan 10                            */
    --cds-tint-teal:         #d9fbfb;   /* Teal 10                            */
    --cds-tint-magenta:      #fff0f7;   /* Magenta 10                         */

    /* Status (support-* and notification-background-* tokens) */
    --cds-support-info:      #0043ce;
    --cds-support-warning:   #f1c21b;
    --cds-support-success:   #24a148;
    --cds-support-error:     #da1e28;
    --cds-notification-info:    #edf5ff;
    --cds-notification-warning: #fcf4d6;
    --cds-notification-success: #defbe6;
    --cds-notification-error:   #fff1f1;
  }

  /* ── Base slide (White theme) ──────────────────────────────────────────────── */
  /* Body text 20/28 (size and leading of heading-03, Regular weight).          */
  /* Content is top-anchored: titles sit at the same place on every slide.      */
  section {
    font-family: 'Plex Sans', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--cds-background);
    color: var(--cds-text-primary);
    padding: 48px 64px;
    font-size: 20px;
    line-height: 1.4;
    letter-spacing: 0;
    align-content: flex-start;   /* the Marp default theme centres content */
    justify-content: flex-start;
  }

  /* ── Headings (Carbon productive headings, text-primary) ───────────────────── */
  /* h1 heading-06 42/50 Light · h2 heading-05 32/40 · h3 heading-04 28/36 ·     */
  /* h4 heading-03 20/28 (the element-styles mapping). Sentence case; neutral.   */
  /* The `compact` slide class takes h3 down to 20/28 (see the end of the file). */
  h1, h2, h3, h4 { color: var(--cds-text-primary); letter-spacing: 0; }
  h1 { font-size: 42px; font-weight: 300; line-height: 1.2; margin: 0 0 16px; }
  h2 { font-size: 32px; font-weight: 400; line-height: 1.25; margin: 0 0 24px; }
  h3 { font-size: 28px; font-weight: 400; line-height: 1.29; margin: 0 0 8px; }
  h4 { font-size: 20px; font-weight: 400; line-height: 1.4; margin: 0 0 8px; }

  /* ── Inline elements (element-styles: bold-text, italic-text, anchor, mark) ── */
  /* Running text stays neutral: bold is weight only, colour is for links.      */
  strong, b { font-weight: 600; color: inherit; }
  em        { font-style: italic; color: inherit; }
  a         { color: var(--cds-link-primary); text-decoration: underline; }
  mark      { background: #fddc69; color: #000000; padding: 0 2px; }   /* Yellow 20 */

  /* ── Lists (element-styles: unordered-list, ordered-list) ──────────────────── */
  /* "–" markers, "▪" when nested; numbered lists decimal → lower-alpha.        */
  ul { list-style-type: "–"; }
  ul ul, ol ul { list-style-type: "▪"; }
  ol { list-style-type: decimal; }
  ol ol { list-style-type: lower-alpha; }
  li { padding-left: 8px; }

  /* ── Code (element-styles: code; Plex Mono code-02 14/20, layer surface) ──── */
  code {
    font-family: 'Plex Mono', Menlo, 'DejaVu Sans Mono', Consolas, Courier, monospace;
    font-size: 0.875em;
    background: var(--cds-layer-01);
    color: var(--cds-text-primary);
    border-radius: 1px;
    padding: 0 2px;
  }
  pre {
    background: var(--cds-layer-01);
    border-radius: 0;
    padding: 16px;
    margin: 8px 0 16px;
  }
  pre code { font-size: 14px; line-height: 1.43; letter-spacing: 0.32px; padding: 0; background: transparent; }

  /* ── Footer and pagination (label-01 size, text-secondary) ─────────────────── */
  footer {
    left: 64px;
    bottom: 24px;
    font-size: 12px;
    letter-spacing: 0.32px;
    color: var(--cds-text-secondary);
  }
  section::after {
    right: 64px;
    bottom: 24px;
    font-size: 12px;
    letter-spacing: 0.32px;
    color: var(--cds-text-secondary);
  }

  /* ── Horizontal rule (element-styles: horizontal-rule, kind subtle) ────────── */
  hr { border: none; height: 1px; padding: 0; background: var(--cds-border-subtle-00); margin: 24px 0; }

  /* ── OPTIONAL: ruled content slide (.ruled) ────────────────────────────────── */
  /* Usage: <!-- _class: ruled -->  · 8px Blue 60 left edge (brand accent).      */
  section.ruled { border-left: 8px solid var(--cds-background-brand); padding-left: 56px; }

  /* ══ Covers (lead) ═════════════════════════════════════════════════════════ */
  /* lead        Gray 10 theme   ·  lead plain  White theme                      */
  /* lead dark   Gray 100 theme                                                   */
  /* Title heading-07 54/64 Light over 12 of 16 columns (75%), left aligned;    */
  /* subtitle heading-04 28/36 in text-secondary; author block at the bottom.   */
  section.lead {
    background: var(--cds-layer-01);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    padding-top: 64px;
  }
  section.lead.plain { background: var(--cds-background); }
  section.lead h1 {
    font-size: 54px;
    font-weight: 300;
    line-height: 1.19;
    max-width: 75%;
    margin-bottom: 16px;
  }
  section.lead h2 {
    font-size: 28px;
    font-weight: 400;
    line-height: 1.29;
    color: var(--cds-text-secondary);
    max-width: 75%;
  }

  /* ── COMPONENT: author block on the cover (.lead-author) ───────────────────── */
  /* Name (SemiBold) / role / contact, body-02 16/24, pushed to the bottom.     */
  .lead-author {
    margin-top: auto;
    font-size: 16px;
    line-height: 1.5;
    color: var(--cds-text-primary);
  }
  .lead-author strong { display: block; font-weight: 600; }
  .lead-author em     { display: block; font-style: normal; color: var(--cds-text-secondary); }

  /* ══ Dark slides: Gray 100 (lead dark, section, end) and Gray 90 (backup) ═══ */
  section.lead.dark, section.section, section.end { background: var(--cds-g100-background); }
  section.backup { background: var(--cds-g90-background); }
  section.lead.dark, section.section, section.backup, section.end {
    color: var(--cds-dark-text-primary);
  }
  section.lead.dark h1, section.section h1, section.backup h1, section.end h1,
  section.lead.dark h3, section.section h3, section.backup h3, section.end h3,
  section.lead.dark strong, section.section strong, section.backup strong, section.end strong,
  section.lead.dark .lead-author, section.end .lead-author {
    color: var(--cds-dark-text-primary);
  }
  section.lead.dark h2, section.section h2, section.backup h2, section.end h2,
  section.lead.dark p, section.section p, section.backup p, section.end p,
  section.lead.dark em, section.section em, section.backup em, section.end em,
  section.lead.dark .small, section.section .small, section.backup .small, section.end .small {
    color: var(--cds-dark-text-secondary);
  }
  section.lead.dark a, section.section a, section.backup a, section.end a {
    color: var(--cds-dark-link-primary);
  }

  /* ── SLIDE CLASS: section (divider, Gray 100) ──────────────────────────────── */
  /* ── SLIDE CLASS: backup  (appendix opener, Gray 90) ───────────────────────── */
  /* h1 heading-07 54/64 Light · h2 heading-04 28/36 · vertically centred.      */
  section.section, section.backup {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  section.section h1, section.backup h1, section.end h1 {
    margin-bottom: 16px;
    font-size: 54px; font-weight: 300; line-height: 1.19; max-width: 75%;
  }
  section.section h2, section.backup h2, section.end h2 {
    font-size: 28px; font-weight: 400; line-height: 1.29; max-width: 75%;
  }

  /* ── SLIDE CLASS: bk (backup content slide) ────────────────────────────────── */
  /* White theme with a 4px border-strong top edge: marks appendix material.    */
  section.bk { border-top: 4px solid var(--cds-border-strong-01); padding-top: 44px; }

  /* ── SLIDE CLASS: end (closing slide, Gray 100) ────────────────────────────── */
  /* Mirrors the cover: a short closing line (# Thank you) at the top, optional */
  /* subtitle, contact block (.lead-author) at the bottom.                      */
  section.end {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    padding-top: 64px;
  }

  /* ── SLIDE CLASS: toc (contents) ───────────────────────────────────────────── */
  /* Title heading-06 42/50 Light; items as a structured list: 20/28 rows       */
  /* separated by 1px border-subtle, number in Blue 60.                         */
  section.toc h1 { margin-bottom: 32px; }
  /* toc-grid: items fill column-first (top→bottom in col 1, then col 2).       */
  /* Default: 3 rows per column (6 items = 3 + 3). For another split set the    */
  /* rows inline: <div class="toc-grid" style="grid-template-rows: repeat(4, auto)"> */
  /* The PPTX export reads the same value (inline style first, then this rule). */
  .toc-grid {
    display: grid;
    grid-template-rows: repeat(3, auto);
    grid-auto-flow: column;
    grid-auto-columns: 1fr;
    gap: 0 32px;
  }
  .toc-item {
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid var(--cds-border-subtle-00);
    font-size: 20px;
    line-height: 1.4;
  }
  .toc-item .toc-num   { min-width: 32px; color: var(--cds-text-secondary); }
  .toc-item .toc-title { color: var(--cds-text-primary); }

  /* ── Footer hidden on cover, contents, divider, backup opener and end ──────── */
  section.lead footer, section.toc footer, section.section footer,
  section.backup footer, section.end footer { display: none; }

  /* ══ Layout: Carbon 2x grid gutters ════════════════════════════════════════ */
  /* .cols   two columns, 32px gutter (wide gutter mode)                        */
  /* .cols3  three columns, 16px gutter (narrow gutter mode)                    */
  .cols  { display: grid; grid-template-columns: 1fr 1fr;     gap: 32px; }
  .cols3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }

  /* ── COMPONENT: card (.card) — Carbon tile ─────────────────────────────────── */
  /* layer-01 surface, 16px padding, square corners, body-02 16/24 text.         */
  /* A 4px top stroke codes the category: Blue 60 by default; .purple .cyan     */
  /* .teal .magenta use the categorical palette. .sm = body-01 14/20, 12/16 pad. */
  .card {
    background: var(--cds-layer-01);
    border-top: 4px solid var(--cds-accent-blue);
    padding: 16px;
    font-size: 16px;
    line-height: 1.5;
  }
  .card h3         { margin: 0 0 8px; font-size: 28px; font-weight: 400; line-height: 1.29; }
  .card.cyan       { border-top-color: var(--cds-accent-cyan); }
  .card.teal       { border-top-color: var(--cds-accent-teal); }
  .card.purple     { border-top-color: var(--cds-accent-purple); }
  .card.magenta    { border-top-color: var(--cds-accent-magenta); }
  .card.sm         { font-size: 14px; line-height: 1.43; letter-spacing: 0.16px; padding: 12px 16px; }
  .card.sm h3      { font-size: 16px; font-weight: 600; line-height: 1.5; letter-spacing: 0; }

  /* ── COMPONENT: KPI (.kpi / .kpi-label) ────────────────────────────────────── */
  /* Number heading-07 54/64 Light, text-primary; label body-02 text-secondary. */
  .kpi       { font-size: 54px; font-weight: 300; line-height: 1.19; color: var(--cds-text-primary); }
  .kpi-label { font-size: 16px; line-height: 1.5; color: var(--cds-text-secondary); }

  /* ── COMPONENT: tag (.pill) — Carbon Tag ───────────────────────────────────── */
  /* tag-background-* / tag-color-* tokens, fully rounded. Default blue;        */
  /* modifiers .cyan .teal .purple .magenta .green .red .gray.                  */
  .pill {
    display: inline-block;
    background: #d0e2ff;
    color: #0043ce;
    border-radius: 24px;
    padding: 4px 12px;
    font-size: 16px;
    line-height: 1.5;
    font-weight: 400;
  }
  .pill.cyan    { background: #bae6ff; color: #00539a; }
  .pill.teal    { background: #9ef0f0; color: #005d5d; }
  .pill.purple  { background: #e8daff; color: #6929c4; }
  .pill.magenta { background: #ffd6e8; color: #9f1853; }
  .pill.green   { background: #a7f0ba; color: #0e6027; }
  .pill.red     { background: #ffd7d9; color: #a2191f; }
  .pill.gray    { background: #e0e0e0; color: #161616; }

  /* ── Blockquote (element-styles: block-quotation) ──────────────────────────── */
  /* quotation-01 at the lg breakpoint: Plex Serif 24/32 Regular,                */
  /* indented 40px (spacing-08), max 50ch, no rule and no fill.                  */
  blockquote {
    font-family: 'Plex Serif', Georgia, Times, serif;
    font-size: 24px;
    font-weight: 400;
    line-height: 1.33;
    font-style: normal;
    color: var(--cds-text-primary);
    background: transparent;
    border: 0;
    padding: 0;
    margin: 24px 0 24px 40px;
    max-width: 50ch;
  }
  blockquote p { margin: 0; }

  /* ── COMPONENT: small text (.small) — helper text 14/20, text-secondary ────── */
  .small { font-size: 14px; line-height: 1.43; letter-spacing: 0.16px; color: var(--cds-text-secondary); }

  /* ── COMPONENT: band (.band) — Carbon inline notification (low contrast) ───── */
  /* notification-background-* fill with a 3px support-* left border, the 20px  */
  /* status icon of @carbon/icons 11.92.0 (Apache-2.0) 16px from the outer edge, */
  /* body-02 16/24 text from 52px; <b> is the notification title (SemiBold).     */
  /* Variants: (default) info · .warn · .success · .error                        */
  .band {
    position: relative;
    background: var(--cds-notification-info);
    border-left: 3px solid var(--cds-support-info);
    padding: 12px 16px 12px 49px;
    font-size: 16px;
    line-height: 1.5;
    color: var(--cds-text-primary);
    text-align: left;
    margin-top: 16px;
  }
  .band::before {
    content: "";
    position: absolute;
    left: 13px;
    top: 14px;
    width: 20px;
    height: 20px;
    background: url("data:image/svg+xml,%3Csvg fill=%22%230043ce%22 xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cpath fill=%22%23ffffff%22 d=%22M16,8a1.5,1.5,0,1,1-1.5,1.5A1.5,1.5,0,0,1,16,8Zm4,13.875H17.125v-8H13v2.25h1.875v5.75H12v2.25h8Z%22 data-icon-path=%22inner-path%22/%3E%3Cpath d=%22M16,2A14,14,0,1,0,30,16,14,14,0,0,0,16,2Zm0,6a1.5,1.5,0,1,1-1.5,1.5A1.5,1.5,0,0,1,16,8Zm4,16.125H12v-2.25h2.875v-5.75H13v-2.25h4.125v8H20Z%22/%3E%3C/svg%3E") center / contain no-repeat;
  }
  .band.warn::before    { background-image: url("data:image/svg+xml,%3Csvg fill=%22%23f1c21b%22 xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cpath fill=%22%23000000%22 d=%22M16,26a1.5,1.5,0,1,1,1.5-1.5A1.5,1.5,0,0,1,16,26Zm-1.125-5h2.25V12h-2.25Z%22 data-icon-path=%22inner-path%22/%3E%3Cpath d=%22M16.002,6.1714h-.004L4.6487,27.9966,4.6506,28H27.3494l.0019-.0034ZM14.875,12h2.25v9h-2.25ZM16,26a1.5,1.5,0,1,1,1.5-1.5A1.5,1.5,0,0,1,16,26Z%22/%3E%3Cpath d=%22M29,30H3a1,1,0,0,1-.8872-1.4614l13-25a1,1,0,0,1,1.7744,0l13,25A1,1,0,0,1,29,30ZM4.6507,28H27.3493l.002-.0033L16.002,6.1714h-.004L4.6487,27.9967Z%22/%3E%3C/svg%3E"); }
  .band.success::before { background-image: url("data:image/svg+xml,%3Csvg fill=%22%2324a148%22 xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cpath d=%22M16,2A14,14,0,1,0,30,16,14,14,0,0,0,16,2ZM14,21.5908l-5-5L10.5906,15,14,18.4092,21.41,11l1.5957,1.5859Z%22/%3E%3Cpath fill=%22%23ffffff%22 d=%22M14 21.591 9 16.591 10.591 15 14 18.409 21.41 11 23.005 12.585 14 21.591z%22 data-icon-path=%22inner-path%22/%3E%3C/svg%3E"); }
  .band.error::before   { background-image: url("data:image/svg+xml,%3Csvg fill=%22%23da1e28%22 xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Cpath fill=%22%23ffffff%22 d=%22M14.9 7.2H17.1V24.799H14.9z%22 data-icon-path=%22inner-path%22 transform=%22rotate%28-45 16 16%29%22/%3E%3Cpath d=%22M16,2A13.914,13.914,0,0,0,2,16,13.914,13.914,0,0,0,16,30,13.914,13.914,0,0,0,30,16,13.914,13.914,0,0,0,16,2Zm5.4449,21L9,10.5557,10.5557,9,23,21.4448Z%22/%3E%3C/svg%3E"); }
  .band b          { font-weight: 600; color: var(--cds-text-primary); }
  .band.warn       { background: var(--cds-notification-warning); border-left-color: var(--cds-support-warning); }
  .band.success    { background: var(--cds-notification-success); border-left-color: var(--cds-support-success); }
  .band.error      { background: var(--cds-notification-error);   border-left-color: var(--cds-support-error); }

  /* ── COMPONENT: flow diagram (.flow / .node / .arrow) ──────────────────────── */
  /* .node   outlined box: 1px border-strong, white fill; label heading-compact-02 */
  /*         16/22 SemiBold, detail body-compact-01 14/18 text-secondary.        */
  /*         Category variants .cyan .teal .purple .magenta: tint fill + stroke. */
  /*         Filled .hero (background-brand) and .dark (background-inverse):     */
  /*         ONLY to highlight a single node.                                    */
  /* .arrow  connector "▸" (or "⇄"), icon-secondary; .obs = Magenta 70 path.    */
  .flow  {
    display: flex;
    align-items: stretch;
    justify-content: center;
    gap: 8px;
    margin: 16px 0;
    flex-wrap: nowrap;
  }
  .node  {
    flex: 1;
    background: var(--cds-background);
    border: 1px solid var(--cds-border-strong-01);
    padding: 12px 8px;
    text-align: center;
    font-size: 14px;
    line-height: 1.29;
    letter-spacing: 0.16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .node b          { color: var(--cds-text-primary); font-size: 16px; font-weight: 600; line-height: 1.38; letter-spacing: 0; display: block; }
  .node small      { color: var(--cds-text-secondary); font-size: 14px; }
  .node.cyan       { border-color: var(--cds-accent-cyan);    background: var(--cds-tint-cyan); }
  .node.teal       { border-color: var(--cds-accent-teal);    background: var(--cds-tint-teal); }
  .node.purple     { border-color: var(--cds-accent-purple);  background: var(--cds-tint-purple); }
  .node.magenta    { border-color: var(--cds-accent-magenta); background: var(--cds-tint-magenta); }
  .node.hero       { border-color: var(--cds-background-brand);   background: var(--cds-background-brand); }
  .node.dark       { border-color: var(--cds-background-inverse); background: var(--cds-background-inverse); }
  .node.hero b, .node.hero small, .node.dark b, .node.dark small { color: var(--cds-text-on-color); }
  .arrow     { display: flex; align-items: center; color: var(--cds-icon-secondary);
               font-size: 24px; line-height: 1; padding: 0 4px; }
  /* Colour modifiers, from the same category accents as the nodes; .obs is the   */
  /* original name of the magenta monitoring path and stays as an alias.          */
  .arrow.blue    { color: var(--cds-accent-blue); }
  .arrow.cyan    { color: var(--cds-accent-cyan); }
  .arrow.teal    { color: var(--cds-accent-teal); }
  .arrow.purple  { color: var(--cds-accent-purple); }
  .arrow.magenta, .arrow.obs { color: var(--cds-accent-magenta); }

  /* ── COMPONENT: process diagram (.process / .step) ─────────────────────────── */
  /* Contiguous tiles (layer-01) with a 4px category stroke on top.             */
  /* .step-num 28/36 Light · <b> heading-compact-01 14/18 SemiBold ·            */
  /* <small> 14/18 text-secondary. Variants: .blue .cyan .teal .purple .magenta  */
  /* (tint fill), .hero (background-brand, ONLY to highlight one step).         */
  .process {
    display: flex;
    align-items: stretch;
    gap: 1px;
    margin: 16px 0;
  }
  .step {
    flex: 1;
    background: var(--cds-layer-01);
    border-top: 4px solid var(--cds-accent-blue);
    padding: 12px 16px 16px;
    font-size: 14px;
    line-height: 1.29;
    letter-spacing: 0.16px;
  }
  .step .step-num { display: block; font-size: 28px; font-weight: 300; line-height: 1.29;
                    color: var(--cds-text-primary); margin-bottom: 8px; letter-spacing: 0; }
  .step b         { display: block; color: var(--cds-text-primary); font-size: 14px; font-weight: 600; margin-bottom: 4px; }
  .step small     { color: var(--cds-text-secondary); font-size: 14px; }
  .step.blue    { border-top-color: var(--cds-accent-blue);    background: var(--cds-tint-blue); }
  .step.cyan    { border-top-color: var(--cds-accent-cyan);    background: var(--cds-tint-cyan); }
  .step.teal    { border-top-color: var(--cds-accent-teal);    background: var(--cds-tint-teal); }
  .step.purple  { border-top-color: var(--cds-accent-purple);  background: var(--cds-tint-purple); }
  .step.magenta { border-top-color: var(--cds-accent-magenta); background: var(--cds-tint-magenta); }
  .step.hero    { border-top-color: var(--cds-background-brand); background: var(--cds-background-brand); }
  .step.hero .step-num, .step.hero b, .step.hero small { color: var(--cds-text-on-color); }

  /* ── Tables (element-styles: table, kind data-table) ───────────────────────── */
  /* Full width; header layer-accent-01, heading-compact-02 16/22 SemiBold      */
  /* text-primary; cells layer-01, body-compact-02 16/22 text-secondary;        */
  /* 1px border-subtle-01 under every row; rows of the Carbon data table size lg */
  /* (48px; padding spacing-04 / spacing-05); the `compact` slide class switches */
  /* to size md (40px). The `table` prefix outranks the Marp default theme       */
  /* (`table td { padding: 6px 13px; border }`).                                 */
  table { display: table; width: 100%; font-size: 16px; line-height: 1.38;
          border-collapse: collapse; border-spacing: 0; margin: 16px 0; }
  table tr { background: transparent; border: 0; }
  table th, table td { border: 0; border-bottom: 1px solid var(--cds-border-subtle-01);
                       box-sizing: border-box; height: 48px; padding: 12px 16px;
                       text-align: left; vertical-align: top; }
  table th { background: var(--cds-layer-accent-01); color: var(--cds-text-primary); font-weight: 600; }
  table td { background: var(--cds-layer-01); color: var(--cds-text-secondary); }

  /* ── COMPONENT: pictogram (img.pictogram) ──────────────────────────────────── */
  /* Carbon pictograms (SVG, single colour via CSS filter), trimmed on the left */
  /* so they align with the text below. Sizes on the 8px grid: .sm 48 (Carbon  */
  /* minimum) · default 80 · .lg 120.                                           */
  /* Colour: default icon-primary Gray 100 on light slides · .white (Gray 10)   */
  /* on dark slides (lead dark, section, backup, end) · .blue = Blue 60 accent  */
  /* on light slides only. .black is kept as an alias of the default.           */
  img.pictogram {
    width: 80px;
    height: 80px;
    display: block;
    margin-bottom: 16px;
    object-fit: contain;
    object-position: left center;
    filter: brightness(0) invert(8.6%);
  }
  img.pictogram.lg { width: 120px; height: 120px; }
  img.pictogram.sm { width: 48px;  height: 48px; margin-bottom: 8px; }
  img.pictogram.blue  { filter: invert(22%) sepia(92%) saturate(2800%) hue-rotate(214deg) brightness(98%) contrast(103%); }
  img.pictogram.white { filter: brightness(0) invert(95.7%); }
  img.pictogram.black { filter: brightness(0) invert(8.6%); }

  /* ══ SLIDE CLASS: compact — the space-saving sizes ════════════════════════ */
  /* Usage: <!-- _class: compact --> (combines with others: `bk compact`).        */
  /* For dense slides only: h3 goes from heading-04 28/36 to heading-03 20/28   */
  /* and tables from row size lg (48px) to md (40px). Both are Carbon sizes.    */
  section.compact h3, section.compact .card h3 { font-size: 20px; line-height: 1.4; }
  section.compact .card.sm h3 { font-size: 16px; line-height: 1.5; }
  section.compact table th, section.compact table td { height: 40px; padding: 8px 16px; }
---

<!-- ═══════════════════════════════════════════════════════════════════════════ -->
<!-- EXAMPLE 05 — Flow Diagrams (.flow, .node variants, .arrow and its colours)  -->
<!-- ═══════════════════════════════════════════════════════════════════════════ -->

<!-- Pattern A: Linear five-node flow — outlined node colour variants -->

## Linear flow — outlined node colour variants

<div class="flow">
  <div class="node"><b>Source</b><small>system · app · DB</small></div>
  <div class="arrow">▸</div>
  <div class="node cyan"><b>Platform</b><small>core component</small></div>
  <div class="arrow">▸</div>
  <div class="node teal"><b>Integration</b><small>connectors · API</small></div>
  <div class="arrow">▸</div>
  <div class="node purple"><b>AI / Agent</b><small>decisions · actions</small></div>
  <div class="arrow">▸</div>
  <div class="node magenta"><b>Destination</b><small>users · analytics</small></div>
</div>

<div class="band"><b>Pattern:</b> outlined nodes, one colour per functional category · filled <code>.node.hero</code> / <code>.node.dark</code> only to highlight a single node</div>

---

<!-- Pattern B: Bidirectional arrow and a coloured arrow (.arrow.magenta) -->

## Flow with observability — bidirectional arrows

<div class="flow">
  <div class="node"><b>System A</b><small>event source</small></div>
  <div class="arrow">⇄</div>
  <div class="node cyan"><b>Event Bus</b><small>routing · filtering</small></div>
  <div class="arrow">▸</div>
  <div class="node teal"><b>Consumer</b><small>processing · storage</small></div>
  <div class="arrow magenta">▸</div>
  <div class="node magenta"><b>Observability</b><small>metrics · logs · traces</small></div>
</div>

<div class="cols">
<div>

**⇄ Bidirectional arrow**
Use `.arrow` with `⇄` for request/response patterns or synchronous integrations.

</div>
<div>

**Magenta observability node**
Use `.node.magenta` + `.arrow.magenta` for monitoring, tracing, and alerting paths.

</div>
</div>

---

<!-- Pattern C: Architecture diagram with .band and two-column context -->

## End-to-end architecture — hybrid platform

<div class="flow">
  <div class="node"><b>Sources</b><small>systems · data · events</small></div>
  <div class="arrow">▸</div>
  <div class="node cyan"><b>Core Platform</b><small>processing · governance</small></div>
  <div class="arrow">▸</div>
  <div class="node teal"><b>Integration</b><small>connectors · APIs</small></div>
  <div class="arrow">▸</div>
  <div class="node purple"><b>AI & Automation</b><small>agents · decisions</small></div>
  <div class="arrow">▸</div>
  <div class="node magenta"><b>Consumers</b><small>apps · analytics · users</small></div>
</div>

<div class="cols">
<div>

**What happens**
- Sources produce real-time and batch data
- The platform processes and governs the flow
- Integration distributes to consumers

</div>
<div>

**Why it matters**
- **Modular** and scalable architecture
- Single backbone — **single source of truth**
- Supports both **batch and streaming** patterns

</div>
</div>

<div class="band"><b>Guiding principle:</b> each block is decoupled and replaceable · no vendor lock-in</div>
