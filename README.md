# IBC2026 vendor scan: build output

This folder is the output of the scan, dropped into the site repo. The site's own home page and layer sit
outside it and are maintained separately, so nothing here writes to the repo root index.

## What this drop contains

```
/ibc2026/index.html        the scan, self-contained apart from Google Fonts
/ibc2026/data.json         the underlying records
/ibc2026/hall5.json        the official Hall 5 exhibitor list used for cross-referencing
/ibc2026/sources/index.html  every source, organised by what it was used for
/favicon.svg               the four-bar mark, also inlined in each page
/bump.py                   version stamp tool
/version-log.json          history of stamped versions
```

`/ibc2026/index.html` ends with the Cloudflare Web Analytics beacon and a deferred `whatsnew.js`, which is
expected to be supplied by the site layer rather than by this build.

## Conventions

Pages are light only. There is no `prefers-color-scheme: dark` block and each page sets
`color-scheme: light`.

Run `python3 bump.py [major|minor|patch] "what changed"` before a drop. The stamp on the page carries the
version and the date; the note goes to `version-log.json` and never onto the page. Patch for corrections to
existing records, minor for new records or a new field, major for a change in what the scan covers.
