# Contributing

Thanks for helping. This project is an unofficial, community template: contributions must use
only open-source material (Carbon tokens and assets under Apache-2.0, the Plex fonts under the OFL)
and must not add logos, brand assets or content from proprietary templates.

## Setup

```bash
pip install -r pptx-export/requirements.txt
python scripts/check_env.py            # Node.js 18+, Chrome or Edge, Python packages, fonts
```

Maintainer tools also need `pip install pyyaml pymupdf` (only for `tools/build_pictograms.py`).

## Where things live

| Change | Edit | Then run |
|---|---|---|
| Colours, type, spacing, components | [`themes/carbon.css`](themes/carbon.css) — take every value from a Carbon token and name it in a comment | `python scripts/sync_css.py`, `python tools/build_examples.py` |
| Allowed raw HTML | [`themes/marp.config.json`](themes/marp.config.json) | the checks below; explain the need in the pull request |
| Agent workflow, content rules | [`SKILL.md`](SKILL.md) | keep it short: details belong in `references/` |
| Snippets and design reference | [`references/`](references/) | — |
| PPTX converter | [`pptx-export/dom/`](pptx-export/dom/) | the checks below, and `tools/check_fidelity.py` if you have PowerPoint |
| Pictogram library | [`tools/pictogram_exclude.txt`](tools/pictogram_exclude.txt), `CARBON_VERSION` in [`tools/build_pictograms.py`](tools/build_pictograms.py) | `python tools/build_pictograms.py` |
| A departure from Carbon | the code, and the "Divergences from Carbon" section of [`references/style-guide.md`](references/style-guide.md) with the reason | — |

## Checks

```bash
python tools/check_examples.py             # lint, CSS in sync, PPTX structure vs tests/baseline.json
python tools/check_examples.py --update    # after an intended change: review the renders first
python tools/check_fidelity.py             # PPTX vs PDF, slide by slide (Windows + PowerPoint)
```

`check_examples.py` runs in CI on every pull request. When a converter or theme change alters
the number of shapes or the speaker notes, look at the regenerated examples, then update the
baseline in the same pull request and say why.

## Pull requests

- One topic per pull request; describe what changes visually and attach a before/after render
  for theme or converter changes.
- Regenerate `examples/pdf` and `examples/pptx` with `python tools/build_examples.py` on a
  machine with the Plex fonts installed when the rendering changes.
- Add a line to the "Unreleased" section of [`CHANGELOG.md`](CHANGELOG.md).
- Contributions are accepted under the [Apache License 2.0](LICENSE).

Security problems: see [`SECURITY.md`](SECURITY.md) instead of opening an issue.
