"""
run_all.py
==========
Runs the full replication pipeline in order and writes every table (.csv)
reported in the paper to ../output/, and every figure (.png, 600 DPI) to
../figures/.

Expected runtime: a few minutes on a standard laptop. The slowest steps are
the wild cluster bootstrap (4,999 replications) and the cluster-count MDE
simulation in 03 and 06, each of which completes in under a minute.

Run individual numbered scripts directly to regenerate only one table or
figure (each script can be run independently, though 04 and 09 depend on
outputs saved by 03 and 08 respectively, and 13 depends on 06).
"""
import importlib.util
import os
import time

HERE = os.path.dirname(__file__)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    t0 = time.time()

    print("=== 01: Table 1 -- Adjacency classification of the ten reintegrated districts ===")
    _load("01_table1_adjacency_classification")

    print("\n=== 02: Table 2 -- Replication of efficiency estimates ===")
    _load("02_table2_replication_efficiency")

    print("\n=== 03: Table 3 -- Direct and spillover effects under alternative inference ===")
    _load("03_table3_spillover_inference")

    print("\n=== 04: Figure 1 -- Randomization inference distribution ===")
    _load("04_figure1_randomization_inference")

    print("\n=== 05: Figure 2 -- TOST equivalence test ===")
    _load("05_figure2_tost_equivalence")

    print("\n=== 06: Table 4 -- Minimum detectable effect by cluster count ===")
    _load("06_table4_mde_by_cluster_count")

    print("\n=== 07: Figure 3 -- Simulated MDE vs. number of adjacent clusters ===")
    _load("07_figure3_mde_simulation")

    print("\n=== 08: Table 5 -- Leave-one-out robustness ===")
    _load("08_table5_leave_one_out")

    print("\n=== 09: Figure 4 -- Leave-one-out forest plot ===")
    _load("09_figure4_leave_one_out")

    print("\n=== 10: Table 6 -- Diagnostic evidence summary ===")
    _load("10_table6_diagnostic_evidence")

    print("\n=== 11: Appendix -- SFA-based robustness check ===")
    _load("11_appendix_sfa_robustness")

    print("\n=== 12: Table 7 -- Literature comparison ===")
    _load("12_table7_literature_comparison")

    print("\n=== 13: Table B1 -- Analytical vs. simulated MDE (Appendix B) ===")
    _load("13_tableB1_analytical_mde")

    print(f"\nAll done in {time.time() - t0:.0f} seconds.")
    print("See ../output/ for all tables (.csv) and ../figures/ for all figures (600 DPI, .png).")
