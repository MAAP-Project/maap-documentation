# MAAP STAC Metadata Recommendations
MAAP uses the STAC (SpatioTemporal Asset Catalog) specification, which provides a common structure for describing and cataloging geospatial data [(STAC)](https://stacspec.org/en).

At a minimum, MAAP metadata should conform to STAC specification requirements. MAAP also requires the STAC-equivalent of certain [Unified Metadata Model (UMM)](https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr/umm) metadata elements (UMM is a metadata schema used in [NASA's Common Metadata Repository (CMR)](https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr)). These elements are included below, and are broken down at the collection and item level.

**Note**: NASA CMR also uses Global Change Master Directory (GCMD) Keywords to help with consistency and searchability. As a best practice, MAAP recommends using GCMD keywords in applicable fields, which are noted below. For more information, see ["GCMD Keyword Viewer"](https://www.earthdata.nasa.gov/data/tools/idn/gcmd-keyword-viewer). Downloadable CSV files of GCMD keywords are also provided for relevant fields. 

## STAC Collection-Level Metadata Fields
- `id`: **Required**. The unique identifier of the collection.
- `version`: **Required**. The version of the data. This is different than the `stac_version` element. 
- `title`: **Required**. A short descriptive title of the datatset. This should differ from the `id`.
- `sci:doi`: **Required if available**. The DOI of the collection should be provided using the [Scientific Citation Extension Specification](https://github.com/stac-extensions/scientific/tree/main). 
  - For more information and resources about DOIs, see [Open Sourcing Code](../../science/oss_documentation/doi_and_licensing.ipynb).  
- `description`: **Required** A detailed description or abstract for the dataset. The description should be useful to the science community, but also approachable for a first time user of the data. It is recommended to include information such as what platforms/instruments were/are used to collect the data, the parameters that are provided, the spatial and temporal coverage, and the purpose and/or intended use of the data.
- `providers`: **Required**. The name of the organization(s) responsible for originating, processing, archiving, and/or distributing the dataset.
- `keywords`: **Required**. Keyword(s) that describe the parameters provided in the data.
  - This is a GCMD-controlled field: [Science Keywords CSV file](https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/sciencekeywords/?format=csv).
- `links`: **Required**. Resources related to a collection. This should include a link to access the data. Other links to consider adding: user's guide, a dataset landing page, ATBD, read-me, the project home page, relevant online data tools, etc. 
- `extent`:
  - `spatial`: **Required**. The spatial extent of the collection, which should encompass all items.
  - `temporal`: **Required**. The temporal extent of the collection, which should encompass all items.
- `summaries`:
  - `platforms`: **Required**. Platforms used for data aquisition.
    - This is a GCMD-controlled field: [Platforms CSV file](https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/platforms?format=csv)
  - `instruments`: **Highly recommended**. Instruments used for data aquisition.
    - This is a GCMD-controlled field: [Instruments CSV file](https://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme/instruments/?format=csv)
  - `mission`: **Highly recommended**. The scientific endeavor(s) with which the collection is associated, including but not limited to field or flight campaigns, projects, missions, scientific programs, etc.
  - `gsd`: **Highly recommended**. The spatial resolution of the data in meters. 
  - `processing:level` **Required**. The level at which the data in the collection are processed, with values ranging from L0 to L4. 
    - MAAP recommends using NASA's Earth Observing System Data and Information System (EOSDIS) processing levels. For more information, please see [Data Processing Levels](https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/data-processing-levels).
- `license`: **Required**. License of the collection and its associated items. The license should be permissive or open. 
  - For more information and resources about licenses, see [Open Sourcing Code](../../science/oss_documentation/doi_and_licensing.ipynb).  
- `sci:citation`: **Highly recommended**. The collection citation.
- `item_assets`:
  - `type`: **Required**. The media type of the asset.
    - [Common Media Types in STAC](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#common-media-types-in-stac) 
- `stac_version`: **Required**. The STAC version the collection implements.

## STAC Item-Level Metadata Fields
- `id`: **Required**. The unique identifier of the item.
- `collection`: **Required**. The ID of the STAC collection that the item is associated with.
- `geometry`: **Required**. The full footprint of the asset represented by the item.
- `bbox`: **Required IF geometry is not `null`**. The bounding box of the asset represented by the item.
- `properties`:
  - `datetime`: **Required**. The temporal extent of the item. If the temporal extent is a date range, `start_datetime` and `end_datetime` can be provided.
  - A provider date is also **required**, and presents a date associated with changes made to the item in the database which it is stored. At least one provider date should be given. Options include: 
    - `created_datetime`: date the item file was created. 
    - `inserted_datetime`: the date the item file was entered into the database.
    - `updated_datetime`: the date the item file was last updated.
- `links`: **Required**. Links to resources and related URLs.
- `assets`: 
  - `href`: **Required**. Link to download the asset object.
  - `type`: **Required**. The media type of the asset object. 
- `stac_version`: **Required**. The STAC version the item implements. 
- `type`: **Required**. The type of the GeoJSON object.


## Additional Resources
- [STAC Collection Specification](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md) 
- [STAC Item Specification]()