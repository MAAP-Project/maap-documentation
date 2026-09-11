# MAAP User Documentation: MyST build.
#
#   make setup     install the Python environment (uv) — Node.js >= 20 must be on PATH (see .nvmrc)
#   make build     build the static site into docs/source/_build/html (+ redirect stubs for old URLs)
#   make serve     serve the built site at http://localhost:8000
#   make start     live-reloading dev server (myst start)
#   make verify    check the build against the old Sphinx page inventory
#   make migrate   re-run the Sphinx -> MyST migration from a pristine docs/source (DESTRUCTIVE, see migration/agent-docs)
#   make clean     remove build output

SRC := docs/source
HTML := $(SRC)/_build/html
PORT ?= 8000

.PHONY: help setup build serve start verify migrate clean

help:
	@sed -n 's/^#   //p' Makefile

setup:
	uv sync --group migration

build:
	cd $(SRC) && uv run myst build --html 2>&1 | tee ../../$(SRC)/_build/build.log
	uv run python migration/gen_redirects.py --html $(HTML)

serve:
	@echo "Serving $(HTML) at http://localhost:$(PORT)/"
	uv run python -m http.server -d $(HTML) $(PORT)

start:
	cd $(SRC) && uv run myst start

verify:
	uv run --group migration python migration/verify.py --src $(SRC) --log $(SRC)/_build/build.log

# DESTRUCTIVE for docs/source: restores it from `develop` and deletes untracked files there.
# Refuses to run unless docs/source has no uncommitted changes (override with FORCE=1).
migrate:
	@if [ -z "$(FORCE)" ] && [ -n "$$(git status --porcelain $(SRC))" ]; then \
	  echo "docs/source has uncommitted changes; commit or stash them first (or FORCE=1)."; exit 1; fi
	git checkout develop -- $(SRC) && git clean -fd $(SRC)
	uv run --group migration python migration/migrate.py --strict

clean:
	rm -rf $(SRC)/_build
