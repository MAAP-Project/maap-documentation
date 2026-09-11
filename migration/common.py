"""Shared helpers for the Sphinx -> MyST migration scripts.

Everything here is deterministic. The slug and anchor-id functions are exact ports
of the mystmd 1.10.1 implementation (see agent-docs/03-spike-results.md).
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SRC = REPO / "docs" / "source"
OUT_DIR = Path(__file__).resolve().parent / "out"

SKIP_DIRS = {".ipynb_checkpoints", "_build", ".venv", "node_modules"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff"}
PAGE_EXTS = {".rst", ".md", ".ipynb"}


# --------------------------------------------------------------------------- ids
def normalize_label(label: str) -> str:
    """mystmd normalizeLabel(): collapse whitespace, strip quotes, trim, lowercase."""
    s = re.sub(r"[\t\n\r ]+", " ", label)
    s = re.sub(r"['‘’\"“”]+", "", s)
    return s.strip().lower()


def create_html_id(identifier: str) -> str:
    """mystmd createHtmlId()."""
    s = identifier.lower()
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"^([0-9-])", r"id-\1", s)
    s = re.sub(r"-[-]+", "-", s)
    s = re.sub(r"(?:^[-]+)|(?:[-]+$)", "", s)
    return s


def heading_id(text: str) -> str:
    """The HTML id mystmd gives a heading (or explicit label) with this text."""
    return create_html_id(normalize_label(text))


def _remove_leading_enumeration(s: str) -> str:
    if re.match(r"^([12][0-9]{3})([^0-9])?", s):
        return s
    if re.match(r"^([0-9]{5})", s):
        return s
    removed = re.sub(r"^([0-9_.-]+)", "", s)
    return removed or s


def _input2name(inp: str) -> str:
    # mystmd input2name(input, /^[a-z0-9-]/, "-") followed by title2name's slice(0, 50)
    marker = "¶"
    chars = [c if re.match(r"^[a-z0-9-]", c) else marker for c in (marker + inp).lower()]
    out = ""
    for c in chars:
        if out and out[-1] == marker and c == marker:
            continue
        out += c
    name = out[1:].replace(marker, "-")
    name = re.sub(r"-+", "-", name)
    if name.startswith("-"):
        name = name[1:]
    if name.endswith("-"):
        name = name[:-1]
    return name


def create_slug(name: str) -> str:
    """mystmd createSlug(): applied to a file stem or a folder name."""
    return _input2name(_remove_leading_enumeration(name).replace("&", "¶and¶"))[:50]


def slug_path(rel_page: str) -> str:
    """URL path (no leading slash) for a page relative to the project root, with
    site.options.folders: true. index.md at the root maps to ''."""
    p = Path(rel_page)
    parts = [create_slug(x) for x in p.parts[:-1]]
    stem = p.stem
    if not parts and stem == "index":
        return ""
    parts.append(create_slug(stem))
    return "/".join(parts)


# ---------------------------------------------------------------------- files
def iter_files(src: Path, exts: set[str]) -> list[Path]:
    out = []
    for root, dirs, files in os.walk(src):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for f in sorted(files):
            if Path(f).suffix in exts:
                out.append(Path(root) / f)
    return out


def rel(src: Path, p: Path) -> str:
    return p.relative_to(src).as_posix()


# -------------------------------------------------------------------- toctree
TOCTREE_RE = re.compile(r"^(?P<indent>[ \t]*)\.\. toctree::[ \t]*$")


@dataclass
class Toctree:
    file: str                       # rst file (relative to src) that contains it
    start: int                      # 0-based line index of the directive
    end: int                        # 0-based exclusive end line index
    options: dict = field(default_factory=dict)
    entries: list[str] = field(default_factory=list)   # relative to src, with extension


def parse_toctrees(src: Path, rst_path: Path) -> list[Toctree]:
    """Regex-based toctree parser. Tolerates a missing trailing newline and
    tab indentation. Entries are resolved relative to the rst file's folder."""
    lines = rst_path.read_text(encoding="utf-8").splitlines()
    result = []
    i = 0
    while i < len(lines):
        m = TOCTREE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        base_indent = len(m.group("indent").expandtabs(4))
        toc = Toctree(file=rel(src, rst_path), start=i, end=i + 1)
        j = i + 1
        while j < len(lines):
            line = lines[j]
            if line.strip() == "":
                j += 1
                continue
            indent = len(line[: len(line) - len(line.lstrip())].expandtabs(4))
            if indent <= base_indent:
                break
            s = line.strip()
            if s.startswith(":"):
                k, _, v = s[1:].partition(":")
                toc.options[k.strip()] = v.strip()
            else:
                target = (rst_path.parent / s).resolve()
                toc.entries.append(target.relative_to(src.resolve()).as_posix())
            j += 1
        toc.end = j
        result.append(toc)
        i = j
    return result


