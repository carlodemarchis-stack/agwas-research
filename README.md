# research.aguywithascarf.com

Static research site for A Guy With A Scarf. No build step, no dependencies.

## Structure

```
/CNAME              research.aguywithascarf.com
/.nojekyll          stops GitHub running Jekyll over the files
/index.html         index of research items
/ibc2026/index.html the IBC2026 vendor scan (self-contained, single file)
/ibc2026/data.json  the underlying records, 98 companies
```

## Deploying

1. Create a public repo, for example `agwas-research`.
2. Copy the contents of this folder into the repo root and push to `main`.
3. Repo Settings → Pages → Source: "Deploy from a branch", Branch: `main`, Folder: `/ (root)`.
4. Under "Custom domain" enter `research.aguywithascarf.com` and save. Tick "Enforce HTTPS" once the
   certificate is issued, which usually takes a few minutes and can take up to an hour.
5. At your DNS provider add a CNAME record:
   `research` → `<your-github-username>.github.io.`
   Do not add an A record; the CNAME alone is correct for a subdomain.

The page lands at `https://research.aguywithascarf.com/ibc2026/`.

## Updating

The scan is a single self-contained HTML file. Replace `/ibc2026/index.html` and push. Pages redeploys
in under a minute. `data.json` is a copy of the records for reuse and is not read by the page.

## Note on access

GitHub Pages serves everything publicly. There is no way to gate a page here, so if any part of this is
meant for paying subscribers, that version needs to live somewhere with access control.
