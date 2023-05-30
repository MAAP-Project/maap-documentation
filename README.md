# maap-documentation
[![Documentation Status](https://readthedocs.org/projects/maap-project/badge/?version=latest)](https://maap-project.readthedocs.io/en/latest/?badge=latest)

This repository serves as the technical documentation for interfacing with the MAAP services.

### Contributing to MAAP Documentation

MAAP documentation is hosted on [maap-project.readthedocs.io](https://maap-project.readthedocs.io), is built using [Sphinx](http://www.sphinx-doc.org/en/master/index.html) and written in [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html). If you want to contribute to the documentation, you can do so by forking the repository, creating a branch for your changes and editing the documentation files in the docs directory of the repo.

This should be built using Python >=3.11.

OS-version of [Pandoc](https://pandoc.org/) is also required.

You need to install Sphinx and supporting packages locally so that you can make sure that your edits show up correctly before you make a pull request to the repo. To do this run the following command:

```
pip install -r requirements.txt
```

After installing the necessary packages you build the docs using the following command from the docs directory:

```
cd docs
make html
```

Once the docs have been built successfully, there should be a `build/` directory with the HTML pages.
To verify the pages look as expected run a local python server.
```
cd build/html
python3 -m http.server
# If you are not prompted open a web browser and go to http://localhost:8000/ (default)
```

## Running Notebooks Locally

To run the documentation notebook code, you must make several configurations.

Install JupyterHub. 

Install the [ipycmc](https://github.com/MAAP-Project/maap-jupyter-ide/tree/master/ipycmc) extension.

Install the `maap-py` library.

1. Switch to your virtual environment that you wish to install in.
2. `pip install matplotlib==3.3.1` 
3. Clone maap-py with `git clone git@github.com:MAAP-Project/maap-py.git`
4. `cd maap-py` then `python setup.py install`
