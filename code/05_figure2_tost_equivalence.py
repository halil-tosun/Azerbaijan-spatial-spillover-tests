"""
Figure 2. TOST equivalence test: the spillover estimate's 90% confidence
interval against two pre-specified equivalence margins.

Computes a two one-sided tests (TOST) procedure for the first-order
spillover coefficient at two equivalence margins (the full replicated direct
effect, and half the direct effect), and plots the estimate's 90%
confidence interval (the interval relevant for TOST at the 5% level on each
side) against both margins.

Produces: figures/Figure2_tost_equivalence.png (600 DPI)
"""
import numpy as np
from scipy import stats as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from _paths import DATA_DIR, FIG_DIR, FIGURE_DPI
from _estimation import build_panel, twfe_cluster_robust

df = build_panel('vrs_bc', DATA_DIR / "table3_dea_bootstrap_full.csv")
fit = twfe_cluster_robust(df, 'vrs_bc', ['treated_post', 'adj1_post'])
est, se, dof = fit['beta'][2], fit['se'][2], fit['n_clusters'] - 1

direct_effect = 0.0566


def tost(estimate, se, dof, delta):
    t_lower = (estimate - (-delta)) / se
    t_upper = (estimate - delta) / se
    p_lower = 1 - st.t.cdf(t_lower, dof)
    p_upper = st.t.cdf(t_upper, dof)
    return max(p_lower, p_upper)


for delta, label in [(direct_effect, "full direct effect"), (direct_effect / 2, "half direct effect")]:
    p = tost(est, se, dof, delta)
    print(f"TOST at Delta={delta:.4f} ({label}): p={p:.4f}")

t_90 = st.t.ppf(0.95, dof)
ci90 = (est - t_90 * se, est + t_90 * se)
print(f"\n90% CI (TOST-relevant): [{ci90[0]:.4f}, {ci90[1]:.4f}]")

fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=FIGURE_DPI)
deltas = [direct_effect, direct_effect / 2]
labels = ['\u0394 = direct effect\n(0.057)', '\u0394 = half direct effect\n(0.028)']
y_positions = [2, 1]

for y, delta, lab in zip(y_positions, deltas, labels):
    ax.axvspan(-delta, delta, ymin=(y - 0.35) / 3, ymax=(y + 0.35) / 3, color='#d4e6d4', alpha=0.6, zorder=1)
    ax.plot([-delta, -delta], [y - 0.35, y + 0.35], color='#2e7d32', linestyle='--', linewidth=1.3)
    ax.plot([delta, delta], [y - 0.35, y + 0.35], color='#2e7d32', linestyle='--', linewidth=1.3)
    ax.text(delta + 0.008, y + 0.32, lab, fontsize=8, va='top', color='#2e7d32')

for y in y_positions:
    ax.plot([ci90[0], ci90[1]], [y, y], color='#c0392b', linewidth=2.5, zorder=3)
    ax.plot(est, y, 'o', color='#c0392b', markersize=7, zorder=4)

ax.axvline(0, color='gray', linewidth=0.8, zorder=0)
ax.set_yticks(y_positions)
ax.set_yticklabels(['Equivalence margin 1', 'Equivalence margin 2'])
ax.set_xlabel('Adjacent \u00d7 Post coefficient', fontsize=10)
ax.set_title('TOST Equivalence Test: Spillover Estimate vs.\nPre-Specified Equivalence Margins', fontsize=11)
ax.set_xlim(-0.2, 0.2)
ax.set_ylim(0.5, 2.6)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#c0392b', marker='o', linewidth=2.5, label='Point estimate, 90% CI'),
    Line2D([0], [0], color='#2e7d32', linestyle='--', label='Equivalence bound (\u00b1\u0394)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure2_tost_equivalence.png", dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
print("\nFigure 2 saved to figures/Figure2_tost_equivalence.png (600 DPI)")
