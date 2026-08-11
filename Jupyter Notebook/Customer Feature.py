"""
STEP 2: Build a customer-level table.

Design choice: since every customer is active throughout (no churn signal),
we reframe the predictive question as VALUE, not survival:

    Using only a customer's FIRST YEAR (2022) behavior, can we predict
    whether they become a HIGH-VALUE customer in year two (2023)?

This is a legitimate, common retail/restaurant use case: identify future VIPs
early so loyalty programs and outreach can target them before competitors do,
rather than reacting after the fact.

Target definition: "high value" = customer's total 2023 revenue is in the
top 30% of all customers. Top 30% (not 50%) gives a meaningfully distinct
"VIP" group rather than splitting an already-homogeneous customer base
down the middle.
"""

import pandas as pd
import numpy as np

df = pd.read_excel("/home/claude/restaurant_project/data/Clean_data.xlsx")
df.columns = [c.strip() for c in df.columns]
df["year"] = df["Order Date"].dt.year

df_2022 = df[df["year"] == 2022]
df_2023 = df[df["year"] == 2023]

# ---- 2022 features (predictors) ----
feat = df_2022.groupby("Customer ID").agg(
    orders_2022=("Order ID", "count"),
    revenue_2022=("Revenue", "sum"),
    avg_order_value_2022=("Revenue", "mean"),
).reset_index()

# category diversity: how many distinct categories a customer ordered from in 2022
cat_diversity = df_2022.groupby("Customer ID")["Category"].nunique().rename("category_diversity_2022")
feat = feat.merge(cat_diversity, on="Customer ID")

# share of 2022 orders that were Main Dishes (the highest-revenue category) -- a proxy
# for whether the customer treats this as a full meal destination vs. snacks/sides
main_share = (
    df_2022.assign(is_main=df_2022["Category"] == "Main Dishes")
    .groupby("Customer ID")["is_main"].mean()
    .rename("main_dish_share_2022")
)
feat = feat.merge(main_share, on="Customer ID")

# preferred payment method in 2022, one-hot encoded
pay_share = (
    df_2022.groupby(["Customer ID", "Payment Method"]).size()
    .unstack(fill_value=0)
)
pay_share = pay_share.div(pay_share.sum(axis=1), axis=0).add_prefix("pay_share_")
feat = feat.merge(pay_share, on="Customer ID")

# order frequency spread across the year (std of orders/month) -- a steady customer
# vs. a bursty one
monthly_orders = df_2022.assign(month=df_2022["Order Date"].dt.month).groupby(["Customer ID", "month"]).size().unstack(fill_value=0)
feat["order_consistency_2022"] = monthly_orders.std(axis=1).reindex(feat["Customer ID"]).values

# ---- 2023 target ----
rev_2023 = df_2023.groupby("Customer ID")["Revenue"].sum().rename("revenue_2023")
feat = feat.merge(rev_2023, on="Customer ID", how="left").fillna({"revenue_2023": 0})

threshold = feat["revenue_2023"].quantile(0.70)
feat["high_value_2023"] = (feat["revenue_2023"] >= threshold).astype(int)

# category_diversity_2022 turned out constant (every customer orders from all 5
# categories) -- no predictive value, so drop it rather than feed the model noise.
feat = feat.drop(columns=["category_diversity_2022"])

feat.to_csv("/home/claude/restaurant_project/data/customer_features.csv", index=False)

print("Customer feature table:", feat.shape)
print("\nHigh-value threshold (2023 revenue, 70th percentile): $%.2f" % threshold)
print("High-value customers:", feat["high_value_2023"].sum(), "/", len(feat))
print("\nFeature preview:")
print(feat.head())
print("\nCorrelation of 2022 features with 2023 high-value flag:")
print(feat.drop(columns=["Customer ID"]).corr(numeric_only=True)["high_value_2023"].sort_values(ascending=False))
