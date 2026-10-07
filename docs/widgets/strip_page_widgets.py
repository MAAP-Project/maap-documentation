#!/usr/bin/env python3
"""Post-build: drop the duplicated ipywidgets state from pages whose widgets were exported.

mystmd copies an executed notebook's whole `metadata.widgets` block (every model's state,
including each anywidget's full JS bundle and any inlined data) into the page JSON as
`widgets`, for the theme's own live-kernel ipywidgets rendering. The
myst-anywidget-static-export plugin has already turned those outputs into self-contained
`anywidget` nodes (with the JS written to sidecar files), so on such pages `widgets` is
dead weight: the NISAR access page was 6.2 MB, 3.8 MB of it this block. The plugin cannot
remove it itself (plugin transforms only see the AST, and mystmd attaches `widgets` after
they run), hence this step. See docs/widgets/README.md.

A page is only stripped when its AST contains `anywidget` nodes AND no un-exported
`widget-view` output remains (those would still need the state to render live).

Usage: python docs/widgets/strip_page_widgets.py [--html docs/source/_build/html]
Runs after `myst build --html` (Makefile `build`, .readthedocs.yml).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_HTML = HERE.parent / "source" / "_build" / "html"
WIDGET_VIEW_MIME = "application/vnd.jupyter.widget-view+json"


def has_node_type(node, type_name: str) -> bool:
    if isinstance(node, dict):
        if node.get("type") == type_name:
            return True
        return any(has_node_type(v, type_name) for v in node.values())
    if isinstance(node, list):
        return any(has_node_type(v, type_name) for v in node)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = ap.parse_args()
    html = args.html.resolve()
    if not (html / "index.html").exists():
        print(f"ERROR: {html}/index.html not found; run `myst build --html` first", file=sys.stderr)
        return 1
    stripped, kept, saved = 0, [], 0
    # Page data files live flat in the html root as <slug>.json (config/xref/search JSON lack `mdast`).
    for page in sorted(html.glob("*.json")):
        data = json.loads(page.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "mdast" not in data or not data.get("widgets"):
            continue
        if not has_node_type(data["mdast"], "anywidget"):
            continue
        if WIDGET_VIEW_MIME in json.dumps(data["mdast"]):
            kept.append(page.name)  # some widget outputs were not exported; the theme may still need the state
            continue
        before = page.stat().st_size
        data["widgets"] = {}
        page.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        saved += before - page.stat().st_size
        stripped += 1
    print(f"[strip_page_widgets] removed duplicated widget state from {stripped} page(s) in {html} ({saved / 1e6:.1f} MB)")
    for name in kept:
        print(f"[strip_page_widgets] kept widgets on {name}: it still has un-exported widget-view outputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
