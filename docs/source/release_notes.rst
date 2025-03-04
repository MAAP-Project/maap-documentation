Release Notes
=======================================

Release notes will mention the release date, a summary for each release, and comprehensive descriptions of major changes, minor changes, feature removal, and bug-fixes. This is typically more comprehensive than the announcements on the GitHub Discussion board: https://github.com/orgs/MAAP-Project/discussions/categories/announcements.

-------------------------------------------------------------
4.2.0
-------------------------------------------------------------
| March 3, 2025
| Release with several important improvements. To use the new features, please start a new v4.2.0 workspace.

Breaking Changes
^^^^^^^^^^^^^^^^^^^
* Updated most packages in all four base images. The Pangeo, isce3, and python images are pinned to versions in pangeo-notebook 2024.11.11 version. Important package updates are:
    * R image: R from 4.2 to 4.3, added rhdf5 from Bioconductor, lidR, and lasR
    * Pangeo image: Xarray now 2024.10, Geopandas 1.0+, Numpy 2.0+, Python 3.12
    * All updated packages here: https://github.com/MAAP-Project/maap-workspaces/pull/169/files 
* All images running on MAAP will now be using mini-forge to avoid licensing issues. Impacts:
    * All conda installs will now pull from conda-forge
    * No longer using R channel on anaconda (also continuing to not use the defaults channel)
    * If you cannot find your package on conda-forge or another open source community channel, we recommend installing your package from their install instructions on their GitHub README or contact the platform team.
    * Anaconda's new terms: https://www.anaconda.com/pricing/terms-of-service-faqs

Added
^^^^^^^^^^^^^^^^^^^
* Container URL in Algorithm Registration UI is now a dropdown where the default is the ``maap_base`` image which is the fastest for algorithm registration 
    * Users who would like to use this faster ``maap_base`` option must self manage their packages (i.e. in an environment.yml). More information in the docs `here <system_reference_guide/algorithm_registration.html#Container-URLs>`_
* Added more packages requested by users for the R image, especially Geotrees specific packages like lasR, partykit, BIOMASS and tidyterra
* The Algorithm-Registration UI input-boxes are narrower to help reduce the need for horizontal scrolling
* Improvements to the Jobs UI: added job duration and more a obvious cancel button, and cleaned up the filter controls
* Using the ``maap_base`` image as the base image for all workspace images

Fixed
^^^^^^^^^^^^^^^^^^^
* Public ssh key is now correctly being pulled from MAAP profile page into ``/projects/.ssh/authorized_keys`` upon workspace launch if it was not already present
* Display SSH info giving undefined error resolved 
* Fixed status filtering issues for Jobs UI
* Fixed a broken documentation link that shows up during algorithm registration 

-------------------------------------------------------------
4.1.1
-------------------------------------------------------------
| October 23, 2024
| Minor release with non-breaking changes. To use the new features, please start a new v4.1.1 workspace.

Fixed
^^^^^^^^^^^^^^^^^^^
* Removed pygeos from all base images.
* Increased number of records in the Jupyter Jobs UI to 200. 
* Expanded s3 permissions for the maap-py ``aws.workspace_bucket_credentials`` function. Credentials for user bucket folders now include full read/write access. See `related documentation <system_reference_guide/accessing_bucket_data.html>`_. 

-------------------------------------------------------------
4.1.0
-------------------------------------------------------------
| October 2, 2024
| Release with several important improvements. To use the new features, please start a new v4.1.0 workspace.

Significant Changes
^^^^^^^^^^^^^^^^^^^
* A new `maap_base` image container is available with a minimal runtime environment for use within DPS. Read more below.
* A way to securely manage credentials for other services (e.g., Google Earth Engine credentials) and pass them into DPS Jobs. This is called Secrets management.
* Organizations feature to help enable dedicated compute resources for user groups and prevent unauthorized access to resource queues.
* MAAP DPS Sandbox queue for quick testing and validating algorithm builds in DPS.
* Some older algorithms may require re-registration due to underlying DPS software being upgraded.

Breaking Changes
^^^^^^^^^^^^^^^^^^^
* Please migrate to the newer version of workspaces as soon as possible in order to leverage the improved security.
* The platform team will help migrate Algorithms to the optimized base images, over the next three months.
* Some older Algorithms may see an error stating /home/ops/.maap-dps.env file not found or /app/dps_wrapper.sh: line 10: python: command not found when running on the DPS. This requires re-registration of the Algorithm.

Added
^^^^^^^^^^^^^^^^^^^
* `Organizations features <system_reference_guide/organizations.html>`_
    * Added new Organizations features and user access-control to DPS job-queues. You will now only see the Job queues that are available to you; if you are missing a queue please ask a team lead or the platform team for help configuring your permissions. 
