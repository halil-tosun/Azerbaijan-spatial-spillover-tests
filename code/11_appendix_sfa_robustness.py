"""
Appendix robustness check: direct and spillover effects using SFA-based
technical efficiency in place of bootstrap-corrected DEA efficiency.

Referenced by Table 6 (Section 3.4/4.2 of the manuscript). As discussed in
the manuscript, DEA and SFA are not expected to attribute post-reintegration
changes to the same component of efficiency, so this check is reported as a
robustness/consistency exercise rather than a like-for-like replication.

Produces: output/Appendix_SFA_robustness.csv
"""
import pandas as pd
from scipy import stats as st
from _paths import DATA_DIR, OUTPUT_DIR, ADJACENT_1ST_ORDER
from _estimation import build_panel, twfe_cluster_robust

df = build_panel('sfa_te_translog', DATA_DIR / "table4_sfa_district_te.csv")

fit1 = twfe_cluster_robust(df, 'sfa_te_translog', ['treated_post'])
coef_t, se_t = fit1['beta'][1], fit1['se'][1]
t_t = coef_t / se_t
p_t = 2 * (1 - st.t.cdf(abs(t_t), fit1['n_clusters'] - 1))

fit2 = twfe_cluster_robust(df, 'sfa_te_translog', ['treated_post', 'adj1_post'])
coef_a, se_a = fit2['beta'][2], fit2['se'][2]
t_a = coef_a / se_a
p_a = 2 * (1 - st.t.cdf(abs(t_a), fit2['n_clusters'] - 1))

rows = [
    ["Treated x Post (SFA)", f"{coef_t:+.4f}", f"{se_t:.4f}", f"{p_t:.4f}"],
    ["Adjacent(1st) x Post (SFA)", f"{coef_a:+.4f}", f"{se_a:.4f}", f"{p_a:.4f}"],
]
table = pd.DataFrame(rows, columns=["Coefficient", "Estimate", "Cluster-robust SE", "p-value"])
table.to_csv(OUTPUT_DIR / "Appendix_SFA_robustness.csv", index=False)

print("SFA-based robustness check (Section 3.4)\n")
print(table.to_string(index=False))
print("\nSaved to output/Appendix_SFA_robustness.csv")
