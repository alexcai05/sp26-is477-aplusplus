import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# path
MERGED_PATH = "data/merged/merged_cleaned.csv"
OUT_DIR     = "findings"

os.makedirs(OUT_DIR, exist_ok=True)

# load the data
df = pd.read_csv(MERGED_PATH)

# make locale names simpler (City, Suburb, Town, Rural)
df["locale_broad"] = df["LOCALE_LABEL"].str.split(":").str[0]

# plot
plt.rcParams.update({"figure.dpi": 150, "font.size": 11})
ALPHA  = 0.4
COLOR  = "#1f77b4"
LOCALE_ORDER = ["City", "Suburb", "Town", "Rural"]

# Question 1: Do universities with higher tuition result in graduates with higher post-graduation earnings?
q1 = df[["latest.cost.tuition.in_state",
          "latest.earnings.10_yrs_after_entry.median"]].dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(q1["latest.cost.tuition.in_state"],
           q1["latest.earnings.10_yrs_after_entry.median"],
           alpha=ALPHA, s=18, color=COLOR)

ax.set_xlabel("In-State Tuition ($)")
ax.set_ylabel("Median Earnings 10 Years After Entry ($)")
ax.set_title("Tuition vs. Post-Graduation Earnings")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "question1_tuition_vs_earnings.png"))
plt.close()

# Question 2: Do graduates from urban universities earn more than those from rural universities?
q2 = df[["locale_broad",
          "latest.earnings.10_yrs_after_entry.median"]].dropna()
q2 = q2[q2["locale_broad"].isin(LOCALE_ORDER)]

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=q2,
            x="locale_broad", y="latest.earnings.10_yrs_after_entry.median",
            order=LOCALE_ORDER, hue="locale_broad", palette="Blues",
            legend=False, ax=ax)

ax.set_xlabel("Locale Type")
ax.set_ylabel("Median Earnings 10 Years After Entry ($)")
ax.set_title("Post-Graduation Earnings by Locale Type")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "question2_locale_vs_earnings.png"))
plt.close()

# Question 3: Do larger universities produce higher-earning graduates?
q3 = df[["latest.student.size",
          "latest.earnings.10_yrs_after_entry.median"]].dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(q3["latest.student.size"],
           q3["latest.earnings.10_yrs_after_entry.median"],
           alpha=ALPHA, s=18, color=COLOR)

ax.set_xlabel("Student Enrollment Size")
ax.set_ylabel("Median Earnings 10 Years After Entry ($)")
ax.set_title("Student Size vs. Post-Graduation Earnings")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "question3_size_vs_earnings.png"))
plt.close()

# Question 4: Do students at universities with higher tuition graduate with more student debt?
q4 = df[["latest.cost.tuition.in_state",
          "latest.aid.median_debt.completers.overall"]].dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(q4["latest.cost.tuition.in_state"],
           q4["latest.aid.median_debt.completers.overall"],
           alpha=ALPHA, s=18, color=COLOR)

ax.set_xlabel("In-State Tuition ($)")
ax.set_ylabel("Median Student Debt ($)")
ax.set_title("Tuition vs. Student Debt")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "question4_tuition_vs_debt.png"))
plt.close()

# Question 5: Do universities with higher tuition have higher graduation rates?
q5 = df[["latest.cost.tuition.in_state",
          "latest.completion.rate_suppressed.four_year"]].dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(q5["latest.cost.tuition.in_state"],
           q5["latest.completion.rate_suppressed.four_year"],
           alpha=ALPHA, s=18, color=COLOR)

ax.set_xlabel("In-State Tuition ($)")
ax.set_ylabel("Four-Year Completion Rate")
ax.set_title("Tuition vs. Graduation Rate")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "question5_tuition_vs_graduation.png"))
plt.close()


# heatmap!
corr_cols = {
    "tuition_in_state":  "latest.cost.tuition.in_state",
    "earnings_10yr":     "latest.earnings.10_yrs_after_entry.median",
    "median_debt":       "latest.aid.median_debt.completers.overall",
    "completion_rate":   "latest.completion.rate_suppressed.four_year",
    "student_size":      "latest.student.size",
}
corr_df = df[list(corr_cols.values())].dropna()
corr_df.columns = list(corr_cols.keys())
corr_matrix = corr_df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap of Key Variables")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "correlation_heatmap.png"))
plt.close()