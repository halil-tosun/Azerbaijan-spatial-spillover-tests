"""
Figure 3. Simulated minimum detectable effect (MDE) as a function of the
number of adjacent districts.

Plots the MDE values computed in 06_table4_mde_by_cluster_count.py against
the number of adjacent clusters, marking the actual design (7 clusters) and
the direct treatment effect benchmark.

Produces: figures/Figure3_mde_simulation.png (600 DPI)
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from _paths import OUTPUT_DIR, FIG_DIR, FIGURE_DPI

df = pd.read_csv(OUTPUT_DIR / "Table4_mde_by_cluster_count.csv")
stable = df[df['n_adjacent_clusters'] <= 50]

fig, ax = plt.subplots(figsize=(7, 5), dpi=FIGURE_DPI)
ax.plot(stable['n_adjacent_clusters'], stable['MDE'], marker='o', color='#1f4e79',
        linewidth=2, markersize=6, label='Simulated MDE')
ax.axhline(0.057, color='#c0392b', linestyle='--', linewidth=1.5, label='Direct treatment effect (0.057)')
actual = df[df['note'] == 'actual'].iloc[0]
ax.scatter([actual['n_adjacent_clusters']], [actual['MDE']], color='#c0392b', s=80, zorder=5,
           label='Actual design (7 adjacent clusters)')
ax.set_xlabel('Number of "adjacent" clusters', fontsize=11)
ax.set_ylabel('Minimum Detectable Effect (MDE)', fontsize=11)
ax.set_title('Statistical Power for Detecting Spillover Effects\nas a Function of Adjacent-Cluster Count', fontsize=12)
ax.legend(fontsize=9, loc='upper right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure3_mde_simulation.png", dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
print("Figure 3 saved to figures/Figure3_mde_simulation.png (600 DPI)")
