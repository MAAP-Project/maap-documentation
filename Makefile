# MAAP User Documentation: MyST build.
#
#   make setup     install the Python environment (uv) — Node.js >= 20 must be on PATH (see .nvmrc)
#   make build     build the static site into docs/source/_build/html (+ redirect stubs for old URLs, 404 page, RTD ad slot)
#   make serve     serve the built site at http://localhost:8000
#   make start     live-reloading dev server (myst start)
#   make clean     remove build output

SRC := docs/source
HTML := $(SRC)/_build/html
PORT ?= 8000

.PHONY: help setup build serve start clean

help:
	@sed -n 's/^#   //p' Makefile

setup:
	uv sync

build:
	cd $(SRC) && uv run myst build --html 2>&1 | tee ../../$(SRC)/_build/build.log
	uv run python docs/redirects/gen_redirects.py --html $(HTML)
	uv run python docs/redirects/gen_404.py --html $(HTML)
	uv run python docs/rtd/add_ad_slot.py --html $(HTML)

serve:
	@echo "Serving $(HTML) at http://localhost:$(PORT)/"
	uv run python -m http.server -d $(HTML) $(PORT)

start:
	cd $(SRC) && uv run myst start

clean:
	rm -rf $(SRC)/_build
