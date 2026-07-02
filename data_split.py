import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

# load dataset

df = pd.read_csv("HMP2_Genus_Filtered.csv")

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

# separate features and labels

feature_cols = [
    c for c in df.columns
    if c not in metadata_cols
]

X = df[feature_cols]
y = df["diagnosis"]
groups = df["Participant ID"]

# participant-aware train/test split

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups)
)

train = df.iloc[train_idx].copy()
test = df.iloc[test_idx].copy()

# save datasets

train.to_csv(
    "HMP2_Train.csv",
    index=False
)

test.to_csv(
    "HMP2_Test.csv",
    index=False
)

# summary

print("Training samples:", len(train))
print("Testing samples:", len(test))

print()

print("Training participants:",
      train["Participant ID"].nunique())

print("Testing participants:",
      test["Participant ID"].nunique())

print()

overlap = set(train["Participant ID"]).intersection(
    set(test["Participant ID"])
)

print("Participants in both sets:", len(overlap))

print()

print("Training diagnosis distribution")
print(train["diagnosis"].value_counts())

print()

print("Testing diagnosis distribution")
print(test["diagnosis"].value_counts())
