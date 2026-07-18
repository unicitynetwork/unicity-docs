# unicity-docs

Aggregated documentation portal for the Unicity stack, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and the [mkdocs-multirepo-plugin](https://github.com/jdoiro3/mkdocs-multirepo-plugin). Content is pulled directly from each source repository at build time, so this repo holds only configuration and a few landing pages, never copies of upstream docs.

Live site: <https://unicitynetwork.github.io/unicity-docs/>

## What gets aggregated

| Section | Source | Imported content |
| --- | --- | --- |
| Unicity Protocol | landing pages in this repo | Overview, Research Papers (links to the release PDFs) |
| AgentSphere / Sphere SDK | `unicity-sphere/sphere-sdk` | README, quickstarts (Node/Browser/CLI), Integration Guide, API Reference, Connect, Nametag Bindings |
| Unicity AOS | `unicity-aos/aos-ce` | README, Release Channels, Runtime Migration (plus a local overview page) |

The exact files pulled from each repo are listed under `plugins.multirepo.nav_repos` in `mkdocs.yml`. To add or remove a page, edit that list **and** the `nav` section, then push.

Because content is imported verbatim, wording in those pages can only be changed in the source repo — not here.

## How updating works (no manual intervention)

The site rebuilds and redeploys automatically on three triggers (see `.github/workflows/deploy.yml`):

- **Push to `main`** — when you change config or landing pages here.
- **Daily schedule** — `cron: "0 5 * * *"` (UTC). Picks up any new commits in the source repos.
- **Manual** — the "Run workflow" button on the Actions tab.

Source-repo edits appear on the site at the next daily build (within 24h), or immediately via a manual run. For automatic instant updates, add a step to a source repo's CI that sends a `repository_dispatch` event of type `upstream-docs-updated` to this repo; the workflow already listens for it.

## Guardrails against 404s

The build runs `mkdocs build --strict`, so **any MkDocs warning fails the build**:

- If an upstream repo removes or renames a file listed in `nav`, CI goes red and **nothing is deployed** — the live site keeps serving the last good build instead of publishing dead nav links. Fix the `imports`/`nav` lists in `mkdocs.yml` to go green again. (This is not hypothetical: `sphere-sdk` dropped 12 doc files in July 2026 and the site silently served ~190 dead links until the build was made strict.)
- `hooks/github_links.py` rewrites relative links inside imported READMEs that point at files in their own repo (source files, `.env.example`, test fixtures) into absolute GitHub URLs, so they resolve instead of 404ing.
- Link/anchor validation is set to `info` rather than `warn` so those upstream-owned links cannot block a deploy. Details in the comments in `mkdocs.yml`.

Trade-off to be aware of: the site fails **stale** rather than **broken**. If a build starts failing and nobody notices, the site quietly stops updating — watch the Actions notifications.

## One-time setup

Already done for this repo, recorded for reference:

1. Create the repository and push these files to `main`.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.

No personal access token is required: the source repos are public, so the workflow's default `GITHUB_TOKEN` can clone them across orgs.

## Local development

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mkdocs serve                 # http://127.0.0.1:8000
mkdocs build --strict        # what CI runs
```

## Notes on the toolchain

Versions are pinned in `requirements.txt` for reproducible builds. Material for MkDocs is in maintenance mode (security fixes committed through at least November 2026) and the multirepo plugin is in maintenance-only status. The pin (`mkdocs-material` pins MkDocs `<2`) keeps builds stable regardless of the MkDocs 2.0 release. Revisit the toolchain before late 2026; the maintainer's successor project is [Zensical](https://squidfunk.github.io/mkdocs-material/blog/), and Docusaurus is the more actively maintained alternative if a migration is warranted.
