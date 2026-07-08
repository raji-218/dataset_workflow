import pandas as pd
import numpy as np

df = pd.read_csv("MTX_155_Unstratified.tsv", sep="\t")

print("="*60)
print("Metatranscriptomics QC")
print("="*60)

print("\nShape")
print(df.shape)

# numeric data
numeric = df.iloc[:,1:]

print("\nPercent zeros")
zeros = (numeric == 0).sum().sum()
total = numeric.size
print(round(zeros/total*100,2))

# prevalence
prevalence = (numeric > 0).sum(axis=1)

print("\nPrevalence")
print(prevalence.describe())

print("\nGenes present in")

print(">=1 sample :", (prevalence >= 1).sum())
print(">=5 samples:", (prevalence >= 5).sum())
print(">=10 samples:", (prevalence >= 10).sum())
print(">=15 samples:", (prevalence >= 15).sum())
print(">=20 samples:", (prevalence >= 20).sum())
print(">=30 samples:", (prevalence >= 30).sum())
print(">=50 samples:", (prevalence >= 50).sum())

# variance
variance = numeric.var(axis=1)

print("\nVariance")
print(variance.describe())

import pandas as pd

df = pd.read_csv("MTX_155_Unstratified.tsv", sep="\t")

numeric = df.iloc[:,1:]

prevalence = (numeric > 0).sum(axis=1)

df = df[prevalence >= 20]

print("="*60)
print("After prevalence filtering")
print("="*60)
print(df.shape)

df.to_csv(
    "MTX_PrevalenceFiltered.tsv",
    sep="\t",
    index=False
)

print("Saved MTX_PrevalenceFiltered.tsv")

import pandas as pd

df = pd.read_csv("MTX_PrevalenceFiltered.tsv", sep="\t")

numeric = df.iloc[:,1:]

variance = numeric.var(axis=1)

df["Variance"] = variance

df = (
    df
    .sort_values("Variance", ascending=False)
    .head(10000)
)

df = df.drop(columns="Variance")

print("="*60)
print("After variance filtering")
print("="*60)
print(df.shape)

df.to_csv(
    "MTX_Top10000.tsv",
    sep="\t",
    index=False
)

print("Saved MTX_Top10000.tsv")

import pandas as pd

df = pd.read_csv("MTX_Top10000.tsv", sep="\t")

df = df.set_index("# Gene Family")

df = df.T

df.index.name = "SampleID"

df.reset_index(inplace=True)

print("="*60)
print("Transposed MTX Dataset")
print("="*60)
print(df.shape)

df.to_csv(
    "MTX_Transposed.csv",
    index=False
)

print("Saved: MTX_Transposed.csv")

import pandas as pd

mtx = pd.read_csv("MTX_Transposed.csv")

matched = pd.read_csv("Matched_Sample_IDs.csv")

print(mtx.shape)
print(matched.shape)
print(mtx.columns[:5])
mtx["SampleID"] = (
    mtx["SampleID"]
    .str.replace("_Abundance-RPKs","",regex=False)
)
merged = matched.merge(
    mtx,
    left_on="MTX",
    right_on="SampleID",
    how="inner"
)
merged = merged.drop(columns="SampleID")
print("="*60)
print("Merged Metatranscriptomics Dataset")
print("="*60)

print("\nShape")
print(merged.shape)

print("\nDiagnosis counts")
print(merged["diagnosis"].value_counts())

print("\nUnique participants")
print(merged["Participant ID"].nunique())

print("\nUnique samples")
print(len(merged))

print("\nMissing values")
print(
    merged.isna().sum().head(10)
)

print("MTX samples before merge:", len(mtx))
print("Matched MTX IDs:", matched["MTX"].nunique())

common = set(mtx["SampleID"]) & set(matched["MTX"])
print("Common samples:", len(common))
remove = [c for c in merged.columns if "unknown" in c.lower()]

print(remove)

merged = merged.drop(columns=remove)

print(merged.shape)

import numpy as np

feature_cols = merged.columns[7:]

variance = merged[feature_cols].var()

print("Zero variance genes:", (variance == 0).sum())

print(mtx["SampleID"].head())

if "UniRef90_unknown" in merged.columns:
    merged = merged.drop(columns=["UniRef90_unknown"])

print(merged.shape)

merged.to_csv(
    "MTX_ML_Dataset.csv",
    index=False
)

print("Saved: MTX_ML_Dataset.csv")
