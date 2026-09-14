

pip install openpyxl

#importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#reading the dataset
gdsc = pd.read_excel('https://github.com/HackBio-Internship/public_datasets/raw/refs/heads/main/GDSC.xlsx')


#check the data
gdsc.head()

gdsc.shape

gdsc.info()

for col in gdsc.columns:
    if gdsc[col].dtype == "object":
        print(col, ":", gdsc[col].nunique())

y = gdsc["LN_IC50"]

# dropped the columns not relevant
X = gdsc.drop(
    columns=[
        "LN_IC50",
        "AUC",
        "Z_SCORE",
        "COSMIC_ID",
    "DRUG_ID"
    ]
)

print(X.shape)


# Convert all categorical predictor variables into numerical format using one-hot encoding.
# After this transformation, all features are numeric and suitable for model training.

X = pd.get_dummies(
    X,
    drop_first=True
)

X.shape

# split data: train , test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

X_train.info()

from xgboost import XGBRegressor

# Train an Extreme Gradient Boosting (XGBoost) regression model to predict IC50.

# n_estimators=100:
# Builds 100 decision trees. A larger number of trees can improve performance
# but increases training time and the risk of overfitting.

# max_depth=6:
# Limits each tree to a maximum depth of 6 levels. This controls model complexity
# and helps prevent overfitting while still capturing non-linear relationships.

# learning_rate=0.1:
# Controls how much each new tree contributes to the final prediction.
# Smaller values make learning more gradual 

# tree_method="hist":
# Uses histogram-based tree construction, which is faster and more memory-efficient
# for large datasets compared to the exact tree-building algorithm.


xgb = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    tree_method="hist",
    random_state=42,
    n_jobs=-1
)


xgb.fit(X_train, y_train)


# Use the trained model to predict IC50 for test data.
y_pred = xgb.predict(X_test)



# Evaluate model performance on the test set using:
# R²: proportion of variation in IC50 explained by the model
# MAE: average prediction error
# RMSE: prediction error with larger mistakes penalized more heavily

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

r2 = r2_score(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

print("R²:", r2)
print("MAE:", mae)
print("RMSE:", rmse)


# Compare training and test R² scores to assess overfitting.

train_pred = xgb.predict(X_train)

train_r2 = r2_score(
    y_train,
    train_pred
)

print("Train R²:", train_r2)
print("Test R²:", r2)

# Extract feature importance scores from the trained XGBoost model.
# Features with higher importance contribute more to predicting IC50.

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": xgb.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print(importance.head(20))

# Visualize the top 20 important features

import matplotlib.pyplot as plt

top20 = importance.head(20)

plt.figure(figsize=(10,8))
plt.barh(
    top20["Feature"],
    top20["Importance"]
)
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 20 XGBoost Features")
plt.tight_layout()
plt.show()


# Assess model stability and generalization using 5-fold cross-validation.
# Report the R² score for each fold and the average R² across all folds.
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    xgb,
    X_train,
    y_train,
    cv=5,
    scoring="r2"
)

print("CV R² scores:", cv_scores)
print("Mean CV R²:", cv_scores.mean())