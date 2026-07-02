import pandas as pd
import scikit_posthocs as sp

# load datasets

df = pd.read_csv("HMP2_Genus_ML_Dataset.csv")
significant = pd.read_csv("Significant_Genera.csv")

# significant genera

genera = significant["Genus"]

results = []

# perform dunn's test

for genus in genera:

    temp = df[["diagnosis", genus]].dropna()

    dunn = sp.posthoc_dunn(
        temp,
        val_col=genus,
        group_col="diagnosis",
        p_adjust="fdr_bh"
    )

    comparisons = [
        ("CD", "UC"),
        ("CD", "nonIBD"),
        ("UC", "nonIBD")
    ]

    for g1, g2 in comparisons:

        group1 = temp[temp["diagnosis"] == g1][genus]
        group2 = temp[temp["diagnosis"] == g2][genus]

        mean1 = group1.mean()
        mean2 = group2.mean()

        median1 = group1.median()
        median2 = group2.median()

        if mean1 > mean2:
            higher = g1
        elif mean2 > mean1:
            higher = g2
        else:
            higher = "Equal"

        results.append([
            genus,
            g1,
            g2,
            mean1,
            mean2,
            median1,
            median2,
            higher,
            dunn.loc[g1, g2]
        ])

# create results table

results = pd.DataFrame(
    results,
    columns=[
        "Genus",
        "Group1",
        "Group2",
        "Mean_Group1",
        "Mean_Group2",
        "Median_Group1",
        "Median_Group2",
        "Higher_in",
        "Adjusted_P_value"
    ]
)

results["Significant"] = results["Adjusted_P_value"] < 0.05

results = results.sort_values("Adjusted_P_value")

print(results.head(30))
significant_results = results[
    results["Significant"] == True
]

significant_results.to_csv(
    "Significant_Dunn_Posthoc.csv",
    index=False
)
results.to_csv(
    "Dunn_Posthoc_Results.csv",
    index=False
)
