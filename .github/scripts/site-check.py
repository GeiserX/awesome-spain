# Copied from the new-repo templates into every docs repo. Repos run different ruff
# settings, so their formatter leaves this file as it is: lint it, do not reformat it.
# fmt: off
"""Post-build check of a Zensical site: the rules `zensical build --strict` does not enforce.

usage: python3 -I .github/scripts/site-check.py <site_dir> [zensical.toml]

Run from the repository root (the workflow does): the config is read from ./zensical.toml
unless its path is given. No config file is an error, never a skipped pass.

Exit 1 on any of these, each printed as one ERROR line:
  - a link or image whose target is not in the built site: a nav entry whose page does not
    exist, a missing image, any other dangling href or src (Zensical validates Markdown page
    links and anchors; it does not validate images, nav entries or raw HTML links). A redirect
    stub's own links (canonical and body) are checked the same way;
  - an href ending in .md: a correct page link is rewritten to a directory URL, so a .md left
    in the HTML is a raw-HTML or unprocessed link, and it opens the llmstxt Markdown copy;
  - a root-absolute link (/getting-started/) outside the site's own path prefix: it breaks
    under https://geiserx.github.io/<repo>/ (MkDocs' `absolute_links: warn`, which Zensical
    ignores);
  - a page that no navigation entry links to: a stray file under docs/ published at a public
    URL that nothing reaches (MkDocs' `nav.omitted_files: warn`, which Zensical ignores);
  - a .py, .pyc or __pycache__ entry in the site: the awesome lists keep their Markdown
    extension under docs/hooks/, and Zensical publishes every file not in exclude_docs;
  - an awesome list's count token left in a page (`<!-- n:proyectos -->`, `n:categorias`,
    `n:retirados`): the Markdown extension that fills them in did not run. Only those three
    names: CashPilot writes other `<!-- n:... -->` comments of its own in its pages;
  - a raw <title>, <textarea>, <xmp>, <plaintext>, <noembed> or <noframes> tag inside a page's
    article: a browser's HTML parser treats everything after it as text, so the rest of the
    page disappears (Markdown passes `<title>` written in prose through as a real tag;
    Telegram-Archive shipped that way);
  - a "Copy as Markdown" button (data-md-copy-url) whose Markdown copy does not exist: the
    llmstxt plugin writes the copies, and only for pages its `sections` globs match.
And, from zensical.toml (Zensical drops what it does not know without a word; under MkDocs
strict an unknown plugin aborted the build):
  - a plugin name Zensical 0.1.0 does not know (`redirect` for `redirects`, `llmstxtt`): the
    plugin's whole output silently vanishes otherwise;
  - a theme feature name the Zensical UI 0.0.41 does not know (the list below is what its
    templates and bundle test for; `search.suggest` and `search.share` are not in it);
  - `theme.variant` other than "modern" or "classic" (anything else is classic, silently),
    and a "modern" config whose index.html does not load the modern stylesheet;
  - a `redirect_maps` entry whose stub was not written;
  - a `[project.plugins.llmstxt]` table with no site/llms.txt, or `content.action.copy` in
    the features with a page that carries no copy button.
Stdlib only (tomllib needs Python 3.11+), so it runs under `python -I` on any runner.
"""

import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlparse

SWALLOW = re.compile(r"<(title|textarea|xmp|plaintext|noembed|noframes)\b", re.IGNORECASE)
TOKEN = re.compile(r"<!--\s*n:(?:proyectos|categorias|retirados)\s*-->")
ARTICLE = re.compile(r"<article\b.*?</article>", re.DOTALL)
ATTR = re.compile(r'\s(?:href|src)="([^"]*)"')
COPY = re.compile(r'\sdata-md-copy-url="([^"]*)"')
NAV = re.compile(r'<a\s+href="([^"]*)"\s+class="md-(?:nav|tabs)__link')
STUB = "<title>Redirecting...</title>"

