# Assignment Notes — Week 4 Team Assignment (RapidMiner → Python)

This document maps the Week 4 requirements to the evidence produced in this repository.

---

## Requirement: Import both worksheets into RapidMiner (training vs scoring)

**RapidMiner version:**
- Imported **Past Loans** worksheet (training data)
- Imported **Loan Applicants** worksheet (scoring data)

**Python version (repo):**
- Reads the same workbook:
  - `Past Loans` used as training data
  - `Loan Applicants` used as scoring data

Evidence:
- `data/CreditRiskData.xlsx`
- Console output prints dataset shapes after loading

---

## Requirement: Set roles (ID and Label)

**RapidMiner version:**
- `Applicant ID` role = **id** in both datasets
- `Good Risk` role = **label** in training dataset

**Python version (repo):**
- `Applicant ID` is excluded from predictors and retained for record tracking
- `Good Risk` is normalized (Yes/No → 1/0) and used as `y` (label)

Evidence:
- Script logic uses:
  - `Applicant ID` kept in outputs
  - `Good Risk` used only in training and not in scoring data

---

## Requirement: Logistic Regression + Apply Model workflow

**RapidMiner version:**
- `Logistic Regression` operator trained on Past Loans
- `Apply Model` operator applied to Loan Applicants
- Predictions + confidence shown in Results

**Python version (repo):**
- `statsmodels.Logit` fits logistic regression on Past Loans
- `.predict()` applied to Loan Applicants
- Generates:
  - predicted class
  - probability/confidence for Yes and No

Evidence:
- `outputs/scored_loan_applicants.csv`
- `outputs/scored_loan_applicants.xlsx`

---

## Requirement: Show model properties + identify strongest/weakest predictors by p-value

**RapidMiner version:**
- Model coefficient table includes p-values (significance)

**Python version (repo):**
- Exports coefficient table including p-values:
  - strongest predictors = smallest p-values
  - weakest predictors = largest p-values

Evidence:
- `outputs/logit_coefficients_pvalues.csv`

Interpretation rule used:
- Lower p-value → more statistically reliable predictor contribution
- High p-values (near 1.0) → variable not statistically significant in this dataset/model

---

## Requirement: Show predictions + confidence percentages + counts of good/bad risk + uncertainty examples

**RapidMiner version:**
- Results view includes:
  - prediction
  - confidence(Yes), confidence(No)

**Python version (repo):**
- Outputs include:
  - prediction (`Yes` / `No`)
  - `confidence(Yes)` and `confidence(No)`
  - uncertainty flag based on a threshold (default 0.70 max confidence)

Evidence:
- `outputs/scored_loan_applicants.xlsx` (formatted like RapidMiner)
- `outputs/scored_loan_applicants.csv`

Uncertainty guideline:
- Lower max confidence indicates borderline predictions (close to 50/50)
- In a real lending workflow, these cases may require additional review or data

---

## Notes About Screenshots

The original assignment requested screenshots from RapidMiner (Design view + Results).  
This repository recreates the same workflow in Python and produces equivalent outputs, but RapidMiner screenshots should be included in the course submission document if required.

