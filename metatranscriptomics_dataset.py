import pandas as pd
import numpy as np
from scipy.stats import kruskal
from statsmodels.stats.multitest import multipletests

# load dataset
df = pd.read_csv("MTX_ML_Dataset.csv")

# remove unknown if present
if "UniRef90_unknown" in df.columns:
    df = df.drop(columns=["UniRef90_unknown"])

# metadata columns
metadata = [
    "Participant ID",
    "visit_num",
    "diagnosis",
    "MET",
    "MGX",
    "MTX",
    "PROT"
]

feature_cols = [c for c in df.columns if c not in metadata]

print("=" * 60)
print("Metatranscriptomics Feature Selection")
print("=" * 60)

print("\nTotal genes:", len(feature_cols))

results = []

for i, gene in enumerate(feature_cols):

    cd = df.loc[df["diagnosis"] == "CD", gene]
    uc = df.loc[df["diagnosis"] == "UC", gene]
    nonibd = df.loc[df["diagnosis"] == "nonIBD", gene]

    try:
        stat, p = kruskal(cd, uc, nonibd)

    except Exception:
        stat = np.nan
        p = np.nan

    results.append([
        gene,
        stat,
        p,
        cd.mean(),
        uc.mean(),
        nonibd.mean()
    ])

    if (i + 1) % 500 == 0:
        print(f"Processed {i+1} / {len(feature_cols)} genes")

results = pd.DataFrame(
    results,
    columns=[
        "Gene",
        "Statistic",
        "P_value",
        "Mean_CD",
        "Mean_UC",
        "Mean_nonIBD"
    ]
)

# remove failed tests
results = results.dropna()

# FDR correction
results["FDR"] = multipletests(
    results["P_value"],
    method="fdr_bh"
)[1]

# sort
results = results.sort_values("FDR")

# significant genes
significant = results[results["FDR"] < 0.05]

print("\n")
print("=" * 60)
print("Feature Selection Results")
print("=" * 60)

print("\nGenes tested:")
print(len(results))

print("\nSignificant genes:")
print(len(significant))

print("\nTop 20 genes")
print(significant.head(20))

results.to_csv(
    "MTX_All_Genes.csv",
    index=False
)

significant.to_csv(
    "MTX_Significant_Genes.csv",
    index=False
)

print("\nSaved:")
print("MTX_All_Genes.csv")
print("MTX_Significant_Genes.csv")
import pandas as pd

df = pd.read_csv("MTX_ML_Dataset.csv")
sig = pd.read_csv("MTX_Significant_Genes.csv")

# keep top 200 genes
sig = sig.sort_values("FDR").head(200)

genes = sig["Gene"].tolist()

metadata = [
    "Participant ID",
    "visit_num",
    "diagnosis",
    "MET",
    "MGX",
    "MTX",
    "PROT"
]

selected = df[metadata + genes]

print("=" * 60)
print("Selected MTX Dataset")
print("=" * 60)

print(selected.shape)

selected.to_csv(
    "MTX_SelectedFeatures.csv",
    index=False
)

print("Saved: MTX_SelectedFeatures.csv")
import pandas as pd

df = pd.read_csv("MTX_SelectedFeatures.csv")

print("="*60)
print("Final MTX Dataset")
print("="*60)

print("\nShape")
print(df.shape)

print("\nDiagnosis")
print(df["diagnosis"].value_counts())

print("\nUnique Participants")
print(df["Participant ID"].nunique())

print("\nUnique Samples")
print(df["MTX"].nunique())
