"""
Table 1. Adjacency classification of the ten reintegrated districts.

Documents, for each reintegrated district, its economic region and its
officially bordering districts (marked with * where the neighbor is itself
reintegrated). Sources: official administrative border descriptions verified
against each district's dedicated record (State Statistical Committee of the
Republic of Azerbaijan; presidential decrees of 7 July 2021 and 5 December
2023). See docs/DATA_DESCRIPTION.md for full per-district sourcing notes.

Produces: output/Table1_adjacency_classification.csv
"""
import pandas as pd
from _paths import OUTPUT_DIR

rows = [
    ["Aghdam", "Karabakh", "Khojaly, Kalbajar*, Tartar, Khojavand*, Aghjabadi, Barda"],
    ["Aghdara", "Karabakh", "Goranboy, Tartar, Aghdam*, Khojaly, Kalbajar*"],
    ["Fuzuli", "Karabakh", "Khojavand*, Aghjabadi, Beylagan, Jabrayil*, (Iran)"],
    ["Gubadli", "East Zangezur", "Lachin*, Khojavand*, Jabrayil*, Zangilan*, (Armenia)"],
    ["Jabrayil", "East Zangezur", "Khojavand*, Fuzuli*, Gubadli*, Zangilan*, (Iran)"],
    ["Kalbajar", "East Zangezur", "Lachin*, Khojaly, Aghdam*, Tartar, Goranboy, Goygol, Dashkasan, (Armenia)"],
    ["Khojavand", "Karabakh", "Lachin*, Shusha*, Khojaly, Aghdam*, Aghjabadi, Fuzuli*, Jabrayil*, Gubadli*"],
    ["Lachin", "East Zangezur", "Kalbajar*, Khojaly, Shusha*, Khojavand*, Gubadli*, (Armenia)"],
    ["Shusha", "Karabakh", "Khojaly, Lachin*, Khojavand*"],
    ["Zangilan", "East Zangezur", "Gubadli*, Jabrayil*, (Armenia, Iran)"],
]

table1 = pd.DataFrame(rows, columns=["Reintegrated district", "Economic region", "Officially bordering districts (* = also reintegrated)"])
table1.to_csv(OUTPUT_DIR / "Table1_adjacency_classification.csv", index=False)

print("Table 1. Adjacency classification of the ten reintegrated districts\n")
print(table1.to_string(index=False))
print("\nNote: Khojaly borders several reintegrated districts but is excluded from the")
print("production panel because no usable observations are available for it.")
print("\nSaved to output/Table1_adjacency_classification.csv")
