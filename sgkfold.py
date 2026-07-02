import pandas as pd
import numpy as np

from xgboost import XGBClassifier

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

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

# feature columns

feature_cols = [
    c for c in df.columns
    if c not in metadata_cols
]

X = df[feature_cols]

# log transform

X = np.log1p(X)

# labels

encoder = LabelEncoder()
y = encoder.fit_transform(df["diagnosis"])

groups = df["Participant ID"]

# stratified grouped cross validation

cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

accuracy = []
precision = []
recall = []
f1 = []

feature_importance = np.zeros(len(feature_cols))

confusion_total = np.zeros((3, 3), dtype=float)

fold = 1

for train_idx, test_idx in cv.split(X, y, groups):

    print("\n==============================")
    print(f"Fold {fold}")
    print("==============================")

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y[train_idx]
    y_test = y[test_idx]

    print("\nTraining distribution")
    print(df.iloc[train_idx]["diagnosis"].value_counts())

    print("\nTesting distribution")
    print(df.iloc[test_idx]["diagnosis"].value_counts())

    model = XGBClassifier(

        objective="multi:softprob",
        num_class=3,

        n_estimators=500,
        learning_rate=0.05,

        max_depth=4,
        min_child_weight=5,

        subsample=0.8,
        colsample_bytree=0.8,

        gamma=1,

        random_state=42,

        eval_metric="mlogloss"
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    pre = precision_score(y_test, pred, average="weighted")
    rec = recall_score(y_test, pred, average="weighted")
    f = f1_score(y_test, pred, average="weighted")

    accuracy.append(acc)
    precision.append(pre)
    recall.append(rec)
    f1.append(f)

    cm = confusion_matrix(y_test, pred)

    confusion_total += cm

    feature_importance += model.feature_importances_

    print("\nAccuracy :", round(acc, 4))
    print("Precision:", round(pre, 4))
    print("Recall   :", round(rec, 4))
    print("F1 Score :", round(f, 4))

    print("\nConfusion Matrix")
    print(cm)

    fold += 1

# average feature importance

feature_importance /= cv.get_n_splits()

importance = pd.DataFrame({

    "Genus": feature_cols,
    "Importance": feature_importance

})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

importance.to_csv(
    "XGBoost_FeatureImportance.csv",
    index=False
)

print("\n======================================")
print("Overall Performance")
print("======================================")

print(f"Accuracy : {np.mean(accuracy):.4f} ± {np.std(accuracy):.4f}")
print(f"Precision: {np.mean(precision):.4f} ± {np.std(precision):.4f}")
print(f"Recall   : {np.mean(recall):.4f} ± {np.std(recall):.4f}")
print(f"F1 Score : {np.mean(f1):.4f} ± {np.std(f1):.4f}")

print("\nAverage Confusion Matrix")

print(np.round(confusion_total / cv.get_n_splits(), 1))

print("\nTop 20 Important Genera")

print(importance.head(20))