# Keys of _PLUGIN_UNSUPPORTED_OPTIONS in zensical/config.py (0.1.0, same set as 0.0.74): every other name is
# dropped by `_convert_plugins` without a message. `material/` prefixes and `social/<x>`,
# `privacy/<x>`, `optimize/<x>` instance names canonicalise the same way Zensical does.
KNOWN_PLUGINS = {
    "api-autonav", "autorefs", "awesome-nav", "blog", "callouts", "exclude", "gh-admonitions",
    "glightbox", "include-markdown", "literate-nav", "llmstxt", "macros", "markdown-exec",
    "markdownextradata", "meta", "mike", "minify", "mkdocs-audio", "mkdocs-autoapi",
    "mkdocs-nav-weight", "mkdocs-video", "mkdocstrings", "offline", "optimize", "privacy",
    "redirects", "rss", "search", "social", "table-reader", "tags",
}
# Feature names the shipped UI tests for (zensical_ui 0.0.41, read from its templates and
# bundle.*.min.js). Regenerate after a bump with:
#   grep -rhoE '"[a-z]+(\.[a-z]+)+" in features' <site-packages>/zensical_ui/templates | sort -u
#   grep -oE '"(navigation|content|search|toc|header|announce)\.[a-z.]+"' .../bundle.*.min.js | sort -u
KNOWN_FEATURES = {
    "announce.dismiss", "content.action.copy", "content.action.edit", "content.action.view",
    "content.code.annotate", "content.code.copy", "content.code.select",
    "content.footnote.tooltips", "content.lazy", "content.tabs.link", "content.tooltips",
    "header.autohide", "navigation.expand", "navigation.footer", "navigation.indexes",
    "navigation.instant", "navigation.instant.prefetch", "navigation.instant.preview",
    "navigation.instant.progress", "navigation.path", "navigation.prune", "navigation.sections",
    "navigation.tabs", "navigation.tabs.sticky", "navigation.top", "navigation.tracking",
    "search.highlight", "toc.follow", "toc.integrate",
}


def body_urls(body: str) -> set[str]:
    return set(ATTR.findall(body))


def canonical_plugin(name: str) -> str:
    name = name.removeprefix("material/")
    return name.split("/", 1)[0] if name.startswith(("social/", "privacy/", "optimize/")) else name


def read_config(path: Path, errors: set[str]) -> dict:
    if not path.is_file():
        errors.add(f"{path}: config file not found (run from the repository root, or pass its path)")
        return {}
    try:
        project = tomllib.loads(path.read_text(encoding="utf-8")).get("project")
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        errors.add(f"{path}: not valid TOML: {e}")
        return {}
    # Every config check reads [project]: without it they would all pass by skipping.
    if not isinstance(project, dict) or not project:
        errors.add(f"{path}: no [project] table, so no config check can run")
        return {}
    return project


