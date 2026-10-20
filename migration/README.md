# Sphinx → MyST migration (record)

The site was converted from Sphinx/nbsphinx to MyST **once**, in September 2026, by
deterministic scripts that ran on `develop` at `0dcbe21`. Their output was committed
in `fdfe10e`. Since then the content under `docs/source/` is the source of truth and
is edited directly. Nothing here is part of the build.

`agent-docs/` is the full record of the migration: plan, decisions, spike results,
**compromises** (`04-compromises.md`) and verification. It refers to scripts such as
`migrate.py`, `verify.py` and `checks/`. Those were removed from the branch before it
was merged, and are kept at the git tag `sphinx-to-myst-migration-scripts`
(`git checkout sphinx-to-myst-migration-scripts -- migration/`). The README there
explains how to re-run them.

The redirect stubs for old Sphinx URLs are part of every build and live in
`docs/redirects/` (`gen_redirects.py` + `redirect_map.json`).
