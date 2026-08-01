# Embedded Finance Revenue Analytics

> A business-focused analytics project that evaluates financial product performance, customer value, partner profitability, and onboarding funnel behavior using SQL and an interactive Streamlit dashboard.

---

## Project Overview

 Finance companies offer financial products through partner platforms such as marketplaces, retailers, and digital businesses.

As the number of products and partners grows, businesses need to understand:

- Which products actually generate revenue?
- Which partners contribute the most value?
- Are customers adopting multiple products?
- Where are customers dropping off during onboarding?
- Which customers have the highest lifetime value?
- Are customers returning to use financial products?
- Which products and partners have the strongest performance?

**Embedded Finance Revenue Analytics** addresses these questions by combining SQL-based business analysis with an interactive Streamlit dashboard.

The project uses a realistic synthetic dataset designed to simulate customers, financial products, partners, transactions, and funnel events.

---

## Business Objectives

The analysis focuses on five major areas:

### 1. Revenue Performance
Understand how revenue changes over time and identify the products and partners driving financial performance.

### 2. Product Adoption
Measure how customers adopt financial products and identify products with strong or weak adoption.

### 3. Customer Value
Analyze customer lifetime value, repeat usage, RFM behavior, and customer segments.

### 4. Partner Performance
Evaluate partner revenue, profitability, and customer value generated through each partner.

### 5. Funnel Performance
Identify conversion rates and drop-off points throughout the financial product onboarding journey.

---

## Key Business Questions

The project answers questions such as:

- What is the monthly revenue trend?
- Which financial product generates the most revenue?
- Which partner contributes the most revenue?
- Which products have the highest adoption?
- How successful is cross-selling?
- Which customers have the highest CLTV?
- Which customers are high-value or at risk?
- What percentage of customers return for repeat usage?
- Where does the largest funnel drop-off occur?
- Which partners are the most profitable?
- How does customer retention change across cohorts?

---

### Partner Analytics

- Partner Revenue
- Partner Profitability
- Partner CLTV
- Partner Performance

### Funnel Analytics

- Funnel Conversion
- Stage-wise Customer Count
- Funnel Drop-off
- Monthly Funnel Trend

---

# SQL Analysis

MySQL is used as the primary analytical layer.

The project demonstrates:

- Aggregations
- `GROUP BY`
- `CASE`
- `JOIN`
- Common Table Expressions (CTEs)
- Window Functions
- Customer Cohort Analysis
- Retention Analysis
- RFM Analysis
- Customer Segmentation
- Funnel Analysis
- Customer Lifetime Value
- Partner Profitability
- Product Performance Analysis
- SQL Views

---

# SQL Architecture

The SQL layer is organized into three files:

```text
sql/
│
├── schema.sql
├── queries.sql
└── views.sql
