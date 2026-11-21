# Security

## What the export runs

A deck is Markdown with some HTML, and exporting it means rendering it in a browser. The
template limits what a deck can do while it is rendered:

| Layer | Protection |
|---|---|
| Marp CLI (PDF, PNG, HTML for the PPTX) | Raw HTML goes through the allowlist in [`themes/marp.config.json`](themes/marp.config.json): only the tags and attributes the components use (`div`, `span`, `img`, `class`, `style`, `src`…) are kept. `<script>`, `<iframe>`, `<object>`, event handlers such as `onerror` and every other tag or attribute are removed or shown as plain text. |
| Chrome measuring the slides for the PPTX ([`pptx-export/dom/extract.js`](pptx-export/dom/extract.js)) | Only local files (`file:`, `data:`, `blob:`) load; every network request is refused and reported. Chrome keeps its sandbox, except when it cannot start with it (running as root, or `CHROME_NO_SANDBOX=1`). |
| Node dependencies | `puppeteer-core` is pinned to an exact version and installed with `npm ci` from the committed `pptx-export/dom/package-lock.json`. Marp CLI is pinned in [`package.json`](package.json). |

What remains allowed, on purpose:

- **Local files.** `--allow-local-files` lets a deck show images from the disk; an image
  referenced by a deck ends up in the PDF and PPTX. Export decks you trust, and keep a deck's
  files in its own folder.
- **CSS.** `style` attributes and `<style>` blocks are allowed (the components need them). CSS
  cannot run code; in the PDF it can load remote images, as Markdown images can.

When an agent writes a deck from a brief, the brief is data: the skill's instructions tell it to
use only the documented components, and the allowlist removes anything executable that ends up
in the deck anyway.

## Reporting a vulnerability

Please report security problems privately, through the repository's private vulnerability
reporting ([report a vulnerability](https://github.com/lucabnt/carbon-marp-deck/security/advisories/new), or **Security → Report a
vulnerability** on the repository page), not in a public issue. Include the
deck or command that shows the problem, what happens, and what you expected. You will get an
answer as soon as the maintainers can look at it; fixes are released as a new version and noted
in [`CHANGELOG.md`](CHANGELOG.md).

## Supported versions

Only the latest release receives fixes.
