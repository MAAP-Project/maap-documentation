OGC on the MAAP
=======================================

**What is OGC?**

The `Open Geospatial Consortium (OGC) <https://www.ogc.org/>`_ is an international standards body that defines open protocols for geospatial data and processing. On the MAAP, OGC is centered around the **OGC Application Packages** — a standard way to package, share, and execute algorithms across different computing platforms.

An OGC application package bundles a `Common Workflow Language (CWL) <https://www.commonwl.org/>`_ workflow with an executable (typically a Docker image). Because CWL is platform-neutral, an application package you build on MAAP can run on any OGC-compliant platform without modification.

**Why use OGC?**

- **Portability** — run the same algorithm on MAAP, on your local machine, or other OGC-compliant platforms without rewriting it.
- **Reproducibility** — the Docker image pins your software environment, so results are consistent regardless of where or when the job runs.
- **Interoperability** — other platforms and tools that speak OGC standards can discover, validate, and execute your algorithm directly.

To get started, select the path below that best describes your situation:

- **I am an existing MAAP user. I have a non-OGC algorithm deployed to the MAAP. How do I convert my algorithm into an OGC application package?** 
  
  Follow the :doc:`transition docs <ogc/transition_to_ogc>` tutorial to register your algorithm as an OGC application package.

  See also the :doc:`OGC-App-Pack GitHub action <ogc/ogc_app_pack_gha>`, which allows users to build & deploy OGC application packages to the MAAP from GitHub directly.

- **I am an existing MAAP user. I do not have an algorithm on the MAAP. How do I register a new algorithm as an OGC application package?** 

  Follow the :doc:`application package guide <ogc/build_application_packages>` tutorial to register your algorithm as an OGC application package.

  See also the :doc:`OGC-App-Pack GitHub action <ogc/ogc_app_pack_gha>`, which allows users to build & deploy OGC application packages to the MAAP from GitHub directly.

- **I am new to MAAP. Where do I start?** 
  
  Follow the instructions in :doc:`Start a Workspace on MAAP Hub <ogc/start_hub_workspace>` to start an OGC workspace.

To see which MAAP software service versions are OGC-compliant and which are not, see :doc:`here. <ogc/software_overview>`.

.. toctree::
   :maxdepth: 2

   ogc/build_application_packages.ipynb
   ogc/software_overview.ipynb
   ogc/start_hub_workspace.ipynb
   ogc/submit_job.ipynb
   ogc/transition_to_ogc.ipynb
   ogc/ogc_app_pack_gha.ipynb