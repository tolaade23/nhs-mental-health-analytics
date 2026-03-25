# NHS Mental Health Services Analytics 2019–2024

[Dashboard](https://tolaade23.github.io/nhs-mental-health-analytics/dashboard.html)
**Data Analyst:** Tola Adeniyi | [adetoladeniyi.com](https://adetoladeniyi.com) | [LinkedIn](https://linkedin.com/in/adetolaadeniyi) | 

---

## Project Overview

A comprehensive analytical study of NHS mental health service delivery across England from 2019 to 2024, covering **789,543 referrals** across seven regions and eight mental health conditions.

This project was built as part of my data analytics portfolio. It draws on my direct experience working within NHS-referred mental health inpatient services at Priory Hospital, which gives me practical insight into how health data is generated, where quality gaps arise, and what the numbers mean in a clinical context.

---

## Key Findings

| Metric | 2019 | 2024 | Change |
|--------|------|------|--------|
| Annual Referrals | 119,647 | 150,461 | **+25.8%** |
| Avg Wait Time | 6.1 weeks | 13.3 weeks | **+118%** |
| Treatment Completion | 71.8% | 62.8% | **-9pp** |
| Staff Vacancy Rate | 8.0% | 16.9% | **+111%** |

**Top insight:** Staff vacancy rates and patient wait times show a strong correlation (r ≈ 0.91), suggesting workforce investment is the most impactful lever available to NHS commissioners.

---

## Project Structure

```
nhs-mental-health-analytics/
│
├── data/
│   ├── nhs_mental_health_aggregate.csv   # 1,344 aggregated records by region/condition/year
│   └── nhs_mental_health_patients.csv    # 10,000 synthetic patient-level records
│
├── analysis/
│   └── nhs_analysis.py                   # Full Python analysis script
│
├── charts/                               # 8 publication-quality visualisations
│   ├── 01_referral_trends.png
│   ├── 02_by_condition.png
│   ├── 03_wait_times.png
│   ├── 04_completion_rate.png
│   ├── 05_demographics.png
│   ├── 06_vacancies_wait.png
│   ├── 07_heatmap.png
│   └── 08_outcomes.png
│
├── dashboard.html  # Interactive HTML dashboard
├── NHS_Mental_Health_Analytics_Report.pdf # Full analytical report (6 pages)
└── README.md
```

---

## Visualisations

The project includes 8 charts covering:

1. **Annual referral volume** — trend line with COVID-19 impact annotation
2. **Referrals by condition** — horizontal bar showing Depression & Anxiety dominance
3. **Wait times by region** — 2019 vs 2024 grouped bar with NHS 18-week target
4. **Treatment completion rate** — declining trend line 2019–2024
5. **Demographics** — age distribution and referral source pie chart
6. **Vacancy vs wait time** — dual-axis correlation chart
7. **Regional condition heatmap** — condition distribution % by NHS region
8. **Treatment outcomes** — patient outcome distribution

---

## Methodology

**Data source:** Modelled dataset based on published NHS Mental Health Services Data Set (MHSDS) statistics, NHS Digital annual reports, and NHS England workforce statistics.

**Dataset generation:** Custom Python script generating realistic synthetic data using:
- Clinically grounded probability distributions
- Regional population weighting (proportional to actual NHS region sizes)
- Year-on-year trend modelling based on published NHS statistics
- COVID-19 impact modelling for 2020 Q2

**Tools used:**
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Matplotlib PdfPages for report generation
- HTML/CSS for interactive dashboard

---

## Analytical Conclusions

1. **Referral demand is structurally elevated** — post-pandemic levels are not returning to 2019 baseline
2. **Wait times require urgent intervention** — 118% increase in 5 years is unsustainable
3. **Commission IAPT capacity** — Depression and Anxiety (52% of referrals) should be the priority
4. **Workforce is the primary lever** — strong vacancy/wait correlation supports the investment case
5. **Completion rates declining** — caseload pressure is driving early discharge, not clinical completion

---

## About the Analyst

I built this project as part of a portfolio demonstrating data analytics, BI, and project management skills targeting roles across data analytics, BI development, ML engineering, and digital project management.

**Background:** 13 years of operational data analytics at Ericsson and Huawei. MSc Applied Artificial Intelligence (Aston University, 2023). Google PM Certified. Microsoft Azure Data Scientist Associate. Neo4j Certified Professional.

**Clinical context:** I currently work within NHS-referred inpatient mental health services at Priory Hospital, which gave me direct insight into how this data is used and generated at point of care and what the quality gaps in real EHR data look like.

📧 detola.adeniyi@gmail.com | 🌐 [adetoladeniyi.com](https://adetoladeniyi.com) | 💼 [LinkedIn](https://linkedin.com/in/adetolaadeniyi) | [Dashboard](https://tolaade23.github.io/nhs-mental-health-analytics/dashboard.html)

---

*Data modelled from published NHS statistics for portfolio demonstration purposes.*
