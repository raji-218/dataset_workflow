import pandas as pd

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

print("dataset shape:", df.shape)
print("unique participants:", df["Participant ID"].nunique())
print("unique samples:", df["SampleID"].nunique())

print("\ndiagnosis counts")
print(df["diagnosis"].value_counts())

print("\nsex distribution")
print(df["sex"].value_counts(dropna=False))

print("\nmissing values")
print(df.isna().sum().sort_values(ascending=False).head(10))

print("\nvisits per participant")
print(df.groupby("Participant ID").size().describe())

# calculate sparsity
zeros = (X == 0).sum().sum()
print("\npercent zeros:", zeros / X.size * 100)

# mean abundance
mean_abundance = X.mean().sort_values(ascending=False)
print("\nmost abundant genera")
print(mean_abundance.head(20))

# prevalence across samples
prevalence = (X > 0).sum().sort_values(ascending=False)
print("\nmost prevalent genera")
print(prevalence.head(20))

# remove rare genera
threshold = int(0.05 * len(df))
keep = prevalence[prevalence >= threshold].index
X_filtered = X[keep]

print("\nfiltered feature matrix:", X_filtered.shape)

# compare disease groups
means = df.groupby("diagnosis")[list(keep)].mean()

difference = (means.max() - means.min()).sort_values(ascending=False)

print("\nlargest abundance differences")
print(difference.head(20))

print("\nfaecalibacterium summary")
print(df.groupby("diagnosis")["Faecalibacterium"].describe())
