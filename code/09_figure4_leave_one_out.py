"""
Figure 4. Leave-one-out robustness check: estimated spillover coefficient
and 95% confidence interval when each adjacent district is excluded in turn.

Requires 08_table5_leave_one_out.py to have been run first.

Produces: figures/Figure4_leave_one_out.png (600 DPI)
"""
import numpy as np
import pandas as pd
from scipy import stats as st
from _paths import DATA_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI, ADJACENT_1ST_ORDER
from _estimation import build_panel, twfe_cluster_robust
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = build_panel('vrs_bc', DATA_DIR / "table3_dea_bootstrap_full.csv")


def run(adjacent_set):
    d = df.copy()
    d['adjacent_post_tmp'] = d['region'].isin(adjacent_set).astype(int) * d['post']
    fit = twfe_cluster_robust(d, 'vrs_bc', ['treated_post', 'adjacent_post_tmp'])
    return fit['beta'][2], fit['se'][2], fit['n_clusters'] - 1


data = [("Baseline (all 7)", *run(ADJACENT_1ST_ORDER))]
for excl in ADJACENT_1ST_ORDER:
    subset = [d for d in ADJACENT_1ST_ORDER if d != excl]
    label = "Excl. " + excl.replace(" district", "")
    data.append((label, *run(subset)))

fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=FIGURE_DPI)
y_pos = np.arange(len(data))[::-1]

for y, (label, coef, se, dof) in zip(y_pos, data):
    tcrit = st.t.ppf(0.975, dof)
    ci_low, ci_high = coef - tcrit * se, coef + tcrit * se
    color = '#1f4e79' if label.startswith('Baseline') else '#5b8ec4'
    ax.plot([ci_low, ci_high], [y, y], color=color, linewidth=2, zorder=2)
    ax.plot(coef, y, 'o', color=color, markersize=7, zorder=3)

ax.axvline(0, color='gray', linewidth=1, linestyle='-', zorder=1)
ax.axvline(0.0566, color='#c0392b', linewidth=1.3, linestyle='--', zorder=1, label='Direct treatment effect (0.057)')

ax.set_yticks(y_pos)
ax.set_yticklabels([d[0] for d in data], fontsize=9)
ax.set_xlabel('Adjacent \u00d7 Post coefficient (95% CI)', fontsize=10)
ax.set_title('Leave-One-Out Robustness: Spillover Estimate\nExcluding Each Adjacent District in Turn', fontsize=11)
ax.legend(loc='lower right', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure4_leave_one_out.png", dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
print("Figure 4 saved to figures/Figure4_leave_one_out.png (600 DPI)")
