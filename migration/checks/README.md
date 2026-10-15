# Browser checks (Playwright + local Chrome)

Scripts used to compare the MyST build with the live Sphinx site in a real browser.
They need `playwright` (run via `uv run --with playwright python ...`) and a local
Google Chrome (`channel="chrome"`, so no browser download). Results are recorded in
`../agent-docs/05-verification.md`.

| Script | What it does |
|---|---|
| `probe_sphinx_pages.py BASE OUTDIR` | Screenshots + DOM counts (iframes, Leaflet maps, tiles, images, xarray reprs, sup, …) for the risky pages on the Sphinx site (old URLs). |
| `probe_myst_pages.py BASE OUTDIR` | Same for the MyST build (new URLs). |
| `probe_iframes.py BASE PAGE...` | Looks inside every iframe on a page: Leaflet containers, tiles loaded, htmlwidgets, size. Used for the R htmlwidget and folium outputs. |
| `probe_sizes.py URL` | Bounding boxes of Leaflet maps / widgets / iframes on one page. |
| `test_redirects.py [BASE]` | Opens old Sphinx URLs (with nbsphinx-style anchors) against the MyST build and reports where they land. |

Example (after `make build && make serve`):

```
uv run --with playwright python migration/checks/probe_myst_pages.py http://localhost:8000 /tmp/shots
uv run --with playwright python migration/checks/probe_iframes.py http://localhost:8000 technical-tutorials/working-with-r/vector-data-visualization/
uv run --with playwright python migration/checks/test_redirects.py http://localhost:8000
```
