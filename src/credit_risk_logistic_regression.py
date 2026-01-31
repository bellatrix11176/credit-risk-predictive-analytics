"""
Credit Risk Logistic Regression — stable fit + RapidMiner-comparable coefficients
PLUS RapidMiner-style Excel output for scored applicants

Repo-friendly version:
- No hard-coded personal filepaths.
- Reads:  data/CreditRiskData.xlsx
- Writes: output/...

Outputs:
1) output/scored_loan_applicants.csv
2) output/logit_coefficients_pvalues.csv
3) output/scored_loan_applicants.xlsx  (RapidMiner-style formatted)
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Excel formatting (RapidMiner-like)
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import FormulaRule


# =========================
# REPO PATHS / SETTINGS
# =========================
# This script is in: repo_root/src/credit_risk_logistic_regression.py
# So repo_root = parent of src/
REPO_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
OUT_DIR = REPO_ROOT / "output"   # matches your folder name: output/

EXCEL_FILE = DATA_DIR / "CreditRiskData.xlsx"  # MUST match your file name exactly

SHEET_TRAIN = "Past Loans"
SHEET_SCORE = "Loan Applicants"

ID_COL = "Applicant ID"
LABEL_COL = "Good Risk"

UNCERTAIN_THRESHOLD = 0.70  # max confidence below this = "uncertain"


def normalize_label(series: pd.Series) -> pd.Series:
    """Convert Yes/No labels to 1/0."""
    s = series.astype(str).str.strip().str.lower()
    mapped = s.map({
        "yes": 1, "no": 0,
        "y": 1, "n": 0,
        "true": 1, "false": 0,
        "1": 1, "0": 0
    })
    if mapped.isna().any():
        mapped = pd.to_numeric(series, errors="coerce")
    return mapped


def to_numeric_df(df: pd.DataFrame) -> pd.DataFrame:
    """Force all columns to numeric; non-numeric becomes NaN."""
    return df.apply(pd.to_numeric, errors="coerce")


def median_impute(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NaNs with column medians."""
    med = df.median(numeric_only=True)
    return df.fillna(med)


def standardize_train(df: pd.DataFrame):
    """Standardize columns using training mean/std."""
    mean = df.mean(axis=0)
    std = df.std(axis=0).replace(0, 1)
    scaled = (df - mean) / std
    return scaled, mean, std


def standardize_apply(df: pd.DataFrame, mean: pd.Series, std: pd.Series) -> pd.DataFrame:
    """Apply training mean/std to standardize scoring data."""
    return (df - mean) / std


