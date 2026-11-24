# OGC on the MAAP

**What is OGC?**

The [Open Geospatial Consortium (OGC)](https://www.ogc.org/) is an international standards body that defines open protocols for geospatial data and processing. On the MAAP, OGC is centered around **OGC Application Packages**: a standard way to package, share, and execute algorithms across different computing platforms.

An OGC application package bundles a [Common Workflow Language (CWL)](https://www.commonwl.org/) workflow with an executable, typically a Docker image. Because CWL is platform neutral, an application package you build on MAAP can run on any OGC compliant platform without modification.

**Why use OGC?**

- **Portability:** Run the same algorithm on MAAP, on your local machine, or other OGC compliant platforms without rewriting it.
- **Reproducibility:** The Docker image pins your software environment, so results are consistent regardless of where or when the job runs.
- **Interoperability:** Other platforms and tools that speak OGC standards can discover, validate, and execute your algorithm directly.

To get started, select the path below that best describes your situation:

- **I have a non OGC algorithm deployed to MAAP. How do I convert it?**

  Follow the [transition tutorial](ogc/transition_to_ogc.ipynb). You can also use the [OGC App Pack GitHub Action](ogc/ogc_app_pack_gha.ipynb) to build and deploy application packages from GitHub.

- **I use MAAP but have not registered an algorithm. How do I register a new OGC application package?**

  Follow the [application package guide](ogc/build_application_packages.ipynb). You can also use the [OGC App Pack GitHub Action](ogc/ogc_app_pack_gha.ipynb).

- **I am new to MAAP. Where do I start?**

  Follow [Start a Workspace on MAAP Hub](ogc/start_hub_workspace.ipynb).

For the OGC support status of MAAP services, see the [software overview](ogc/software_overview.ipynb).

```{toc}
:context: children
:depth: 2
```
