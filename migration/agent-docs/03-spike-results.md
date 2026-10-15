# Spike results

Real-build answers to the open questions, with evidence. Spike setup: a copy of
`docs/source` in the scratchpad with a hand-written `myst.yml` (18 pages covering the
risky notebooks), built with `mystmd 1.10.1` on Node 22 via `myst build --html`, served
over HTTP and probed with Playwright/Chrome (DOM counts, iframe contents, screenshots).
The baseline is the live site `https://docs.maap-project.org/en/latest/` probed the same
way, plus a local Sphinx build of `develop` (system pandoc 3.x via Homebrew).

## Baseline facts (live Sphinx site, 2026-09-11)

| Page | What renders today |
|---|---|
| `working_with_r/visualizing_with_titiler-pgstac` | 2 interactive Leaflet maps (htmlwidgets) inline, 650x400 px (100% of the 696 px content column); 31 tiles loaded; 5 broken tile images (titiler tiles); RequireJS "Mismatched anonymous define()" page errors, maps still work |
| `working_with_r/vector_data_visualization` | 3 interactive Leaflet maps inline, 650x400 px, legends (AGBD, Elevation) present |
| `visualization/visualizing_titiler-pgstac` (folium) | 2 `srcdoc` iframes, 650x390, Leaflet with tiles + layer control |
| `access/direct_access` | 4 xarray HTML reprs |
| `science/ATL08/ATL08` | 1 xarray repr, 3 images, 9 outputs |
| `search/collections` | 7 outputs, Bootstrap-style alert div in markdown |
| `work_with_git` | 18 images incl. the inline `<img height=450>` |
| `user_data/stac_metadata` | 33 `<sup>` elements |
| `working_with_r/access_aws_maap` | 4 HTML tables (R data frames), 20 outputs |
| `science/GEDI/GEDI_L2A` | 1 folium iframe, 1 table |
| `visualize_lonboard` | widget views have no saved state: text fallback only |

## Answers

