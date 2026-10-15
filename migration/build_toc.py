"""Step 4 (runs before convert_rst so section pages can get their extra links):
turn the toctree tree into project.toc for myst.yml.

Rules (see agent-docs/02-decisions.md):
  * order and nesting preserved; .rst targets become .md
  * a file that appears in several toctrees is listed once, under the parent whose
    stem matches its folder name (else its first occurrence); the other section pages
    get an explicit markdown link after their inline {toc} list
  * orphan notebooks are appended as hidden entries to the top-level section whose
    folder contains them, so their URLs stay reachable as they were under Sphinx
"""
from __future__ import annotations

from pathlib import Path

from common import die, page_title


def _md(f: str) -> str:
    return f[:-4] + ".md" if f.endswith(".rst") else f


def run(ctx) -> None:
    inv = ctx.inventory
    src: Path = ctx.src
    tree = inv["toctree_tree"]

    # Occurrences of each file: (parent_file, position)
    occ: dict[str, list[str]] = {}

    def collect(node):
        for toc in node["toctrees"]:
            for child in toc["entries"]:
                occ.setdefault(child["file"], []).append(node["file"])
                collect(child)
    collect(tree)

    keep_under: dict[str, str] = {}
    for f, parents in occ.items():
        if len(parents) > 1:
            folder = Path(f).parent.name
            match = [p for p in parents if Path(p).stem == folder]
            keep_under[f] = match[0] if match else parents[0]

    ctx.extra_section_links = {}

    def entries(node) -> list[dict]:
        out = []
        for toc in node["toctrees"]:
            for child in toc["entries"]:
                f = child["file"]
                if f in keep_under and keep_under[f] != node["file"]:
                    title = page_title(src / f) or Path(f).stem
                    target = Path(f).relative_to(Path(node["file"]).parent).as_posix() if Path(f).is_relative_to(Path(node["file"]).parent) else f
                    ctx.extra_section_links.setdefault(node["file"], []).append((title, _md(target)))
                    ctx.report.add(node["file"], "", "TOC_DEDUP_LINK", f, f"listed under {keep_under[f]}")
                    continue
                e = {"file": _md(f)}
                ch = entries(child)
                if ch:
                    e["children"] = ch
                out.append(e)
        return out

    toc = [{"file": "index.md"}] + entries(tree)

    # Orphans -> hidden entries under the section owning their top folder
    def top_folders(node, acc: set):
        for t in node["toctrees"]:
            for c in t["entries"]:
                acc.add(Path(c["file"]).parts[0])
                top_folders(c, acc)
        return acc
    sections = [c for t in tree["toctrees"] for c in t["entries"]]
    for orphan in inv["orphans"]:
        top = Path(orphan).parts[0]
        owners = [s for s in sections if top in top_folders(s, set())]
        if not owners:
            die(f"orphan {orphan} cannot be assigned to a section (new folder?)")
        sec = next(e for e in toc if e["file"] == _md(owners[0]["file"]))
        sec.setdefault("children", []).append({"file": _md(orphan), "hidden": True})
        ctx.report.add(orphan, "", "TOC_ORPHAN_HIDDEN", orphan, f"under {owners[0]['file']}")

    ctx.toc = toc
    n = sum(1 for _ in _walk(toc))
    print(f"[build_toc] {n} toc entries ({len(keep_under)} deduplicated, {len(inv['orphans'])} hidden orphans)")


def _walk(entries):
    for e in entries:
        yield e
        yield from _walk(e.get("children", []))
