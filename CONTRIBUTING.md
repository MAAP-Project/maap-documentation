# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Doc Bugs

Report documentation bugs at <https://github.com/MAAP-Project/maap-documentation/issues>.

If you are reporting a bug in the documentation, please include:

-   Any details about your environment that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug.

### Write Documentation

The MAAP project could always use more documentation and examples, whether as part of the official docs page or on the web in blog posts, articles, and such. If you provide any written docs, please let us know and we can add it to the docs page.

### Submit Feedback

The best way to send feedback is to file an issue at <https://github.com/MAAP-Project/maap-documentation/issues>.

If you are proposing a new example:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to provide examples.
-   Remember that contributions from others are always welcome :)

## Get Started!

Ready to contribute? Here's how to set up the documentation for local development:

#### 1.  Fork the `maap-documentation` repo on GitHub.
#### 2.  Clone your fork locally:


    $ git clone git@github.com:your_name_here/maap-documentation.git

#### 3.  Install your local copy into a virtual environment.
Assuming you have `conda` installed, this is how you set up your fork for local development:


    $ conda create -n maap python=3.7
    $ conda activate maap
    $ cd maap-documentation/
    $ pip install requirements.txt

#### 4.  Create a branch for local development::


    $ git checkout -b username-name_of_feature

Now you can make your changes locally.
To do this, typically you create your notebook of the example you would like added to the documentation and save the notebook under the `maap-documentation/docs/source/` directory. After the file has been saved, update the `index.rst` file to add the new documentation to the Table of Contents tree (toctree).
Run the command `$ make html` within the `docs/` directory to build your HTML pages and verify the changes are correct.

#### 5.  Commit your changes and push your branch to GitHub:


    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin username-name_of_feature

#### 6.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that all of the required code and files have been committed and pushed to the brach.

Go to Github.com and submit a pull request. Select the _base_ branch as `develop`, `develop` is where we stage all documentation before pushing to the `master` branch. Select the branch you would like to merge into `develop` as the _compare_ branch.
Please provide a succinct title of the changes you would like to merge and detailed information on what was changed. We will then assign someone working on MAAP to review, possibly provide comments, and accept your changes.
