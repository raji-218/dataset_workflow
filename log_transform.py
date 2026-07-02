import pandas as pd
import numpy as np

# load datasets

train = pd.read_csv("HMP2_Train.csv")
test = pd.read_csv("HMP2_Test.csv")

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

# feature columns

feature_cols = [
    c for c in train.columns
    if c not in metadata_cols
]

# apply log transformation

train[feature_cols] = np.log1p(train[feature_cols])

test[feature_cols] = np.log1p(test[feature_cols])

# save transformed datasets

train.to_csv(
    "HMP2_Train_Log.csv",
    index=False
)

test.to_csv(
    "HMP2_Test_Log.csv",
    index=False
)

print("Log transformation complete.")

print()

print("Training shape:", train.shape)
print("Testing shape:", test.shape)
