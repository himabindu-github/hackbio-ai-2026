import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("gdsc_multiomics.csv")

# Keep only numeric columns
numeric_cols = df.select_dtypes(include=np.number).columns

# Remove target from features
feature_cols = [c for c in numeric_cols if c != "LN_IC50"]

X = df[feature_cols]
y = df["LN_IC50"]


# -----------------------------
# Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------
# Models
# -----------------------------

models = {
    "Random Forest": RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
}


# -----------------------------
# Train / Evaluate
# -----------------------------

for name, model in models.items():

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    print("\n", "="*50)
    print(name)
    print("="*50)

    print("R2   :", round(r2, 4))
    print("RMSE :", round(rmse, 4))
    print("MAE  :", round(mae, 4))