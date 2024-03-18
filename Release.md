This documentation is published on ReadTheDocs.org

Admins can manage the builds at https://readthedocs.org/projects/maap-project/


## Release Checklist

1. [Tag] the `master` branch as latest by [creating a new release](https://github.com/MAAP-Project/maap-documentation/releases/new).
Increment the version under semantic versioning rules (TLDR, major.minor.bugfix, you'll mostly be incrementing the minor number)
This will build as **Stable** https://docs.maap-project.org/en/stable/

2. Open a PR and Merge the Changes from `develop` to `Master`, this will update **latest** https://docs.maap-project.org/en/latest/
