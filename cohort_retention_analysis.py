import pandas as pd
import numpy as np

def build_cohort_table(df: pd.DataFrame):
    df["signup_month"] = pd.to_datetime(df["signup_month"]).dt.to_period("M")
    df["activity_month"] = pd.to_datetime(df["activity_month"]).dt.to_period("M")

    first_seen = df.groupby("user_id")["signup_month"].first()
    base = pd.DataFrame(first_seen).reset_index()

    cohort_sizes = base.groupby("signup_month")["user_id"].nunique()

    df = df.merge(base, on=["user_id", "signup_month"], how="left", suffixes=("", "_cohort"))
    df["months_since_signup"] = (df["activity_month"] - df["signup_month"]).apply(lambda p: p.n)

    active_users = df.groupby(["signup_month", "months_since_signup"])["user_id"].nunique().unstack(fill_value=0)
    retention = active_users.divide(cohort_sizes, axis=0)

    return cohort_sizes, active_users, retention

def cohort_revenue(df: pd.DataFrame):
    df["signup_month"] = pd.to_datetime(df["signup_month"]).dt.to_period("M")
    df["activity_month"] = pd.to_datetime(df["activity_month"]).dt.to_period("M")
    df["months_since_signup"] = (df["activity_month"] - df["signup_month"]).apply(lambda p: p.n)

    revenue = df.groupby(["signup_month", "months_since_signup"])["revenue_usd"].sum().unstack(fill_value=0)
    return revenue

if __name__ == "__main__":
    df = pd.read_csv("retention_events.csv")

    # Pakai copy supaya fungsi nggak saling modifikasi df yang sama
    cohort_sizes, active_users, retention = build_cohort_table(df.copy())
    revenue = cohort_revenue(df.copy())

    print("===== Cohort sizes =====")
    print(cohort_sizes)

    print("\n===== Retention rate by cohort (first 6 months) =====")
    print(retention.iloc[:, :6].round(3))

    print("\n===== Revenue by cohort (first 6 months) =====")
    print(revenue.iloc[:, :6].round(1))

    retention.to_csv("cohort_retention_matrix.csv")
    revenue.to_csv("cohort_revenue_matrix.csv")
    print("\nSaved cohort_retention_matrix.csv and cohort_revenue_matrix.csv.")
