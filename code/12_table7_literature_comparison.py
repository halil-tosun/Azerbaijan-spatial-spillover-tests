"""
Table 7. Comparison studies of conflict-related spatial spillovers.

Situates this paper's design alongside recent large-scale studies of
conflict-related spatial spillovers (Section 4.3). N figures are approximate
and drawn from publicly available abstracts and data descriptions rather
than a systematic review of the comparison studies' full replication
materials; this table is a documentation/synthesis table, not a computation.

Produces: output/Table7_literature_comparison.csv
"""
import pandas as pd
from _paths import OUTPUT_DIR

rows = [
    ["Jedwab et al. (2025)", "Boko Haram insurgency, Cameroon/Chad/Niger",
     "0.1\u00b0\u00d70.1\u00b0 grid cells", "~1,546\u201325,491", "Not identified"],
    ["Alfano & Cornelissen (2026)", "Al-Shabaab insurgency, Somalia",
     "Markets / transport routes", "Dozens of major markets, national network", "Not identified"],
    ["This paper", "Nagorno-Karabakh reintegration, Azerbaijan",
     "Districts", "9 treated + 7 adjacent", "Yes (Table 4)"],
]
table7 = pd.DataFrame(rows, columns=["Study", "Setting", "Spatial unit", "Approx. N (units)", "Power/MDE reported?"])
table7.to_csv(OUTPUT_DIR / "Table7_literature_comparison.csv", index=False)

print("Table 7. Comparison studies of conflict-related spatial spillovers\n")
print(table7.to_string(index=False))
print("\nSaved to output/Table7_literature_comparison.csv")
