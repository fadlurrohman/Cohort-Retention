import numpy as np
import pandas as pd

def generate_retention_data(n_users: int = 4000, random_state: int = 1234) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    signup_months = pd.period_range("2024-01", "2024-12", freq="M")

    rows = []
    for user_id in range(1, n_users + 1):
        uid = f"U{user_id:05d}"
        signup = rng.choice(signup_months)
        # Baseline retention probability decays over months
        base_retention = rng.uniform(0.3, 0.8)
        max_months = 15
        for m in range(max_months):
            month = (signup + m).to_timestamp("M")
            if month > pd.Timestamp("2025-03-31"):
                break
            # Survival style: p(active) decreases over time
            p_active = base_retention * (0.8 ** m)
            if rng.random() <= p_active:
                revenue = rng.uniform(10, 150)
                rows.append({
                    "user_id": uid,
                    "signup_month": signup.to_timestamp("M"),
                    "activity_month": month,
                    "revenue_usd": float(round(revenue, 2)),
                })
            else:
                # User churns; break the loop.
                break

    df = pd.DataFrame(rows)
    df.to_csv("retention_events.csv", index=False)
    print(f"Generated retention_events.csv with {len(df)} rows for {n_users} users")
    return df

if __name__ == "__main__":
    generate_retention_data()
