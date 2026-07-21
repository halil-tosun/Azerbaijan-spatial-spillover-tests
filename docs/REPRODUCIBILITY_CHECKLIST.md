# REPRODUCIBILITY CHECKLIST

- [x] All raw data required to reproduce every table and figure are included in `data/raw/` as static files.
- [x] No internet connection is required to run any part of the analysis.
- [x] All code is written in Python 3 using only open-source packages (NumPy, pandas, SciPy, Matplotlib); no proprietary or licensed software is used at any stage.
- [x] All estimators (two-way fixed effects, cluster-robust variance, wild cluster bootstrap, randomization inference) are implemented directly in the provided code rather than relying on an opaque third-party package, so that every computational step is inspectable.
- [x] All random-number generation uses fixed seeds, specified explicitly in each script.
- [x] Every table and figure reported in the manuscript has a corresponding, individually runnable script, documented in the Script-to-Manuscript Correspondence table in `README.md`.
- [x] A single `run_all.py` script reproduces the entire pipeline end to end.
- [x] Figures are saved at 600 DPI publication-quality resolution.
- [x] The environment is fully specified in both `requirements.txt` (pip) and `environment.yml` (conda).
- [x] The district-adjacency classification is fully sourced (see `docs/DATA_DESCRIPTION.md`), and the reasons an automated GIS alternative was rejected are documented (`docs/GADM_ISSUES.md`).
- [x] Known sources of numerical variation across software versions are documented in `docs/CODEBOOK.md`.

## Verification steps for a reviewer or independent replicator

1. Clone or unzip the repository.
2. Install the environment (`environment.yml` or `requirements.txt`).
3. Run `python code/run_all.py` from the `code/` directory.
4. Confirm that `output/` contains 9 CSV files and `figures/` contains 4 PNG files at 600 DPI.
5. Compare the printed console output for each table against the corresponding table in the manuscript; all values should match to at least 2-3 decimal places (see `docs/CODEBOOK.md` for expected sources of minor numerical variation in bootstrap- and permutation-based results).
