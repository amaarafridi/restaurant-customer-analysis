# Restaurant Customer Analysis & Business Intelligence Dashboard

## 📌 Project Overview

This project analyzes restaurant customer and order data to understand customer behavior, revenue performance, customer value, and opportunities for business improvement.

The project combines **Python/Jupyter Notebook analysis**, an **Excel dashboard**, a **business presentation**, and a **stakeholder report** to turn the analysis into practical business recommendations.

---

## 🎯 Business Objective

The main objectives of this project are to:

- Analyze customer ordering behavior
- Understand customer revenue and order patterns
- Compare customer value across 2022 and 2023
- Identify high-value customers
- Explore payment-method behavior
- Evaluate whether historical customer behavior can predict future customer value
- Develop actionable recommendations for stakeholders

---

## 🛠️ Tools & Technologies

- **Python**
- **Jupyter Notebook**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Excel**
- **Microsoft PowerPoint**
- **Microsoft Word**

---

## 📂 Project Structure

```text
restaurant-customer-analysis/
│
├── README.md
│
├── Jupyter_Notebook/
│   ├── restaurant_analysis.ipynb
│   ├── Customer_Features
│   ├── EDA
│   ├── Model
│   └── Finding_Summary
│
├── Excel_Dashboard/
│   ├── restaurant_stakeholder_dashboard.xlsx
│   └── Customer_Features
│
├── Presentation/
│   └── restaurant_analysis_presentation.pptx
│
└── Report/
    └── restaurant_stakeholder_report
```

---

## 🔎 Analysis Process

The project follows a structured data-analysis workflow:

1. Data loading and understanding
2. Data preparation
3. Exploratory data analysis
4. Customer-level analysis
5. Revenue analysis
6. Customer value analysis
7. Payment-method analysis
8. Predictive modeling
9. Model evaluation
10. Business recommendations

---

## 📊 Key Findings

The analysis identified several important business findings:

- The analysis covers **100 customers** and **16,658 orders** across the two-year period.
- Total revenue was approximately **$332K**.
- **Main Dishes represented 47% of total revenue**.
- Grilled Chicken, Pasta Alfredo, and Steak were identified as the leading dishes in the analysis.
- Customer revenue between 2022 and 2023 showed a relatively weak correlation of **0.10**.
- The best tested predictive model achieved a **ROC-AUC of 0.55**, indicating limited predictive strength.
- The available customer history was therefore not strong enough to confidently support a future high-value/VIP customer targeting strategy.

---

## 💡 Business Recommendations

Based on the analysis, the main recommendations are:

### 1. Protect Current Revenue Drivers

Focus inventory, menu management, and operational attention on the products and categories that currently contribute the most revenue.

### 2. Investigate Flat Revenue Performance

The analysis suggests that revenue remained relatively stable rather than showing a strong sustained growth trend. Further investigation into marketing, promotions, customer acquisition, and demand drivers is recommended.

### 3. Improve Customer Data

Additional customer information could improve future analysis and predictive modeling, including:

- Party size
- Promotion exposure
- Customer feedback
- Loyalty-program engagement
- Customer acquisition source
- Visit frequency

### 4. Revisit Predictive Customer Segmentation

Once richer customer-level data is available, predictive models can be retrained and evaluated to identify customers with a higher probability of becoming high-value customers.

---

## 📈 Deliverables

### Jupyter Notebook

Contains the Python-based data analysis, exploration, modeling, and findings.

### Excel Dashboard

Provides an interactive business view of customer and revenue metrics.

### Presentation

Summarizes the analysis and communicates the major findings and recommendations.

### Stakeholder Report

Provides a detailed written interpretation of the analysis and recommended business actions.

---

## 📁 Dataset

The analysis uses a publicly available dataset downloaded from **Kaggle**.

The original dataset and its associated license should be consulted for data ownership, attribution, and redistribution requirements.

---

## 👤 Project Purpose

This project was developed as a data analytics and business intelligence portfolio project to demonstrate the ability to:

- Work with real-world data
- Perform exploratory data analysis
- Analyze customer behavior
- Build business-focused dashboards
- Evaluate predictive models
- Communicate analytical findings
- Translate data into stakeholder recommendations