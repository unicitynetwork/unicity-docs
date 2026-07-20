"""Rewrite relative links in imported pages to absolute GitHub URLs.

Pages pulled in by the multirepo plugin are READMEs written for GitHub. They
link to files that live in their own repo (source files, .env.example, test
fixtures) which are NOT part of this docs site. MkDocs would otherwise emit
those as site-relative links, producing 404s.

This hook rewrites relative links into absolute URLs pointing at the file in its
source repository whenever the target is not a page that actually exists on this
site. That covers two cases:

  1. non-Markdown targets (source files, .env.example, test fixtures), and
  2. Markdown targets the portal does not import (e.g. an upstream README links
     to docs/foo.md but foo.md is not in our `imports` list).

Links to Markdown pages we DO import are left untouched so they stay internal.
"""
import posixpath
import re

# nav prefix -> (owner/repo, branch)
REPOS = {
    "sphere/": ("unicity-sphere/sphere-sdk", "main"),
    "aos/": ("unicity-aos/aos-ce", "main"),
}

# [text](target) — capture the target, ignoring images (![...]) via lookbehind
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?\s*\)")

SKIP_PREFIXES = ("http://", "https://", "//", "#", "mailto:", "tel:", "data:")


def _is_site_page(files, site_path):
    """True if site_path is a page MkDocs actually built."""
    try:
        return files.get_file_from_path(site_path) is not None
    except Exception:
        return False


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    prefix = next((p for p in REPOS if src.startswith(p)), None)
    if prefix is None:
        return markdown  # locally authored page: leave untouched

    repo, branch = REPOS[prefix]
    in_repo_dir = posixpath.dirname(src[len(prefix):])

    def fix(match):
        text, target = match.group(1), match.group(2)
        if target.startswith(SKIP_PREFIXES):
            return match.group(0)
        path, _, anchor = target.partition("#")
        if not path:
            return match.group(0)  # pure anchor on this page
        resolved = posixpath.normpath(posixpath.join(in_repo_dir, path))
        if resolved.startswith(".."):
            return match.group(0)  # escapes the repo: leave as-is
        if path.endswith(".md") and _is_site_page(files, prefix + resolved):
            return match.group(0)  # a page we import: keep the link internal
        kind = "tree" if target.endswith("/") else "blob"
        url = f"https://github.com/{repo}/{kind}/{branch}/{resolved}"
        if anchor:
            url = f"{url}#{anchor}"
        return f"[{text}]({url})"

    return LINK_RE.sub(fix, markdown)
