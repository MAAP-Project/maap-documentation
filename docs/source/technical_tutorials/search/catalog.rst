MAAP's Dual Catalog
=======================================

MAAP users are advised to use two catalogs:

1. Use NASA's Operational CMR to discover NASA-produced and curated data: https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html.
2. Use MAAP STAC for data not found in NASA CMR, and data produced by MAAP users: https://stac.maap-project.org/api.html.

.. warning::
	The https://cmr.maap-project.org catalog will be deprecated by **May 1, 2023**. Users should request collections they need from this catalog to be made discoverable in the MAAP STAC or NASA's Operational CMR if they're not already there.

More information on each catalog and migrating from MAAP's CMR is detailed in the bottom of this page.

=======================================
MAAP STAC
=======================================

MAAP STAC (https://stac.maap-project.org) is dedicated to datasets not accessible via NASA's CMR, such as GEDI Cal/Val datasets, ESA datasets, and user-shared data products.

STAC discovery
---------------------------------------

Users can discover data in MAAP STAC using pystac-client or https://stac-browser.maap-project.org.

API documentation is available here: https://stac.maap-project.org/api.html (will return MAAP STAC results).

The general STAC API spec is here: https://api.stacspec.org/v1.0.0-rc.1/core/.

An example of using pystac-client is included above and in `Searching STAC Documentation <searching_the_stac_catalog.ipynb>`_.

Data Access via STAC
---------------------------------------

Data assets (files) published to STAC have not moved from the S3 bucket ``s3://nasa-maap-data-store``. ESA data is accessible via public HTTP access. NASA data in S3 is accessible publicly or via role-based bucket policy access.

Users are encouraged to use common AWS S3 libraries for NASA data access, such as Python's boto3.

Each item should have a "data" asset which includes a URL to the data.

For example, https://stac.maap-project.org/collections/BIOSAR1/items/biosar1_roi_lidar58 includes:

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

=======================================
NASA's Operational CMR
=======================================

CMR Discovery
---------------------------------------

Users can discover data NASA's Operational CMR via its publicly accessible API: https://cmr.earthdata.nasa.gov and user interface: https://search.earthdata.nasa.gov.

CMR Search documentation can be found in `Searching Collections <collections.ipynb>`_ and `Searching Granules <granules.ipynb>`_ and https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html.

CMR Access
---------------------------------------

For all NASA MAAP users, access to NASA'S Operational data is provided via a federated access token. Anything that is in NASA's Operational CMR should be accessed via maap-py so that the federated access token can be used. Users can also access data from LPDAAC (and possibly other DAACs in the future) without maap-py since the workspace should have access via a role-based bucket policy on the LPDAAC cloud bucket.

Anyone can access data through Earthdata Login as well.

Find more documentation about how to access data in CMR in the `Access <../accessing.html>`_ section of this documentation.

=======================================
Migrating from MAAP's CMR
=======================================

If you're migrating code from using https://cmr.maap-project.org, we're here to help. The documentation below should support migrating to https://cmr.earthdata.nasa.gov and https://stac.maap-project.org. If not, please contact the data team for assistance.

Migration Steps:
----------------

1. Identify where your code is using https://cmr.maap-project.org and which datasets are being discovered and accessed.
2. Once you've identified the datasets, use https://search.earthdata.nasa.gov or https://stac-browser.maap-project.org to find out if the dataset is available through NASA's Operational CMR or MAAP's STAC catalog. If you don't see your datasets in one of those places, reach out to the data team so they can prioritize that dataset for publication to MAAP STAC.
3. If the dataset is in NASA's Operational CMR and you're using MAAP's Python library ``maap-py`` to discover and access data, add the parameter ``cmr_host="cmr.earthdata.nasa.gov"`` to your ``maap.searchCollection`` and ``maap.searchGranule`` function calls. Update the ``concept_id`` to match the one from NASA's Operational CMR if you're using it to identify a specific collection or granule.
4. If the dataset is in MAAP STAC, use ``pystac_client`` (https://pystac-client.readthedocs.io/en/stable/) or an HTTP library to call the STAC HTTP API endpoints directly.

Examples:
----------------

Example of switching a granule search to NASA's Operational CMR:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The code below discovers granules from the ``ABoVE LVIS L2 Geolocated Surface Elevation Product``:

.. code-block:: python

  COLLECTION_ID = 'C1200125288-NASA_MAAP' 
  results = maap.searchGranule(concept_id=COLLECTION_ID)
  pprint(f'Got {len(results)} results')

This dataset exists in NASA's Operational CMR. Using https://search.earthdata.nasa.gov, I discovered the collection's ``concept_id`` by searching for "ABoVE LVIS L2 Geolocated Surface Elevation Product" and copying the ``concept_id`` from the URL of the result to modify the code below:

.. code-block:: python

  COLLECTION_ID = 'C1513105984-NSIDC_ECS'
  results = maap.searchGranule(
    cmr_host='cmr.earthdata.nasa.gov',
    concept_id=COLLECTION_ID
  )
  pprint(f'Got {len(results)} results')

Example of switching a granule search to MAAP STAC:
+++++++++++++++++++++++++++++++++++++++++++++++++++

This code discovers granules from the ``Landsat 8 Operational Land Imager (OLI) Surface Reflectance Analysis Ready Data (ARD) V1, Peru and Equatorial Western Africa, April 2013-January 2020``.

.. code-block:: python

  COLLECTION_ID = 'C1200110769-NASA_MAAP' 

  results = maap.searchGranule(concept_id=COLLECTION_ID)
  pprint(f'Got {len(results)} results')


You can use https://stac-browser.maap-project.org to find the STAC collection ID for that dataset, which is ``Landsat8_SurfaceReflectance``.

.. code-block:: python

  from pystac_client import Client
  URL = 'https://stac.maap-project.org/'
  cat = Client.open(URL)
  for collection in cat.get_all_collections():
      print(collection)

  collection = cat.get_collection('Landsat8_SurfaceReflectance')
  items = collection.get_items()