* `Secrets Management <system_reference_guide/jobs_maappy.html#Passing-Credentials-for-Other-Services-into-Jobs-(Secrets-Management)>`_ 
    * Added ability to `store Secrets using maap-py <system_reference_guide/jobs_maappy.html#Passing-Credentials-for-Other-Services-into-Jobs-(Secrets-Management)>`_ and utilize them within DPS Jobs. This will help accommodate things like passing Google Earth Engine credentials to your Algorithm in a secure way.  
* New `maap_base` image
    * New `maap_base` image that will speed up Algorithm Registration and smaller DPS Jobs significantly containing just conda by reducing the time for the system to build the runtime environment. Smaller jobs will also run more quickly. 
    * In order to use this new container, algorithm build scripts must specify all of the required libraries in their conda environment.yaml file. 
    * To use this new image, specify the following url during algorithm registration ``mas.maap-project.org/root/maap-workspaces/custom_images/maap_base:v4.1.0``.
* MAAP DPS Sandbox queue
    * A new queue ``maap-dps-sandbox`` has been added for quick testing of registered algorithms. 
    * This new queue has limited resources (8gb), and a max run time of 10 minutes for algorithms.
    * The motivation for the queue is for users to quickly test their algorithm build, conda env, run script, input handling, etc.
    * This is the only queue available to Guest accounts
* DPS software upgraded to HySDS v5.2.0

Fixed
^^^^^^^^^^^^^^^^^^^
* Upon registering an Algorithm using the Registration UI, the build-link now opens in a new tab. It also provides the path to where the config yaml file is stored in your workspace and a notification with the registration link and algorithm name:branch.
* Better error-handling when an Algorithm fails to register.

Security Improvements
^^^^^^^^^^^^^^^^^^^^^
* Enhanced security for the DPS job-management workspace to check if a user is logged in.

Known Issues
^^^^^^^^^^^^^^^^^^^^^
* Some older algorithms failing 
   * Some older algorithms may see an error stating ``/home/ops/.maap-dps.env file not found`` or ``/app/dps_wrapper.sh: line 10: python: command not found`` when running on the DPS.
   * This is known to happen when the same github repository is used for registering multiple algorithms using the same branch (eg. main or master). This can be resolved by re-registering your algorithm.
   * For the future, if you want an algorithm container to stay unchanged, consider using github tags and registering an algorithm from that tag (eg v1, v2, etc).

FAQs
^^^^^^^^^^^^^^^^^^^^^
* I dont see the resource queue I used in the past
    * Check if you can use any alternative available queues.
    * If not, contact the platform team to request your specific queue.
* My algorithm is now failing
    * If your previously successful algorithm is now failing, try re-registering once again. 
    * If for any reason re-registering is not an option reach out to the Platform Team.

-------------------------------------------------------------
4.0.0
-------------------------------------------------------------
| July 3, 2024
| Major new release with breaking changes.

Breaking Changes
^^^^^^^^^^^^^^^^^
* The “Basic Stable” workspace stack has been renamed to “Python (default)”. The associated default `vanilla` conda environment has been renamed to `python`.

Workspace impacts:

* This does not impact the `r` or `icse3` workspaces.
* If you are using the Basic Stable (vanilla) workspace, please upgrade to the new Python (default) workspace. 
* To use the new workspace to run a `vanilla` algorithm (e.g., running your existing algorithm in the Jupyter Terminal), you will need to update your scripts to reference the `python` conda environment instead of `vanilla`.

DPS Algorithm Impacts:

* To use the new Python (default) as the base image for your DPS runs, you will need to update your build scripts and environment.yml files to use `python` instead of `vanilla`. Additionally, your run script will need to make sure it’s running in the `python` conda environment (not `vanilla`). 
* DPS algorithms being registered will use the new container URL mas.maap-project.org/root/maap-workspaces/base_images/python:v4.0.0 — also ensure that they are using `python` as the conda-environment name and not `vanilla`.