# ------------------------------------------------------------------- headings
FENCE_RE = re.compile(r"^\s*(```|~~~)")
ATX_RE = re.compile(r"^\s{0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
LABEL_RE = re.compile(r"^\((?P<label>[^()\s]+)\)=\s*$")


def strip_inline_markup(text: str) -> str:
    """Plain text of a markdown heading, as both nbsphinx and mystmd see it."""
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("`", "")
    t = re.sub(r"(\*\*|__)(.+?)\1", r"\2", t)
    t = re.sub(r"(?<!\w)(\*|_)(.+?)\1(?!\w)", r"\2", t)
    return t.strip()


@dataclass
class Heading:
    level: int
    text: str          # plain text
    html_id: str       # mystmd id (label-derived when an explicit label precedes it)
    label: str | None  # explicit label if any


def headings_from_markdown(md_text: str) -> list[Heading]:
    out: list[Heading] = []
    in_fence = None
    pending_label = None
    for line in md_text.splitlines():
        fm = FENCE_RE.match(line)
        if fm:
            if in_fence is None:
                in_fence = fm.group(1)
            elif fm.group(1) == in_fence:
                in_fence = None
            continue
        if in_fence:
            continue
        lm = LABEL_RE.match(line)
        if lm:
            pending_label = lm.group("label")
            continue
        hm = ATX_RE.match(line)
        if hm:
            text = strip_inline_markup(hm.group(2))
            if pending_label:
                out.append(Heading(len(hm.group(1)), text, heading_id(pending_label), pending_label))
            else:
                out.append(Heading(len(hm.group(1)), text, heading_id(text), None))
            pending_label = None
            continue
        if line.strip():
            pending_label = None
    return out


def headings_from_notebook(nb: dict) -> list[Heading]:
    out = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            out.extend(headings_from_markdown("".join(cell.get("source", []))))
    return out


def load_headings(path: Path) -> list[Heading]:
    if path.suffix == ".ipynb":
        return headings_from_notebook(json.loads(path.read_text(encoding="utf-8")))
    if path.suffix == ".md":
        return headings_from_markdown(path.read_text(encoding="utf-8"))
    if path.suffix == ".rst":
        return headings_from_rst(path.read_text(encoding="utf-8"))
    return []


def headings_from_rst(text: str) -> list[Heading]:
    """Good enough for anchor resolution: underlined (and over+underlined) titles."""
    lines = text.splitlines()
    out = []
    styles: list[str] = []
    for i in range(len(lines) - 1):
        t, u = lines[i], lines[i + 1]
        if t.strip() and u.strip() and len(set(u.strip())) == 1 and u.strip()[0] in '=-^~"\'`#*+:.' and len(u.strip()) >= 3 and not TOCTREE_RE.match(t):
            if i > 0 and lines[i - 1].strip() == u.strip():
                style = "over" + u.strip()[0]
            else:
                style = u.strip()[0]
            if style not in styles:
                styles.append(style)
            text_ = strip_inline_markup(re.sub(r"`([^`<]*)<[^>]*>`_+", r"\1", t.strip()))
            out.append(Heading(styles.index(style) + 1, text_, heading_id(text_), None))
    return out


def page_title(path: Path) -> str | None:
    hs = load_headings(path)
    return hs[0].text if hs else None


# --------------------------------------------------------------------- report
@dataclass
class Report:
    rows: list[tuple] = field(default_factory=list)

    def add(self, file: str, where: str, kind: str, old: str, new: str = ""):
        self.rows.append((file, where, kind, old, new))

    def count(self, kind: str) -> int:
        return sum(1 for r in self.rows if r[2] == kind)

    def print(self, title: str, kinds: set[str] | None = None):
        rows = [r for r in self.rows if kinds is None or r[2] in kinds]
        print(f"\n== {title} ({len(rows)} rows) ==")
        for f, w, k, o, n in rows:
            print(f"  {k:<18} {f}:{w}  {o}" + (f"  ->  {n}" if n else ""))

    def write_markdown(self, path: Path, title: str):
        lines = [f"# {title}", "", f"{len(self.rows)} rows.", "", "| kind | file | where | old | new |", "|---|---|---|---|---|"]
        for f, w, k, o, n in self.rows:
            esc = lambda s: str(s).replace("|", "\\|")
            lines.append(f"| {k} | `{esc(f)}` | {esc(w)} | `{esc(o)}` | `{esc(n)}` |" if n else f"| {k} | `{esc(f)}` | {esc(w)} | `{esc(o)}` |  |")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def write_notebook(path: Path, nb: dict) -> None:
    """Serialize like nbformat (sort_keys, indent=1, ensure_ascii=False)."""
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
