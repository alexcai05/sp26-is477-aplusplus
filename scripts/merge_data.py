import pandas as pd
import os

CLEANED_DIR = "data/cleaned"
OUTPUT_DIR  = "data/merged"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# load the cleaned datasets
clean_sc    = pd.read_csv(os.path.join(CLEANED_DIR, "scorecard_cleaned.csv"))
clean_ipeds = pd.read_csv(os.path.join(CLEANED_DIR, "ipeds_cleaned.csv"))

print(f"  Scorecard cleaned shape: {clean_sc.shape}")
print(f"  IPEDS cleaned shape:     {clean_ipeds.shape}")

# merge! inner join on UNITID
merged = pd.merge(clean_sc, clean_ipeds, on="UNITID", how="inner", suffixes=("_sc", "_ipeds"))

# don't need two columns for school name so drop one
if "INSTNM" in merged.columns:
    merged = merged.drop(columns=["INSTNM"])

sc_only = len(clean_sc) - len(merged)
ipeds_only = len(clean_ipeds[~clean_ipeds["UNITID"].isin(clean_sc["UNITID"])])
print(f"  Matched records:          {len(merged)}")
print(f"  Scorecard rows unmatched: {sc_only}  (excluded from merge)")
print(f"  IPEDS rows unmatched:     {ipeds_only}  (excluded from merge)")

merged.to_csv(os.path.join(OUTPUT_DIR, "merged_cleaned.csv"), index=False)
print(f"  merged_cleaned shape: {merged.shape}")