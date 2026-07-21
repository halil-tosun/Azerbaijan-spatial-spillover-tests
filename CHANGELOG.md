# Changelog

## [1.0.0] - Initial release

- Complete replication package for all tables (1-7, B1) and figures (1-4).
- District-level efficiency panel (bootstrap-corrected DEA, translog SFA) included as static data.
- Sourced district-adjacency classification, with documentation of why an automated GIS approach (GADM v4.1) was rejected.
- All estimators (two-way fixed effects, cluster-robust variance, wild cluster bootstrap, Fisher-style randomization inference) implemented directly in NumPy/SciPy.
- Figures produced at 600 DPI.
