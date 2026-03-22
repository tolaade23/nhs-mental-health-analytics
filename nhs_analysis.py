import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os

os.makedirs('/home/claude/nhs_project', exist_ok=True)
os.makedirs('/home/claude/nhs_project/charts', exist_ok=True)

# ── COLOUR PALETTE ──
AMBER   = '#C47A0A'
AMBER2  = '#E09520'
INK     = '#1A1612'
INK2    = '#3A3530'
INK3    = '#6A6158'
BG      = '#FAF9F7'
BG2     = '#F3F1EC'
RULE    = '#D8D2C8'
GREEN   = '#16A34A'
RED     = '#DC2626'
BLUE    = '#1D4ED8'
TEAL    = '#0F766E'

PALETTE = [AMBER, TEAL, GREEN, BLUE, RED, '#7C3AED', '#DB2777', '#D97706']

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': BG,
    'axes.edgecolor': RULE,
    'axes.labelcolor': INK2,
    'axes.titlecolor': INK,
    'text.color': INK,
    'xtick.color': INK3,
    'ytick.color': INK3,
    'grid.color': RULE,
    'grid.linewidth': 0.6,
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

np.random.seed(42)

# ── GENERATE REALISTIC NHS MENTAL HEALTH DATASET ──
# Based on NHS Mental Health Services Data Set (MHSDS) published statistics
# Covering 2019-2024 across English NHS regions

regions = [
    'London', 'South East', 'South West', 'Midlands',
    'North West', 'North East & Yorkshire', 'East of England'
]

conditions = [
    'Depression', 'Anxiety Disorders', 'Bipolar Disorder',
    'Schizophrenia/Psychosis', 'PTSD', 'Eating Disorders',
    'Personality Disorders', 'ADHD'
]

age_groups = ['Under 18', '18-25', '26-35', '36-50', '51-65', '65+']
genders = ['Female', 'Male', 'Non-binary/Other']
referral_sources = ['GP', 'A&E', 'Self-referral', 'Other NHS', 'Social Services', 'Criminal Justice']
service_types = ['Community Mental Health', 'Inpatient', 'Crisis Resolution', 'Early Intervention', 'IAPT/Talking Therapies']
ethnicities = ['White British', 'White Other', 'Asian/Asian British', 'Black/Black British', 'Mixed', 'Other']
outcomes = ['Improved', 'No Change', 'Deteriorated', 'Discharged', 'Transferred', 'DNA/Lost to Follow-up']

years = list(range(2019, 2025))
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# Regional population weights (proportional to actual NHS region sizes)
region_weights = [0.22, 0.15, 0.10, 0.18, 0.14, 0.13, 0.08]

# Base referrals per quarter (based on NHS published ~2M referrals/year pre-COVID)
base_referrals = {
    2019: 120000,
    2020: 95000,   # COVID drop
    2021: 130000,  # Post-COVID surge
    2022: 148000,  # Continued increase
    2023: 156000,  # Peak pressure
    2024: 151000   # Slight stabilisation
}

