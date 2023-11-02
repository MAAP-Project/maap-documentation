Release Notes
=======================================

-------------------------------------------------------------
3.1.3
-------------------------------------------------------------
| November 2, 2023
| Minor feature additions and bug fixes.


Added
^^^^^^^^^^^^
* Capability to stop running jobs from the MAAP API (maap-py maap.cancelJob("id"))
* New maap-py method aws.workspace_bucket_credentials() for accessing user workspace bucket from outside the ADE
* Jobs UI: expose the entire stderr
* maap-py: add maap.downloadGranule() direct download of Earthdata Cloud URLs
* Add 'listContainer' support to MAAP API and maap-py 

Fixed
^^^^^^^^^^^^
* Removed 5-second delay when submitting jobs to DPS. 
* Fixed maap-py.deleteAlgorithm() 404 error.

Changed
^^^^^^^^^^^^
* Sort/filtering enhancements in the ADE Jobs UI
* Copy submit job code with formatting when using Submit Job UI.
* Alphabetize the list of algorithms available in the job submission ui.
* ADE menu cleanup: updated menu items for jobs/algorithms and persistence of extensions on page refresh

Removed
^^^^^^^^^^^^
* Removed shared documents from the MAAP portal along with Memphis WordPress Plugin


-------------------------------------------------------------
3.1.1
-------------------------------------------------------------
| October 4, 2023
| Minor feature additions and bug fixes.


Added
^^^^^^^^^^^^
* DPS authentication support--jobs can now access secure API endpoints such as aws.earthdata_s3_credentials. 
* Added memory extension in the footer bar of Jupyter workspaces indicating memory usage within a notebook.

Fixed
^^^^^^^^^^^^
* Presigned url bug fix for missing output when generated s3 urls.
* Fixed maap-py.deleteAlgorithm() 404 error.

Changed
^^^^^^^^^^^^
* Updated stac_ipyleaflet to 0.3.5 for Pangeo.
* Updated MAAP help tour.
* Migrated DPS instances to OL8.

Removed
^^^^^^^^^^^^
* isce2 workspaces are now deprecated.


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
