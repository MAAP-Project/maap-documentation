MAAP STAC Metadata Guidance
==================================

MAAP uses the STAC (SpatioTemporal Asset Catalog) specification, which
provides a common structure for describing and cataloging geospatial
data `(STAC) <https://stacspec.org/en>`__.

At a minimum, MAAP metadata should conform to STAC specification
requirements. MAAP also requires the STAC-equivalent of certain `Unified
Metadata Model
(UMM) <https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr/umm>`__
metadata elements (UMM is a metadata schema used in `NASA’s Common
Metadata Repository
(CMR) <https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr>`__). These
elements are included below, and are broken down at the collection and
item level.

Requirements are noted by schema as follows:

- ``element``:sup:`1`: required by STAC

- ``element``:sup:`2`: required by UMM

- ``element``:sup:`3`: not required by STAC or UMM, but still required by MAAP

**Note**: NASA CMR also uses Global Change Master Directory (GCMD)
Keywords to help with consistency and searchability. As a best practice,
MAAP recommends using GCMD keywords in applicable fields, which are
noted below. For more information, see `“GCMD Keyword
Viewer” <https://www.earthdata.nasa.gov/data/tools/idn/gcmd-keyword-viewer>`__.
Downloadable CSV files of GCMD keywords are also provided for relevant
fields.

`STAC Collection-Level Metadata Fields <https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md>`__
----------------------------------------------------------------------------------------------------------------------------------------

-  ``id``:sup:`1,2`: **Required**. The unique identifier of the collection. 

-  ``version``:sup:`2`: **Required**. The version of the data. This is different
   than the ``stac_version`` element.

-  ``title``:sup:`1,2`: **Required**. A short descriptive title of the datatset.
   This should differ from the ``id``.

-  ``sci:doi``:sup:`2`: **Required if available**. The DOI of the collection
   should be provided using the `Scientific Citation Extension
   Specification <https://github.com/stac-extensions/scientific/tree/main>`__.

   -  For more information and resources about DOIs, see `Open Sourcing
      Code <../../science/oss_documentation/doi_and_licensing.ipynb>`__.

-  ``description``:sup:`1,2`: **Required**. A detailed description or abstract for
   the dataset. The description should be useful to the science
   community, but also approachable for a first time user of the data.
   It is recommended to include information such as what
   platforms/instruments were/are used to collect the data, the
   parameters that are provided, the spatial and temporal coverage, and
   the purpose and/or intended use of the data.

-  ``providers``:sup:`2`: **Required**. The name of the organization(s)
   responsible for originating, processing, archiving, and/or
   distributing the dataset. Multiple roles can belong to the same
   organization.

   -  Producer: the organization responsible for producing the data.

      -  Example: if a MAAP team collects or generates the data, add the
         “producer” role to the “MAAP” provider.

   -  Processor: the organization responsible for processing the data.

      -  Example: if a MAAP team processes the data (e.g., re-grids or
         re-projects the data to create a higher level product), add the
         “processor” role to the “MAAP” provider.

   -  Host: The organization responsible for storing or archiving the
      data.

      -  Example: if data are hosted in a MAAP bucket, add the “host”
         role to the “MAAP” provider.
      -  Example: if data are hosted in the NASA CMR, the “host” role
         would be added to the respective NASA DAAC.

-  ``keywords``:sup:`2`: **Required**. Keyword(s) that describe the parameters
   provided in the data.

   -  This is a GCMD-controlled field: `Science Keywords CSV
      file <https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/sciencekeywords/?format=csv>`__.

-  ``links``:sup:`1,2`: **Required**. Resources related to a collection. This
   should include a link to access the data. Other links to consider
   adding: user’s guide, a dataset landing page, ATBD, read-me, the
   project home page, relevant online data tools, etc.

-  ``extent``:

   -  ``spatial``:sup:`1,2`: **Required**. The spatial extent of the collection,
      which should encompass all items.
   -  ``temporal``:sup:`1,2`: **Required**. The temporal extent of the collection,
      which should encompass all items.

-  ``summaries``:

   -  ``platforms``:sup:`2`: **Required**. Platforms used for data aquisition.

      -  This is a GCMD-controlled field: `Platforms CSV
         file <https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/platforms?format=csv>`__

   -  ``instruments``:sup:`3`: **Required**. Instruments used for data
      aquisition.

      -  This is a GCMD-controlled field: `Instruments CSV
         file <https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/instruments/?format=csv>`__

   -  ``mission``:sup:`3`: **Required**. The scientific endeavor(s)
      with which the collection is associated, including but not limited
      to field or flight campaigns, projects, missions, scientific
      programs, etc.

   -  ``gsd``:sup:`3`: **Required**. The spatial resolution of the
      data in meters.

   -  ``processing:level``:sup:`2`: **Required**. The level at which the data in
      the collection are processed, with values ranging from L0 to L4.

      -  MAAP recommends using NASA’s Earth Observing System Data and
         Information System (EOSDIS) processing levels. For more
         information, please see `Data Processing
         Levels <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/data-processing-levels>`__.

