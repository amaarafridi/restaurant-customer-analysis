"""
STEP 1: Explore the raw transaction data.

This is real data (16,658 orders, 100 customers, Jan 2022 - Dec 2023), so unlike
the demo, we don't generate anything -- we characterize what's actually here
before deciding what to model.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 150

df = pd.read_excel("/home/claude/restaurant_project/data/Clean_data.xlsx")
df.columns = [c.strip() for c in df.columns]

print("Shape:", df.shape)
print("Date range:", df["Order Date"].min().date(), "to", df["Order Date"].max().date())
print("Unique customers:", df["Customer ID"].nunique())
print("Unique items:", df["Item"].nunique(), "across", df["Category"].nunique(), "categories")
print("\nRevenue by category:")
print(df.groupby("Category")["Revenue"].sum().sort_values(ascending=False))

# ---- Chart 1: Monthly revenue trend ----
monthly = df.set_index("Order Date").resample("ME")["Revenue"].sum()
plt.figure(figsize=(9, 4.5))
plt.plot(monthly.index, monthly.values, color="#B85042", linewidth=2.5, marker="o", markersize=4)
plt.title("Monthly Revenue, Jan 2022 - Dec 2023")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/monthly_revenue.png", transparent=True)
plt.close()

# ---- Chart 2: Revenue by category ----
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 4.5))
colors = ["#B85042"] + ["#A7BEAE"] * (len(cat_rev) - 1)
bars = plt.bar(cat_rev.index, cat_rev.values, color=colors)
plt.title("Total Revenue by Category")
plt.ylabel("Revenue ($)")
for b in bars:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 1500, f"${b.get_height():,.0f}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/revenue_by_category.png", transparent=True)
plt.close()

# ---- Chart 3: Top 10 items by revenue ----
top_items = df.groupby("Item")["Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(7, 5))
plt.barh(top_items.index[::-1], top_items.values[::-1], color="#B85042")
plt.title("Top 10 Items by Revenue")
plt.xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/top_items.png", transparent=True)
plt.close()

# ---- Chart 4: Payment method mix ----
pay_mix = df["Payment Method"].value_counts(normalize=True).sort_values(ascending=False)
plt.figure(figsize=(6, 4.5))
colors2 = ["#B85042", "#A7BEAE", "#E7E8D1", "#888780"]
bars2 = plt.bar(pay_mix.index, pay_mix.values, color=colors2[:len(pay_mix)])
plt.title("Payment Method Mix")
plt.ylabel("Share of orders")
for b in bars2:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 0.005, f"{b.get_height():.0%}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/payment_mix.png", transparent=True)
plt.close()

print("\nCharts saved.")
print("\nPayment mix:\n", pay_mix)
print("\nTop 5 items:\n", top_items.head())
