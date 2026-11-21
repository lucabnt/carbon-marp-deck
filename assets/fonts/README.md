# Plex fonts

The typeface of the Carbon Design System, bundled so that every deck renders in Plex even
where it is not installed.

| File | Face | Used for |
|---|---|---|
| `PlexSans-Light.woff2`, `-LightItalic` | Plex Sans 300 | titles from 42 px, KPI and step numbers |
| `PlexSans-Regular.woff2`, `-Italic` | Plex Sans 400 | body text |
| `PlexSans-SemiBold.woff2`, `-SemiBoldItalic` | Plex Sans 600 | bold text, labels, table headers |
| `PlexSerif-Regular.woff2`, `-Italic`, `-SemiBold` | Plex Serif | pull quotes |
| `PlexMono-Regular.woff2`, `-SemiBold` | Plex Mono | code |

Source: the official Plex release packages (Sans 1.3.6, Serif 2.0.0, Mono 2.5.0), "complete"
woff2 files. The fonts are unmodified; only the file names are shortened. Licence: SIL Open Font
License 1.1, see [`LICENSE-OFL.txt`](LICENSE-OFL.txt) and the copyright notice in
[`NOTICE`](../../NOTICE). "Plex" is a Reserved Font Name: the fonts must not be modified under
that name.

## How they are used

- `themes/carbon.css` declares them with `@font-face` under the family names `Plex Sans`,
  `Plex Serif` and `Plex Mono`.
- `scripts/new_deck.py` and `scripts/export_deck.py` copy this folder to `assets/fonts/` next to
  the deck, because the theme loads the files with a path relative to the deck.
- **PDF**: always rendered in Plex.
- **PPTX**: PowerPoint cannot use web fonts. The PPTX names the installed Plex families (the
  mapping is `INSTALLED_FONT_NAMES` in `scripts/toolchain.py`), so the machine that opens it needs
  the Plex desktop fonts (TTF or OTF) installed. `python scripts/check_env.py` reports whether
  they are.