def save_scored_excel_rapidminer_style(scored_full: pd.DataFrame, out_xlsx: Path):
    """Save a RapidMiner-like Results table with styling."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Scored Loan Applicants"

    # Write dataframe
    for r in dataframe_to_rows(scored_full, index=False, header=True):
        ws.append(r)

    # Header styling
    header_fill = PatternFill("solid", fgColor="D9E1F2")
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.fill = header_fill

    # Freeze and filter
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Table styling
    table = Table(displayName="ScoredApplicants", ref=ws.dimensions)
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    table.tableStyleInfo = style
    ws.add_table(table)

    # Column widths (quick auto-fit)
    for col_idx, col_name in enumerate(scored_full.columns, start=1):
        max_len = len(str(col_name))
        for val in scored_full[col_name].head(100).astype(str).values:
            max_len = max(max_len, len(val))
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max(10, max_len + 2), 30)

    # Conditional formatting for prediction column
    pred_name = "prediction(Good Risk)"
    if pred_name in scored_full.columns:
        pred_col_letter = get_column_letter(scored_full.columns.get_loc(pred_name) + 1)
        green_fill = PatternFill("solid", fgColor="C6EFCE")
        red_fill = PatternFill("solid", fgColor="FFC7CE")

        yes_rule = FormulaRule(formula=[f'${pred_col_letter}2="Yes"'], fill=green_fill)
        no_rule = FormulaRule(formula=[f'${pred_col_letter}2="No"'], fill=red_fill)

        ws.conditional_formatting.add(f"{pred_col_letter}2:{pred_col_letter}{len(scored_full)+1}", yes_rule)
        ws.conditional_formatting.add(f"{pred_col_letter}2:{pred_col_letter}{len(scored_full)+1}", no_rule)

    # Optional highlight: uncertain_flag True
    if "uncertain_flag" in scored_full.columns:
        unc_col_letter = get_column_letter(scored_full.columns.get_loc("uncertain_flag") + 1)
        yellow_fill = PatternFill("solid", fgColor="FFEB9C")
        unc_rule = FormulaRule(formula=[f'${unc_col_letter}2=TRUE'], fill=yellow_fill)
        ws.conditional_formatting.add(f"{unc_col_letter}2:{unc_col_letter}{len(scored_full)+1}", unc_rule)

    wb.save(out_xlsx)


def main():
    # Ensure output directory exists
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Excel file not found:\n{EXCEL_FILE}\n\n"
            f"Expected repo structure:\n"
            f"- data/CreditRiskData.xlsx\n"
            f"- src/credit_risk_logistic_regression.py"
        )

    # Load data
    past = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_TRAIN)
    apps = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_SCORE)

    print("Loaded:")
    print(" Past Loans:", past.shape)
    print(" Loan Applicants:", apps.shape)
    print()

    # Training prep
    y = normalize_label(past[LABEL_COL])
    if y.isna().any():
        bad_rows = y[y.isna()].index[:10].tolist()
        raise ValueError(f"Label conversion failed (NaNs) at rows: {bad_rows}")

    X = past.drop(columns=[ID_COL, LABEL_COL])
    X = median_impute(to_numeric_df(X))

    # Standardize for numerical stability (prevents exp overflow)
    X_scaled, x_mean, x_std = standardize_train(X)
    Xs_const = sm.add_constant(X_scaled, has_constant="add")

    # Fit
    logit = sm.Logit(y, Xs_const)
    result = logit.fit(disp=False, method="lbfgs", maxiter=2000)

    if not result.mle_retvals.get("converged", True):
        print("⚠️ Model did not fully converge (still usable, but interpret p-values cautiously).")
    print("✅ Model fit complete.\n")

    # Unscale coefficients for RapidMiner comparison
    params = result.params.copy()
    b0_scaled = params["const"]
    b_scaled = params.drop("const")

    b_unscaled = b_scaled / x_std
    b0_unscaled = b0_scaled - np.sum(b_scaled * (x_mean / x_std))

    table = pd.DataFrame({
        "Attribute": ["Intercept"] + list(b_scaled.index),
        "Coefficient_unscaled": [b0_unscaled] + list(b_unscaled.values),
        "Coefficient_scaled": [b0_scaled] + list(b_scaled.values),
        "Std_Error_scaled": [result.bse["const"]] + list(result.bse.drop("const").values),
        "z_Value_scaled": [result.tvalues["const"]] + list(result.tvalues.drop("const").values),
        "p_Value": [result.pvalues["const"]] + list(result.pvalues.drop("const").values)
    })

    out_pvals = OUT_DIR / "logit_coefficients_pvalues.csv"
    table.to_csv(out_pvals, index=False)

    # Score applicants
    X_apps = apps.drop(columns=[ID_COL])
    X_apps = X_apps.reindex(columns=X.columns)
    X_apps = median_impute(to_numeric_df(X_apps))

    X_apps_scaled = standardize_apply(X_apps, x_mean, x_std)
    Xas_const = sm.add_constant(X_apps_scaled, has_constant="add")

    prob_yes = result.predict(Xas_const).values
    prob_no = 1 - prob_yes
    pred = (prob_yes >= 0.5).astype(int)

    scored = pd.DataFrame({
        ID_COL: apps[ID_COL],
        "prediction_good_risk": np.where(pred == 1, "Yes", "No"),
        "confidence_yes": prob_yes,
        "confidence_no": prob_no
    })
    scored["max_confidence"] = scored[["confidence_yes", "confidence_no"]].max(axis=1)
    scored["uncertain_flag"] = scored["max_confidence"] < UNCERTAIN_THRESHOLD

    out_scored_csv = OUT_DIR / "scored_loan_applicants.csv"
    scored.to_csv(out_scored_csv, index=False)

    # Build RapidMiner-like sheet
    scored_full = apps.copy()
    scored_full["prediction(Good Risk)"] = scored["prediction_good_risk"]
    scored_full["confidence(Yes)"] = scored["confidence_yes"].round(3)
    scored_full["confidence(No)"] = scored["confidence_no"].round(3)
    scored_full.insert(0, "Row No.", range(1, len(scored_full) + 1))
    scored_full["max_confidence"] = scored["max_confidence"].round(3)
    scored_full["uncertain_flag"] = scored["uncertain_flag"]

    out_scored_xlsx = OUT_DIR / "scored_loan_applicants.xlsx"
    save_scored_excel_rapidminer_style(scored_full, out_scored_xlsx)

    print("✅ Saved outputs:")
    print(f"- {out_scored_csv}")
    print(f"- {out_pvals}")
    print(f"- {out_scored_xlsx}")


if __name__ == "__main__":
    main()
