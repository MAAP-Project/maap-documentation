# Interactive widgets on the static docs site: reference notes

Notes gathered on 2026-09-29/30 while planning kernel-free interactive widgets for
the MyST docs site, starting with `docs/source/science/NISAR/NISAR_access.ipynb`.
The implementation plan lives outside the repo at
`~/.claude/plans/let-s-get-to-looking-swirling-balloon.md`; this file is the
durable reference for how the pieces fit together and how to execute notebooks
so their widgets survive the static build.

Local checkouts referenced below (all under `~/seed/`):

| Repo | What |
|---|---|
| `manywidgets` | anywidget-based widget library (PyPI `manywidgets`, 0.2.0a1 at time of writing) |
| `myst-anywidget-static-export` | the MyST plugin that renders anywidget outputs statically (GitHub release asset `plugin.mjs`, v0.3.1) |
| `anywidget-experiments` | frozen origin of the plugin; holds the detailed upstream-bug write-ups |
| `manywidgets-playground` | example consumer site; mystmd 1.10.1, same as this repo |

## 1. anywidget in one page

- A widget is a Python `anywidget.AnyWidget` subclass with an `_esm` trait (a JS
  module, as a string or a `Path`) and an optional `_css` trait. Synced traits are
  declared with `traitlets ... .tag(sync=True)`.
- The JS module default-exports `{ initialize?({model}), render({model, el, host?}) }`.
  It reads traits with `model.get(name)`, writes with `model.set(name, v)` +
  `model.save_changes()`, subscribes with `model.on("change:name", fn)`, and
  `render` returns a cleanup function.
- `_esm` and `_css` are ordinary synced traits, so **the full JS and CSS text is
  stored in the notebook's widget state**, and every static page carries a copy.
- In a live kernel, Python-side `observe` callbacks, `Button.on_click`, `on_msg`
  etc. work. On the static site there is no kernel, so **none of them run**.
  Anything computed in Python must be precomputed into traits.

## 2. Where widget state lives in an `.ipynb`

- Displaying a widget produces a cell output with mime
  `application/vnd.jupyter.widget-view+json` = `{"model_id": "<uuid>", ...}` plus a
  `text/plain` fallback (`Map(layers=...)`, `Table(...)`) that is what renders when
  no state is available.
- The state of every model in the kernel is saved under
  `notebook.metadata.widgets["application/vnd.jupyter.widget-state+json"].state[model_id]`
  = `{model_name, model_module, model_module_version, state: {...}, buffers?: [...]}`.
