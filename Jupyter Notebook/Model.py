"""
STEP 3: Predictive model.

Key difference from a typical churn model: we only have 100 customers.
A single 75/25 train/test split would leave ~25 customers in the test set --
too few for a stable accuracy or AUC estimate (a handful of lucky/unlucky
predictions would swing the score by 10+ points).

Instead we use Leave-One-Out Cross-Validation (LOOCV): train on 99 customers,
predict the 1 held out, repeat 100 times. This uses every customer as a test
case exactly once, giving the most stable estimate possible from this sample
size. It's slower than a single split, but with only 100 rows and simple
models, it's instant.

We again compare Logistic Regression (interpretable) and Random Forest.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, confusion_matrix
from sklearn.pipeline import Pipeline

feat = pd.read_csv("/home/claude/restaurant_project/data/customer_features.csv")

X = feat.drop(columns=["Customer ID", "revenue_2023", "high_value_2023"])
y = feat["high_value_2023"]

loo = LeaveOneOut()

# --- Logistic Regression pipeline (scaling inside the CV loop to avoid leakage) ---
logit_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
])
logit_probs = cross_val_predict(logit_pipe, X, y, cv=loo, method="predict_proba")[:, 1]
logit_preds = (logit_probs >= 0.5).astype(int)

# --- Random Forest ---
rf = RandomForestClassifier(
    n_estimators=300, max_depth=4, min_samples_leaf=4,
    class_weight="balanced", random_state=42, n_jobs=-1
)
rf_probs = cross_val_predict(rf, X, y, cv=loo, method="predict_proba")[:, 1]
rf_preds = (rf_probs >= 0.5).astype(int)

print("=== Logistic Regression (LOOCV) ===")
print(classification_report(y, logit_preds, digits=3))
print("ROC-AUC:", round(roc_auc_score(y, logit_probs), 3))

print("\n=== Random Forest (LOOCV) ===")
print(classification_report(y, rf_preds, digits=3))
print("ROC-AUC:", round(roc_auc_score(y, rf_probs), 3))

# ---- Chart: ROC curves ----
plt.figure(figsize=(6, 6))
for name, probs, color in [("Logistic Regression", logit_probs, "#A7BEAE"),
                            ("Random Forest", rf_probs, "#B85042")]:
    fpr, tpr, _ = roc_curve(y, probs)
    auc = roc_auc_score(y, probs)
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.2f})", color=color, linewidth=2.5)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Model Comparison: ROC Curve (Leave-One-Out CV)")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/roc_curve.png", transparent=True)
plt.close()

# Random Forest (AUC 0.41, below chance) is not a usable model here -- with 100 rows
# and weak underlying signal it overfits noise. Logistic Regression (AUC 0.55) is the
# weak-but-real signal, so it -- not the Random Forest -- is what we chart and report.
logit_full = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
])
logit_full.fit(X, y)
coefs = pd.Series(logit_full.named_steps["clf"].coef_[0], index=X.columns).sort_values()
plt.figure(figsize=(7, 5))
colors_bar = ["#A7BEAE" if v < 0 else "#B85042" for v in coefs.values]
plt.barh(coefs.index, coefs.values, color=colors_bar)
plt.title("Logistic Regression Coefficients (Standardized)")
plt.xlabel("Effect on high-value likelihood")
plt.axvline(0, color="#888780", linewidth=0.8)
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/feature_importance.png", transparent=True)
plt.close()

# ---- Chart: Confusion matrix (Logistic Regression, LOOCV) ----
cm = confusion_matrix(y, logit_preds)
plt.figure(figsize=(5.5, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Oranges", cbar=False,
            xticklabels=["Predicted Regular", "Predicted High-Value"],
            yticklabels=["Actual Regular", "Actual High-Value"], annot_kws={"size": 14})
plt.title("Logistic Regression: Confusion Matrix (LOOCV)")
plt.tight_layout()
plt.savefig("/home/claude/restaurant_project/charts/confusion_matrix.png", transparent=True)
plt.close()

print("\nLogistic Regression coefficients:\n", coefs.sort_values(ascending=False))
print("\nAll model charts saved.")
