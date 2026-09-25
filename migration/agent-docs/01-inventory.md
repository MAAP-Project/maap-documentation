# Inventory of the Sphinx site (as of develop @ 0dcbe21, 2026-09-11)

## Layout

- Everything lives in `docs/source/`: `conf.py`, `index.rst`, 6 section `.rst` pages,
  20 `.rst` files in total, 90 `.ipynb`, no Markdown sources.
- Images: `docs/source/_static/` (~120 files plus 8 sub-folders), and nested
  `getting_started/_static/`, `system_reference_guide/faq/_static/`,
  `technical_tutorials/dps_tutorial/_static/`, `science/ESA_CCI/images/`, plus loose
  images next to notebooks (`science/HLS/*.png`,
  `technical_tutorials/search/federated-collection-discovery/*.png`,
  `technical_tutorials/search/maap-stac-browser.png`).
- Non-page content referenced from notebooks:
  `system_reference_guide/example_conda_configuration_files/*.yml`,
  `technical_tutorials/dps_tutorial/algorithm_config_template.yml`,
  `technical_tutorials/user_data/demo_memory_profiling*.py`.
- Build: RTD (`.readthedocs.yml`, sphinx builder, python 3.11, `requirements.txt`,
  formats pdf + epub). No GitHub Actions. Published at `https://docs.maap-project.org`
  (RTD project `maap-project`; versions `/en/latest` = master, `/en/stable` = tags,
  `/en/develop`, frozen `/en/last-ade-release`).

## Sphinx configuration (`docs/source/conf.py`)

- Extensions: `nbsphinx`, `IPython.sphinxext.ipython_console_highlighting`,
  `sphinx_copybutton`. `nbsphinx_execute = 'never'` (stored outputs only).
- Theme `sphinx_rtd_theme`, `logo_only`, logo `_static/nasamaap_logo.png`, favicon
  `_static/maapsheep-80x80.png`, `navigation_depth: 4`.
- `setup(app)` injects `custom.css` (RTD-theme selectors only) and, from CDNs,
  Leaflet 1.9.4 CSS/JS, proj4js, proj4leaflet, leaflet-providers, plus RequireJS via
  `nbsphinx_requirejs_path`. Purpose: make the R htmlwidgets leaflet outputs work.
- No intersphinx, autodoc, substitutions, prolog/epilog, templates, extra JS,
  sitemap, analytics or redirects.

## rst usage

| Construct | Count | Where |
|---|---|---|
| `.. toctree::` | 15 | index + 6 section pages + 8 nested section pages |
| `.. code-block::` | 8 | `search/catalog.rst`, `user_data/stac_metadata.rst`, `personal_access_tokens.rst` |
| `.. note::` / `.. warning::` | 2 + 2 | `personal_access_tokens.rst`, `searching.rst` (tab-indented body) |
| `.. image::` | 2 | `personal_access_tokens.rst` (`:alt:`, `:width: 100%`) |
| `.. attention::` | 1 | `index.rst` |
| `:sup:` role | 33 | `technical_tutorials/user_data/stac_metadata.rst` (pattern ``` ``element``:sup:`1,2` ```) |
| `:ref:` role | 6 | 3 boilerplate (genindex/modindex/search) in `index.rst`; `Working with R <working_with_r_section>` x2 in `technical_tutorials.rst`; `pat-nasa-esa` in `personal_access_tokens.rst` |
| Labels | 2 | `working_with_r_section` (`technical_tutorials/working_with_r.rst`), `pat-nasa-esa` (`personal_access_tokens.rst`) |
| Line blocks (`| text`) | many | `release_notes.rst` (release date + summary lines) |
| Hand-written relative `.html` links | 9 | `release_notes.rst` (with nbsphinx anchors), `searching.rst`, `search/catalog.rst`; `stac_metadata.rst` links to an `.ipynb` |

Other rst quirks: `release_notes.rst` uses over+underlined version titles and `^^^^`
underlines shorter than their titles; several section files lack a trailing newline;
no tables, definition lists, includes, raw blocks, or substitutions.

## Navigation (toctrees)

```
index.rst (maxdepth 1)
  getting_started.rst            -> 5 notebooks in getting_started/
  science_examples.rst           -> 19 notebooks + science/oss_documentation.rst (3 notebooks)
  technical_tutorials.rst        -> dps_tutorial/dps_tutorial_demo.ipynb,
                                    searching.rst (7 nb + search/catalog.rst + working_with_r/find_data_in_r.rst),
                                    visualizing.rst (7 nb), accessing.rst (9 nb + find_data_in_r.rst),
                                    querying.rst (1 nb), user_data.rst (2 nb + user_data/stac_metadata.rst),
                                    working_with_r.rst (find_data_in_r.rst + 8 nb)
  system_reference.rst           -> 13 nb + personal_access_tokens.rst,
                                    ade_custom_extensions.rst (2 nb), faq.rst (6 nb)
  troubleshooting_guides.rst     -> 3 notebooks
  release_notes.rst
```