Added
^^^^^^^^^^^^
* JupyterLab has been updated to v4.
* All extensions are available to be installed via pip now.
* Added lonboard to all images.
* Added all packages from the previous vanilla workspace (now called python) to the R workspace.
* Maap-py no longer tracks a maap.cfg file. When using maap.py you should no longer indicate the API endpoint URL (maap = MAAP() instead of maap = MAAP(api.maap-project.org)).
* Integrated Playwright testing framework into custom JupyterLab extensions.
* Added support for the "maap-data-reader" assumed role. This allows DPS jobs and workspaces direct s3 access to certain DAAC buckets without requiring credentials or manual token refreshing (see https://docs.maap-project.org/en/latest/technical_tutorials/access/direct_access.html).
* Migrated MAAP API PostgreSQL instances to RDS.

Fixed
^^^^^^^^^^^^
* The default base image in the ADE algorithm registration form now shows the correct MAS environment and workspace type.
* The API error "Client is not EDL policy compatible" is now included in the response from the maap-py method aws.earthdata_s3_credentials(url) when applicable.

------

-------------------------------------------------------------
3.1.5
-------------------------------------------------------------
| April 1, 2024
| Minor feature additions and bug fixes.

Added
^^^^^^^^^^^^
* Open in file browser button for output of completed jobs in Jobs UI: https://github.com/MAAP-Project/Community/issues/656
* Bug submission reporting new option for help menu: https://github.com/MAAP-Project/Community/issues/302
* Cancel/dismiss a job from the Jobs UI: https://github.com/MAAP-Project/Community/issues/753
* Added more packages to pangeo/r images: https://github.com/MAAP-Project/Community/issues/898, https://github.com/MAAP-Project/Community/issues/902
* Implemented cache for /edcCredentials: https://github.com/MAAP-Project/Community/issues/910
* Added stac_ipyleaflet to all ADE images: https://github.com/MAAP-Project/Community/issues/884
* Upgraded PHP to 8.x: https://github.com/MAAP-Project/Community/issues/921
* Upgraded WordPress to 6.4.3 and disabled auto updates: https://github.com/MAAP-Project/Community/issues/899, https://github.com/MAAP-Project/Community/issues/912
* New algorithm UI frontend jupyter extension: https://github.com/MAAP-Project/Community/issues/686, https://github.com/MAAP-Project/Community/issues/832
* EBS encryption on all instances in MCP: https://github.com/MAAP-Project/Community/issues/892
* All jupyter extensions now available on pip: https://github.com/MAAP-Project/Community/issues/817

Fixed
^^^^^^^^^^^^
* SSH key uploads fixed: https://github.com/MAAP-Project/Community/issues/850
* Link updates for MAAP API and MAAP logo in help menu: https://github.com/MAAP-Project/Community/issues/920, https://github.com/MAAP-Project/Community/issues/945
* Buttons for Jobs UI no longer remain grayed out after click: https://github.com/MAAP-Project/Community/issues/911
* Jobs inputs numbers now appear properly in Jobs UI Inputs tab: https://github.com/MAAP-Project/Community/issues/858
* Duplicate Job tag in Jobs UI resolved: https://github.com/MAAP-Project/Community/issues/797 
* Mounting for triaged-jobs folder: https://github.com/MAAP-Project/Community/issues/933
* Added missing dependency for awscli: https://github.com/MAAP-Project/Community/issues/938
* Fixed triaged-jobs s3fs mapping: https://github.com/MAAP-Project/Community/issues/932
* Shared buckets no longer dropping frequently: https://github.com/MAAP-Project/Community/issues/759

Changed
^^^^^^^^^^^^
* rio_tiler package now in base image so available for DPS images: https://github.com/MAAP-Project/Community/issues/929
* Removed ability to navigate to /search from our homepage: https://github.com/MAAP-Project/Community/issues/924
* Removed rgedi and isce2 workspaces: https://github.com/MAAP-Project/Community/issues/893

------

-------------------------------------------------------------
3.1.4
-------------------------------------------------------------
| January 22, 2024
| Minor feature additions and bug fixes.


Added
^^^^^^^^^^^^
* Log rotation for MAAP API: https://github.com/MAAP-Project/Community/issues/887
* Added dps-job-management shared workspace to track job status: https://github.com/MAAP-Project/Community/issues/754
* Added new packages to workspaces: https://github.com/MAAP-Project/Community/issues/729, https://github.com/MAAP-Project/Community/issues/743, https://github.com/MAAP-Project/Community/issues/742
* Submit Job button disables after submit to prevent users double submitting jobs: https://github.com/MAAP-Project/Community/issues/663

Fixed
^^^^^^^^^^^^
* Resolved UWG-reported workspace sluggishness: https://github.com/MAAP-Project/Community/issues/877, https://github.com/MAAP-Project/Community/issues/807
* Resolved libarchive error: https://github.com/MAAP-Project/Community/issues/860
* Resolved maap-py package dependency issues: https://github.com/MAAP-Project/Community/issues/885
* Fixed bug where username was not attached to job unless you opened the View Jobs tab before submitting: https://github.com/MAAP-Project/Community/issues/866

Changed
^^^^^^^^^^^^
* Set conda-forge as default channel: https://github.com/MAAP-Project/Community/issues/862
* Changed MAAP API flask service to gunicorn: https://github.com/MAAP-Project/Community/issues/886
* Cleaned up obsolete token code in maap-py: https://github.com/MAAP-Project/Community/issues/868
* Switch to libmamba solver: https://github.com/MAAP-Project/Community/issues/731
* STAC ipyleaflet bumped to v0.3.6 in Pangeo: https://github.com/MAAP-Project/Community/issues/890
* Updated MAAP API CMR data endpoint to better handler error responses: https://github.com/MAAP-Project/Community/issues/888
* Updated interface to maap-py granule.getDownloadUrl() to return http url: https://github.com/MAAP-Project/Community/issues/848

------

-------------------------------------------------------------
3.1.3
-------------------------------------------------------------
| November 2, 2023
| Minor feature additions and bug fixes.


Added
^^^^^^^^^^^^
* Capability to stop running jobs from the MAAP API (maap-py ``maap.cancelJob("id")``): https://github.com/MAAP-Project/Community/issues/640
* New maap-py method ``aws.workspace_bucket_credentials()`` for accessing user workspace bucket from outside the ADE: https://github.com/MAAP-Project/Community/issues/825
* Jobs UI: expose the entire stderr; split "View" and "Submit" into two tabs: https://github.com/MAAP-Project/Community/issues/651
* maap-py: add ``maap.downloadGranule()`` direct download of Earthdata Cloud URLs: https://github.com/MAAP-Project/Community/issues/515
* Add 'listContainer' support to MAAP API and maap-py: https://github.com/MAAP-Project/Community/issues/818

Fixed
^^^^^^^^^^^^
* Removed 5-second delay when submitting jobs to DPS: https://github.com/MAAP-Project/Community/issues/762
* ADE menu cleanup: updated menu items for jobs/algorithms and persistence of extensions on page refresh: https://github.com/MAAP-Project/Community/issues/833

Changed
^^^^^^^^^^^^
* Sort/filtering enhancements in the ADE Jobs UI: https://github.com/MAAP-Project/Community/issues/649
* Copy submit job code with formatting when using Submit Job UI: https://github.com/MAAP-Project/Community/issues/791
* Alphabetize the list of algorithms available in the job submission ui: https://github.com/MAAP-Project/Community/issues/829

Removed
^^^^^^^^^^^^
* Archived shared documents from the MAAP portal along with Memphis WordPress Plugin: https://github.com/MAAP-Project/Community/issues/821

------

-------------------------------------------------------------
3.1.1
-------------------------------------------------------------
| October 4, 2023
| Minor feature additions and bug fixes.


Added
^^^^^^^^^^^^
* DPS authentication support--jobs can now access secure API endpoints such as aws.earthdata_s3_credentials: https://github.com/MAAP-Project/Community/issues/717
* Added memory extension in the footer bar of Jupyter workspaces indicating memory usage within a notebook: https://github.com/MAAP-Project/Community/issues/749

Fixed
^^^^^^^^^^^^
* Presigned url bug fix for missing output when generated s3 urls: https://github.com/MAAP-Project/Community/issues/758
* Fixed maap-py.deleteAlgorithm() 404 error: https://github.com/MAAP-Project/Community/issues/814

Changed
^^^^^^^^^^^^
* Updated stac_ipyleaflet to 0.3.5 for Pangeo.
* Updated MAAP help tour: https://github.com/MAAP-Project/Community/issues/618
* Migrated DPS instances to OL8: https://github.com/MAAP-Project/Community/issues/739

Removed
^^^^^^^^^^^^
* isce2 workspaces are now deprecated.

------

-------------------------------------------------------------
3.1.0
-------------------------------------------------------------
| August 4, 2023
| Hotfix to handle bugs that make working in the “new” ops ADE difficult


Added
^^^^^^^^^^^^
* Added more capacity to the new ADE cluster to support more concurrent users.

Fixed
^^^^^^^^^^^^
* Error with cursor jumping around in Jupyter & Opening blank notebook error (disable Jupyter collaboration feature): https://github.com/MAAP-Project/Community/issues/735 
* Nested eclipse che menu error: https://github.com/MAAP-Project/Community/issues/733 (PR: https://github.com/MAAP-Project/maap-workspaces/pull/47)
* Add Show/Hide Che sidebar extension: https://github.com/MAAP-Project/Community/issues/692 
* DPS notifications bug: https://github.com/MAAP-Project/Community/issues/778 
* Maap libs extension can now show notifications: https://github.com/MAAP-Project/Community/issues/780 
* Api_server now present in MAAP() instance (changing use of maapsec): https://github.com/MAAP-Project/Community/issues/781 
* Open SSL fix: https://github.com/MAAP-Project/Community/issues/737 
* Update Jupyter server to include API endpoints: https://github.com/MAAP-Project/Community/issues/685 

Changed
^^^^^^^^^^^^
Removed
^^^^^^^^^^^^
* Remove ipycmc from default MAAP icon upper left of notebooks: https://github.com/MAAP-Project/Community/issues/779 
