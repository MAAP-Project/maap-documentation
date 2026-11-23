# Catalog background and migration notes

MAAP users often work across more than one catalog. In practice, the collection you want may live in MAAP STAC, NASA's Operational CMR, ESA MAAP STAC, or another upstream STAC API.

For the recommended starting point, see [Collection Discovery with Federated Search](federated-collection-discovery/collection_discovery.ipynb). This page is mainly background for users who want extra catalog context or who are migrating older workflows.

## Catalogs of interest

### MAAP STAC

MAAP STAC (<https://stac.maap-project.org>) contains collections that MAAP publishes through its STAC API, including MAAP-hosted and partner datasets.

### NASA's Operational CMR

NASA's Operational CMR is available through its APIs at <https://cmr.earthdata.nasa.gov> and through Earthdata Search at <https://search.earthdata.nasa.gov>.

For MAAP users, access to NASA operational data is often easiest through `maap-py` because it can use the federated access token. Anyone can also access data through Earthdata Login.

Find more documentation about how to access data in CMR in the [Access](../accessing.md) section of this documentation.

## Migrating from MAAP's CMR

The <https://cmr.maap-project.org> catalog was deprecated on **May 1, 2023**.

If you're migrating code from MAAP's CMR, the general approach is:

1. Identify where your code is using <https://cmr.maap-project.org> and which datasets are being discovered and accessed.
2. Use Federated Search, Earthdata Search, or MAAP STAC tools to determine where those datasets now live.
3. Update your discovery and item-search code to use the appropriate source catalog.

## Examples

### Example of switching a granule search to NASA's Operational CMR

The code below discovers granules from the `ABoVE LVIS L2 Geolocated Surface Elevation Product`:

```python
COLLECTION_ID = 'C1200125288-NASA_MAAP'
results = maap.searchGranule(concept_id=COLLECTION_ID)
pprint(f'Got {len(results)} results')
```

This dataset exists in NASA's Operational CMR. Using <https://search.earthdata.nasa.gov>, you can discover the collection's `concept_id` and update the code like this:

```python
COLLECTION_ID = 'C1513105984-NSIDC_ECS'
results = maap.searchGranule(
  cmr_host='cmr.earthdata.nasa.gov',
  concept_id=COLLECTION_ID
)
pprint(f'Got {len(results)} results')
```

### Example of switching a granule search to MAAP STAC

This code discovers granules from the `Landsat 8 Operational Land Imager (OLI) Surface Reflectance Analysis Ready Data (ARD) V1, Peru and Equatorial Western Africa, April 2013-January 2020`.

```python
COLLECTION_ID = 'C1200110769-NASA_MAAP'

results = maap.searchGranule(concept_id=COLLECTION_ID)
pprint(f'Got {len(results)} results')
```

If Federated Search or STAC Browser shows that the dataset now lives in MAAP STAC with collection ID `Landsat8_SurfaceReflectance`, switch to a STAC client workflow:

```python
from pystac_client import Client

URL = 'https://stac.maap-project.org/'
cat = Client.open(URL)
collection = cat.get_collection('Landsat8_SurfaceReflectance')
items = collection.get_items()
```