def main(site_dir: str, config_path: str) -> int:
    site = Path(site_dir).resolve()
    index = site / "index.html"
    if not index.is_file():
        print(f"ERROR {site_dir}: no index.html (did the build run?)")
        return 1
    m = re.search(r'<link rel="canonical" href="([^"]+)"', index.read_text(errors="replace"))
    # Directory URLs assumed (every repo's default): with use_directory_urls off or the
    # offline plugin on, the prefix and page checks below do not apply as written.
    prefix = urlparse(m.group(1)).path if m else "/"
    prefix = prefix if prefix.endswith("/") else prefix + "/"
    errors: set[str] = set()
    nav_targets: set[Path] = set()
    pages: list[Path] = []
    cfg = read_config(Path(config_path), errors)

    def resolve(page: Path, url: str):
        u = urlparse(url)
        if u.scheme or u.netloc or url == "" or url.startswith("#"):
            return None
        path = unquote(u.path)
        if path.startswith("/"):
            if not path.startswith(prefix):
                return "ABS"
            target = site / path[len(prefix):]
        else:
            target = page.parent / path
        if path.endswith("/") or target.is_dir():
            target = target / "index.html"
        return target.resolve()

    for p in site.rglob("*"):
        if p.suffix in (".py", ".pyc") or "__pycache__" in p.parts:
            errors.add(f"{p.relative_to(site)}: source file published (add its directory to exclude_docs)")

    for page in sorted(site.rglob("*.html")):
        text = page.read_text(errors="replace")
        rel = page.relative_to(site)
        stub = STUB in text  # a redirect stub: its links are checked, it is not a page
        if rel.name == "index.html" and not stub:
            pages.append(page)
        for art in ARTICLE.findall(text):
            for tag in SWALLOW.findall(art):
                errors.add(f"{rel}: raw <{tag}> in the page body hides everything after it in a browser")
            for tok in TOKEN.findall(art):
                errors.add(f"{rel}: build token {tok} was not filled in (extension not loaded?)")
        # <head> holds <link rel="alternate" type="text/markdown" href="./index.md"> from the
        # llmstxt plugin, a legitimate .md href; the .md rule looks at the body only.
        body = text.split("</head>", 1)[-1]
        for url in ATTR.findall(text):
            t = resolve(page, url)
            if t == "ABS":
                errors.add(f"{rel}: absolute link {url} (outside {prefix})")
            elif t is not None and not t.is_relative_to(site):
                # ../LICENSE from the top page: the file exists in the checkout, not on Pages.
                errors.add(f"{rel}: {url} leaves the built site (resolves to {t})")
            elif t is not None and not t.exists():
                shown = t.relative_to(site) if t.is_relative_to(site) else t
                errors.add(f"{rel}: {url} -> missing {shown}")
            elif t is not None and unquote(urlparse(url).path).endswith(".md") and url in body_urls(body):
                errors.add(f"{rel}: {url} links a Markdown source, not a page URL (raw HTML link?)")
        copies = COPY.findall(text)
        for url in copies:
            t = resolve(page, url)
            if isinstance(t, Path) and not t.is_file():
                errors.add(f"{rel}: Copy as Markdown points at {url}, which was not written (llmstxt sections?)")
        if rel.name == "index.html" and not stub and not copies \
                and "content.action.copy" in ((cfg.get("theme") or {}).get("features") or []):
            errors.add(f"{rel}: content.action.copy is on but the page has no Copy as Markdown button")
        for url in NAV.findall(text):
            t = resolve(page, url)
            if isinstance(t, Path):
                nav_targets.add(t)

    for page in pages:
        if page.resolve() not in nav_targets:
            errors.add(f"{page.relative_to(site)}: page is in no navigation entry (stray page)")

    if cfg:
        plugins = cfg.get("plugins") or {}
        for name in plugins:
            if canonical_plugin(name) not in KNOWN_PLUGINS:
                errors.add(f"zensical.toml: plugin {name!r} is unknown to Zensical and silently ignored")
        theme = cfg.get("theme") or {}
        for f in theme.get("features") or []:
            if f not in KNOWN_FEATURES:
                errors.add(f"zensical.toml: feature {f!r} is unknown to the Zensical UI and silently ignored")
        variant = theme.get("variant", "classic")
        if variant not in ("modern", "classic"):
            errors.add(f"zensical.toml: theme.variant {variant!r} is not modern or classic (Zensical falls back to classic silently)")
        elif variant == "modern" and "assets/stylesheets/modern/" not in index.read_text(errors="replace"):
            errors.add("index.html does not load the modern stylesheet although theme.variant is modern")
        # The offline plugin turns directory URLs off (zensical/config.py,
        # _apply_offline_plugin), so a redirect stub becomes old.html there.
        offline = plugins.get("offline", False)
        offline_on = "offline" in plugins and (offline or {}).get("enabled", True) is not False
        directory_urls = cfg.get("use_directory_urls", True) and not offline_on
        for src in (plugins.get("redirects") or {}).get("redirect_maps") or {}:
            s = src.removesuffix(".md")
            # A README page is its folder's index: sub/README.md -> sub/index.html in every mode.
            if s == "README" or s.endswith("/README"):
                s = s[: -len("README")] + "index"
            if not directory_urls or s == "index" or s.endswith("/index"):
                stub = site / (s + ".html")
            else:
                stub = site / s / "index.html"
            if not stub.is_file() or STUB not in stub.read_text(errors="replace"):
                errors.add(f"redirect_maps {src!r}: no redirect stub at {stub.relative_to(site)}")
        if "llmstxt" in plugins and not (site / "llms.txt").is_file():
            errors.add("llmstxt plugin is configured but site/llms.txt was not written")

    for e in sorted(errors):
        print("ERROR", e)
    print(f"site-check: {len(pages)} pages, {len(errors)} errors, prefix {prefix}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: site-check.py <site_dir> [zensical.toml]")
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "zensical.toml"))
