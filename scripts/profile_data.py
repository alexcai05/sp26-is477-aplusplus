import pandas as pd
import json
import os
from datetime import datetime

# all the paths
RAW_SCORECARD = "data/raw/scorecard_raw.csv"
RAW_IPEDS     = "data/raw/ipeds_hd2024.csv"
OUT_DIR       = "data/profiling"

os.makedirs(OUT_DIR, exist_ok=True)

# load the raw data
sc = pd.read_csv(RAW_SCORECARD)
ipeds = pd.read_csv(RAW_IPEDS)

# missing value stats per column
def missing_stats(df):
    result = {}
    for col in df.columns:
        n = int(df[col].isna().sum())
        result[col] = {
            "missing_count": n,
            "missing_pct": round(n / len(df) * 100, 1)
        }
    return result

# descriptive stats
def desc_stats(df):
    result = {}
    for col, stats in df.describe().to_dict().items():
        result[col] = {k: round(v, 4) for k, v in stats.items()}
    return result

# report!
sc_ids = set(sc["id"].dropna().astype(int))
ipeds_ids = set(ipeds["UNITID"].dropna().astype(int))

report = {
    "generation_timestamp": datetime.now().isoformat(),
    "scorecard_dataset": {
        "shape": {"rows": sc.shape[0], "columns": sc.shape[1]},
        "missing_values": missing_stats(sc),
        "descriptive_stats": desc_stats(sc),
        "duplicates": {
            "duplicate_rows": int(sc.duplicated().sum()),
            "duplicate_id": int(sc.duplicated(subset="id").sum()),
            "duplicate_school_name": int(sc.duplicated(subset="school.name").sum())
        },
        "implausible_values": {
            "student_size_zero": int((sc["latest.student.size"] == 0).sum()),
            "student_size_negative": int((sc["latest.student.size"] < 0).sum()),
            "tuition_in_state_negative": int((sc["latest.cost.tuition.in_state"] < 0).sum()),
            "tuition_out_of_state_negative": int((sc["latest.cost.tuition.out_of_state"] < 0).sum()),
            "completion_rate_above_1": int((sc["latest.completion.rate_suppressed.four_year"] > 1.0).sum()),
            "completion_rate_negative": int((sc["latest.completion.rate_suppressed.four_year"] < 0.0).sum())
        }
    },
    "ipeds_dataset": {
        "shape": {"rows": ipeds.shape[0], "columns": ipeds.shape[1]},
        "missing_values": missing_stats(ipeds),
        "duplicates": {
            "duplicate_rows": int(ipeds.duplicated().sum()),
            "duplicate_unitid": int(ipeds.duplicated(subset="UNITID").sum())
        },
        "sentinel_values": {
            "control_negative3": int((ipeds["CONTROL"] == -3).sum()),
            "locale_negative3": int((ipeds["LOCALE"] == -3).sum())
        },
        "control_value_counts": ipeds["CONTROL"].value_counts().sort_index().to_dict(),
        "locale_value_counts": ipeds["LOCALE"].value_counts().sort_index().to_dict()
    },
    "join_key_alignment": {
        "ids_in_both": len(sc_ids & ipeds_ids),
        "ids_in_scorecard_only": len(sc_ids - ipeds_ids),
        "ids_in_ipeds_only": len(ipeds_ids - sc_ids)
    }
}

out_path = os.path.join(OUT_DIR, "data_profile_report.json")
with open(out_path, "w") as f:
    json.dump(report, f, indent=2)