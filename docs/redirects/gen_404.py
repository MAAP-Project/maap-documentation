#!/usr/bin/env python3
"""Post-build: write a standalone 404.html that sends new MyST URLs to the old Sphinx pages.

Older documentation versions on Read the Docs (the release tags, `last-ade-release`, …) are
Sphinx builds with URLs like /en/stable/getting_started.html. The RTD version menu keeps the
current path when switching versions, so from a MyST page (/en/develop/getting-started/) it
links to /en/stable/getting-started/, which does not exist in a Sphinx version.

Read the Docs serves 404.html from the requested version or, if that version has none (the
Sphinx builds have none), from the default version. This page looks the MyST path up in
redirect_map.json (reversed) and redirects to the Sphinx path in the same version; otherwise
it shows a plain "page not found" with a link to that version's home page.

The page is plain HTML (not a MyST/React page) because RTD serves it under any version and
URL, so it must not depend on the build's assets. It only maps MyST -> Sphinx paths: the
reverse direction is handled by the redirect stubs (gen_redirects.py), and mapping one way
only means a missing Sphinx page cannot bounce back and forth.

Usage: python docs/redirects/gen_404.py [--html docs/source/_build/html]
Runs after `myst build --html` (Makefile `build`, .readthedocs.yml).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_HTML = HERE.parent / "source" / "_build" / "html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Page not found - MAAP User Documentation</title>
<style>
  body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; max-width: 40rem;
         margin: 4rem auto; padding: 0 1rem; line-height: 1.5; color: #1f2937; }}
  a {{ color: #1d4ed8; }}
  #redirecting {{ display: none; }}
</style>
<script>
(function () {{
  // New MyST path (no surrounding slashes) -> old Sphinx path, from redirect_map.json.
  var OLD = {reverse_map};
  // Read the Docs paths look like /<language>/<version>/<page>; elsewhere the site is at /.
  var m = location.pathname.match(/^(\\/[a-z]{{2}}(?:-[a-z]+)?\\/[^\\/]+\\/)(.*)$/);
  var base = m ? m[1] : "/";
  var page = (m ? m[2] : location.pathname.slice(1)).replace(/index\\.html$/, "").replace(/\\/+$/, "");
  window.MAAP_404_BASE = base;
  if (Object.prototype.hasOwnProperty.call(OLD, page)) {{
    document.documentElement.className = "redirecting";
    location.replace(base + OLD[page] + location.hash);
  }}
}})();
</script>
<style>.redirecting #notfound {{ display: none; }} .redirecting #redirecting {{ display: block; }}</style>
</head>
<body>
<p id="redirecting">Redirecting to this page in this version of the documentation…</p>
<div id="notfound">
<h1>Page not found</h1>
<p>This page does not exist in this version of the MAAP User Documentation. It may have moved,
or it may not exist in the version you switched to.</p>
<p><a id="home" href="/">Go to the documentation home page</a> for this version.</p>
</div>
<script>document.getElementById("home").href = window.MAAP_404_BASE || "/";</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = ap.parse_args()
    html = args.html.resolve()
    if not (html / "index.html").exists():
        print(f"ERROR: {html}/index.html not found; run `myst build --html` first", file=sys.stderr)
        return 1
    mapping = json.loads((HERE / "redirect_map.json").read_text())
    reverse = {new.strip("/"): old for old, new in mapping.items() if new.strip("/")}
    if len(set(reverse)) != len([n for n in mapping.values() if n.strip("/")]):
        print("ERROR: two old pages map to the same new path", file=sys.stderr)
        return 1
    dest = html / "404.html"
    if dest.exists():
        print(f"[gen_404] replacing the existing {dest}")
    reverse_json = json.dumps(reverse, sort_keys=True, separators=(",", ":"))
    dest.write_text(TEMPLATE.format(reverse_map=reverse_json), encoding="utf-8")
    print(f"[gen_404] wrote {dest} ({len(reverse)} MyST -> Sphinx paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
