"""
Table 5. Leave-one-out robustness: excluding each adjacent district in turn.

Re-estimates the first-order spillover coefficient after excluding each of
the seven adjacent districts in turn (reassigning it to the control group),
to verify that the null result is not driven by any single district.

Produces: output/Table5_leave_one_out.csv
"""
import pandas as pd
from scipy import stats as st
from _paths import DATA_DIR, OUTPUT_DIR, ADJACENT_1ST_ORDER
from _estimation import build_panel, twfe_cluster_robust

df = build_panel('vrs_bc', DATA_DIR / "table3_dea_bootstrap_full.csv")


def run(adjacent_set):
    d = df.copy()
    d['adjacent_post_tmp'] = d['region'].isin(adjacent_set).astype(int) * d['post']
    fit = twfe_cluster_robust(d, 'vrs_bc', ['treated_post', 'adjacent_post_tmp'])
    coef, se, dof = fit['beta'][2], fit['se'][2], fit['n_clusters'] - 1
    t = coef / se
    p = 2 * (1 - st.t.cdf(abs(t), dof))
    return coef, se, p


rows = []
coef0, se0, p0 = run(ADJACENT_1ST_ORDER)
rows.append(["(none \u2014 baseline)", f"{coef0:+.3f}", f"{se0:.3f}", f"{p0:.3f}"])

for excl in ADJACENT_1ST_ORDER:
    subset = [d for d in ADJACENT_1ST_ORDER if d != excl]
    coef, se, p = run(subset)
    label = excl.replace(" district", "")
    rows.append([label, f"{coef:+.3f}", f"{se:.3f}", f"{p:.3f}"])

table5 = pd.DataFrame(rows, columns=["Excluded district", "Coefficient", "Cluster-robust SE", "p-value"])
table5.to_csv(OUTPUT_DIR / "Table5_leave_one_out.csv", index=False)

print("Table 5. Leave-one-out robustness: excluding each adjacent district in turn\n")
print(table5.to_string(index=False))
print("\nSaved to output/Table5_leave_one_out.csv")
