"""MkDocs hooks for the one-page site.

on_page_markdown replaces the `<!-- n:... -->` tokens in docs/index.md with
numbers counted from README.md and DELETED.md at build time, so the home page
never states a stale figure.

on_page_content adds loading="lazy" to every image except the banner, so a
page with about 2,100 shields.io badges paints before they all arrive, and
fails the build if the list did not come through the include. A missing
section marker already fails the build in pymdownx.snippets (check_paths:
true raises SnippetMissingError); this check is for markers that exist but
enclose the wrong lines.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = re.compile(r"^- \[[^\]]+\]\(https?://", re.MULTILINE)
H2 = re.compile(r"^## (.+)$", re.MULTILINE)
NOT_CATEGORIES = {"Contenido", "Insignia", "Contribuir", "Nota", "Descargo de responsabilidad"}
IMG = re.compile(r"<img\b[^>]*>")


def _counts():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    deleted = (ROOT / "DELETED.md").read_text(encoding="utf-8")
    return {
        "proyectos": len(ENTRY.findall(readme)),
        "categorias": sum(1 for h in H2.findall(readme) if h not in NOT_CATEGORIES),
        "retirados": len(ENTRY.findall(deleted)),
    }


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "index.md":
        return markdown
    for key, value in _counts().items():
        markdown = markdown.replace(f"<!-- n:{key} -->", str(value))
    if "<!-- n:" in markdown:
        raise RuntimeError("docs/index.md has a count token the hook does not know")
    return markdown


def on_page_content(html, page, config, files):
    if page.file.src_uri != "index.md":
        return html
    if 'id="contenido"' not in html or 'id="insignia"' not in html:
        raise RuntimeError(
            "docs/index.md did not include the README list: "
            "check the `--8<-- [start:lista]` and `[end:lista]` markers in README.md"
        )

    def lazy(match):
        tag = match.group(0)
        if "banner.svg" in tag or "loading=" in tag:
            return tag
        return tag.replace("<img", '<img loading="lazy" decoding="async"', 1)

    return IMG.sub(lazy, html)
