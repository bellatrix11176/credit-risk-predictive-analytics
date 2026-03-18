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

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

Copyright (c) 2026 Gina Aulabaugh / PixelKraze, LLC

You are free to:
  Share — copy and redistribute the material in any medium or format
  Adapt — remix, transform, and build upon the material

Under the following terms:
  Attribution — You must give appropriate credit to Gina Aulabaugh / PixelKraze, LLC,
  provide a link to the license, and indicate if changes were made.

  NonCommercial — You may not use the material for commercial purposes without
  explicit written permission from the copyright holder.

No additional restrictions — You may not apply legal terms or technological measures
that legally restrict others from doing anything the license permits.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/

🌐 **PixelKraze Analytics (Portfolio):** https://pixelkraze.com/?utm_source=github&utm_medium=readme&utm_campaign=portfolio&utm_content=homepage

