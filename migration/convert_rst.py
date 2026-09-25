"""Step 2: convert every .rst to MyST Markdown.

Pipeline per file: pre-process rst text -> rst2myst (pinned 0.4.0 via uvx) ->
post-process markdown -> write .md and delete the .rst.
Links are NOT rewritten here (rewrite_links handles .md and .ipynb uniformly).
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from common import die, iter_files, rel, parse_toctrees

RST2MYST = ["uvx", "--python", "3.12", "--from", "rst-to-myst[sphinx]==0.4.0", "rst2myst", "stream", "-"]
LINEBREAK = "@@LINEBREAK@@"
ADORN = '=-^~"\'`#*+:.'


def _is_adornment(line: str) -> bool:
    s = line.strip()
    return len(s) >= 3 and len(set(s)) == 1 and s[0] in ADORN


def preprocess(text: str, relpath: str) -> str:
    lines = text.splitlines()

    # Leading tabs -> spaces (docutils would also do this, but keeps logs clean)
    lines = [re.sub(r"^\t+", lambda m: "    " * len(m.group(0)), l) for l in lines]

    # index.rst: drop the "Indices and tables" boilerplate (genindex/modindex/search)
    if relpath == "index.rst":
        for i, l in enumerate(lines):
            if l.strip() == "Indices and tables" and i + 1 < len(lines) and _is_adornment(lines[i + 1]):
                lines = lines[:i]
                break

    # Pad too-short underlines / overlines so docutils does not warn
    # Only unindented lines can be section titles/adornments; indented ones are
    # directive bodies (e.g. '...' inside a json code-block).
    for i in range(len(lines)):
        if (_is_adornment(lines[i]) and not lines[i][:1].isspace() and i >= 1 and lines[i - 1].strip()
                and not lines[i - 1][:1].isspace() and not _is_adornment(lines[i - 1])):
            title_len = len(lines[i - 1].rstrip())
            if len(lines[i].strip()) < title_len:
                lines[i] = lines[i].strip()[0] * title_len
                if i >= 2 and _is_adornment(lines[i - 2]) and lines[i - 2].strip()[0] == lines[i].strip()[0]:
                    lines[i - 2] = lines[i]

    # Line blocks: '| a' / '| b' -> one paragraph with hard line breaks
    out = []
    i = 0
    while i < len(lines):
        if re.match(r"^\|( |$)", lines[i]):
            block = []
            while i < len(lines) and re.match(r"^\|( |$)", lines[i]):
                block.append(re.sub(r"^\s*\|\s?", "", lines[i]).rstrip())
                i += 1
            out.append((" " + LINEBREAK + " ").join(block))
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + "\n"


def run_rst2myst(rst_text: str, name: str) -> str:
    proc = subprocess.run(RST2MYST, input=rst_text, capture_output=True, text=True)
    if proc.returncode != 0:
        die(f"rst2myst failed on {name}:\n{proc.stderr}")
    warnings = [l for l in proc.stderr.splitlines() if l.strip() and "line_block" not in l and "docutils.nodes.line" not in l]
    for w in warnings:
        print(f"[convert_rst] rst2myst {name}: {w}")
    return proc.stdout


TOCTREE_FENCE_RE = re.compile(r"^```\{toctree\}\n(?P<body>.*?)^```\n?", re.S | re.M)


def postprocess(md: str, relpath: str, original_labels: list[str], extra_links: list[tuple[str, str]]) -> str:
    # 1. Sphinx-quickstart comment block at top of index (invisible in both systems)
    if relpath == "index.rst":
        md = re.sub(r"\A(%[^\n]*\n)+\n?", "", md)

    # 2. toctree fences -> caption paragraph + {toc} directive
    def repl(m):
        body = m.group("body")
        opts = dict(re.findall(r"^:(\w+):\s*(.*)$", body, re.M))
        caption = opts.get("caption", "").strip().strip("'\"")
        depth = opts.get("maxdepth", "").strip()
        parts = []
        if caption:
            parts.append(f"**{caption}**\n")
        if relpath == "index.rst":
            directive = "```{toc}\n:context: project\n:depth: 1\n```"
        else:
            directive = "```{toc}\n:context: children\n" + (f":depth: {depth}\n" if depth else "") + "```"
        parts.append(directive)
        if extra_links:
            parts.append("\n" + "\n".join(f"- [{title}]({target})" for title, target in extra_links))
        return "\n".join(parts) + "\n"
    md = TOCTREE_FENCE_RE.sub(repl, md)

    # 3. Restore original label text (rst2myst normalises e.g. a_b -> a-b; {ref} keeps a_b)
    for lab in original_labels:
        norm = re.sub(r"[^a-z0-9]+", "-", lab.lower()).strip("-")
        md = re.sub(rf"^\({re.escape(norm)}\)=\s*$", f"({lab})=", md, flags=re.M)

    # 4. Line-block markers -> hard line breaks
    md = re.sub(r"\s*" + re.escape(LINEBREAK) + r"\s*", "\\\\\n", md)

    # 5. Whitespace normalisation
    md = re.sub(r"[ \t]+$", "", md, flags=re.M)
    md = re.sub(r"\n{3,}", "\n\n", md).strip("\n") + "\n"

    if "{eval-rst}" in md:
        die(f"{relpath}: eval-rst block survived conversion")
    return md


def run(ctx) -> None:
    src: Path = ctx.src
    rst_files = iter_files(src, {".rst"})
    print(f"[convert_rst] converting {len(rst_files)} rst files")
    for path in rst_files:
        relpath = rel(src, path)
        text = path.read_text(encoding="utf-8")
        labels = re.findall(r"^\.\. _([^:\s]+):\s*$", text, re.M)
        extra = ctx.extra_section_links.get(relpath, [])
        md = postprocess(run_rst2myst(preprocess(text, relpath), relpath), relpath, labels, extra)
        md_path = path.with_suffix(".md")
        md_path.write_text(md, encoding="utf-8")
        path.unlink()
        ctx.report.add(relpath, "", "RST_CONVERTED", relpath, rel(src, md_path))
