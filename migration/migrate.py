#!/usr/bin/env python3
"""Deterministic Sphinx -> MyST migration of docs/source.

Run from a pristine Sphinx tree (see agent-docs/00-overview.md):
    git checkout develop -- docs/source && git clean -fd docs/source
    uv run python migration/migrate.py [--src DIR] [--strict]

Steps: inventory -> build_toc -> convert_rst -> rewrite_links -> write_config -> cleanup.
A full report of every change goes to migration/out/migration-report.md and to stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

import build_toc, cleanup, convert_rst, inventory, rewrite_links, write_config  # noqa: E402
from common import DEFAULT_SRC, OUT_DIR, Report, slug_path  # noqa: E402


@dataclass
class Context:
    src: Path
    report: Report = field(default_factory=Report)
    inventory: dict = field(default_factory=dict)
    toc: list = field(default_factory=list)
    extra_section_links: dict = field(default_factory=dict)
    overrides: dict = field(default_factory=dict)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="MyST project root (default docs/source)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on unresolved links")
    ap.add_argument("--skip-cleanup", action="store_true")
    args = ap.parse_args()
    ctx = Context(src=args.src.resolve())
    ctx.overrides = yaml.safe_load((Path(__file__).parent / "overrides.yml").read_text()) or {}

    inventory.run(ctx)
    build_toc.run(ctx)
    convert_rst.run(ctx)
    rewrite_links.run(ctx)
    write_config.run(ctx)
    if not args.skip_cleanup:
        cleanup.run(ctx)

    # Redirect map for the old Sphinx URLs (committed; used post-build by gen_redirects.py)
    redirect_map = {}
    for old in ctx.inventory["old_pages"]:
        new = slug_path(old + ".md")
        redirect_map[old + ".html"] = "/" + (new + "/" if new else "")
    (Path(__file__).parent / "redirect_map.json").write_text(json.dumps(redirect_map, indent=1, sort_keys=True) + "\n")

    OUT_DIR.mkdir(exist_ok=True)
    ctx.report.write_markdown(OUT_DIR / "migration-report.md", "Migration report")
    ctx.report.print("Link rewrites", {"REWRITTEN"})
    ctx.report.print("Needs attention", {"ANCHOR_UNRESOLVED", "ANCHOR_UNRESOLVED_ALLOWED", "MISSING", "MISSING_ALLOWED", "OTHER_UNTOUCHED", "NB_REFORMATTED", "TOC_DEDUP_LINK", "TOC_ORPHAN_HIDDEN"})
    bad = ctx.report.count("ANCHOR_UNRESOLVED") + ctx.report.count("MISSING")
    print(f"\nDone. {len(redirect_map)} redirects mapped. Unresolved/missing links: {bad}. Report: {OUT_DIR / 'migration-report.md'}")
    return 1 if (args.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
