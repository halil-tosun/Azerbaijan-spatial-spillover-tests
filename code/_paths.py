"""
Shared path configuration. Every script imports this so the package runs
identically regardless of the current working directory it is launched from.

Tables and other numerical outputs are written to ../output/ (as .csv).
Figures (.png) are written to ../figures/ at 600 DPI.
"""
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
DATA_DIR = ROOT_DIR / "data" / "raw"
OUTPUT_DIR = ROOT_DIR / "output"
FIG_DIR = ROOT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

FIGURE_DPI = 600

# ---------------------------------------------------------------------------
# District adjacency classification, verified against official administrative
# border descriptions (see docs/DATA_DESCRIPTION.md and docs/GADM_ISSUES.md
# for full sourcing and the reasons an automated GIS approach was rejected).
# ---------------------------------------------------------------------------

TREATED = [
    'Aghdam district', 'Fuzuli district', 'Gubadli district', 'Jabrayil district',
    'Kalbajar district', 'Khojavand district', 'Lachin district', 'Shusha district',
    'Zangilan district',
]

REINTEGRATED_FOR_ADJACENCY = TREATED + ['Aghdara district']

ADJACENT_1ST_ORDER = [
    'Aghjabadi district', 'Barda district', 'Beylagan district', 'Dashkasan district',
    'Goranboy district', 'Goygol district', 'Tartar district',
]

ADJACENT_2ND_ORDER = [
    'Zardab district', 'Imishli district', 'Agdash district', 'Yevlakh district',
    'Samukh district', 'Shamkir district', 'Gadabay district', 'Ganja city',
]

POST_YEAR_CUTOFF = 2021  # first full year following the November 2020 ceasefire
