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

MIT License

Copyright (c) 2026 Gina Aulabaugh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

🌐 **PixelKraze Analytics (Portfolio):** https://pixelkraze.com/?utm_source=github&utm_medium=readme&utm_campaign=portfolio&utm_content=homepage

