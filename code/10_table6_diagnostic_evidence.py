"""
Table 6. Diagnostic evidence distinguishing limited statistical power from
model misspecification.

This table summarizes the diagnostic checks reported in Sections 3.4 and 4.2
of the manuscript (each computed by a separate script in this package:
03_table3_spillover_inference.py for the WCR comparison, the second-order
coefficient, and randomization inference; 11_appendix_sfa_robustness.py for
the SFA-based robustness check). It is reproduced here verbatim as a
synthesis table, not as an independent computation.

Produces: output/Table6_diagnostic_evidence.csv
"""
import pandas as pd
from _paths import OUTPUT_DIR

rows = [
    ["Alternative inference for the direct effect (WCR)",
     "Assess whether inference changes under few-cluster methods",
     "WCR p=0.136 versus Tosun's (2026) event-study p=0.0015",
     "Lower precision reflects the simplified pooled specification rather than a failure to replicate the estimates reported by Tosun (2026)"],
    ["Second-order neighbourhood definition",
     "Assess sensitivity to the spatial definition of exposure",
     "Coefficient = +0.011; p=0.81",
     "Similar estimates across neighbourhood definitions provide no evidence that results are driven by the choice of adjacency ring"],
    ["Alternative efficiency measure (SFA)",
     "Assess sensitivity to efficiency measurement",
     "Direct and spillover effects remain statistically imprecise",
     "Consistent qualitative results across efficiency estimators suggest limited identifying information rather than estimator choice"],
    ["Fisher randomization inference",
     "Distribution-free assessment of statistical significance",
     "p=0.502; observed estimate at the 24.7th percentile of the placebo distribution",
     "Independently corroborates the inference obtained from the wild cluster bootstrap"],
]
table6 = pd.DataFrame(rows, columns=["Diagnostic check", "Motivation", "Result", "Interpretation"])
table6.to_csv(OUTPUT_DIR / "Table6_diagnostic_evidence.csv", index=False)

print("Table 6. Diagnostic evidence distinguishing limited statistical power from model misspecification\n")
for _, r in table6.iterrows():
    print(f"- {r['Diagnostic check']}: {r['Result']}")
print("\nSaved to output/Table6_diagnostic_evidence.csv")
print("(Full numerical values are computed independently in 03_table3_spillover_inference.py")
print(" and 11_appendix_sfa_robustness.py; this script reproduces the synthesis only.)")