- Binary traits (`DataView`/`ArrayBuffer`, e.g. lonboard's Arrow tables) are stored
  out-of-band as `buffers: [{path: ["trait", 0], data: "<base64>", encoding: "base64"}]`.
- **Which execution paths capture this state:**
  - `jupyter nbconvert --to notebook --execute --inplace nb.ipynb` (nbclient):
    captures everything, including buffers. **This is the path to use.**
  - mystmd's own executor (`project.execute`): captures **nothing**, it drops all
    widget comm messages (`packages/myst-execute/src/kernel.ts`). Do not rely on it.
  - JupyterLab *Settings → Save Widget State Automatically*: saves JSON state but
    **silently drops binary buffers** (`WidgetModel.serialize` does
    `JSON.parse(JSON.stringify(v))`, turning `DataView`s into `{}`). See
    `~/seed/anywidget-experiments/docs/upstream-widget-buffer-serialization.md`.
    It also saves *every* live model, including stale ones from earlier runs, so
    restart the kernel and run all once before saving.
- Consequence for our own widgets: **keep every trait JSON-only** (encode arrays as
  base64 strings inside JSON, never as binary traits). Then both the nbconvert and
  the JupyterLab paths produce complete state. Base64 in a JSON string costs the
  same bytes as the plugin's own buffer inlining, which is also base64.

Quick check that a notebook has usable state:

```bash
python3 - <<'EOF'
import json, sys
nb = json.load(open("docs/source/science/NISAR/NISAR_access.ipynb"))
state = nb["metadata"].get("widgets", {}).get("application/vnd.jupyter.widget-state+json", {}).get("state", {})
print("models in state:", len(state))
views = [o["data"]["application/vnd.jupyter.widget-view+json"]["model_id"]
         for c in nb["cells"] if c["cell_type"] == "code"
         for o in c.get("outputs", []) if "application/vnd.jupyter.widget-view+json" in o.get("data", {})]
for mid in views:
    m = state.get(mid)
    if m is None:
        print("MISSING state for view", mid); continue
    size = len(json.dumps(m))
    print(f"{mid}  {m['model_module']}.{m['model_name']}  {size/1e6:.2f} MB  buffers={len(m.get('buffers', []))}")
print("total widget state:", len(json.dumps(state))/1e6, "MB")
EOF
```

## 3. The `myst-anywidget-static-export` plugin

Source: `~/seed/myst-anywidget-static-export` (TypeScript; `npm test` builds and
runs vitest; `nox -s docs` builds the demo site). The single deliverable is
`dist/plugin.mjs`, attached to GitHub Releases. There is no npm package. The
"9 hacks" that make it work are documented in its `docs/design-notes.md`.

Consumer configuration (`docs/source/myst.yml`), always pinned to a release:

```yaml
project:
  plugins:
    - https://github.com/developmentseed/myst-anywidget-static-export/releases/download/v0.3.1/plugin.mjs
```

### What it does at build time

1. One `project`-stage transform runs over every `.ipynb` page. It re-reads the
   raw notebook JSON from disk and takes `metadata.widgets[...].state`. No state →
   no-op for that notebook (so adding the plugin changes nothing for notebooks
   without saved state).
2. For each AST `output` node carrying `widget-view+json`, it takes the `model_id`.
   If that model is an ipywidgets `VBox`/`HBox`, it recurses into `children` and
   uses the **first** model with `model_module === "anywidget"`, dropping the
   siblings (this exists for lonboard's `Map`, which displays as a VBox). Use
   manywidgets `Row`/`Column`/`Grid` for layout, not ipywidgets boxes.
3. It builds the renderer-visible model: the root state minus `_`-prefixed keys,
   plus `_myst_buffers`, `_myst_submodels` (a BFS of every `IPY_MODEL_<id>`
   reference; children's `_esm`/`_css` ride along here, inline in the page JSON),
   `_myst_links` (jslink/jsdlink `LinkModel`s), `_myst_root_id`,
   `_myst_anywidget_id`, `_myst_css_text`.
4. It writes content-hashed sidecars into `_widget_assets/` **next to the source
   notebook** (so inside `docs/source/`; gitignore `**/_widget_assets/`):
   `<hash>.source.mjs`, `<hash>.wrapper.mjs`, `<hash>.css`, `<hash>.state.json`,
   `myst-anywidget-static-host.mjs`, `manifest.json`.
5. It rewrites the node to `{type: "anywidget", esm: "_widget_assets/<h>.wrapper.mjs", model}`.
   mystmd copies the ESM into `_build/html/build/`, and `@myst-theme/anywidget`
   mounts it inside a shadow DOM (`.myst-anywidget` host element).

### The browser host runtime

- No-ops `model.save_changes` / `model.send` / `model.off` (the theme's
  `MystAnyModel` throws "not implemented" for them) and installs `widget_manager`
  via `Object.defineProperty` (the prototype has a throwing getter).
- Hydrates base64 buffers back into `DataView`s (a port of ipywidgets `put_buffers`).
- Provides sub-model proxies and `widget_manager.get_model(id)` from `_myst_submodels`.
- Injects CSS as a `<style>` element in the **shadow root**. Never a `<link>` inside
  the render target `el`: React's `createRoot(el)` (lonboard) wipes it.
- Keeps a page-scoped registry: `host.getModel(ref)`, `host.waitForModel(ref)`
  (5 s timeout), `host.getWidget`, `host.renderChild(ref, el)` (for containers),
  `host.on/off/emit`. Roots are keyed by `widget_id`, model UUID and
  `_anywidget_id`; sub-models by `model_id`.
- Installs jslinks with an initial source→target push.
- `model.receiveCustomMessage(content, buffers)` is a local stand-in for kernel
  custom messages (added for lonboard `fly_to`).

### Limits and known bugs

- **No kernel**: Python callbacks never run. Browser-side state still changes, so
  jslinks and `Binder`s respond.
- **No size guards.** Everything is inlined. One lonboard `Map` is ~3.4 MB of
  `_esm` + ~337 KB of CSS; the manywidgets `map-compare` page is 30 MB of page
  JSON. Budget page weight explicitly.
- Pages must be served over HTTP (dynamic `import()` and absolute asset URLs).
  `make serve` is fine; `file://` is not.
- Only `.ipynb` pages get widgets; a `python` code fence in Markdown renders nothing.
- **baseURI registry bug** (`~/seed/manywidgets/myst-static-export-baseuri-registry-bug.md`):
  the registry is keyed on `document.baseURI` (`src/runtime/registry.ts`), which
  includes the query string and hash. After any `history.replaceState`/`pushState`
  (MyST TOC anchor clicks, the `Fullscreen` widget writing `?fullscreen=`), later
  `host.getModel`/`renderChild` calls land in a fresh empty registry and time out.
  Fix: key on `location.origin + location.pathname`. Not yet fixed as of v0.3.1.
- **deck.gl duplicate layer ids**: two or more lonboard maps starting at once on a
  page (e.g. `MapCompare`) intermittently render no layers
  (`lonboard-duplicate-layer-ids-fix.md`). One lonboard map per page is fine.
- lonboard `RasterLayer` (COG) fetches tiles from the kernel via `on_msg`, so it
  cannot work statically. Serve rasters as XYZ tiles (TiTiler) with
  `BitmapTileLayer`, or precompute the pixels into the widget state.
- lonboard `DataFilterExtension` *category* filters break under static export
  (playground note); use one layer per category.
- `host.getWidget` does not resolve children; use `renderChild`.

## 4. manywidgets

`~/seed/manywidgets` (`pip install manywidgets`, `[lonboard]` extra for the
lonboard interop widgets). Every widget subclasses `BaseWidget` (auto
`widget_id`, theming via `theme_vars`) and lives in
`src/manywidgets/<name>/{widget.py, src/index.ts, style.css, doc.md, tests/}`.
`scripts/build.mjs` bundles each `src/index.ts` with esbuild (inlining the shared
`packages/core` helpers) to `dist/widget.js`, which hatch-jupyter-builder ships
in the wheel. Docs pages are generated from `doc.md`; the agent skill API
reference is regenerated with `npm run skill:gen`.

Widgets (v0.2.0a1):

| Group | Widgets |
|---|---|
| Charts | `Chart` (Chart.js; line/scatter/bar; `add_series`, `clicked_point`/`hover_point`) |
| Inputs | `Slider`, `RangeSlider`, `Dropdown`, `Toggle`, `Button`, `NumberInput` |
| Displays | `Stat`, `NumberDisplay`, `Text` (markdown), `Legend` |
| Layout | `Row`, `Column`, `Grid`, `GridItem`, `Fullscreen` |
| Linking | `Binder` (transform + dotted paths); plain `ipywidgets.jslink/jsdlink` for pass-through |
| lonboard interop | `LayerToggle`, `FilterBinder`, `LayerFilter`, `MapFlyer`, `MapCompare` |

Gaps found: no table/datagrid widget, no lightweight map (map rendering is
delegated to lonboard, ~3.7 MB per map), no time/date slider formatting.

Static-safe authoring rules (from `docs/guides/create-your-own-widget.md` and the
shipped skill's `references/authoring.md`):

1. Wrap every `save_changes()` (`safeSaveChanges`); it throws on some hosts.
2. One listener per trait (`onChange`/`onChanges`), not `"change:a change:b"`.
3. Style through `_css` (or `ensureShadowCss`). Never inject a `<link>` into `el`.
4. Vanilla DOM. Avoid React `createRoot(el)`.
5. JSON-only traits where possible (see §2). Binary traits force the nbconvert path.
6. Reach other widgets via `resolveModel(model, ref)` (roots by `widget_id`).
7. Containers: `widget_serialization` child traits + `_myst_child_traits` +
   `renderChild(args, ref, el)`.
8. Tolerate late-registering models (wrapper modules load asynchronously).

Out-of-tree widgets cannot yet import `@manywidgets/core` (ESM is loaded from a
string/Blob URL, so bare imports fail); the options are in
`custom-widget-authoring-options.md`. Building new generic widgets *inside*
manywidgets sidesteps this, which is why the NISAR widgets go there.

Other useful files in that repo: `layout-improvement-notes.md`,
`manywidgets-upstream-suggestions.md`, `docs/examples/*.ipynb` (lonboard map,
map-compare, fullscreen dashboard), `scripts/browser_check.py` (Playwright check
that queries inside `.myst-anywidget` shadow roots; the pattern to copy for
verifying this site).

## 5. State of this repo (2026-09-30)

- `docs/source/myst.yml` has no `plugins:` yet.
- 7 `widget-view+json` outputs exist across 2 notebooks
  (`technical_tutorials/visualization/visualize_lonboard.ipynb`: 4 lonboard maps;
  `Visualizing_OPERA-DISP_tile_with_TiTiler-MultiDim.ipynb`: 3 tqdm bars). None
  has saved state, so only the text fallback renders. `visualize_lonboard` would
  need nbconvert re-execution (lonboard needs buffers).
- folium maps (12 notebooks) and the R htmlwidgets already render as `srcdoc`
  iframes, no plugin needed.
- The NISAR notebooks have no widgets at all today: matplotlib PNGs (1.08 MB in
  `NISAR_access`), a `KeysView(...)` text dump of the DataTree, and a 305 KB
  xarray HTML repr in `Simulated_NISAR`.
- Post-build customisations are Python scripts under `docs/redirects/` and
  `docs/rtd/`, run from `make build` and mirrored in `.readthedocs.yml`.

## 6. Executing a widget notebook on the MAAP hub

Notebooks are never executed locally or in CI; auth only works on the hub.

1. In a hub terminal, in a checkout of the branch, make sure the notebook kernel
   env has the widget packages (`%pip install -q "manywidgets>=..."` in the first
   code cell is the convention the other notebooks use with `!pip install`).
2. Execute with nbclient so widget state (including any buffers) is captured:

   ```bash
   jupyter kernelspec list   # find the kernel name, e.g. the "Python [conda env:notebook]" one
   jupyter nbconvert --to notebook --execute --inplace \
     --ExecutePreprocessor.kernel_name=<name> --ExecutePreprocessor.timeout=1800 \
     docs/source/science/NISAR/NISAR_access.ipynb
   ```

   `earthaccess.login()` must not prompt under nbconvert: check `~/.netrc` or the
   `EARTHDATA_*` env vars first.
3. Fallback when nbconvert is not an option: in JupyterLab enable *Save Widget
   State Automatically*, **restart the kernel, run all once**, save. Only safe for
   JSON-only widgets (§2).
4. Run the state check in §2. Every view's `model_id` must exist in the state.
5. Copy the notebook back (git on the hub, or download) and commit.
6. Locally: `make build && make serve`, open the page with no kernel, exercise
   the widgets, click a TOC anchor and navigate away/back, check light and dark
   themes, then check the RTD PR preview (widgets + version flyout + ad slot).

To iterate on widgets without repeated hub runs: capture the intermediate data
once on the hub (e.g. granule metadata JSON + quantized arrays as an `.npz`),
copy it back, and build the same widgets from that fixture in an uncommitted
scratch notebook that nbconvert can execute locally.

## 7. Spike results (2026-10-07): plugin wired into this site

Done with a throwaway copy of the plugin repo's `counter-demo.ipynb` (committed
widget state, 2 models) placed in the toc, and a locally built `plugin.mjs`
carrying the registry-scope fix (released as v0.3.2). Checked with a headless
Chromium script (Playwright, no kernel) against `make build` + `http.server`:

- The counter mounts inside `.myst-anywidget`'s shadow root and `+` increments
  (JS-only state).
- After `location.hash` changes (what a TOC anchor click does), the registry
  still has exactly one key (`origin + path`) and the widget works. The MyST
  theme **remounts the widget on a hash change**, so browser-side state resets
  to the saved state: expect a reader's slider tweaks to reset when they click a
  heading anchor. That is theme behaviour, not something the plugin controls.
- Client-side navigation away and back re-mounts a working widget.
- No console errors, no React hydration (#418) errors; the RTD ad-slot,
  redirect and 404 post-build scripts ran unchanged.
- Diff of `_build/html` against a baseline build without the plugin: every
  other page differs only by regenerated React `key` ids and the nav entry
  for the spike page. **The plugin is a no-op for notebooks without
  `metadata.widgets`.**
- Build needs Node on `PATH` for `uv run myst` (Node 22 used here).
- Note for `make clean && make build`: the `tee ../../docs/source/_build/build.log`
  in the Makefile fails when `_build/` does not exist yet, so `make` stops
  before the post-build scripts even though `myst build` succeeded. Create the
  directory first (or fix the Makefile with a `mkdir -p`).

## 8. New generic widgets for this work (manywidgets 0.3.0, 2026-10-07)

Added to `~/seed/manywidgets` (released by Sanjay to PyPI; notebooks
`%pip install "manywidgets[geo]>=0.3"`):

- **`Table`** (`src/manywidgets/table/`): sortable, selectable table of dicts.
  `rows`, `columns` (`{key, label, format: text|number|bytes|datetime}`),
  `id_key`, two-way `selected` / `hovered`. `Table.from_records`,
  `Table.from_dataframe`.
- **`GeoMap`** (`src/manywidgets/geo_map/`): MapLibre GL map (bundled, ~1.1 MB
  minified, no CDN). Basemaps `positron | dark-matter | voyager | satellite |
  osm | none | auto`. Layers are JSON specs added with `add_geojson(data,
  id_property=, tooltip=)`, `add_xyz(url)` and `add_grid(GridLayer)`. Two-way
  `selected` / `hovered` feature ids, `view_state`, `fit_bounds` (None = fit
  layers), `layer_state` (what the built-in panel edits: visibility, opacity,
  active band, stretch, colormap), `controls`, `zoom_to_selected`.
- **`GridLayer.from_arrays({name: 2-D array}, corners, quantize=, units=,
  default_ranges=, composites=)`**: quantizes each band to uint8 (0 = nodata,
  base64 in JSON), placed by four outer corners (TL, TR, BR, BL) so a projected
  window keeps its pixels. `corners_from_bounds(l, b, r, t, crs)` /
  `corners_from_coords(x, y, crs)` need pyproj (`[geo]` extra). Colouring is
  done in the browser; hover shows per-band values.

Design rules that made these work statically: JSON-only traits; MapLibre's CSS
injected into the shadow root via `ensureShadowCss` (and the widget's own
`position` rule made more specific than `.maplibregl-map`); the panel writes a
small `layer_state` dict rather than the multi-MB `layers` list; an explicit
`band_names` list because object key order is not preserved through the
notebook → plugin → page pipeline; `fit_bounds` must be a real 4-list (a
traitlets `List(None)` pitfall produced `[]`).

Verified end to end on the manywidgets docs build with the plugin
(`docs/examples/geomap-table.ipynb`, synthetic data): both maps mount with no
kernel, table ↔ map selection links through `jslink`, the panel's band switch
repaints the raster, no console errors. Check script pattern:
`manywidgets/scripts/browser_check.py` (Playwright, shadow-root queries, Chromium
launched with `--use-angle=swiftshader` for WebGL).

Sizes observed: executed example notebook 2.7 MB (two GeoMaps ⇒ two copies of
the 1.1 MB bundle in widget state, plus 0.3 MB of grid data); page JSON carries
only the model state (ESM goes to a content-hashed sidecar, shared by instances).

## 9. First real page: NISAR_access (2026-10-07)

Executed on the MAAP hub with `jupyter nbconvert --execute` (kernel `python3`,
`.netrc` created once via `earthaccess.login(strategy="interactive", persist=True)`;
small 4 GB profile is enough). Result: 10 widget models, 3.8 MB of widget state;
notebook 3.9 MB (was 1.1 MB with the PNG). Browser check on the built page
passes (table ↔ footprint map selection, raster panel, band repaint, 0 errors).
The notebook has CRLF line endings (only file in the repo that does); the hub
normalises them to LF on upload/execute, so convert back before committing to
keep the diff content-only.

**Page weight finding:** `science.nisar.nisar-access.json` is 6.5 MB, of which
**3.8 MB is `page.widgets`** — mystmd copies the notebook's whole
`metadata.widgets` state into the page JSON (for the theme's own ipywidgets/thebe
rendering) *in addition to* the plugin's `anywidget` nodes, so every ESM bundle
and the raster payload are shipped twice. The plugin cannot remove it: mystmd
runs plugin transforms with only the AST + vfile (`plugin(undefined, {select,
selectAll})(tree, vfile)`) and attaches `postData.widgets = pre.widgets` *after*
they run, with no setting to turn it off. **Resolved with a post-build step**,
`docs/widgets/strip_page_widgets.py` (Makefile + `.readthedocs.yml`, after
`add_ad_slot.py`): for every page JSON that has `anywidget` nodes and no
un-exported `widget-view` output left, `widgets` is replaced by `{}`. NISAR
access page JSON: 6.2 MB → 2.5 MB; the browser check still passes (the theme
does not need `page.widgets` for `anywidget` nodes). A second, smaller
duplication remains: a GeoMap nested in a `Column` carries its 1.1 MB `_esm`
inline in `_myst_submodels` (known plugin limitation; root widgets use a shared
sidecar). Worth an upstream mystmd issue: skip `page.widgets` when the
notebook's widget outputs were transformed away.
