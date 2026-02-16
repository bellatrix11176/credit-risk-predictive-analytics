# Credit Risk Predictive Analytics (Logistic Regression)

This repository contains an end-to-end **credit risk predictive analytics** workflow implemented in **Python** using **logistic regression**. The model is trained on historical loan outcomes and then applied to new applicants to predict whether each applicant is likely to be **Good Risk** or **Bad Risk**, along with probability-based confidence scores.

This project was originally completed in RapidMiner for a Week 4 team assignment, and then reproduced in Python for transparency, reproducibility, and portfolio-quality documentation.

---

## What This Project Does

- Loads a single Excel workbook (`CreditRiskData.xlsx`) with two sheets:
  - **Past Loans** = training data (includes the label `Good Risk`)
  - **Loan Applicants** = scoring data (unlabeled; used for predictions)
- Trains a **logistic regression** model to predict `Good Risk`
- Evaluates predictor strength using **p-values**
- Scores loan applicants with:
  - predicted class (`Yes` / `No`)
  - `confidence(Yes)` and `confidence(No)` probabilities
  - an uncertainty flag based on a confidence threshold
- Generates outputs in both CSV and formatted Excel

---

🌐 **PixelKraze Analytics (Portfolio):** https://pixelkraze.com/?utm_source=github&utm_medium=readme&utm_campaign=portfolio&utm_content=homepage

