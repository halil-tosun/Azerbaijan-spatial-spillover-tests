"""
Table 4. Minimum detectable effect (MDE) under alternative numbers of
adjacent clusters.

Computes the minimum detectable effect (80% power, two-sided alpha=0.05) for
the current design (7 adjacent clusters), and simulates how the MDE would
change with a larger pool of adjacent clusters by drawing random placebo
"adjacent" sets from the non-treated district pool.

Produces: output/Table4_mde_by_cluster_count.csv
"""
import numpy as np
import pandas as pd
from scipy import stats as st
from _paths import DATA_DIR, OUTPUT_DIR, TREATED, ADJACENT_1ST_ORDER
from _estimation import build_panel, twfe_cluster_robust

df = build_panel('vrs_bc', DATA_DIR / "table3_dea_bootstrap_full.csv")


def mde(se, dof, power=0.80, alpha=0.05):
    t_alpha = st.t.ppf(1 - alpha / 2, dof)
    t_power = st.norm.ppf(power)
    return (t_alpha + t_power) * se


def se_for_adjacent_set(adjacent_set):
    d = df.copy()
    d['adjacent_post_tmp'] = d['region'].isin(adjacent_set).astype(int) * d['post']
    fit = twfe_cluster_robust(d, 'vrs_bc', ['treated_post', 'adjacent_post_tmp'])
    return fit['se'][2], fit['n_clusters']


rng = np.random.default_rng(42)
control_pool = [r for r in df['region'].unique() if r not in TREATED]
cluster_counts = [7, 10, 15, 20, 25, 30]
n_sim = 30

results = []
for cc in cluster_counts:
    if cc == 7:
        se, nc = se_for_adjacent_set(ADJACENT_1ST_ORDER)
        results.append({'n_adjacent_clusters': cc, 'mean_se': se, 'MDE': mde(se, nc - 1), 'note': 'actual'})
        continue
    ses = []
    for _ in range(n_sim):
        sampled = rng.choice(control_pool, size=min(cc, len(control_pool)), replace=False)
        se, nc = se_for_adjacent_set(list(sampled))
        ses.append(se)
    mean_se = np.mean(ses)
    results.append({'n_adjacent_clusters': cc, 'mean_se': mean_se, 'MDE': mde(mean_se, 65),
                     'note': f'simulated (avg of {n_sim})'})

table4 = pd.DataFrame(results)
table4.to_csv(OUTPUT_DIR / "Table4_mde_by_cluster_count.csv", index=False)

print("Table 4. Minimum detectable effect (MDE) under alternative numbers of adjacent clusters\n")
print(table4.to_string(index=False))
print(f"\nRatio of current-design MDE to direct effect (0.057): {table4['MDE'].iloc[0]/0.057:.2f}x")
print("Saved to output/Table4_mde_by_cluster_count.csv")