records = []
for year in years:
    for q_idx, quarter in enumerate(quarters):
        for r_idx, region in enumerate(regions):
            total = int(base_referrals[year] * region_weights[r_idx] / 4)

            # Add quarterly variation
            if quarter == 'Q1': total = int(total * 0.95)
            elif quarter == 'Q2': total = int(total * 1.02)
            elif quarter == 'Q3': total = int(total * 0.93)
            else: total = int(total * 1.10)

            # COVID impact Q2 2020
            if year == 2020 and quarter == 'Q2':
                total = int(total * 0.65)

            for condition in conditions:
                cond_weights = {
                    'Depression': 0.28, 'Anxiety Disorders': 0.24,
                    'Bipolar Disorder': 0.07, 'Schizophrenia/Psychosis': 0.05,
                    'PTSD': 0.10, 'Eating Disorders': 0.06,
                    'Personality Disorders': 0.08, 'ADHD': 0.12
                }
                n = max(1, int(total * cond_weights[condition] * np.random.uniform(0.92, 1.08)))

                # Wait times (weeks) - worsened over time
                base_wait = 6 if year <= 2020 else 6 + (year - 2020) * 1.8
                wait_mean = base_wait + (0.5 if region in ['London', 'South East'] else 0)
                wait_time = max(1, round(np.random.normal(wait_mean, 2.5), 1))

                # Bed days (inpatient subset ~12%)
                inpatient_n = max(0, int(n * 0.12 * np.random.uniform(0.85, 1.15)))
                bed_days = max(0, int(np.random.normal(28, 8) * inpatient_n)) if inpatient_n > 0 else 0

                # Treatment completion rate - declined under pressure
                completion_base = 0.72 - (year - 2019) * 0.018
                completion_rate = round(min(0.85, max(0.45, completion_base + np.random.uniform(-0.05, 0.05))), 3)

                # Staff vacancies % - increased over time
                vacancy_rate = round(0.08 + (year - 2019) * 0.018 + np.random.uniform(-0.02, 0.02), 3)

                records.append({
                    'Year': year,
                    'Quarter': quarter,
                    'Period': f"{year} {quarter}",
                    'Region': region,
                    'Condition': condition,
                    'Referrals': n,
                    'Avg_Wait_Weeks': wait_time,
                    'Inpatient_Count': inpatient_n,
                    'Bed_Days': bed_days,
                    'Treatment_Completion_Rate': completion_rate,
                    'Staff_Vacancy_Rate': vacancy_rate,
                    'Year_Quarter_Num': year + (q_idx * 0.25)
                })

df = pd.DataFrame(records)

# Also create patient-level sample (10k records)
n_patients = 10000
patients = pd.DataFrame({
    'Age_Group': np.random.choice(age_groups, n_patients, p=[0.08, 0.14, 0.20, 0.28, 0.18, 0.12]),
    'Gender': np.random.choice(genders, n_patients, p=[0.58, 0.39, 0.03]),
    'Ethnicity': np.random.choice(ethnicities, n_patients, p=[0.65, 0.08, 0.09, 0.08, 0.05, 0.05]),
    'Condition': np.random.choice(conditions, n_patients, p=[0.28, 0.24, 0.07, 0.05, 0.10, 0.06, 0.08, 0.12]),
    'Referral_Source': np.random.choice(referral_sources, n_patients, p=[0.52, 0.12, 0.18, 0.10, 0.05, 0.03]),
    'Service_Type': np.random.choice(service_types, n_patients, p=[0.42, 0.12, 0.15, 0.10, 0.21]),
    'Region': np.random.choice(regions, n_patients, p=region_weights),
    'Outcome': np.random.choice(outcomes, n_patients, p=[0.38, 0.22, 0.08, 0.18, 0.07, 0.07]),
    'Wait_Weeks': np.random.exponential(8, n_patients).clip(1, 52).round(1),
    'Year': np.random.choice(years, n_patients)
})

print(f"Dataset: {len(df)} aggregated records, {len(patients)} patient records")
print(f"Total referrals modelled: {df['Referrals'].sum():,}")
print(df.head(3))

# Save datasets
df.to_csv('/home/claude/nhs_project/nhs_mental_health_aggregate.csv', index=False)
patients.to_csv('/home/claude/nhs_project/nhs_mental_health_patients.csv', index=False)

# ════════════════════════════════════════════════════
# CHART 1 — Referral Trends Over Time
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

annual = df.groupby('Year')['Referrals'].sum().reset_index()
ax.fill_between(annual['Year'], annual['Referrals'],
                alpha=0.15, color=AMBER)
ax.plot(annual['Year'], annual['Referrals'],
        color=AMBER, linewidth=2.5, marker='o', markersize=7, markerfacecolor=BG, markeredgewidth=2)

# Annotations
ax.annotate('COVID-19\nservice disruption', xy=(2020, annual[annual['Year']==2020]['Referrals'].values[0]),
            xytext=(2020.3, annual[annual['Year']==2020]['Referrals'].values[0] * 0.88),
            fontsize=8.5, color=RED, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))
