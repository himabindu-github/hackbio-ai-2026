import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("gdsc_multiomics.csv")


# -----------------------------
# Create labels
# -----------------------------

q25 = df["LN_IC50"].quantile(0.25)
q75 = df["LN_IC50"].quantile(0.75)

sensitive = df[df["LN_IC50"] <= q25].copy()
resistant = df[df["LN_IC50"] >= q75].copy()

sensitive["Response"] = 0
resistant["Response"] = 1

df_cls = pd.concat(
    [sensitive, resistant],
    ignore_index=True
)

print(df_cls["Response"].value_counts())


# -----------------------------
# Features
# -----------------------------

numeric_cols = df_cls.select_dtypes(
    include=np.number
).columns

feature_cols = [
    c for c in numeric_cols
    if c not in ["LN_IC50", "Response"]
]

X = df_cls[feature_cols]
y = df_cls["Response"]


# -----------------------------
# Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------
# Models
# -----------------------------

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        eval_metric="logloss"
    )
}


# -----------------------------
# Train / Evaluate
# -----------------------------

for name, model in models.items():

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)

    prec = precision_score(y_test, y_pred)

    rec = recall_score(y_test, y_pred)

    f1 = f1_score(y_test, y_pred)

    auc = roc_auc_score(y_test, y_prob)

    print("\n", "="*50)
    print(name)
    print("="*50)

    print("Accuracy :", round(acc, 4))
    print("Precision:", round(prec, 4))
    print("Recall   :", round(rec, 4))
    print("F1       :", round(f1, 4))
    print("ROC-AUC  :", round(auc, 4))