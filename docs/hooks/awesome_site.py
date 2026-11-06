"""Build-time work for an awesome list's site, as a Python-Markdown extension.

Zensical does not run MkDocs `hooks`, and it says nothing when it skips them. It does run
Markdown extensions, so docs/hooks/site.py (the old hook) became this file. Load it with
    [project.markdown_extensions]
    "docs.hooks.awesome_site" = {}
and build with `python -m zensical build` (which puts the repo root on sys.path; the bare
`zensical` command does not, and fails with ModuleNotFoundError, so a missing path cannot
pass quietly). Options, for a list whose README is not in Spanish:
    "docs.hooks.awesome_site" = { section = "list", ids = ["contents"] }
`section` is the README snippet section the list page includes (`--8<-- "README.md:lista"`
by default); `ids` are the heading ids that must be present in that page's HTML (default
"contenido" and "insignia": the Contenido index and the Insignia badge section of the
Spanish lists).

Preprocessor (before snippets): on the page that includes the list, remembers that this is
the list page; and, on any page, replaces <!-- n:proyectos -->, <!-- n:categorias --> and
<!-- n:retirados --> with counts from README.md and DELETED.md, so the home page never
states a stale figure. A token it does not know fails the build.

Postprocessor (after the HTML is assembled): adds loading="lazy" decoding="async" to every
<img> except the banner, so a page with 2,000 shields.io badges paints before they all arrive;
and, on the list page, fails the build when a required id is missing or fewer list entries
rendered than README.md holds (markers that exist but enclose the wrong lines; a missing
marker already fails in pymdownx.snippets with check_paths). The check runs on the page that
carries the include, with or without count tokens, as the old hook ran it on index.md.
"""

import re
from pathlib import Path

from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor

ROOT = Path.cwd()  # the repo root: zensical reads zensical.toml from here
ENTRY = re.compile(r"^- \[[^\]]+\]\(https?://")
# DELETED.md also lists repos that no longer exist, with no link to give: "- `owner/repo` - reason".
RETIRED = re.compile(r"^- (?:\[[^\]]+\]\(https?://|`[^`]+` - )")
H2 = re.compile(r"^## (.+)$")
NOT_CATEGORIES = {
    "Contenido", "Insignia", "Mantenedores", "Contribuir", "Nota", "Descargo de responsabilidad",
    "Contents", "Contributing", "Badge for listed projects", "License",
}
# Any name after n:, so a misspelt token (n:Proyectos, n:pro_yectos) fails as unknown
# instead of staying an invisible comment where a count should be.
TOKEN = re.compile(r"<!--\s*n:([^\s>]+?)\s*-->")
IMG = re.compile(r"<img\b[^>]*>")
LISTED = re.compile(r"<li>\s*<a href=\"https?://")


def counts() -> dict[str, int]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    deleted = (ROOT / "DELETED.md").read_text(encoding="utf-8") if (ROOT / "DELETED.md").exists() else ""
    section, cats, n = None, set(), 0
    for line in readme.splitlines():
        h = H2.match(line)
        if h:
            section = h.group(1).strip()
            continue
        if section is None or section in NOT_CATEGORIES:
            continue  # the Contenido index and the Mantenedores profiles are not projects
        if ENTRY.match(line):  # a section counts as a category only once it lists a project
            cats.add(section)
            n += 1
    return {
        "proyectos": n,
        "categorias": len(cats),
        "retirados": sum(1 for line in deleted.splitlines() if RETIRED.match(line)),
    }


class Counts(Preprocessor):
    def __init__(self, md, include):
        super().__init__(md)
        self.include = include

    def run(self, lines):
        text = "\n".join(lines)
        if self.include.search(text):
            self.md.awesome_list_page = True
        if not TOKEN.search(text):
            return lines
        c = counts()
        unknown = sorted({k for k in TOKEN.findall(text) if k not in c})
        if unknown:
            raise RuntimeError(f"docs page has count tokens this extension does not know: {unknown}")
        return TOKEN.sub(lambda m: str(c[m.group(1)]), text).split("\n")


class Lazy(Postprocessor):
    def __init__(self, md, ids):
        super().__init__(md)
        self.ids = ids

    def run(self, html):
        # Python-Markdown also runs postprocessors over every heading's text (toc builds its
        # entries that way): only the page body carries the page's <h1>.
        if "<h1" not in html:
            return html
        if getattr(self.md, "awesome_list_page", False):
            self.md.awesome_list_page = False
            listed, expected = len(LISTED.findall(html)), counts()["proyectos"]
            missing = [i for i in self.ids if not re.search(rf'<h[1-6][^>]*\sid="{re.escape(i)}"', html)]
            if missing or listed < expected:
                raise RuntimeError(
                    f"the list page shows {listed} of the README's {expected} projects and lacks "
                    f"the ids {missing}: check the `--8<-- [start:...]` and `[end:...]` markers in "
                    "README.md and the section headings"
                )

        def lazy(m):
            tag = m.group(0)
            if "banner.svg" in tag or "loading=" in tag:
                return tag
            return tag.replace("<img", '<img loading="lazy" decoding="async"', 1)

        return IMG.sub(lazy, html)


class AwesomeSite(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "section": ["lista", "README.md snippet section the list page includes"],
            "ids": [["contenido", "insignia"], "heading ids that must be present on the list page"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        section = re.escape(self.getConfig("section"))
        include = re.compile(r'--8<--\s+"README\.md:' + section + '"')
        md.preprocessors.register(Counts(md, include), "awesome_counts", 33)  # before snippets (32)
        md.postprocessors.register(Lazy(md, list(self.getConfig("ids"))), "awesome_lazy", 0)  # after raw HTML is restored


def makeExtension(**kwargs):
    return AwesomeSite(**kwargs)
