"""
Figure 1. Randomization inference for the spillover effect.

Plots the distribution of placebo "Adjacent x Post" coefficients obtained
from 2,000 random reassignments of the adjacency indicator among untreated
districts (holding the treated districts fixed), together with the observed
estimate. Requires 03_table3_spillover_inference.py to have been run first
(it saves the placebo distribution used here).

Produces: figures/Figure1_randomization_inference.png (600 DPI)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from _paths import OUTPUT_DIR, FIG_DIR, FIGURE_DPI

placebo = np.load(OUTPUT_DIR / "_ri_placebo_distribution.npy")
observed = np.load(OUTPUT_DIR / "_ri_observed.npy")[0]

fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=FIGURE_DPI)
ax.hist(placebo, bins=40, color='#a8c4e0', edgecolor='white', alpha=0.9,
        label='Placebo distribution\n(2,000 random 7-district assignments)')
ax.axvline(observed, color='#c0392b', linewidth=2.5, label=f'Observed estimate ({observed:.3f})')
ax.axvline(0, color='gray', linewidth=1, linestyle=':')
ax.set_xlabel('Estimated "Adjacent \u00d7 Post" coefficient', fontsize=11)
ax.set_ylabel('Frequency', fontsize=11)
ax.set_title('Randomization Inference: Observed Spillover Estimate\nvs. Placebo Distribution', fontsize=12)
ax.legend(fontsize=9, loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure1_randomization_inference.png", dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
print("Figure 1 saved to figures/Figure1_randomization_inference.png (600 DPI)")
