"""
Table 3. Estimated direct and spillover effects under alternative inference
procedures.

Reports the direct treatment effect (Treated x Post) and first-/second-order
spillover coefficients (Adjacent x Post), each estimated by the two-way
fixed-effects specification described in Section 2.4, together with
conventional cluster-robust standard errors, a restricted wild cluster
bootstrap (WCR, Rademacher weights, 4,999 replications), and Fisher-style
randomization inference (2,000 placebo reassignments) for the first-order
spillover coefficient.

Note on specifications: consistent with the manuscript, the direct effect
is estimated from a model containing only Treated x Post; the first-order
spillover coefficient is estimated from a model containing Treated x Post
and Adjacent(1st) x Post; the second-order spillover coefficient is
estimated from a model containing all three regressors together. This
mirrors how each successive robustness check in Section 3.4 extends the
specification used in Section 3.2.

Produces: output/Table3_spillover_inference.csv
"""
import numpy as np
from scipy import stats as st
from _paths import DATA_DIR, POST_YEAR_CUTOFF
from _estimation import build_panel, twfe_cluster_robust, wild_cluster_bootstrap, randomization_inference
import pandas as pd
from _paths import OUTPUT_DIR, TREATED

df = build_panel('vrs_bc', DATA_DIR / "table3_dea_bootstrap_full.csv")


def ci95(coef, se, dof):
    tcrit = st.t.ppf(0.975, dof)
    return coef - tcrit * se, coef + tcrit * se


# --- Direct effect (Treated only) ---
fit1 = twfe_cluster_robust(df, 'vrs_bc', ['treated_post'])
coef_t, se_t = fit1['beta'][1], fit1['se'][1]
ci_t = ci95(coef_t, se_t, fit1['n_clusters'] - 1)
wcr_t = wild_cluster_bootstrap(df, 'vrs_bc', ['treated_post'], target_idx=1)

# --- First-order spillover (Treated + Adjacent(1st)) ---
fit2 = twfe_cluster_robust(df, 'vrs_bc', ['treated_post', 'adj1_post'])
coef_a1, se_a1 = fit2['beta'][2], fit2['se'][2]
ci_a1 = ci95(coef_a1, se_a1, fit2['n_clusters'] - 1)
wcr_a1 = wild_cluster_bootstrap(df, 'vrs_bc', ['treated_post', 'adj1_post'], target_idx=2)

donor_pool = [r for r in df['region'].unique() if r not in TREATED]
adjacent_1st = ['Aghjabadi district', 'Barda district', 'Beylagan district', 'Dashkasan district',
                'Goranboy district', 'Goygol district', 'Tartar district']
ri = randomization_inference(df, 'vrs_bc', 'treated_post', adjacent_1st, donor_pool)

# --- Second-order spillover (Treated + Adjacent(1st) + Adjacent(2nd)) ---
fit3 = twfe_cluster_robust(df, 'vrs_bc', ['treated_post', 'adj1_post', 'adj2_post'])
coef_a2, se_a2 = fit3['beta'][3], fit3['se'][3]
ci_a2 = ci95(coef_a2, se_a2, fit3['n_clusters'] - 1)

rows = [
    ["Treated x Post (direct effect)", f"{coef_t:+.4f}", f"{se_t:.4f}",
     f"[{ci_t[0]:.3f}, {ci_t[1]:.3f}]", f"p={wcr_t['p_wcr']:.3f} [{wcr_t['ci_wcr'][0]:.3f}, {wcr_t['ci_wcr'][1]:.3f}]", "\u2014"],
    ["Adjacent(1st) x Post", f"{coef_a1:+.4f}", f"{se_a1:.4f}",
     f"[{ci_a1[0]:.3f}, {ci_a1[1]:.3f}]", f"p={wcr_a1['p_wcr']:.3f} [{wcr_a1['ci_wcr'][0]:.3f}, {wcr_a1['ci_wcr'][1]:.3f}]",
     f"p={ri['p_ri']:.3f} ({ri['percentile']:.1f}th pctile)"],
    ["Adjacent(2nd) x Post", f"{coef_a2:+.4f}", f"{se_a2:.4f}",
     f"[{ci_a2[0]:.3f}, {ci_a2[1]:.3f}]", "\u2014", "\u2014"],
]
table3 = pd.DataFrame(rows, columns=["Coefficient", "Estimate", "Cluster-robust SE", "95% CI (cluster-robust)",
                                       "Wild cluster bootstrap", "Randomization inference"])
table3.to_csv(OUTPUT_DIR / "Table3_spillover_inference.csv", index=False)

print("Table 3. Estimated direct and spillover effects under alternative inference procedures\n")
print(table3.to_string(index=False))
print("\nSaved to output/Table3_spillover_inference.csv")

# Save residuals/objects needed by Figure 1 (randomization inference plot) for reuse
np.save(OUTPUT_DIR / "_ri_placebo_distribution.npy", ri['placebo'])
np.save(OUTPUT_DIR / "_ri_observed.npy", np.array([ri['observed']]))
