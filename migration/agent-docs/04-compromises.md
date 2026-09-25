# Compromises and gaps (READ THIS)

This is the list of everything in the MyST site that is NOT a faithful reproduction
of the Sphinx site. Each entry states what changes, which pages are affected, why,
the evidence, and the follow-up. Items marked UNVERIFIED have not yet been tested
against a real build and must not be assumed to be fine.

Status legend: OPEN (needs a fix or a sign-off), ACCEPTED (user signed off),
FIXED (no longer a compromise), UNVERIFIED (not tested yet).

## C1. Visual theme changes from sphinx_rtd_theme to MyST book-theme — OPEN

Every page. The layout, fonts, sidebar and colours change. `docs/source/_static/custom.css`
only styled RTD-theme selectors and is dropped. Content and structure are unchanged.
Follow-up: theme/CSS polish after phase 1.

## C2. PDF and epub downloads are no longer produced — OPEN

RTD currently builds `pdf` and `epub` formats from the Sphinx site. mystmd can
export PDF (LaTeX/Typst) but that is a separate pipeline and not configured in
phase 1. Follow-up: evaluate `myst build --pdf`.

## C3. URL paths change; old paths are served by redirect stubs — OPEN

MyST builds `docs/source/technical_tutorials/search/catalog.md` as
`/technical-tutorials/search/catalog/` (lowercase, underscores to dashes, no
`.html`). Every old `<path>.html` URL gets a generated stub that redirects to the
new page and translates old-style `#Heading-Anchors` to the new lowercase form.
Deep links therefore keep working, but the canonical URLs are new.

## C4. Rich notebook outputs — PARTLY VERIFIED (spike), full pass pending

Spike (see `03-spike-results.md`): R htmlwidgets render as interactive Leaflet maps
in isolated iframes (full width after a one-line CSS fix), folium iframes, xarray
reprs, pandas and R tables all match the live site on the pages tested. Still to be
checked page by page in the full build: `text/latex`, `text/markdown`,
`application/geo+json`, `image/png`, pystac `<style>` outputs, the raw cell in
`direct_access.ipynb`, and every remaining notebook (automated output audit in
`05-verification.md`).

## C5. R htmlwidget maps are rendered inside iframes — FIXED (behavioural note)

Under nbsphinx the R Leaflet maps were injected into the page DOM (with Leaflet and
RequireJS loaded site-wide from CDNs). Under MyST each widget is an isolated iframe
with its own document, which is why the CDN injection is no longer needed and the
RequireJS "Mismatched anonymous define()" errors seen on the live site disappear.
The maps are interactive and full width. Difference for users: none expected;
recorded because the mechanism changed.

## C6. Sidebar shows "Finding and Accessing Data in R" once instead of three times — OPEN (minor)

Under Sphinx this stub page appeared in the sidebar under Search, Access and Working
with R. Under MyST it is listed once (Working with R). The inline lists on the Search
and Access pages still include it. Reason and alternatives in `02-decisions.md`.

## C7. Hidden orphan pages — FIXED (behaviour preserved)

Five notebooks were not in any Sphinx toctree but were built and reachable by URL
(`science/GEE/gee.ipynb`, `science/NISAR/Simulated_NISAR.ipynb`,
`system_reference_guide/Secrets_Manager.ipynb`,
`technical_tutorials/dps_tutorial/DPS_runner_template.ipynb`,
`technical_tutorials/dps_tutorial/dps_stac_metadata.ipynb`). They are now `hidden: true`
toc entries: built, linkable, not shown in the sidebar. Same as before.

## Pre-existing content issues found during migration (not caused by it)

- `technical_tutorials/dps_tutorial/*.ipynb`: links written as
  `dps-stac.maap-project.org` / `titiler-dps-stac.maap-project.org` without `https://`
  resolve to nothing today. Left unchanged; maintainers may want to fix.
- `getting_started/getting_started.ipynb` links to
  `../system_reference_guide/ssh.ipynb#accessing-maap-workspaces-over-ssh`, an anchor
  that never resolved under nbsphinx. It resolves under MyST.
- A notebook links to `../granules.ipynb`, which does not exist at that path (see the
  link-rewrite report).
