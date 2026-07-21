"""
Table B1 (Appendix B). Theoretical versus simulated MDE by number of
adjacent clusters.

Compares a simple analytical scaling law, SE(G) = SE(G0) * sqrt(G0/G), for
the cluster-robust standard error of the spillover coefficient against the
Monte Carlo simulation reported in Table 4, and reports the number of
adjacent clusters (G) implied by each approach for reaching an MDE equal to
the direct treatment effect.

Requires 06_table4_mde_by_cluster_count.py to have been run first.

Produces: output/TableB1_analytical_mde.csv
"""
import numpy as np
import pandas as pd
from scipy import stats as st
from _paths import OUTPUT_DIR

sim = pd.read_csv(OUTPUT_DIR / "Table4_mde_by_cluster_count.csv")
SE_G0 = sim.loc[sim['note'] == 'actual', 'mean_se'].iloc[0]
G0 = int(sim.loc[sim['note'] == 'actual', 'n_adjacent_clusters'].iloc[0])


def se_theory(G):
    return SE_G0 * np.sqrt(G0 / G)


def mde(se, dof=65, power=0.80, alpha=0.05):
    t_alpha = st.t.ppf(1 - alpha / 2, dof)
    t_power = st.norm.ppf(power)
    return (t_alpha + t_power) * se


rows = []
for _, r in sim.iterrows():
    G = r['n_adjacent_clusters']
    se_t = se_theory(G)
    mde_t = mde(se_t)
    rows.append([f"{G:.0f}" + (" (actual)" if r['note'] == 'actual' else ""),
                 f"{se_t:.4f}", f"{mde_t:.3f}", f"{r['mean_se']:.4f}", f"{r['MDE']:.3f}"])

tableB1 = pd.DataFrame(rows, columns=["G (adjacent clusters)", "SE (theory)", "MDE (theory)",
                                        "SE (simulated)", "MDE (simulated)"])
tableB1.to_csv(OUTPUT_DIR / "TableB1_analytical_mde.csv", index=False)

print("Table B1. Theoretical versus simulated MDE by number of adjacent clusters\n")
print(tableB1.to_string(index=False))

target_mde = 0.057
t_alpha = st.t.ppf(0.975, 65)
t_power = st.norm.ppf(0.80)
required_se = target_mde / (t_alpha + t_power)
required_G = G0 * (SE_G0 / required_se) ** 2
print(f"\nTheoretical G required for MDE = direct effect ({target_mde}): {required_G:.1f}")
print("Saved to output/TableB1_analytical_mde.csv")
