import pandas as pd

# load dataset

df = pd.read_csv("HMP2_Genus_ML_Dataset.csv")

# metadata columns

metadata_cols = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num",
    "sex",
    "BMI",
    "Age at diagnosis",
    "is_inflamed"
]

# microbiome features

feature_cols = [
    c for c in df.columns
    if c not in metadata_cols
]

X = df[feature_cols]

# keep genera present in at least 5% of samples

threshold = int(0.05 * len(df))

prevalence = (X > 0).sum()

keep = prevalence[prevalence >= threshold].index

filtered = pd.concat(
    [df[metadata_cols], X[keep]],
    axis=1
)

print("Original features:", len(feature_cols))
print("Filtered features:", len(keep))

filtered.to_csv(
    "HMP2_Genus_Filtered.csv",
    index=False
)
