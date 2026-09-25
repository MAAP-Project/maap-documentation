#!/usr/bin/env python3
"""Post-build verification of the MyST site against the Sphinx inventory.

Checks:
  1. every old Sphinx page URL has a built MyST page (via redirect_map.json) and a stub
  2. every toc `file:` entry produced a page directory with index.html
  3. the build log (if given) has no unknown directive / unexpected option / missing file
  4. output audit: per notebook, the cell outputs in the source .ipynb versus the output
     nodes in the built page JSON (_build/site/content/*.json), by MIME type

Usage: python migration/verify.py [--src docs/source] [--log build.log]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_SRC, slug_path  # noqa: E402

HERE = Path(__file__).resolve().parent
BAD_LOG_PATTERNS = ["unknown directive", "unexpected option", "Referenced file not found", "not found in project", "❌"]


def toc_files(entries):
    for e in entries:
        if "file" in e:
            yield e["file"]
        yield from toc_files(e.get("children", []))


def notebook_output_mimes(nb_path: Path) -> Counter:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    c: Counter = Counter()
    for cell in nb.get("cells", []):
        for o in cell.get("outputs", []) or []:
            t = o.get("output_type")
            if t in ("display_data", "execute_result"):
                for mime in o.get("data", {}):
                    c[mime] += 1
            elif t == "stream":
                c["stream/" + o.get("name", "?")] += 1
            elif t == "error":
                c["error"] += 1
    return c


def built_output_mimes(content_json: Path) -> Counter:
    d = json.loads(content_json.read_text(encoding="utf-8"))
    c: Counter = Counter()

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "output":
                jd = n.get("jupyter_data") or {}
                t = jd.get("output_type")
                if t in ("display_data", "execute_result"):
                    for mime in (jd.get("data") or {}):
                        c[mime] += 1
                elif t == "stream":
                    c["stream/" + jd.get("name", "?")] += 1
                elif t == "error":
                    c["error"] += 1
                elif "data" in n and isinstance(n["data"], list):
                    for o in n["data"]:
                        ot = o.get("output_type")
                        if ot in ("display_data", "execute_result"):
                            for mime in (o.get("data") or {}):
                                c[mime] += 1
                        elif ot == "stream":
                            c["stream/" + o.get("name", "?")] += 1
                        elif ot == "error":
                            c["error"] += 1
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(d)
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    ap.add_argument("--log", type=Path)
    args = ap.parse_args()
    src = args.src.resolve()
    html = src / "_build" / "html"
    content = src / "_build" / "site" / "content"
    failures = 0

    cfg = yaml.safe_load((src / "myst.yml").read_text())
    files = list(toc_files(cfg["project"]["toc"]))

    # 1 + 2: pages and stubs
    mapping = json.loads((HERE / "redirect_map.json").read_text())
    for old, new in mapping.items():
        page = html / new.strip("/") / "index.html"
        if not page.exists():
            print(f"FAIL page missing: {new} (from {old})"); failures += 1
        if old != "index.html" and not (html / old).exists():
            print(f"FAIL redirect stub missing: {old}"); failures += 1
    for f in files:
        sp = slug_path(f)
        page = html / sp / "index.html"
        if not page.exists():
            print(f"FAIL toc entry not built: {f} -> {sp}"); failures += 1
    print(f"[verify] {len(files)} toc files, {len(mapping)} old URLs checked, {sum(1 for p in html.rglob('index.html'))} index.html files in build")

    # 3: build log
    if args.log and args.log.exists():
        log = args.log.read_text(encoding="utf-8", errors="replace")
        for pat in BAD_LOG_PATTERNS:
            for line in log.splitlines():
                if pat in line:
                    print(f"FAIL build log: {line.strip()}"); failures += 1
        warns = [l for l in log.splitlines() if "⚠️" in l]
        print(f"[verify] build log: {len(warns)} warnings")

    # 4: output audit
    mismatches = 0
    for f in files:
        if not f.endswith(".ipynb"):
            continue
        src_c = notebook_output_mimes(src / f)
        cj = content / (slug_path(f).replace("/", ".") + ".json")
        if not cj.exists():
            print(f"FAIL content json missing for {f}: {cj.name}"); failures += 1
            continue
        built_c = built_output_mimes(cj)
        if src_c != built_c:
            mismatches += 1
            diff = {k: (src_c.get(k, 0), built_c.get(k, 0)) for k in set(src_c) | set(built_c) if src_c.get(k, 0) != built_c.get(k, 0)}
            print(f"OUTPUT MISMATCH {f}: source vs built {diff}")
    print(f"[verify] output audit: {mismatches} notebooks with output differences")
    failures += mismatches

    print("[verify] " + ("OK" if failures == 0 else f"{failures} problems"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