-  ``license``:sup:`1,2`: **Required**. License of the collection and its
   associated items. The license should be permissive or open.

   -  For more information and resources about licenses, see `Open
      Sourcing
      Code <../../science/oss_documentation/doi_and_licensing.ipynb>`__.

-  ``sci:citation``:sup:`3`: **Required**. The collection citation.

-  ``item_assets``:

   -  ``type``:sup:`2`: **Required**. The media type of the asset.

      -  `Common Media Types in
         STAC <https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#common-media-types-in-stac>`__

      - Note: UMM requires a data format at the collection level, which the ``item asset type`` provides in STAC.

-  ``stac_version``:sup:`1,2`: **Required**. The STAC version the collection
   implements.
   
   - Note: UMM requires ``Metadata Specification``, which has a purpose similar to ``stac_version``.

`STAC Item-Level Metadata Fields <https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md>`__
----------------------------------------------------------------------------------------------------------------------

-  ``id``:sup:`1,2`: **Required**. The unique identifier of the item.

-  ``collection``:sup:`1,2`: **Required**. The ID of the STAC collection that the
   item is associated with.

-  ``geometry``:sup:`1`: **Required**. The full footprint of the asset
   represented by the item.

-  ``bbox``:sup:`1`: **Required IF geometry is not null**. The bounding box
   of the asset represented by the item.

-  ``properties``:

   -  ``datetime``:sup:`1`: **Required**. The temporal extent of the item. If
      the temporal extent is a date range, ``start_datetime`` and
      ``end_datetime`` can be provided.

   -  A provider date is also **required** per UMM, and presents a date
      associated with changes made to the item in the database which it
      is stored. At least one provider date should be given. Options
      include:

      -  ``created_datetime``: date the item file was created.
      -  ``inserted_datetime``: the date the item file was entered into
         the database.
      -  ``updated_datetime``: the date the item file was last updated.

-  ``links``:sup:`1`: **Required**. Links to resources and related URLs.

-  ``assets``:

   -  ``href``:sup:`1`: **Required**. Link to download the asset object.
   -  ``type``:sup:`3`: **Required**. The media type of the asset object.
   -  ``roles``:sup:`3`: **Required**. The purpose of the asset object.

-  ``stac_version``:sup:`1,2`: **Required**. The STAC version the item implements.

   - Note: UMM requires ``Metadata Specification``, which has a purpose similar to ``stac_version``.

-  ``type``:sup:`1`: **Required**. The type of the GeoJSON object.

MAAP STAC Metadata Examples
-----------------------------
Below are metadata examples created for MAAP's `"ICESat-2 Boreal v2.1: Gridded Aboveground Biomass Density" <https://stac-browser.maap-project.org/collections/icesat2-boreal-v2.1-agb>`__ dataset.
We have only included a small portion of the metadata - click on the header to see the full example json files.

`Collection <https://github.com/MAAP-Project/icesat2-boreal-stac/blob/main/examples/agb/collection.json>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: json
  
  "item_assets": {
    "cog": {
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": [
        "data"
      ],
      "gsd": 30,
      "processing:level": "L4",
      ...
     }
   },

   "license": "CC-BY",

   "summaries": {
      "platform": [
         "LANDSAT-8",
         "LANDSAT-9",
         "SENTINEL-2A",
         "SENTINEL-2B",
         "ICESat-2"
      ],
      "gsd": {
         "minimum": 30,
         "maximum": 30
     }
   },
   
   "stac_extensions": [
      "https://stac-extensions.github.io/version/v1.2.0/schema.json",
      "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
      "https://stac-extensions.github.io/render/v2.0.0/schema.json",
      "https://stac-extensions.github.io/scientific/v1.0.0/schema.json"
   ]


`Item <https://github.com/MAAP-Project/icesat2-boreal-stac/blob/main/examples/agb/boreal_agb_2020_202411251732556086_0000004/boreal_agb_2020_202411251732556086_0000004.json>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: json

  "properties": {
    "start_datetime": "2020-01-01T00:00:00+00:00",
    "end_datetime": "2020-12-31T23:59:59+00:00",
    "created_datetime": "2024-01-25T00:11:00+00:00",
    "proj:epsg": null,
    "proj:geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [
            -2241478.0000000047,
            9243304.00000001
          ],
          ...
   },

    "assets": {
      "cog": {
         "href": "s3://maap-ops-workspace/aliz237/dps_output/run_boreal_biomass_map/dev_v1.5/AGB_H30_2020/full_run/2024/11/25/09/38/51/560230/boreal_agb_2020_202411251732556086_0000004.tif",
         "type": "image/tiff; application=geotiff; profile=cloud-optimized",
         "title": "Gridded predictions of aboveground biomass (Mg/ha)",
         "description": "Gridded predictions of aboveground biomass (Mg/ha)",
         "gsd": 30,
         "processing:level": "L4",
         ...
         },
      ...
      }

Additional Resources
-----------------------------
- `UMM-C Schema <https://git.earthdata.nasa.gov/projects/EMFD/repos/unified-metadata-model/browse/collection>`__ 
- `UMM-G Schema <https://git.earthdata.nasa.gov/projects/EMFD/repos/unified-metadata-model/browse/granule>`__ 