# maap-documentation
[![Documentation Status](https://readthedocs.org/projects/maap-project/badge/?version=latest)](https://maap-project.readthedocs.io/en/latest/?badge=latest) [![DOI](https://zenodo.org/badge/235617200.svg)](https://zenodo.org/doi/10.5281/zenodo.10499174)

This repository serves as the technical documentation for interfacing with the MAAP services.

### Contributing to MAAP Documentation

MAAP documentation is hosted on [maap-project.readthedocs.io](https://maap-project.readthedocs.io) (served at https://docs.maap-project.org) and is built with [MyST](https://mystmd.org) (the engine behind [Jupyter Book 2](https://jupyterbook.org)). Pages are Jupyter notebooks (`.ipynb`) and [MyST Markdown](https://mystmd.org/guide) files under `docs/source/`; the table of contents is the `toc` section of `docs/source/myst.yml`. If you want to contribute to the documentation, you can do so by forking the repository, creating a branch for your changes and editing the documentation files in the docs directory of the repo.

Requirements for building locally:

- Python >= 3.12 and [uv](https://docs.astral.sh/uv/) (installs `mystmd` into a project virtual environment)
- Node.js >= 20 on your `PATH` (`nvm use` picks up the version in `.nvmrc`)

To build the docs:

```
make setup       # uv sync
make build       # writes the static site to docs/source/_build/html
make serve       # http://localhost:8000
```

`make start` runs the MyST live-reloading development server instead. `make help` lists all targets.

Notebooks are **not** executed during the build: the site renders the outputs that are stored in the committed `.ipynb` files (this was also the case with the previous Sphinx build). Execute notebooks on the MAAP Hub and commit the executed notebook.

The site was migrated from Sphinx/reStructuredText in September 2026; the migration scripts and a full record of the decisions and compromises are in `migration/` (see `migration/agent-docs/`).

## Running Notebooks Locally

To run the documentation notebook code, you must make several configurations.

Install JupyterHub. 

Install the `maap-py` library.

1. Switch to your virtual environment that you wish to install in.
2. `pip install matplotlib==3.3.1` 
3. Clone maap-py with `git clone git@github.com:MAAP-Project/maap-py.git`
4. `cd maap-py` then `python setup.py install`
