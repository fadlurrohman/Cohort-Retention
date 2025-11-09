# Cohort Retention & Revenue Analysis

This project simulates user sign-ups and monthly activity for Agoda-like customers.

We:
- Build monthly **cohorts** based on sign-up month.
- Calculate retention rate by months since sign-up.
- Compute cohort-level revenue and simple LTV-style metrics.

## Files

- `generate_retention_data.py` – create synthetic signup + activity data.
- `cohort_retention_analysis.py` – build retention matrix and revenue summary.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generate_retention_data.py
python cohort_retention_analysis.py
```
