# CODEBOOK

## Analytical Workflow and Script-by-Script Description

This codebook documents the purpose, inputs, and outputs of every script in `code/`, in the order they are executed by `run_all.py`.

---

### `_paths.py` (helper, not run directly)

Defines shared directory paths and the district-adjacency classification (`TREATED`, `ADJACENT_1ST_ORDER`, `ADJACENT_2ND_ORDER`) used throughout the package. See `DATA_DESCRIPTION.md` for the sourcing of these lists.

### `_estimation.py` (helper, not run directly)

Implements the two-way fixed-effects (within-transformation) estimator with cluster-robust standard errors, the restricted wild cluster bootstrap (Rademacher weights), and Fisher-style randomization inference, all directly in NumPy/SciPy (no specialized econometrics package is used anywhere in this repository).

### `01_table1_adjacency_classification.py`

**Input:** none (hard-coded, sourced classification).
**Output:** `output/Table1_adjacency_classification.csv`.
Documents each reintegrated district's economic region and officially bordering districts.

### `02_table2_replication_efficiency.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv`, `data/raw/table4_sfa_district_te.csv`.
**Output:** `output/Table2_replication_efficiency.csv`.
Verifies that the district-level efficiency panel included in this package reproduces previously reported summary statistics (raw and bootstrap-corrected DEA efficiency; SFA mean technical efficiency and log-likelihood).

### `03_table3_spillover_inference.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv`.
**Output:** `output/Table3_spillover_inference.csv`, plus two intermediate NumPy files (`_ri_placebo_distribution.npy`, `_ri_observed.npy`) consumed by script 04.
Estimates the direct treatment effect and first-/second-order spillover coefficients under cluster-robust inference, wild cluster bootstrap, and randomization inference.

### `04_figure1_randomization_inference.py`

**Input:** the two `.npy` files saved by script 03.
**Output:** `figures/Figure1_randomization_inference.png` (600 DPI).

### `05_figure2_tost_equivalence.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv`.
**Output:** `figures/Figure2_tost_equivalence.png` (600 DPI). Also prints the TOST p-values reported in the text.

### `06_table4_mde_by_cluster_count.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv`.
**Output:** `output/Table4_mde_by_cluster_count.csv`.
Computes the minimum detectable effect (MDE) for the actual design (7 adjacent clusters) and simulates the MDE for larger placebo adjacent-cluster counts (10-30), using 30 random draws per cluster count.

### `07_figure3_mde_simulation.py`

**Input:** `output/Table4_mde_by_cluster_count.csv`.
**Output:** `figures/Figure3_mde_simulation.png` (600 DPI).

### `08_table5_leave_one_out.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv`.
**Output:** `output/Table5_leave_one_out.csv`.
Re-estimates the first-order spillover coefficient with each adjacent district excluded in turn.

### `09_figure4_leave_one_out.py`

**Input:** `data/raw/table3_dea_bootstrap_full.csv` (re-estimates the same models as script 08).
**Output:** `figures/Figure4_leave_one_out.png` (600 DPI).

### `10_table6_diagnostic_evidence.py`

**Input:** none (synthesis table reproducing, verbatim, the results computed by scripts 03 and 11).
**Output:** `output/Table6_diagnostic_evidence.csv`.

### `11_appendix_sfa_robustness.py`

**Input:** `data/raw/table4_sfa_district_te.csv`.
**Output:** `output/Appendix_SFA_robustness.csv`.
Re-estimates the direct and first-order spillover effects using SFA-based technical efficiency in place of bootstrap-corrected DEA efficiency.

### `12_table7_literature_comparison.py`

**Input:** none (hard-coded synthesis of publicly available information on comparison studies; see manuscript Section 4.3 for sourcing caveats).
**Output:** `output/Table7_literature_comparison.csv`.

### `13_tableB1_analytical_mde.py`

**Input:** `output/Table4_mde_by_cluster_count.csv`.
**Output:** `output/TableB1_analytical_mde.csv`.
Computes the theoretical SE/MDE scaling law, SE(G) = SE(G0)*sqrt(G0/G), and compares it against the simulation from script 06.

---

## Notes on Reproducibility

- All random number generation uses fixed seeds (see individual scripts). Different NumPy/SciPy versions can in principle produce small (typically third-decimal-place) differences in bootstrap- and permutation-based results through differences in floating-point summation order; substantive conclusions are unaffected.
- No internet connection is required to run any part of this package; all data are provided as static files in `data/raw/`.
