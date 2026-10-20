#!/usr/bin/env python3
"""Post-build: give Read the Docs' ad an explicit slot outside the React-rendered page.

On mystmd sites RTD's EthicalAds add-on otherwise appends its ad to <article>. When that
happens before the MyST theme (React) has hydrated the page, React sees HTML it did not
render (error #418), clears the whole document and re-renders it, which also deletes the
RTD version flyout, search and notifications (https://github.com/readthedocs/addons/issues/278).

If a page contains an element matching `[data-ea-publisher]`, RTD fills that element instead
(https://docs.readthedocs.com/platform/stable/advertising/ad-customization.html). This script
adds one as the last child of <body> in every MyST page; React leaves trailing body nodes
alone, so hydration succeeds and the RTD add-ons stay.

Usage: python docs/rtd/add_ad_slot.py [--html docs/source/_build/html]
Runs after `myst build --html` (Makefile `build`, .readthedocs.yml).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_HTML = HERE.parent / "source" / "_build" / "html"
SLOT = '<div id="ethical-ad-placement" data-ea-publisher="readthedocs" data-ea-type="text"></div>'
MYST_PAGE_MARKER = "window.__remixContext"  # redirect stubs and other files lack it


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = ap.parse_args()
    html = args.html.resolve()
    if not (html / "index.html").exists():
        print(f"ERROR: {html}/index.html not found; run `myst build --html` first", file=sys.stderr)
        return 1
    patched = 0
    for page in sorted(html.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        if MYST_PAGE_MARKER not in text or SLOT in text:
            continue
        if text.count("</body>") != 1:
            print(f"ERROR: expected one </body> in {page}", file=sys.stderr)
            return 1
        page.write_text(text.replace("</body>", SLOT + "</body>"), encoding="utf-8")
        patched += 1
    print(f"[add_ad_slot] added the RTD ad slot to {patched} pages in {html}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
