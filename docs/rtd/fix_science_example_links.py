#!/usr/bin/env python3
"""Point Science Examples links at pages in the current site version.

MyST's ``{toc}`` links can lose the Read the Docs version prefix. On
case-insensitive file systems, some also resolve as static notebook downloads.
The generated links retain their intended page URLs in ``urlSource``. Correct
the built page and its client-side JSON without changing the source toc.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def site_prefix(override: str | None) -> str:
    if override is not None:
        return "/" + override.strip("/") if override.strip("/") else ""
    if os.environ.get("READTHEDOCS") == "True":
        language = os.environ["READTHEDOCS_LANGUAGE"]
        version = os.environ["READTHEDOCS_VERSION"]
        return f"/{language}/{version}"
    return "/" + os.environ["BASE_URL"].strip("/") if os.environ.get("BASE_URL", "").strip("/") else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, default=Path("docs/source/_build/html"))
    parser.add_argument("--base-url", help="Site path prefix, for example /en/latest/")
    args = parser.parse_args()

    page_json = args.html / "science-examples.json"
    page_html = args.html / "science-examples" / "index.html"
    data = json.loads(page_json.read_text(encoding="utf-8"))
    prefix = site_prefix(args.base_url)
    replacements: dict[str, str] = {}

    def fix_links(node: object) -> None:
        if isinstance(node, dict):
            source = node.get("urlSource")
            url = node.get("url")
            if node.get("type") == "link" and isinstance(source, str) and source.startswith("/science/") and isinstance(url, str):
                destination = prefix + source
                if url != destination:
                    replacements[url] = destination
                    node["url"] = destination
            for value in node.values():
                fix_links(value)
        elif isinstance(node, list):
            for value in node:
                fix_links(value)

    fix_links(data["mdast"])
    html = page_html.read_text(encoding="utf-8")
    original_html = html
    for old, new in replacements.items():
        old_href = f'href="{old}"'
        new_href = f'href="{new}"'
        if old_href not in html and new_href not in html:
            raise ValueError(f"Generated HTML is missing Science Examples link {old}")
        html = html.replace(old_href, new_href)
        html = html.replace(f'"url":"{old}"', f'"url":"{new}"')
    if prefix:
        html = html.replace('"url":"/science/', f'"url":"{prefix}/science/')
    if replacements or html != original_html:
        page_json.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        page_html.write_text(html, encoding="utf-8")
    print(f"[fix_science_example_links] corrected {len(replacements)} Science Examples links")


if __name__ == "__main__":
    main()
