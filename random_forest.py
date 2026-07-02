import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# load datasets

train = pd.read_csv("HMP2_Train_Log.csv")
test = pd.read_csv("HMP2_Test_Log.csv")

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

# features and labels

feature_cols = [
    c for c in train.columns
    if c not in metadata_cols
]

X_train = train[feature_cols]
y_train = train["diagnosis"]

X_test = test[feature_cols]
y_test = test["diagnosis"]

# build random forest model

rf = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)

# train model

rf.fit(X_train, y_train)

# predictions

y_pred = rf.predict(X_test)

# evaluation

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix\n")
print(confusion_matrix(y_test, y_pred))

# feature importance

importance = pd.DataFrame({
    "Genus": feature_cols,
    "Importance": rf.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 20 Important Genera\n")
print(importance.head(20))

importance.to_csv(
    "RandomForest_FeatureImportance.csv",
    index=False
)
print(X_train.shape)
print(X_test.shape)
print(feature_cols[:10])
print((X_train == 0).sum().sum() / X_train.size)

print(train["diagnosis"].value_counts(normalize=True))

print()

print(test["diagnosis"].value_counts(normalize=True))
