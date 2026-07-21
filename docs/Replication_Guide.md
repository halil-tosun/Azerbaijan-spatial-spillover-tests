# Replication Guide

**When Are Spatial Spillover Tests Underpowered? A Cautionary Application to Post-Conflict Agricultural Recovery in Azerbaijan**

Author: Halil Tosun, Ph.D.

ORCID: https://orcid.org/0000-0001-5117-0390

E-mail: halilibrahimtosun@gmail.com

---

## 1. Overview

This guide walks through reproducing every table and figure reported in the paper, starting from a clean clone or unzip of the repository.

## 2. Requirements

- Python 3.10 or 3.11 (recommended), or any Python 3.9+ installation
- ~50 MB of free disk space
- No GPU or specialized hardware required
- No internet connection required (all data are provided as static CSV files in `data/raw/`)

## 3. Setup

### Option A -- conda (recommended)

```bash
conda env create -f environment.yml
conda activate spillover-repro
```

### Option B -- pip

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Running the Full Pipeline

```bash
cd code
python run_all.py
```

This runs all 13 numbered scripts in the order in which their outputs appear in the paper (Table 1 first, Table B1 last, matching the order documented in `docs/CODEBOOK.md`). Expect the full run to complete in approximately two minutes; the wild cluster bootstrap (script 03) and the cluster-count MDE simulation (script 06) are the slowest individual steps.

## 5. Running an Individual Script

Every script can also be run on its own, e.g.:

```bash
cd code
python 08_table5_leave_one_out.py
```

Each script prints its results to the console in addition to saving them to `output/` (tables, `.csv`) or `figures/` (figures, 600 DPI `.png`). Note that scripts 04, 07, 09, and 13 depend on outputs saved by earlier scripts (03, 06, 06, and 08/06 respectively); running `run_all.py`, or running the numbered scripts in order, ensures these dependencies are satisfied.

## 6. Verifying the Results

After running `run_all.py`, check that:

1. `output/` contains 9 result files (`.csv`), plus two intermediate `.npy` files used internally by Figure 1.
2. `figures/` contains 4 `.png` files, each at 600 DPI.
3. The printed console values for Tables 2, 3, 4, and 5 match the corresponding tables in the manuscript to at least 2-3 decimal places.
4. The printed randomization-inference p-value at the end of script 03 (approximately 0.50) matches the value used in the caption of Figure 1.

## 7. Known Sources of Numerical Variation

- All bootstrap- and permutation-based results (Table 3's wild cluster bootstrap and randomization inference columns, and Table 4/Figure 3's cluster-count simulation) use fixed random seeds and will reproduce closely on rerun with the same NumPy version. Different NumPy/SciPy versions can in principle produce small (typically third-decimal-place) differences through differences in floating-point summation order; substantive conclusions are unaffected.
- The SFA-based robustness check (script 11) is estimated from a separate data file (`table4_sfa_district_te.csv`) with slightly different sample coverage than the DEA-based analysis; small numerical differences relative to any previously circulated draft values are expected and do not affect the qualitative conclusion (both direct and spillover effects remain statistically imprecise under SFA).

## 8. Contact

For questions about this replication package, please contact:

Halil Tosun, Ph.D. -- https://orcid.org/0000-0001-5117-0390
