# Copied from the new-repo templates into every docs repo. Repos run different ruff
# settings, so their formatter leaves this file as it is: lint it, do not reformat it.
# fmt: off
"""Post-build check of a Zensical site: the rules `zensical build --strict` does not enforce.

usage: python3 -I .github/scripts/site-check.py <site_dir> [zensical.toml]

Run from the repository root (the workflow does): the config is read from ./zensical.toml
unless its path is given. No config file is an error, never a skipped pass.

Exit 1 on any of these, each printed as one ERROR line:
  - a link or image whose target is not in the built site: a nav entry whose page does not
    exist, a missing image, any other dangling href or src, in any quoting and with HTML
    entities decoded (Zensical validates Markdown page links; it does not validate images,
    nav entries or raw HTML links). A full URL into the site itself
    (https://geiserx.github.io/<repo>/...) is checked the same way. A redirect stub's own
    links (canonical and body) are checked too;
  - a link whose #fragment is not an id on the target page, including links that come in
    through a snippet include (Zensical 0.1.0 does not check those; MkDocs strict did);
  - an href ending in .md: a correct page link is rewritten to a directory URL, so a .md left
    in the HTML is a raw-HTML or unprocessed link, and it opens the llmstxt Markdown copy;
  - a root-absolute link (/getting-started/) outside the site's own path prefix: it breaks
    under https://geiserx.github.io/<repo>/ (MkDocs' `absolute_links: warn`, which Zensical
    ignores). The prefix comes from site_url, else the home page's canonical link; with
    neither, that is an error rather than a check that cannot fire;
  - a page that no navigation entry links to: a stray file under docs/ published at a public
    URL that nothing reaches (MkDocs' `nav.omitted_files: warn`, which Zensical ignores);
  - a .py, .pyc or __pycache__ entry in the site: the awesome lists keep their Markdown
    extension under docs/hooks/, and Zensical publishes every file not in exclude_docs;
  - an awesome list's count token left in a page (`<!-- n:proyectos -->`, `n:categorias`,
    `n:retirados`): the Markdown extension that fills them in did not run. Only those three
    names: CashPilot writes other `<!-- n:... -->` comments of its own in its pages;
  - a raw <title>, or an unclosed <textarea>, <xmp>, <noembed>, <noframes>, or any
    <plaintext>, in a page's article outside inline SVG and MathML: a browser's HTML parser
    treats everything after it as text, so the rest of the page disappears (Markdown passes
    `<title>` written in prose through as a real tag; Telegram-Archive shipped that way);
  - a "Copy as Markdown" button (data-md-copy-url) whose Markdown copy does not exist in the
    site: the llmstxt plugin writes the copies, and only for pages its `sections` globs match.
And, from zensical.toml (Zensical drops what it does not know without a word; under MkDocs
strict an unknown plugin aborted the build):
  - a plugin name Zensical 0.1.0 does not know (`redirect` for `redirects`, `llmstxtt`): the
    plugin's whole output silently vanishes otherwise;
  - a theme feature name the Zensical UI 0.0.41 does not know (the list below is what its
    templates and bundle test for; `search.suggest` and `search.share` are not in it);
  - `theme.variant` other than "modern" or "classic" (anything else is classic, silently),
    and a "modern" config whose index.html does not load the modern stylesheet;
  - a `redirect_maps` entry whose stub was not written;
  - an enabled llmstxt plugin with no site/llms.txt, or `content.action.copy` in the
    features with a page that carries no copy button.
Plugin keys are read the way Zensical reads them (`material/redirects` is `redirects`), and
a plugin with `enabled = false` is treated as off. With directory URLs off (the offline
plugin turns them off) every .html file is a page.
Stdlib only (tomllib needs Python 3.11+), so it runs under `python -I` on any runner.
"""

