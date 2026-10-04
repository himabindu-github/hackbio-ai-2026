
## Predicting Cancer Cell Line Drug Sensitivity Using XGBoost

This project uses an optimized XGBoost Regressor to predict how cancer cell lines respond to different drugs. Using data from the Genomics of Drug Sensitivity in Cancer (GDSC) dataset, the model maps biological, molecular, and chemical features to predict drug sensitivity, measured as LN_IC50 (the natural log of the half-maximal inhibitory concentration).

------------------------------
## What this project does

* The Goal: Predict drug sensitivity (LN_IC50). Lower values mean a cancer cell line is highly sensitive to a drug, while higher values mean increased resistance.
* The Data: Features include multi-omic profiles (gene expression, methylation, copy number alterations), tissue types, and drug action targets across 162,103 observations.
* The Solution: A tuned XGBoost regression model that handles the complex, non-linear relationships between biological features and drug performance.

------------------------------
## The Workflow
### 1. Cleaning & Preventing Data Leakage
To make sure the model evaluated realistically, a few features were removed before training:

* AUC and Z_SCORE were dropped entirely. Because these are alternative metrics calculated directly from the same dose-response experiments as $LN\_IC50$, keeping them would cheat the model and artificially inflate its scores.
* Unique identifiers like COSMIC_ID and DRUG_ID were removed so the model would learn from biological traits rather than specific database tags.

### 2. Feature Processing
Categorical columns (like drug names, target pathways, and cancer classifications) were converted to a numeric format using one-hot encoding. This expanded the dataset to a clean matrix of 1,298 columns.

### 3. Model Training
The data was split into 80% for training (129,682 records) and 20% for testing (32,421 records), keeping a fixed random seed (42) for reproducibility.


------------------------------
## Results
Tuning the model parameters using a 5-fold cross-validation randomized search made a major difference in final accuracy. Below is a direct comparison of the baseline model against the optimized configuration:

| Model Configuration | Validation Strategy | R² Score | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) |
|---|---|---|---|---|
| Baseline XGBoost | 80/20 Random Split | 0.673 | 1.305 | 1.626 |
| Tuned XGBoost | 5-Fold Cross-Validation | 0.783 | — | — |
| Tuned XGBoost | 80/20 Random Split | 0.786 | 1.019 | 1.315 |

The training R² (0.787) and test R² (0.786) for the tuned model are incredibly close, showing that the model does not suffer from high variance or overfitting on the dataset split.


------------------------------
## Important Validation Caveat & Summary

While a test R² of ~0.786 demonstrates strong predictive power on this split, it is important to note a structural limitation in how the model was evaluated. Because the dataset was divided using a standard random train–test split, measurements from the same cell lines or the same drugs appear in both the training and testing sets. This allows the model to learn the specific baseline behavior of a drug or cell line and apply that knowledge to the test set, which inflates performance metrics.
Consequently, these results do not prove that the model can successfully predict how a brand-new, completely unseen drug will perform, or how an untested cell line will behave. To evaluate the model's true generalizability for real-world discovery, future iterations should implement stricter holdout strategies, such as splitting data explicitly by dropping entire drug or cell-line blocks from the training data.


------------------------------
## What the model found important
When looking at which features influenced the predictions the most, a few biological targets and specific drugs stood out:

   1. TARGET_Metabolism & TARGET_anti-oxidant proteins: These biological systems had the highest overall feature importance, meaning a cell line's metabolic and oxidative stress regulations are massive indicators of how it will respond to treatment.
   2. Specific Drugs: Compounds like Dactinomycin, Sepantronium bromide, and Bortezomib were incredibly strong individual predictors. These were also some of the most potent drugs in the dataset during exploratory analysis.
   3. TARGET_PATHWAY_Mitosis: This pathway ranked high, which lines up with the biological reality that drugs targeting cell division/mitosis are widely effective across many diverse cancer types.