1. **`{toc}` directive with `:context: children`**: works on section pages and renders
   an inline bulleted list of child page titles, like the RTD theme's inline toctree.
   A preceding `**Search Topics**` paragraph reproduces the toctree caption. On the
   root `index.md` it fails ("Current page not found in project pages for children
   Table of Contents"); `:context: project` with `:depth: 1` is the equivalent for the
   root page (tested, see below).
2. **Inline HTML in markdown**: `<sup>`, `<sub>`, `<img src height="40">` (rendered
   with `style="height:40px"`), `<div class="alert alert-block alert-info">` (class
   preserved) and `<a href="file.md">` (resolved to an internal link) all render.
   No conversion of inline HTML is needed.
3. **`url:` toc entries** with a site-relative value are accepted and shown in the nav
   and in the `{toc}` list (with an external-link icon). This is how the page listed in
   three toctrees (`find_data_in_r`) can appear under Search and Access without
   creating duplicate pages. Listing the same `file:` twice DOES build a second page
   with a `-1` slug (`collections-1`), so duplicates must be avoided.
4. **Rich outputs**:
   - **R htmlwidgets** (full `<!doctype html>` documents in `text/html`): mystmd
     renders each in an isolated iframe (`iframe.jp-mod-isolated`, the JupyterLab
     isolated-output mechanism). Inside the iframes the Leaflet maps are fully
     interactive: 1 `.leaflet-container` each, tiles loaded (10/12, 8/8, 4/4, 6/6, 4/4),
     layer controls and legends present, no page errors (the RequireJS conflicts on the
     live site disappear because each widget has its own document). The Leaflet/Proj4/
     RequireJS CDN injection from `conf.py` is therefore not needed. ONE GAP: the
     iframes are 300x416 px (browser default iframe width) instead of the 650x400 px
     (100% of the content column) on the live site. Fix tested below.
   - **folium**: identical to live, `srcdoc` iframes at 100% width with tiles loaded.
   - **xarray reprs**: 4/4 and 1/1 present. **pandas / R tables**: 1/1 and 4/4.
     **pystac `<style>` outputs**: page renders, no errors.
   - `output_matplotlib_strings: show` keeps every text/plain output.
5. **URL layout** with `site.options.folders: true`: `_build/html/<slug path>/index.html`,
   e.g. `science/GEDI/GEDI_L2A.ipynb` -> `/science/gedi/gedi-l2a/`; root `index.md` -> `/`.
6. **rst2myst 0.4.0** (`uvx --python 3.12 --from 'rst-to-myst[sphinx]==0.4.0' rst2myst stream`)
   runs fine. Output checked on `index.rst`, `searching.rst`, `technical_tutorials.rst`,
   `working_with_r.rst`, `personal_access_tokens.rst`, `stac_metadata.rst`,
   `catalog.rst`, `release_notes.rst`:
   - `:sup:` -> `` {sup}`1,2` `` (works in mystmd, alias of `{superscript}`).
   - `.. note::`/`warning`/`attention` -> `:::{note}` colon fences. `.. image::` ->
     ```` ```{image} ```` with `:alt:`/`:width:`. `.. code-block:: python` -> ```` ```python ````.
   - Labels: `.. _pat-nasa-esa:` -> `(pat-nasa-esa)=` (unchanged), but
     `.. _working_with_r_section:` -> `(working-with-r-section)=` (docutils id
     normalisation) while the `{ref}` roles keep `working_with_r_section`. The
     post-processor must restore the original label text so refs resolve.
   - Line blocks (`| March 3, 2026` / `| Release with ...`) are emitted as two
     separate paragraphs with "no visit method for line_block" warnings. Sphinx
     rendered them as two adjacent lines. The pre-processor joins them into one
     paragraph with hard line breaks.
   - `.. toctree::` -> ```` ```{toctree} ```` fence listing the files (replaced by the
     post-processor). rst comments -> `%` comment lines (invisible in both).
   - "Title underline too short" warnings on `release_notes.rst` are harmless: docutils
     still makes headings. Pre-processor pads underlines anyway to keep logs clean.
7. **Raw cell** in `direct_access.ipynb`: page built with no warning; rendering to be
   compared with the baseline in the verification pass (raw cells are not rendered by
   nbsphinx either).
8. **Explicit labels replace implicit heading anchors**: a `(label)=` before a heading
   makes `#label` the heading's id and `#heading-text` no longer resolves. The link
   rewriter must map anchors to the label when one exists.

## Fix tests
(see below; filled in as they run)

### Fix 1: full-width isolated output iframes (R htmlwidgets)

Added `site.options.style: custom.css` with a single rule:

```css
iframe.jp-mod-isolated { width: 100%; }
```

Result: the three R map iframes on `vector_data_visualization` measure 721x416 px
(100% of the MyST content column) instead of 300x416. This matches the live site,
where the maps are 100% of the content column (650x400 in the RTD theme). The
height comes from the widget's own 400 px map plus margins in both cases.
This CSS file is part of the migration (it replaces the RTD-only `custom.css`).

### Fix 2: root page section list

`index.md` uses `{toc}` with `:context: project` and `:depth: 1`, which renders the
six top-level sections as a list, equivalent to the root `toctree` with `maxdepth 1`.
Verified in the built page text: "Search", "Risky pages" listed under the attention
box.

### Baseline Sphinx build warnings worth knowing (local build of `develop`)

- 5x "document isn't included in any toctree" (the orphan notebooks; they are still built).
- `File not found: 'system_reference_guide/custom-environments.html#Custom-environments'`
  (x2) and `'getting_started/getting_started.html#Creating-a-workspace'`: nbsphinx
  cannot resolve relative `.html` links at build time; they only work because the
  output file happens to exist. The MyST link rewriter turns them into real
  cross-references.
- `undefined label: '/system_reference_guide/ssh.ipynb#accessing-maap-workspaces-over-ssh'`:
  this anchor is already broken on the live site (lowercase anchor against an
  nbsphinx Title-Case id). Under MyST the lowercase form is the correct one, so the
  link starts working.
- `File not found: 'technical_tutorials/dps_tutorial/dps-stac.maap-project.org'` (x2):
  markdown links written without `https://`; broken today, left as is (content bug,
  recorded for the maintainers in `04-compromises.md` under "pre-existing issues").
