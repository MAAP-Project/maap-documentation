# Sphinx → MyST migration (frozen record)

These scripts converted the Sphinx/nbsphinx site to MyST **once**. They ran on
`develop` at `0dcbe21`, and the output was committed in `fdfe10e`. From then on the
content under `docs/source/` is the source of truth and is edited directly. Nothing
here is part of the build, and it is not maintained.

What is here:

- `agent-docs/`: the full record of the migration: plan, decisions, spike results,
  **compromises** (`04-compromises.md`) and verification.
- `migrate.py` and the step modules it runs (`inventory`, `build_toc`, `convert_rst`,
  `rewrite_links`, `write_config`, `cleanup`), plus `overrides.yml`.
- `verify.py`: structural checks and a notebook output audit of a build against the
  old Sphinx inventory.
- `checks/`: browser (Playwright) comparisons with the old site; see `checks/README.md`.

The redirect stubs for old Sphinx URLs are part of every build. They moved to
`docs/redirects/` (`gen_redirects.py` + `redirect_map.json`).

## Re-running (only if ever needed)

The scripts expect a pristine Sphinx tree in `docs/source`, so run them on a throwaway
branch or clone, not on a branch with MyST content:

```
git restore --source=0dcbe21 --staged --worktree docs/source && git clean -fd docs/source
uv sync --group migration
uv run --group migration python migration/migrate.py --strict
```

`migrate.py` writes the redirect map to `migration/redirect_map.json`, and `verify.py`
reads it from there. Copy it from `docs/redirects/` (or back there) to match.
