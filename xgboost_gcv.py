import pandas as pd
import numpy as np

from xgboost import XGBClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.preprocessing import LabelEncoder

# load filtered dataset

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

# features

feature_cols = [
    c for c in df.columns
    if c not in metadata_cols
]

X = df[feature_cols]

# optional log transform

X = np.log1p(X)

# labels

encoder = LabelEncoder()
y = encoder.fit_transform(df["diagnosis"])

groups = df["Participant ID"]

# 5-fold grouped cross validation

gkf = GroupKFold(n_splits=5)

accuracy = []
precision = []
recall = []
f1 = []

feature_importance = np.zeros(len(feature_cols))

fold = 1

for train_idx, test_idx in gkf.split(X, y, groups):

    print(f"\nFold {fold}")

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y[train_idx]
    y_test = y[test_idx]

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=3,

        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,

        subsample=0.8,
        colsample_bytree=0.8,

        random_state=42,

        eval_metric="mlogloss"
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    accuracy.append(
        accuracy_score(y_test, pred)
    )

    precision.append(
        precision_score(
            y_test,
            pred,
            average="weighted"
        )
    )

    recall.append(
        recall_score(
            y_test,
            pred,
            average="weighted"
        )
    )

    f1.append(
        f1_score(
            y_test,
            pred,
            average="weighted"
        )
    )

    feature_importance += model.feature_importances_

    print("Accuracy:", accuracy[-1])

    fold += 1

# average feature importance

feature_importance /= 5

importance = pd.DataFrame({
    "Genus": feature_cols,
    "Importance": feature_importance
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

importance.to_csv(
    "XGBoost_FeatureImportance.csv",
    index=False
)

print("\n==============================")
print("Average Performance")
print("==============================")

print("Accuracy :", np.mean(accuracy))
print("Precision:", np.mean(precision))
print("Recall   :", np.mean(recall))
print("F1 Score :", np.mean(f1))

print("\nStandard Deviation")

print("Accuracy :", np.std(accuracy))
print("F1 Score :", np.std(f1))

print("\nTop 20 Features")

print(importance.head(20))