Captions used: "Getting Started:", "Science Examples:", "System Reference Guide:",
"Search Topics:", "Visualize:", "Access:", "Query:", "User Data:". No `:hidden:`,
`:glob:`, `:titlesonly:` or explicit entry titles.

Quirks:
- `technical_tutorials/working_with_r/find_data_in_r.rst` appears in 3 toctrees
  (searching, accessing, working_with_r). It is a 3-line stub linking to OpenScapes.
- 5 notebooks are in no toctree but are built by Sphinx and reachable by URL, two are
  linked from other notebooks: `science/GEE/gee.ipynb`,
  `science/NISAR/Simulated_NISAR.ipynb`, `system_reference_guide/Secrets_Manager.ipynb`
  (linked from `jobs_maappy.ipynb`), `technical_tutorials/dps_tutorial/DPS_runner_template.ipynb`
  (linked), `technical_tutorials/dps_tutorial/dps_stac_metadata.ipynb`.

## Notebooks (90)

- nbformat 4.2 (2), 4.4 (28), 4.5 (60). Kernels: python3 70, R (`ir`/`ir4`) 9,
  conda env kernels 9, other 2. 55 notebooks have stored outputs, 35 have none.
- No nbsphinx metadata, all cell tag lists empty, no `%%html`, no attachments.
- One raw cell: `technical_tutorials/access/direct_access.ipynb` (a shell snippet, no
  `raw_mimetype`).
- 8 notebooks whose first heading is `##`/`###` (nbsphinx used it as the page title):
  `getting_started/{about_maap,getting_started,maap_overview}.ipynb`,
  `science/ESA_CCI/ESA_CCI_V4.ipynb`,
  `system_reference_guide/{accessing_bucket_data,create_workspace,share_data,ssh}.ipynb`.
  `getting_started/running_at_scale.ipynb` has two H1s.

### Output MIME types across all notebooks

| MIME | Cells | Notes |
|---|---|---|
| text/plain | 192 | |
| text/html | 88 (29 notebooks) | pandas tables, xarray reprs (`<style>` + `<svg>`), pystac `<style>` blocks, folium `<iframe srcdoc>` (12 notebooks), R htmlwidgets as full `<!doctype html>` documents (2 notebooks: `technical_tutorials/working_with_r/visualizing_with_titiler-pgstac.ipynb`, `vector_data_visualization.ipynb`), R `<style> .list-inline` vectors |
| image/png | 31 | |
| text/latex | 30 | |
| text/markdown | 30 | |
| application/vnd.jupyter.widget-view+json | 7 (2 notebooks) | `visualize_lonboard.ipynb`, `Visualizing_OPERA-DISP_tile_with_TiTiler-MultiDim.ipynb`; no widget state saved, so only the text/plain fallback renders today |
| application/geo+json | 2 | |
| application/vnd.holoviews_exec.v0+json | 1 | |

Largest notebooks: `science/HLS/HLSL30.ipynb` 3.0 MB, `working_with_r/vector_data_visualization.ipynb` 2.9 MB, `science/GEDI/GEDI_L2A.ipynb` 2.6 MB.

### Links inside notebook markdown cells

| Kind | Count |
|---|---|
| external http(s) | 255 |
| relative assets (images, yml, py) | 173 |
| absolute `https://docs.maap-project.org/...` | 91 (41 of them to `getting_started/getting_started.html`; some to `/en/develop/` and `/en/troubleshooting-section/`) |
| relative `.ipynb` | 36 (several with nbsphinx anchors, e.g. `#Container-URLs`, `#Submit-a-Job`) |
| relative `.rst` | 4 (`../science_examples.rst`, `../system_reference.rst`, `../technical_tutorials.rst`) |
| relative `.html` | 3 (`../system_reference_guide/custom-environments.html#Custom-environments`, `getting_started.html#Creating-a-workspace`, `custom-environments.html#Custom-environments`) |
| in-page `#anchor` | 6 |
| known broken | `../granules.ipynb` (no such file at that depth) |

Inline HTML in markdown cells: `<img src="../_static/gitlab2.png" height="450">`
(`work_with_git.ipynb`), `<div class="alert alert-block alert-info">` with an
`<a href="federated-collection-discovery/collection_discovery.html">`
(`search/collections.ipynb`), `<sub>` (`troubleshooting/kernel_resetting.ipynb`),
literal `.. note::` text in `custom-environments.ipynb` (renders as plain text today).

Anchor formats: nbsphinx = heading text with spaces replaced by `-`, case and
punctuation preserved (`#Passing-Credentials-for-Other-Services-into-Jobs-(Secrets-Management)`).
mystmd = lowercase, non-alphanumerics to `-`, collapsed
(`#passing-credentials-for-other-services-into-jobs-secrets-management`).
