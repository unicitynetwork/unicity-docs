# unicity-docs

Aggregated documentation portal for the Unicity stack, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and the [mkdocs-multirepo-plugin](https://github.com/jdoiro3/mkdocs-multirepo-plugin). Content is pulled directly from each source repository at build time, so this repo holds only configuration and a few landing pages, never copies of upstream docs.

## What gets aggregated

| Section | Source repo | Imported content |
| --- | --- | --- |
| Unicity Protocol | landing pages in this repo | Overview, Research Papers (links to release PDFs) |
| State Transition SDK (JS) | `unicitynetwork/state-transition-sdk-js` | README, token protocol spec |
| AgentSphere / Sphere SDK | `unicity-sphere/sphere-sdk` | README, ARCHITECTURE, quickstarts, API, and curated `docs/` pages |
| AgentStack / AstridOS | `unicity-astrid/astrid` | README and `docs/` pages |

The exact files pulled from each repo are listed under `plugins.multirepo.nav_repos` in `mkdocs.yml`. To add or remove a page, edit that list and the `nav` section, then push.

## How updating works (no manual intervention)

The site rebuilds and redeploys automatically on three triggers (see `.github/workflows/deploy.yml`):

- **Push to `main`** — when you change config or landing pages here.
- **Daily schedule** — `cron: "0 5 * * *"` (UTC). Picks up any new commits in the source repos.
- **Manual** — the "Run workflow" button on the Actions tab.

Source-repo edits appear on the site at the next daily build (within 24h). For instant updates, add a small step to a source repo's CI that sends a `repository_dispatch` event of type `upstream-docs-updated` to this repo; the workflow already listens for it.

## One-time setup

1. Create this repository as `unicitynetwork/unicity-docs` (public) and push these files to `main`.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. That's it. The first push triggers a build; the site publishes to `https://unicitynetwork.github.io/unicity-docs/`.

No personal access token is required: the source repos are public, so the workflow's default `GITHUB_TOKEN` can clone them.

## Local development

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mkdocs serve   # http://127.0.0.1:8000
```

## Notes on the toolchain

Versions are pinned in `requirements.txt` for reproducible builds. Material for MkDocs is in maintenance mode (security fixes committed through at least November 2026) and the multirepo plugin is in maintenance-only status. The pin (`mkdocs-material` pins MkDocs `<2`) keeps builds stable regardless of the MkDocs 2.0 release. Revisit the toolchain before late 2026; the maintainer's successor project is [Zensical](https://squidfunk.github.io/mkdocs-material/blog/), and Docusaurus is the more actively maintained alternative if a migration is warranted.
