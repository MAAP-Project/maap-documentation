"""Step 1: inventory the pristine Sphinx tree.

Produces ctx.inventory (also written to migration/out/inventory.json):
  toctree_tree   nested structure starting at index.rst, in source order
  toctree_files  every file referenced by any toctree (relative to src)
  orphans        page files (.ipynb/.rst) not in any toctree
  old_pages      every page path Sphinx built, as '<path-without-ext>' (for redirects)
"""
from __future__ import annotations

import json
from pathlib import Path

from common import PAGE_EXTS, OUT_DIR, die, iter_files, parse_toctrees, rel


def build_tree(src: Path, file: str, seen_stack: tuple = ()) -> dict:
    node = {"file": file, "toctrees": []}
    path = src / file
    if path.suffix != ".rst" or not path.exists():
        return node
    if file in seen_stack:
        die(f"toctree cycle at {file}")
    for toc in parse_toctrees(src, path):
        node["toctrees"].append({
            "options": toc.options,
            "entries": [build_tree(src, e, seen_stack + (file,)) for e in toc.entries],
        })
    return node


def flatten(node: dict, acc: list[str]) -> None:
    for toc in node["toctrees"]:
        for child in toc["entries"]:
            acc.append(child["file"])
            flatten(child, acc)


def run(ctx) -> None:
    src: Path = ctx.src
    if not (src / "index.rst").exists():
        die(f"{src}/index.rst not found: inventory must run on the pristine Sphinx tree")
    tree = build_tree(src, "index.rst")
    toc_files: list[str] = []
    flatten(tree, toc_files)
    all_pages = [rel(src, p) for p in iter_files(src, PAGE_EXTS)]
    missing = [f for f in toc_files if not (src / f).exists()]
    if missing:
        die(f"toctree entries missing on disk: {missing}")
    orphans = [p for p in all_pages if p not in toc_files and p != "index.rst"]
    old_pages = sorted({str(Path(p).with_suffix("")) for p in all_pages})
    ctx.inventory = {
        "toctree_tree": tree,
        "toctree_files": toc_files,
        "orphans": orphans,
        "old_pages": old_pages,
        "page_files": all_pages,
    }
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "inventory.json").write_text(json.dumps(ctx.inventory, indent=1), encoding="utf-8")
    dup = sorted({f for f in toc_files if toc_files.count(f) > 1})
    print(f"[inventory] {len(all_pages)} page files, {len(set(toc_files))} distinct in toctrees, "
          f"{len(orphans)} orphans, {len(dup)} files in more than one toctree: {dup}")
    print(f"[inventory] orphans: {orphans}")
