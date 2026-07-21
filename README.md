# When Are Spatial Spillover Tests Underpowered?

## Open Science Replication Package

This repository contains the complete replication package accompanying the manuscript **"When Are Spatial Spillover Tests Underpowered? A Cautionary Application to Post-Conflict Agricultural Recovery in Azerbaijan."**

---

## Repository Overview

This repository follows open science and computational reproducibility principles and includes:

- Complete Python source code for every table and figure
- The underlying district-level panel data
- A fully documented, sourced district-adjacency classification
- Comprehensive documentation
- Software environment specifications
- A step-by-step replication guide

---

## Repository Structure

```text
Replication_Package/
├── code/
├── data/
├── docs/
├── figures/
├── output/
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Documentation

- **docs/CODEBOOK.md** -- Analytical workflow and script-by-script description
- **docs/DATA_DESCRIPTION.md** -- Data sources, variable definitions, and adjacency-classification sourcing
- **docs/GADM_ISSUES.md** -- Documents why an automated GIS approach to adjacency was rejected in favor of the sourced classification used here
- **docs/REPRODUCIBILITY_CHECKLIST.md** -- Reproducibility checklist
- **docs/Replication_Guide.md** -- Complete replication guide

## Installation

```bash
conda env create -f environment.yml
conda activate spillover-repro
```

or

```bash
pip install -r requirements.txt
```

## Run

```bash
cd code
python run_all.py
```

This reproduces the complete analytical workflow: replication of previously reported efficiency estimates, the direct treatment effect, first- and second-order spillover estimates under three inference procedures (cluster-robust, wild cluster bootstrap, and Fisher-style randomization inference), a formal TOST equivalence test, a minimum-detectable-effect (MDE) analysis with cluster-count simulation, a leave-one-out robustness check, an SFA-based robustness check, and the analytical MDE derivation reported in Appendix B.

Expected runtime is approximately two minutes on a standard laptop.

## Script-to-Manuscript Correspondence

| Script | Produces | Manuscript location |
|---|---|---|
| `01_table1_adjacency_classification.py` | Table 1 | Section 2.3 |
| `02_table2_replication_efficiency.py` | Table 2 | Section 3.1 |
| `03_table3_spillover_inference.py` | Table 3 | Section 3.2 |
| `04_figure1_randomization_inference.py` | Figure 1 | Section 3.2 |
| `05_figure2_tost_equivalence.py` | Figure 2 | Section 3.2 |
| `06_table4_mde_by_cluster_count.py` | Table 4 | Section 3.3 |
| `07_figure3_mde_simulation.py` | Figure 3 | Section 3.3 |
| `08_table5_leave_one_out.py` | Table 5 | Section 3.4 |
| `09_figure4_leave_one_out.py` | Figure 4 | Section 3.4 |
| `10_table6_diagnostic_evidence.py` | Table 6 | Section 4.2 |
| `11_appendix_sfa_robustness.py` | SFA robustness values underlying Table 6 | Section 3.4 |
| `12_table7_literature_comparison.py` | Table 7 | Section 4.3 |
| `13_tableB1_analytical_mde.py` | Table B1 | Appendix B |

## Data Provenance

The district-level efficiency panel (`data/raw/table3_dea_bootstrap_full.csv`, `data/raw/table4_sfa_district_te.csv`) is regenerated from the official district-level panel compiled from the State Statistical Committee of the Republic of Azerbaijan, using the bootstrap-corrected DEA and translog SFA procedures described in Section 2.2 of the manuscript. Re-running these procedures reproduces the previously reported statistics closely (see `docs/DATA_DESCRIPTION.md` for the verification checks).

The district-adjacency classification (`code/_paths.py`) is built from official administrative border descriptions rather than automated GIS boundary files; see `docs/GADM_ISSUES.md` for why an automated approach was rejected.

## Citation

Please cite both the published article and this archived repository. Citation metadata are provided in `CITATION.cff`.

## License

MIT License (code). Data files retain the licensing terms of their original sources; see `docs/DATA_DESCRIPTION.md`.

## Contact

**Halil Tosun, Ph.D.**

ORCID: https://orcid.org/0000-0001-5117-0390

**Version:** 1.0.0

**Archive DOI:** To be assigned upon public archival of this repository.
