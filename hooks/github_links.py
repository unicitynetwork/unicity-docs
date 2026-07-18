"""Rewrite relative links in imported pages to absolute GitHub URLs.

Pages pulled in by the multirepo plugin are READMEs written for GitHub. They
link to files that live in their own repo (source files, .env.example, test
fixtures) which are NOT part of this docs site. MkDocs would otherwise emit
those as site-relative links, producing 404s.

This hook rewrites any relative link that does not target a Markdown page into
an absolute URL pointing at the file in its source repository, so every link on
the site resolves. Markdown links (.md) are left alone: those are real pages.
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
        if not path or path.endswith(".md"):
            return match.group(0)  # real doc page (or pure anchor)
        resolved = posixpath.normpath(posixpath.join(in_repo_dir, path))
        if resolved.startswith(".."):
            return match.group(0)  # escapes the repo: leave as-is
        kind = "tree" if target.endswith("/") else "blob"
        url = f"https://github.com/{repo}/{kind}/{branch}/{resolved}"
        if anchor:
            url = f"{url}#{anchor}"
        return f"[{text}]({url})"

    return LINK_RE.sub(fix, markdown)
