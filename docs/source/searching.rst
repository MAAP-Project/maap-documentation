Search
=======================================

# MAAP's Dual Catalog

There are 2 catalogs MAAP users are advised to use:

* NASA's Operational CMR: https://cmr.earthdata.nasa.gov
* MAAP STAC: https://stac.maap-project.org.

cmr.maap-project.org will be deprecated this year so users are encouraged to request collections that are available in cmr.maap-project.org to be made discoverable in stac.maap-project.

# MAAP STAC

MAAP STAC is dedicated to datasets which are not accessible via NASA’s CMR, such as GEDI Cal/Val datasets, ESA datasets and user-shared data products.
Nothing in MAAP STAC is also discoverable via NASA's operational CMR.

## STAC discovery

discovered via pystac-client or maap-stac-browser

## STAC access

accessed via public access or role-based bucket policy access

## STAC documentation

STAC Search documentation can be found in search/searching_the_stac_catalog.ipynb.


# NASA's Operational CMR

## CMR Discovery

Users can discover data via it's publicly accessible API: cmr.earthdata.nasa.gov and user interface: search.earthdata.nasa.gov.

## CMR ACcess

For all NASA MAAP users, access to data is provided via a federated access token. Anything that is in NASA's operational CMR should be accessed via maap-py so that the federated access token can be used. Users can also access data from LPDAAC (and possible other DAACs in the future) without maap-py since the workspace should have access via a role-based bucket policy on the LPDAAC cloud bucket

Anyone can access data through Earthdata Login as well.

## CMR Documentation

CMR Search documentation can be found in search/collections.ipynb and search/granules.ipynb.


.. toctree::
  :maxdepth: 2
  :caption: Search:
  
  search/searching_edsc_gui
  search/collections.ipynb
  search/granules.ipynb
  search/searching_compiling_list_of_granule_ids.ipynb
  search/cmr_collection_table.ipynb
  search/deprecated_collection_table.ipynb
  search/searching_the_stac_catalog.ipynb

