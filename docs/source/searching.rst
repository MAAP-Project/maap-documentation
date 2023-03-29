=======================================
Search
=======================================

MAAP's Dual Catalog
=======================================

There are 2 catalogs MAAP users are advised to use:

* NASA's Operational CMR: https://cmr.earthdata.nasa.gov
* MAAP STAC: https://stac.maap-project.org

https://cmr.maap-project.org will be deprecated by **May 1, 2023** so users are encouraged to request collections they need from https://cmr.maap-project.org to be made discoverable in stac.maap-project if they are not already there or in NASA's Operational CMR.

Additional information on each catalog and migrating from MAAP's CMR is detailed below.

Migrating from MAAP's CMR
=======================================

If you are migrating code from use of https://cmr.maap-project.org, that's great news! And we are here to help.

We are hoping the documentation below is enough to support migrating from https://cmr.maap-project.org to cmr.earthdata.nasa.gov and https://stac.maap-project.org, but if not please contact the data team for assistance.

Migration Steps:
----------------

1. Identify where in your code you are using https://cmr.maap-project.org and which datasets are being discovered and accessed.
2. Once those datasets are identified, use https://search.earthdata.nasa.gov or https://stac-browser.maap-project.org to find out if that dataset is available through NASA's Operational CMR or MAAP's STAC catalog. You will probably use the collection title or ID to search. **If you don't see your datasets in one of those places, please reach out to the data team so we can prioritize that dataset for publication to MAAP STAC.** At time of writing, there are still 21 datasets in process of being published from MAAP's CMR to MAAP STAC.
3. If the dataset is in NASA's Operational CMR and you are using MAAP's python library maap-py to discover and access data, you should be able to add the parameter ``cmr_host="cmr.earthdata.nasa.gov`` to your ``maap.searchCollection`` and ``maap.searchGranule`` function calls. In the near future, the default host for maap-py will be https://cmr.earthdata.nasa.gov, but we don't want to make that change until we know we won't be breaking any existing workflows. If you are using a ``concept_id`` to identify a specific collection or granule, you will also need to update the ``concept_id`` to match the ``concept_id`` from NASA's operational CMR.

For example, the code below discovers granules from the ``ABoVE LVIS L2 Geolocated Surface Elevation Product``:

.. code-block:: python

  COLLECTION_ID = 'C1200125288-NASA_MAAP' 
  results = maap.searchGranule(concept_id=COLLECTION_ID)
  pprint(f'Got {len(results)} results')


This dataset exists in NASA's Operational CMR. Using https://search.earthdata.nasa.gov, I was able to discover the collection concept ID by searching for "ABoVE LVIS L2 Geolocated Surface Elevation Product" and copying the ``concept_id`` from the URL of the result to modify the code below:

.. code-block:: python

  COLLECTION_ID = 'C1513105984-NSIDC_ECS'
  results = maap.searchGranule(
    cmr_host='cmr.earthdata.nasa.gov',
    concept_id=COLLECTION_ID
  )
  pprint(f'Got {len(results)} results')


1. If the dataset is in MAAP STAC, you will need to use [`pystac_client`](https://pystac-client.readthedocs.io/en/stable/) or any http library you prefer to call the API endpoints directly.

This code discovers granules from the ``Landsat 8 Operational Land Imager (OLI) Surface Reflectance Analysis Ready Data (ARD) V1, Peru and Equatorial Western Africa, April 2013-January 2020``.

.. code-block:: python

  COLLECTION_ID = 'C1200110769-NASA_MAAP' 

  results = maap.searchGranule(concept_id=COLLECTION_ID)
  pprint(f'Got {len(results)} results')


You can use https://stac-browser.maap-project.org to find the STAC collection ID for that dataset, which is `Landsat8_SurfaceReflectance`.


.. code-block:: python

  from pystac_client import Client
  URL = 'https://stac.maap-project.org/'
  cat = Client.open(URL)
  for collection in cat.get_all_collections():
      print(collection)

  collection = cat.get_collection('Landsat8_SurfaceReflectance')
  items = collection.get_items()



MAAP STAC
=======================================

MAAP STAC is dedicated to datasets which are **not** accessible via NASA's CMR, such as GEDI Cal/Val datasets, ESA datasets and user-shared data products.

STAC discovery
---------------------------------------

Users can discover data in MAAP STAC via pystac-client or https://stac-browser.maap-project.org. 

API documentation is testable here: https://stac.maap-project.org/docs (will return MAAP STAC results).

The general STAC API spec is here: https://api.stacspec.org/v1.0.0-rc.1/core/.

An example of using pystac-client is included above and in search/searching_the_stac_catalog.ipynb.

Data access via STAC
---------------------------------------

Data published to STAC is still stored in ``s3://nasa-maap-data-store`` OR ESA's BMAP catalog and is accessible via public access or role-based bucket policy access. Each item should have a "data" asset which includes a URL to the data. For example, https://stac.maap-project.org/collections/BIOSAR1/items/biosar1_roi_lidar58 includes:

.. code-block:: json

  "assets": {
    "data": {
      "href": "https://bmap-catalogue-data.oss.eu-west-0.prod-cloud-ocb.orange-business.com/Campaign_data/biosar1/biosar1_roi_lidar58.shx",
      "type": "application/octet-stream",
      "roles": [
        "data"
      ]
    },
  }

NASA's Operational CMR
=======================================

CMR Discovery
---------------------------------------

Users can discover data via it's publicly accessible API: https://cmr.earthdata.nasa.gov and user interface: https://search.earthdata.nasa.gov.

CMR Access
---------------------------------------

For all NASA MAAP users, access to NASA'S Operational data is provided via a federated access token. Anything that is in NASA's Operational CMR should be accessed via maap-py so that the federated access token can be used. Users can also access data from LPDAAC (and possibly other DAACs in the future) without maap-py since the workspace should have access via a role-based bucket policy on the LPDAAC cloud bucket

Anyone can access data through Earthdata Login as well.

CMR Documentation
---------------------------------------

CMR Search documentation can be found in search/collections.ipynb and search/granules.ipynb and https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html.


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

