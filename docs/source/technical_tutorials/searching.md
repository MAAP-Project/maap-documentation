# Search

MAAP provides its own STAC API, but MAAP users often work with collections that live in NASA CMR, ESA MAAP STAC, and other upstream catalogs.

The recommended MAAP data discovery workflow is:

1. Use [Federated Search](search/federated-collection-discovery/collection_discovery.ipynb) to discover relevant collections across catalogs.
2. Identify the collection's source STAC API and collection ID from the result.
3. Continue with item-level search in that source STAC API.

This keeps the starting point focused on finding the right collection before choosing a source-specific workflow.

## Commonly used catalogs

- [MAAP STAC](https://stac.maap-project.org) for MAAP-published collections.
- [NASA CMR STAC](https://cmr.earthdata.nasa.gov/stac/ALL) and Earthdata Search for many NASA collections.
- [ESA MAAP STAC](https://catalog.maap.eo.esa.int/catalogue/) for ESA-hosted collections.
- Other upstream STAC APIs that may be configured in Federated Search.

:::{warning}
The <https://cmr.maap-project.org> catalog was deprecated on **May 1, 2023**. Users should request collections they need from this catalog to be made discoverable in MAAP STAC or NASA's Operational CMR if they're not already there.
:::

If you are migrating older code or want more catalog background, see [Catalog background and migration notes](search/catalog.md).

Specialized tutorials for NASA CMR, Earthdata Search, and R remain available below when you already know which source you need.

**Search Topics:**

```{toc}
:context: children
:depth: 2
```

- [Finding and Accessing Data in R (OpenScapes)](working_with_r/find_data_in_r.md)
