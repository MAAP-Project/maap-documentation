"""Step 3: rewrite relative cross-links in notebook markdown cells and in the
converted .md files so they resolve under mystmd.

  * .rst targets -> .md ; .html targets -> the real source file (.ipynb/.md)
  * nbsphinx-style anchors (#Title-Case-(Parens)) -> mystmd ids, resolved against the
    target page's actual headings (or explicit labels); never guessed
  * absolute URLs, images and other assets are left untouched
Every change and every unresolved link is reported. Notebooks are re-serialised
exactly like nbformat does, so diffs are limited to the edited cells.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

from common import IMAGE_EXTS, Heading, heading_id, iter_files, load_headings, rel

JSON_VARIANTS = [
    dict(indent=1, ensure_ascii=False, sort_keys=True),   # nbformat default
    dict(indent=1, ensure_ascii=False, sort_keys=False),
    dict(indent=2, ensure_ascii=False, sort_keys=False),
    dict(indent=2, ensure_ascii=False, sort_keys=True),
    dict(indent=1, ensure_ascii=True, sort_keys=True),
    dict(indent=4, ensure_ascii=False, sort_keys=False),
]


def detect_json_variant(raw: str, nb: dict):
    """Find the json.dumps settings that reproduce the on-disk bytes, if any."""
    for kw in JSON_VARIANTS:
        for trailing in ("\n", ""):
            if json.dumps(nb, **kw) + trailing == raw:
                return kw, trailing
    return None, None

# ](target) and ](target "title") ; also <a href="..."> / <img src="...">
MD_LINK_RE = re.compile(r"(?P<pre>\]\(\s*<?)(?P<target>(?:[^()\s>]|\([^()\s]*\))+)(?P<post>>?(?:\s+\"[^\"]*\")?\s*\))")
HTML_ATTR_RE = re.compile(r"(?P<pre>\b(?:href|src)=\")(?P<target>[^\"]+)(?P<post>\")")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
SKIP_EXTS = IMAGE_EXTS | {".yml", ".yaml", ".py", ".csv", ".txt", ".json", ".sh", ".cfg", ".toml", ".zip", ".h5", ".tif"}


class Resolver:
    def __init__(self, src: Path, report, allow_missing: set[str], allow_anchors: set[str]):
        self.src = src
        self.report = report
        self.allow_missing = allow_missing
        self.allow_anchors = allow_anchors
        self._headings: dict[Path, list[Heading]] = {}

    def headings(self, path: Path) -> list[Heading]:
        if path not in self._headings:
            self._headings[path] = load_headings(path)
        return self._headings[path]

    def resolve_anchor(self, target: Path, anchor: str) -> str | None:
        key = heading_id(unquote(anchor))
        hs = self.headings(target)
        for h in hs:
            if h.html_id == key or (h.label and heading_id(h.label) == key) or heading_id(h.text) == key:
                return h.html_id
        return None

    def rewrite(self, file: str, where: str, target: str) -> str | None:
        """Return the rewritten target, or None to leave it untouched."""
        if SCHEME_RE.match(target) or target.startswith("//"):
            return None
        if "#" in target:
            path_part, anchor = target.split("#", 1)
        else:
            path_part, anchor = target, ""
        here = self.src / file
        if path_part == "":
            if anchor == "":
                self.report.add(file, where, "OTHER_UNTOUCHED", target)
                return None
            # in-page anchor
            new = self.resolve_anchor(here, anchor)
            if new is None:
                self.report.add(file, where, "ANCHOR_UNRESOLVED", target)
                return None
            return None if new == anchor else "#" + new
        ext = Path(path_part).suffix.lower()
        if ext in SKIP_EXTS:
            return None
        if ext not in {".rst", ".html", ".ipynb", ".md"}:
            self.report.add(file, where, "OTHER_UNTOUCHED", target)
            return None
        base = (here.parent / unquote(path_part))
        candidates = []
        if ext == ".html":
            candidates = [base.with_suffix(e) for e in (".ipynb", ".md", ".rst")]
        elif ext == ".rst":
            candidates = [base.with_suffix(".md"), base]
        else:
            candidates = [base]
        found = next((c for c in candidates if c.exists()), None)
        if found is None:
            kind = "MISSING_ALLOWED" if target in self.allow_missing else "MISSING"
            self.report.add(file, where, kind, target)
            return None
        new_ext = ".md" if found.suffix == ".rst" else found.suffix
        rel_new = path_part[: -len(Path(path_part).suffix)] + new_ext
        new_anchor = ""
        if anchor:
            resolved = self.resolve_anchor(found, anchor)
            if resolved is None:
                kind = "ANCHOR_UNRESOLVED_ALLOWED" if target in self.allow_anchors else "ANCHOR_UNRESOLVED"
                self.report.add(file, where, kind, target, rel_new + "#" + anchor)
                new_anchor = "#" + anchor
            else:
                new_anchor = "#" + resolved
        new = rel_new + new_anchor
        if new == target:
            return None
        self.report.add(file, where, "REWRITTEN", target, new)
        return new


def rewrite_text(text: str, file: str, where: str, resolver: Resolver) -> str:
    def sub(m):
        new = resolver.rewrite(file, where, m.group("target"))
        return m.group("pre") + (new if new is not None else m.group("target")) + m.group("post")
    text = MD_LINK_RE.sub(sub, text)
    text = HTML_ATTR_RE.sub(sub, text)
    return text


def run(ctx) -> None:
    src: Path = ctx.src
    allow = set(ctx.overrides.get("allow_missing_links", []) or [])
    allow_anchors = set(ctx.overrides.get("allow_unresolved_anchors", []) or [])
    resolver = Resolver(src, ctx.report, allow, allow_anchors)
    changed_nb = changed_md = 0
    for path in iter_files(src, {".ipynb"}):
        file = rel(src, path)
        raw = path.read_text(encoding="utf-8")
        nb = json.loads(raw)
        touched = False
        for i, cell in enumerate(nb.get("cells", [])):
            if cell.get("cell_type") != "markdown":
                continue
            src_lines = cell.get("source", [])
            as_list = isinstance(src_lines, list)
            text = "".join(src_lines) if as_list else src_lines
            new = rewrite_text(text, file, f"cell {i}", resolver)
            if new != text:
                touched = True
                cell["source"] = new.splitlines(keepends=True) if as_list else new
        if touched:
            kw, trailing = detect_json_variant(raw, json.loads(raw))
            if kw is None:
                kw, trailing = JSON_VARIANTS[0], "\n"
                ctx.report.add(file, "", "NB_REFORMATTED", "on-disk JSON formatting not reproducible; re-serialised like nbformat")
            path.write_text(json.dumps(nb, **kw) + trailing, encoding="utf-8")
            changed_nb += 1
    for path in iter_files(src, {".md"}):
        file = rel(src, path)
        text = path.read_text(encoding="utf-8")
        new = rewrite_text(text, file, "", resolver)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed_md += 1
    r = ctx.report
    print(f"[rewrite_links] notebooks changed: {changed_nb}, md changed: {changed_md}, "
          f"rewritten: {r.count('REWRITTEN')}, unresolved anchors: {r.count('ANCHOR_UNRESOLVED')}, "
          f"(+{r.count('ANCHOR_UNRESOLVED_ALLOWED')} allowed), missing: {r.count('MISSING')} (+{r.count('MISSING_ALLOWED')} allowed), other: {r.count('OTHER_UNTOUCHED')}")
