# Why an Automated GIS Adjacency Approach Was Rejected

An initial attempt to construct the district-level adjacency classification used GADM v4.1 (https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_AZE_shp.zip), the most widely used open administrative-boundary GIS dataset. Inspecting the level-2 (district) attribute table revealed the following problems, which make this source unsuitable for identifying adjacency among Azerbaijan's current (post-2021) districts:

1. **Outdated administrative structure.** The dataset groups districts into pre-2021 Soviet-era economic-region categories (e.g., "Yukhari-Karabakh," "Kalbajar-Lachin"), inconsistent with Azerbaijan's 7 July 2021 territorial reform, which the underlying production panel and this package's analysis both follow.
2. **Missing districts.** Gubadli district -- one of the ten reintegrated districts central to this analysis -- does not appear in the dataset at all.
3. **Duplicated and unlabelled records.** Several districts (e.g., Kalbajar, Tartar, Yevlakh) appear more than once, and a number of records have no district name (`NAME_2 = NA`), rendering unambiguous matching to the production panel impossible.
4. **Ambiguous city/district conflation.** Cities (e.g., Baku, Ganja, Yevlakh) are coded as separate "City" type records distinct from their surrounding "District" records, complicating direct matching to the production panel's district-level observations.

Given these issues, using GADM-derived polygons to construct a district-level contiguity matrix risked silently misclassifying adjacency relationships in ways that would be difficult to detect after the fact. We instead constructed the adjacency classification manually from official administrative border descriptions (see `DATA_DESCRIPTION.md` and `code/_paths.py`), a standard practice in regional economics when authoritative, up-to-date GIS boundary data are unavailable.
