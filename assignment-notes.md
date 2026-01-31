# Assignment Notes — Week 4 Team Assignment (Credit Risk Modeling)

This document maps the Week 4 team assignment requirements to the evidence produced in this repository. The original assignment was completed in RapidMiner, and the same workflow was later reproduced in Python for reproducibility, transparency, and portfolio purposes.

---

## Dataset Overview

The assignment uses a single Excel workbook:

- **CreditRiskData.xlsx**

This workbook contains two worksheets:
- **Past Loans** — historical loan data with a labeled outcome (`Good Risk`)
- **Loan Applicants** — new, unlabeled applicants used for scoring

Both worksheets are used consistently in RapidMiner and Python.

---

## Requirement: Import Both Worksheets (Training vs Scoring)

### RapidMiner
- Imported **Past Loans** worksheet as the training dataset
- Imported **Loan Applicants** worksheet as the scoring dataset

### Python Implementation
- Reads the same Excel file
- Uses:
  - `Past Loans` for model training
  - `Loan Applicants` for prediction and scoring

Evidence:
- `data/CreditRiskData.xlsx`
- Console output confirms dataset shapes after loading

---

## Requirement: Designate Roles (ID and Label)

### RapidMiner
- `Applicant ID` assigned the **ID** role in both datasets
- `Good Risk` assigned the **Label** role in the training dataset

### Python Implementation
- `Applicant ID` excluded from predictors and retained for record identification
- `Good Risk` normalized from Yes/No to 1/0 and used as the dependent variable during training

Evidence:
- Script logic explicitly separates ID, label, and predictors
- Applicant ID preserved in all scored output files

---

## Requirement: Build Logistic Regression Model and Apply Model

### RapidMiner
- Logistic Regression operator trained on Past Loans
- Apply Model operator used to score Loan Applicants
- Both the trained model and predictions displayed in Results view

### Python Implementation
- Logistic regression fitted using `statsmodels.Logit`
- Model trained on Past Loans
- Predictions generated for Loan Applicants using the trained model

Evidence:
- `outputs/scored_loan_applicants.csv`
- `outputs/scored_loan_applicants.xlsx`

---

## Model Results and Interpretation

The logistic regression model was trained using historical loan data from the *Past Loans* dataset, with **Good Risk** as the target variable. The model estimates the probability that a loan applicant will be classified as a good credit risk based on multiple financial and demographic attributes.

Based on the model’s coefficient table and associated p-values, **Debt to Income**, **Number of Missed/Late Payments**, and **Credit Score** emerged as the strongest predictors of credit risk. These variables had the lowest p-values, indicating stronger statistical evidence that they meaningfully contribute to predicting loan outcomes within this dataset. Higher debt-to-income ratios and a greater number of missed or late payments were associated with a lower likelihood of being classified as a good risk, while higher credit scores increased the probability of a favorable classification.

In contrast, **Lines of Credit**, **Marital Status**, and the **Intercept** exhibited very high p-values. This indicates that the model could not reliably distinguish the effects of these variables from random variation in the data. While these attributes were included in the model, their high p-values suggest that they should not be heavily relied upon when interpreting credit risk outcomes for this dataset.

---

## Prediction Results for Loan Applicants

After training, the model was applied to the *Loan Applicants* dataset to generate predictions and confidence scores. Each applicant received a predicted classification (**Yes** or **No** for Good Risk) along with confidence percentages representing the model’s estimated probability for each outcome.

The scoring results showed a larger number of applicants predicted as **No (Bad Risk)** compared to **Yes (Good Risk)**. This outcome aligns with the influence of strong predictors such as debt-to-income ratio and missed payments, which significantly affect the model’s classification decisions.

---

## Confidence and Uncertainty Analysis

In addition to predicted class labels, the model provides confidence values that indicate how strongly the model supports each prediction. Applicants with confidence values closer to **0.50** represent borderline cases where the model is less certain about the classification.

These uncertain predictions suggest that the applicant’s attributes place them near the decision boundary between good and bad risk. In a real-world lending context, such cases would typically require additional review, supplemental data, or alternative evaluation criteria rather than an automatic approval or rejection. Including confidence measures demonstrates how predictive analytics can support decision-making without fully replacing human judgment.

---

## Requirement: Examine Model Properties and Identify Predictors

### RapidMiner
- Examined the logistic regression coefficient table containing:
  - Coefficients
  - Standardized coefficients
  - Z-values
  - **P-values**

### Python Implementation
- Exported a coefficient table including:
  - Scaled and unscaled coefficients
  - P-values for statistical significance

Evidence:
- `outputs/logit_coefficients_pvalues.csv`

Interpretation approach:
- **Lower p-values** indicate stronger statistical evidence for predictor relevance
- **Higher p-values** indicate weaker or unreliable predictors in this dataset

---

## RapidMiner Screenshots Included

The following screenshots are included to document the original RapidMiner execution and satisfy assignment requirements:

### 1. Process / Design View  
**File:** `docs/RapidMiner-Design-View.png`  
Shows:
- Import of training and scoring datasets
- Role assignment for ID and Label
- Logistic Regression operator
- Apply Model operator

---

### 2. Logistic Regression Model Properties  
**File:** `docs/RapidMiner-Logistic-Regression-Model.png`  
Shows:
- Coefficients
- Standardized coefficients
- Z-values
- P-values for each predictor

---

### 3. Prediction Results (Apply Model Statistics)  
**File:** `docs/ExampleSet-Statistics.png`  
Shows:
- Predicted Good Risk values
- Confidence(Yes) and Confidence(No)
- Counts and summary statistics for scored applicants

---

## Relationship Between RapidMiner and Python

The Python implementation in this repository reproduces the same predictive analytics workflow performed in RapidMiner, including:
- Logistic regression model training
- Statistical interpretation using p-values
- Scoring of new loan applicants
- Confidence-based uncertainty analysis

RapidMiner screenshots provide visual confirmation of assignment execution, while the Python code provides a reproducible and transparent implementation of the same process suitable for portfolio use.

