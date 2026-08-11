# Restaurant Order Data — Findings Summary

## Dataset
16,658 orders from 100 customers, January 2022 - December 2023 (a full 2-year
transaction history). Fields: order/customer IDs, category, item, price, quantity,
revenue, order date, and payment method. No missing values.

## Important scoping note
The original workflow this analysis followed was built around **churn** prediction.
That framing does not fit this data: **every one of the 100 customers placed an
order within the final 20 days of the dataset** — there is no inactive or lapsed
segment to detect. The business question was reframed to fit what the data can
actually answer: *given a customer's first-year (2022) ordering behavior, can we
identify who becomes a high-value customer in year two (2023)?*

## Business Overview

- **Total revenue analyzed:** ~$332,000 across the two years.
- **Main Dishes dominate revenue** ($156,317, 47% of total), more than the next
  three categories (Starters, Desserts, Side Dishes) combined.
- **Top single items by revenue:** Grilled Chicken ($38,382), Pasta Alfredo
  ($38,227), Steak ($35,849).
- **Payment methods are evenly split** — Cash (32%), Credit Card (32%), Digital
  Wallet (31%), with a small Unknown category (5%).
- **Monthly revenue is flat**, oscillating between roughly $12,200 and $15,400
  with no clear growth or seasonal trend across the two years.

## Predictive Model: Can we spot future high-value customers early?

**Target:** customers whose 2023 revenue fell in the top 30% (≥$1,757), predicted
using only their 2022 behavior (order count, revenue, average order value,
category mix, payment method mix, order consistency).

**Method note:** with only 100 customers, a standard 75/25 train/test split would
leave just ~25 customers to evaluate on — too few to trust. We used **Leave-One-Out
Cross-Validation** instead: each customer is held out and predicted once, using a
model trained on the other 99, giving the most stable estimate this sample size allows.

| Model | ROC-AUC | Read |
|---|---|---|
| Logistic Regression | **0.55** | Barely better than a coin flip |
| Random Forest | 0.41 | Worse than random — overfits noise on this sample size |

**The honest finding: 2022 behavior does not meaningfully predict 2023 value.**
The correlation between a customer's 2022 revenue and their 2023 revenue is just
**0.10** — essentially no year-over-year persistence. Customers who spent heavily
in year one were not reliably the ones spending heavily in year two.

Of the weak signal that exists, Logistic Regression coefficients suggest:
- A higher **share of Main Dish orders** in 2022 is the strongest (still weak)
  positive signal.
- **Order count in 2022** has a modest positive association.
- **Average order value in 2022** is *negatively* associated with becoming
  high-value in 2023 — a possible early sign of large-order customers not
  returning as consistently, though this should not be over-read given the
  model's low overall accuracy.

## Recommendations

1. **Don't build a "future VIP" targeting program on this data as-is.** The
   model isn't reliable enough to act on (regular precision/recall near chance
   for the high-value class). Acting on it would misdirect loyalty spend.
2. **Investigate why value doesn't persist year-over-year.** This is itself a
   useful finding — it suggests either (a) customers' spending is driven by
   factors not captured here (life events, group size, promotions), or (b) this
   customer base is already fairly homogeneous in engagement, so "high value"
   status is close to noise around a stable mean.
3. **Collect richer behavioral signals** if future-value prediction is a goal:
   party size, time of day/week, promotional exposure, review/feedback data, or
   loyalty program engagement would likely carry more signal than order history alone.
4. **Use the descriptive findings operationally today:** Main Dishes carry the
   business — menu, staffing, and inventory decisions should weight accordingly.
   The flat revenue trend is worth investigating from a growth/marketing
   perspective independent of the customer-value question.

## Limitations

- Only 100 customers — even with LOOCV, any model built on this sample carries
  wide uncertainty.
- The dataset's category labels are noisy (e.g., "Garlic Bread" appears logged
  under multiple categories); category-level revenue figures use the labels as
  given.
- This is a scoping exercise: it shows the analysis is honestly reported when the
  data doesn't support the original question, and it identifies what to collect
  next rather than forcing a model that isn't there.
