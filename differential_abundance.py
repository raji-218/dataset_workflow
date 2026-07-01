import pandas as pd
from scipy.stats import kruskal
from statsmodels.stats.multitest import multipletests

df = pd.read_csv("HMP2_Genus_ML_Dataset.csv")

metadata_cols = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num",
    "sex",
    "BMI",
    "Age at diagnosis",
    "is_inflamed",
]

# separate microbiome features
X = df.drop(columns=metadata_cols)

# remove rare genera
threshold = int(0.05 * len(df))
prevalence = (X > 0).sum()
keep = prevalence[prevalence >= threshold].index

results = []

# compare abundance across disease groups
for genus in keep:

    cd = df[df["diagnosis"] == "CD"][genus].dropna()
    uc = df[df["diagnosis"] == "UC"][genus].dropna()
    healthy = df[df["diagnosis"] == "nonIBD"][genus].dropna()

    stat, p = kruskal(cd, uc, healthy)

    results.append(
        [
            genus,
            stat,
            p,
            cd.mean(),
            uc.mean(),
            healthy.mean(),
        ]
    )

results = pd.DataFrame(
    results,
    columns=[
        "Genus",
        "Statistic",
        "P_value",
        "Mean_CD",
        "Mean_UC",
        "Mean_nonIBD",
    ],
)

# correct for multiple testing
results["FDR"] = multipletests(
    results["P_value"],
    method="fdr_bh",
)[1]

results = results.sort_values("FDR")

significant = results[results["FDR"] < 0.05]

print(significant.head(20))

significant.to_csv("Significant_Genera.csv", index=False)