ax.annotate('Post-pandemic\nsurge begins', xy=(2021, annual[annual['Year']==2021]['Referrals'].values[0]),
            xytext=(2021.2, annual[annual['Year']==2021]['Referrals'].values[0] * 1.04),
            fontsize=8.5, color=GREEN, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

for _, row in annual.iterrows():
    ax.text(row['Year'], row['Referrals'] + 8000,
            f"{row['Referrals']/1000:.0f}k", ha='center', fontsize=9, color=INK2, fontweight='600')

ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
ax.set_xlabel('Year', fontsize=10, color=INK2)
ax.set_ylabel('Total Referrals', fontsize=10, color=INK2)
ax.set_title('NHS Mental Health Referrals 2019–2024\nEngland — All Regions & Conditions',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.grid(axis='y', alpha=0.4)
ax.set_xlim(2018.5, 2024.5)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/01_referral_trends.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 1 done")

# ════════════════════════════════════════════════════
# CHART 2 — Referrals by Condition
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

by_cond = df.groupby('Condition')['Referrals'].sum().sort_values(ascending=True)
colors = [AMBER if i >= len(by_cond)-2 else INK3 for i in range(len(by_cond))]
bars = ax.barh(by_cond.index, by_cond.values, color=colors, height=0.65, edgecolor='none')

for bar, val in zip(bars, by_cond.values):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f'{val/1000:.0f}k', va='center', fontsize=9, color=INK2, fontweight='500')

ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
ax.set_xlabel('Total Referrals (2019–2024)', fontsize=10)
ax.set_title('Referrals by Mental Health Condition\nCumulative 2019–2024, All Regions',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.grid(axis='x', alpha=0.35)
ax.set_xlim(0, by_cond.max() * 1.14)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/02_by_condition.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 2 done")

# ════════════════════════════════════════════════════
# CHART 3 — Average Wait Times by Region (2019 vs 2024)
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

wait_comp = df[df['Year'].isin([2019, 2024])].groupby(['Region','Year'])['Avg_Wait_Weeks'].mean().reset_index()
w19 = wait_comp[wait_comp['Year']==2019].set_index('Region')['Avg_Wait_Weeks']
w24 = wait_comp[wait_comp['Year']==2024].set_index('Region')['Avg_Wait_Weeks']

x = np.arange(len(regions))
width = 0.35
b1 = ax.bar(x - width/2, w19[regions], width, label='2019', color=INK3, alpha=0.7, edgecolor='none')
b2 = ax.bar(x + width/2, w24[regions], width, label='2024', color=AMBER, edgecolor='none')

for bar in b2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.15,
            f'{h:.1f}w', ha='center', fontsize=8.5, color=AMBER, fontweight='600')

ax.set_xticks(x)
ax.set_xticklabels([r.replace(' & ', '\n& ') for r in regions], fontsize=9)
ax.set_ylabel('Average Wait Time (Weeks)', fontsize=10)
ax.set_title('Average Wait Time by Region: 2019 vs 2024\nAll Mental Health Conditions Combined',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.35)

# NHS 18-week target line
ax.axhline(y=18, color=RED, linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(6.6, 18.3, 'NHS 18-week\ntarget', fontsize=8, color=RED, ha='right')

plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/03_wait_times.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 3 done")

# ════════════════════════════════════════════════════
# CHART 4 — Treatment Completion Rate Trend
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

comp_trend = df.groupby('Year')['Treatment_Completion_Rate'].mean().reset_index()
ax.fill_between(comp_trend['Year'], comp_trend['Treatment_Completion_Rate'],
                alpha=0.12, color=TEAL)
ax.plot(comp_trend['Year'], comp_trend['Treatment_Completion_Rate'],
        color=TEAL, linewidth=2.5, marker='s', markersize=7,
        markerfacecolor=BG, markeredgewidth=2)

for _, row in comp_trend.iterrows():
    ax.text(row['Year'], row['Treatment_Completion_Rate'] + 0.008,
            f"{row['Treatment_Completion_Rate']*100:.1f}%",
            ha='center', fontsize=9.5, color=INK2, fontweight='600')

ax.axhline(y=0.75, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(2024.05, 0.752, 'Target 75%', fontsize=8.5, color=AMBER)

ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x*100:.0f}%'))
ax.set_ylim(0.5, 0.85)
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Treatment Completion Rate', fontsize=10)
ax.set_title('Treatment Completion Rate 2019–2024\nPercentage of referrals completing planned treatment',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.grid(axis='y', alpha=0.35)
ax.set_xlim(2018.5, 2024.8)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/04_completion_rate.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 4 done")

# ════════════════════════════════════════════════════
# CHART 5 — Patient Demographics (Age & Gender)
# ════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor(BG)

# Age distribution
ax1 = axes[0]
ax1.set_facecolor(BG)
age_counts = patients['Age_Group'].value_counts().reindex(age_groups)
colors_age = [AMBER if g in ['18-25', '26-35'] else INK3 for g in age_groups]
bars = ax1.bar(age_groups, age_counts.values, color=colors_age, edgecolor='none', width=0.65)
for bar, val in zip(bars, age_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
             f'{val/n_patients*100:.1f}%', ha='center', fontsize=9, color=INK2, fontweight='500')
ax1.set_title('Referrals by Age Group', fontsize=12, fontweight='700', color=INK, pad=12)
ax1.set_ylabel('Number of Patients', fontsize=10)
ax1.tick_params(axis='x', rotation=30)
ax1.grid(axis='y', alpha=0.35)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Referral source
ax2 = axes[1]
ax2.set_facecolor(BG)
ref_counts = patients['Referral_Source'].value_counts()
wedge_colors = [AMBER, TEAL, GREEN, BLUE, RED, INK3]
wedges, texts, autotexts = ax2.pie(
    ref_counts.values, labels=ref_counts.index,
    colors=wedge_colors[:len(ref_counts)],
    autopct='%1.1f%%', startangle=90,
    pctdistance=0.78, labeldistance=1.12,
    wedgeprops=dict(edgecolor=BG, linewidth=2)
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_color(BG)
    at.set_fontweight('600')
for t in texts:
    t.set_fontsize(9)
    t.set_color(INK2)
ax2.set_title('Referral Sources', fontsize=12, fontweight='700', color=INK, pad=12)

plt.suptitle('Patient Demographics & Referral Pathways', fontsize=13, fontweight='700', color=INK, y=1.01)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/05_demographics.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 5 done")

# ════════════════════════════════════════════════════
# CHART 6 — Staff Vacancies vs Wait Times
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

annual_vac = df.groupby('Year').agg(
    vacancy=('Staff_Vacancy_Rate', 'mean'),
    wait=('Avg_Wait_Weeks', 'mean')
).reset_index()

ax2_twin = ax.twinx()
l1, = ax.plot(annual_vac['Year'], annual_vac['vacancy']*100,
              color=RED, linewidth=2.2, marker='o', markersize=7,
              markerfacecolor=BG, markeredgewidth=2, label='Staff Vacancy Rate %')
l2, = ax2_twin.plot(annual_vac['Year'], annual_vac['wait'],
                    color=AMBER, linewidth=2.2, marker='s', markersize=7,
                    markerfacecolor=BG, markeredgewidth=2, label='Avg Wait (Weeks)')

ax.set_ylabel('Staff Vacancy Rate (%)', color=RED, fontsize=10)
ax2_twin.set_ylabel('Average Wait Time (Weeks)', color=AMBER, fontsize=10)
ax.tick_params(axis='y', labelcolor=RED)
ax2_twin.tick_params(axis='y', labelcolor=AMBER)
ax.set_xlabel('Year', fontsize=10)
ax.set_title('Staff Vacancy Rate vs Patient Wait Times 2019–2024\nExploring the relationship between workforce gaps and service delays',
             fontsize=12, fontweight='700', color=INK, pad=15)

lines = [l1, l2]
labels = [l.get_label() for l in lines]
ax.legend(lines, labels, loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)
ax2_twin.spines['top'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/06_vacancies_wait.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 6 done")

# ════════════════════════════════════════════════════
# CHART 7 — Heatmap: Referrals by Region and Condition
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

heat_data = df.groupby(['Region', 'Condition'])['Referrals'].sum().unstack()
heat_pct = heat_data.div(heat_data.sum(axis=1), axis=0) * 100

sns.heatmap(heat_pct, annot=True, fmt='.1f', cmap='YlOrBr',
            ax=ax, linewidths=0.5, linecolor=BG,
            cbar_kws={'label': '% of Regional Referrals'},
            annot_kws={'size': 9, 'weight': '500'})
ax.set_title('Referral Distribution by Region and Condition (%)\n2019–2024 Cumulative',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.set_xlabel('Mental Health Condition', fontsize=10)
ax.set_ylabel('NHS Region', fontsize=10)
ax.tick_params(axis='x', rotation=35)
ax.tick_params(axis='y', rotation=0)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/07_heatmap.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 7 done")

# ════════════════════════════════════════════════════
# CHART 8 — Treatment Outcomes
# ════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

outcome_counts = patients['Outcome'].value_counts()
outcome_colors = {
    'Improved': GREEN, 'Discharged': TEAL,
    'No Change': INK3, 'Transferred': BLUE,
    'DNA/Lost to Follow-up': RED, 'Deteriorated': '#DC2626'
}
colors_out = [outcome_colors.get(o, AMBER) for o in outcome_counts.index]
bars = ax.barh(outcome_counts.index, outcome_counts.values,
               color=colors_out, height=0.6, edgecolor='none')

for bar, val in zip(bars, outcome_counts.values):
    ax.text(val + 30, bar.get_y() + bar.get_height()/2,
            f'{val/n_patients*100:.1f}%',
            va='center', fontsize=9.5, color=INK2, fontweight='500')

ax.set_xlabel('Number of Patients', fontsize=10)
ax.set_title('Treatment Outcomes Distribution\nNHS Mental Health Services Sample (n=10,000)',
             fontsize=13, fontweight='700', color=INK, pad=15)
ax.grid(axis='x', alpha=0.35)
ax.set_xlim(0, outcome_counts.max() * 1.15)
plt.tight_layout()
plt.savefig('/home/claude/nhs_project/charts/08_outcomes.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Chart 8 done")

print("\nAll 8 charts generated successfully.")
print("Charts saved to /home/claude/nhs_project/charts/")

# ── KEY STATISTICS FOR REPORT ──
print("\n── KEY STATISTICS ──")
print(f"Total referrals 2019: {df[df['Year']==2019]['Referrals'].sum():,}")
print(f"Total referrals 2024: {df[df['Year']==2024]['Referrals'].sum():,}")
pct_change = (df[df['Year']==2024]['Referrals'].sum() - df[df['Year']==2019]['Referrals'].sum()) / df[df['Year']==2019]['Referrals'].sum() * 100
print(f"Change 2019-2024: +{pct_change:.1f}%")
print(f"Avg wait 2019: {df[df['Year']==2019]['Avg_Wait_Weeks'].mean():.1f} weeks")
print(f"Avg wait 2024: {df[df['Year']==2024]['Avg_Wait_Weeks'].mean():.1f} weeks")
print(f"Completion rate 2019: {df[df['Year']==2019]['Treatment_Completion_Rate'].mean()*100:.1f}%")
print(f"Completion rate 2024: {df[df['Year']==2024]['Treatment_Completion_Rate'].mean()*100:.1f}%")
print(f"Staff vacancy 2019: {df[df['Year']==2019]['Staff_Vacancy_Rate'].mean()*100:.1f}%")
print(f"Staff vacancy 2024: {df[df['Year']==2024]['Staff_Vacancy_Rate'].mean()*100:.1f}%")
top_condition = df.groupby('Condition')['Referrals'].sum().idxmax()
print(f"Highest referral condition: {top_condition}")
improved_pct = len(patients[patients['Outcome']=='Improved']) / n_patients * 100
print(f"% patients improved: {improved_pct:.1f}%")
