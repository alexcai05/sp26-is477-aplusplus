import pandas as pd
import os

RAW_SCORECARD = "data/raw/scorecard_raw.csv"
RAW_IPEDS     = "data/raw/ipeds_hd2024.csv"
OUTPUT_DIR       = "data/cleaned"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# load the raw data
scorecard_df = pd.read_csv(RAW_SCORECARD)
ipeds_df     = pd.read_csv(RAW_IPEDS)

print(f"  Scorecard raw shape: {scorecard_df.shape}")
print(f"  IPEDS raw shape:     {ipeds_df.shape}")


# clean the college scorecard dataset
clean_sc = scorecard_df.copy()

# get rid of rows where student size is 0 or missing
clean_sc = clean_sc[clean_sc["latest.student.size"].notna() & (clean_sc["latest.student.size"] > 0)]

# get rid of rows with missing data in ALL of the relevant columns
key_cols = [
    "latest.cost.tuition.in_state",
    "latest.cost.tuition.out_of_state",
    "latest.earnings.10_yrs_after_entry.median",
    "latest.aid.median_debt.completers.overall",
    "latest.completion.rate_suppressed.four_year",
]
clean_sc = clean_sc.dropna(subset=key_cols, how="all")

# rename id to UNITID to make it easier to join datasets in a later step
clean_sc = clean_sc.rename(columns={"id": "UNITID"})

print(f"  Scorecard cleaned shape: {clean_sc.shape}")
clean_sc.to_csv(os.path.join(OUTPUT_DIR, "scorecard_cleaned.csv"), index=False)


# clean IPEDS HD2024
clean_IPEDS = ipeds_df.copy()

# IPEDS uses -3 for "not applicable" so turn those into NaN
clean_IPEDS["CONTROL"] = clean_IPEDS["CONTROL"].replace(-3, float("nan"))
clean_IPEDS["LOCALE"]  = clean_IPEDS["LOCALE"].replace(-3, float("nan"))

# turn CONTROL codes into readable labels
control_map = {1: "Public", 2: "Private nonprofit", 3: "Private for-profit"}
clean_IPEDS["CONTROL_LABEL"] = clean_IPEDS["CONTROL"].map(control_map)

# turn LOCALE codes to readable labels (first digit = urbanicity level)
locale_map = {
    11: "City: Large", 12: "City: Midsize", 13: "City: Small",
    21: "Suburb: Large", 22: "Suburb: Midsize", 23: "Suburb: Small",
    31: "Town: Fringe", 32: "Town: Distant", 33: "Town: Remote",
    41: "Rural: Fringe", 42: "Rural: Distant", 43: "Rural: Remote",
}
clean_IPEDS["LOCALE_LABEL"] = clean_IPEDS["LOCALE"].map(locale_map)

print(f"  IPEDS cleaned shape: {clean_IPEDS.shape}")
clean_IPEDS.to_csv(os.path.join(OUTPUT_DIR, "ipeds_cleaned.csv"), index=False)