import re
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SWALLOW = re.compile(r"<(title|textarea|xmp|plaintext|noembed|noframes)\b", re.IGNORECASE)
FOREIGN = re.compile(r"<(svg|math)\b.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
TOKEN = re.compile(r"<!--\s*n:(?:proyectos|categorias|retirados)\s*-->")
ARTICLE = re.compile(r"<article\b.*?</article>", re.DOTALL)
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




class Page(HTMLParser):
    """The parts of one built HTML file the checks read, from a real HTML parser: any
    quoting, entities decoded, nothing taken from <script>/<style> text or escaped code."""

    def __init__(self, text: str):
        """Parse one file's text completely."""
        super().__init__(convert_charrefs=True)
        self.urls: list[tuple[str, str, bool]] = []  # (tag, url, in <head>)
        self.ids: set[str] = set()
        self.copies: list[str] = []
        self.nav: list[str] = []
        self.canonical: str | None = None
        self.in_head = True
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        """Record ids, URLs, copy targets, nav links and the canonical link of one tag."""
        a = {k: v or "" for k, v in attrs}
        if tag == "body":
            self.in_head = False
        for key in ("id", "name") if tag == "a" else ("id",):
            if a.get(key):
                self.ids.add(a[key])
        for key in ("href", "src"):
            if key in a:
                self.urls.append((tag, a[key], self.in_head))
        if "data-md-copy-url" in a:
            self.copies.append(a["data-md-copy-url"])
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical = a.get("href")
        classes = a.get("class", "").split()
        # The toc's #heading entries carry md-nav__link too: they point at the page itself,
        # so only links with a path count toward reachability.
        if tag == "a" and ("md-nav__link" in classes or "md-tabs__link" in classes) and urlparse(a.get("href", "")).path:
            self.nav.append(a["href"])

    handle_startendtag = handle_starttag


def canonical_plugin(name: str) -> str:
    """The plugin name Zensical resolves a config key to (`material/search` is `search`)."""
    name = name.removeprefix("material/")
    return name.split("/", 1)[0] if name.startswith(("social/", "privacy/", "optimize/")) else name


def plugin_on(plugins: dict, name: str) -> bool:
    """True when the plugin is configured under any of its key spellings and not `enabled = false`."""
    for key, opts in plugins.items():
        if canonical_plugin(key) == name:
            return not (isinstance(opts, dict) and opts.get("enabled", True) is False)
    return False


def plugin_opts(plugins: dict, name: str) -> dict:
    """The plugin's option table, under whichever key spelling the config uses."""
    for key, opts in plugins.items():
        if canonical_plugin(key) == name and isinstance(opts, dict):
            return opts
    return {}


def swallowing_tags(article: str) -> list[str]:
    """Raw tags in an article that make a browser treat the rest of the page as text."""
    # <title> inside inline SVG is the SVG's accessible name, and MathML has its own
    # content model: neither swallows the page, so both are cut out first.
    art = FOREIGN.sub("", article)
    found = []
    for m in SWALLOW.finditer(art):
        tag = m.group(1).lower()
        closed = re.search(rf"</{tag}\s*>", art[m.end():], re.IGNORECASE)
        if tag in ("title", "plaintext") or not closed:
            found.append(tag)
    return found


def read_config(path: Path, errors: set[str]) -> dict:
    """The [project] table of zensical.toml; an unreadable or empty config is an error."""
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
    """Run every check over the built site and config; print one ERROR line each, return 1 if any."""
    site = Path(site_dir).resolve()
    index = site / "index.html"
    if not index.is_file():
        print(f"ERROR {site_dir}: no index.html (did the build run?)")
        return 1
    errors: set[str] = set()
    cfg = read_config(Path(config_path), errors)
    plugins = cfg.get("plugins") or {}
    # The offline plugin turns directory URLs off (zensical/config.py, _apply_offline_plugin).
    directory_urls = cfg.get("use_directory_urls", True) is not False and not plugin_on(plugins, "offline")

    site_url = cfg.get("site_url") or Page(index.read_text(encoding="utf-8", errors="replace")).canonical or ""
    origin = urlparse(site_url)
    prefix = origin.path or ""
    if not site_url:
        errors.add("no site_url in zensical.toml and no canonical link in index.html: the "
                   "root-absolute link check has no prefix to check against")
        prefix = "/"
    prefix = prefix if prefix.endswith("/") else prefix + "/"

    parsed: dict[Path, Page] = {}

    def parse(path: Path) -> Page:
        """Each file is parsed once: fragment checks read target pages again."""
        if path not in parsed:
            parsed[path] = Page(path.read_text(encoding="utf-8", errors="replace"))
        return parsed[path]

    def resolve(page: Path, url: str):
        """None for a URL outside this site, "ABS" for a rooted path outside the prefix,
        else the file the URL lands on (not necessarily existing)."""
        u = urlparse(url)
        if u.scheme in ("http", "https") and u.netloc and u.netloc == origin.netloc:
            if not u.path.startswith(prefix) and u.path + "/" != prefix:
                return None  # another site on the same host (geiserx.github.io/<other repo>)
        elif u.scheme or u.netloc:
            return None
        if url == "" or url.startswith("#"):
            return page
        path = unquote(u.path)
        if path.startswith("/"):
            if not path.startswith(prefix) and path + "/" != prefix:
                return "ABS"
            target = site / path[len(prefix):]
        else:
            target = page.parent / path
        if path.endswith("/") or target.is_dir():
            target = target / "index.html"
        return target.resolve()

    for p in site.rglob("*"):
        if p.suffix in (".py", ".pyc") or "__pycache__" in p.relative_to(site).parts:
            errors.add(f"{p.relative_to(site)}: source file published (add its directory to exclude_docs)")

    nav_targets: set[Path] = set()
    pages: list[Path] = []
    copy_on = "content.action.copy" in ((cfg.get("theme") or {}).get("features") or [])
    for page in sorted(site.rglob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        rel = page.relative_to(site)
        stub = STUB in text  # a redirect stub: its links are checked, it is not a page
        is_page = not stub and (rel.name == "index.html" if directory_urls else rel.as_posix() != "404.html")
        if is_page:
            pages.append(page)
        for art in ARTICLE.findall(text):
            for tag in swallowing_tags(art):
                errors.add(f"{rel}: raw <{tag}> in the page body hides everything after it in a browser")
            for tok in TOKEN.findall(art):
                errors.add(f"{rel}: build token {tok} was not filled in (extension not loaded?)")
        doc = parse(page)
        for tag, url, in_head in doc.urls:
            t = resolve(page, url)
            if t is None:
                continue
            if t == "ABS":
                errors.add(f"{rel}: absolute link {url} (outside {prefix})")
            elif not t.is_relative_to(site):
                # ../LICENSE from the top page: the file exists in the checkout, not on Pages.
                errors.add(f"{rel}: {url} leaves the built site (resolves to {t})")
            elif not t.exists():
                errors.add(f"{rel}: {url} -> missing {t.relative_to(site)}")
            else:
                # <head> holds <link rel="alternate" type="text/markdown" href="./index.md">
                # from the llmstxt plugin, a legitimate .md href; this rule reads the body only.
                if not in_head and unquote(urlparse(url).path).endswith(".md"):
                    errors.add(f"{rel}: {url} links a Markdown source, not a page URL (raw HTML link?)")
                frag = unquote(urlparse(url).fragment)
                # #top and text fragments (#:~:text=) are valid in a browser with no matching id.
                special = frag.lower() == "top" or frag.startswith(":~:")
                if tag == "a" and frag and not special and t.suffix == ".html" and frag not in parse(t).ids:
                    errors.add(f"{rel}: {url} -> no id {frag!r} on {t.relative_to(site)}")
        for url in doc.copies:
            t = resolve(page, url)
            if t is None or t == "ABS" or not t.is_relative_to(site) or not t.is_file():
                errors.add(f"{rel}: Copy as Markdown points at {url}, which is not in the site (llmstxt sections?)")
        if is_page and copy_on and not doc.copies:
            errors.add(f"{rel}: content.action.copy is on but the page has no Copy as Markdown button")
        for url in doc.nav:
            t = resolve(page, url)
            if isinstance(t, Path):
                nav_targets.add(t)

    for page in pages:
        if page.resolve() not in nav_targets:
            errors.add(f"{page.relative_to(site)}: page is in no navigation entry (stray page)")

    if cfg:
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
        elif variant == "modern" and "assets/stylesheets/modern/" not in index.read_text(encoding="utf-8", errors="replace"):
            errors.add("index.html does not load the modern stylesheet although theme.variant is modern")
        redirects = plugin_opts(plugins, "redirects") if plugin_on(plugins, "redirects") else {}
        for src in redirects.get("redirect_maps") or {}:
            s = src.removesuffix(".md")
            # A README page is its folder's index: sub/README.md -> sub/index.html in every mode.
            if s == "README" or s.endswith("/README"):
                s = s[: -len("README")] + "index"
            if not directory_urls or s == "index" or s.endswith("/index"):
                stub = site / (s + ".html")
            else:
                stub = site / s / "index.html"
            if not stub.is_file() or STUB not in stub.read_text(encoding="utf-8", errors="replace"):
                errors.add(f"redirect_maps {src!r}: no redirect stub at {stub.relative_to(site)}")
        if plugin_on(plugins, "llmstxt") and not (site / "llms.txt").is_file():
            errors.add("llmstxt plugin is configured but site/llms.txt was not written")

    for e in sorted(errors):
        print("ERROR", e)
    print(f"site-check: {len(pages)} pages, {len(errors)} errors, prefix {prefix}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: site-check.py <site_dir> [zensical.toml]")
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "zensical.toml"))
