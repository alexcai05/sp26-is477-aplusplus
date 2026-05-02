# Snakefile (End-to-End Analysis Workflow)
#
# Usage:
#   snakemake --cores 1
#
# To pass your College Scorecard API key:
#   snakemake run_all --cores 1 --config api_key=YOUR_API_KEY

API_KEY = config.get("api_key", "")

rule run_all:
    input:
        "results/q1_tuition_vs_earnings.png",
        "results/q2_locale_vs_earnings.png",
        "results/q3_size_vs_earnings.png",
        "results/q4_tuition_vs_debt.png",
        "results/q5_tuition_vs_graduation.png",
        "results/correlation_heatmap.png"

rule acquire:
    output:
        "data/raw/scorecard_raw.csv",
        "data/raw/ipeds_hd2024.csv"
    shell:
        "python scripts/acquire_data.py --api-key {API_KEY}"

rule profile:
    input:
        "data/raw/scorecard_raw.csv",
        "data/raw/ipeds_hd2024.csv"
    output:
        "data/profiling/profile_report.json"
    shell:
        "python scripts/profile_data.py"

rule clean:
    input:
        "data/raw/scorecard_raw.csv",
        "data/raw/ipeds_hd2024.csv"
    output:
        "data/cleaned/scorecard_cleaned.csv",
        "data/cleaned/ipeds_cleaned.csv"
    shell:
        "python scripts/clean_data.py"

rule merge:
    input:
        "data/cleaned/scorecard_cleaned.csv",
        "data/cleaned/ipeds_cleaned.csv"
    output:
        "data/merged/merged_cleaned.csv",
        "data/merged/merge_stats.json"
    shell:
        "python scripts/merge_data.py"

rule analyze:
    input:
        "data/merged/merged_cleaned.csv"
    output:
        "results/q1_tuition_vs_earnings.png",
        "results/q2_locale_vs_earnings.png",
        "results/q3_size_vs_earnings.png",
        "results/q4_tuition_vs_debt.png",
        "results/q5_tuition_vs_graduation.png",
        "results/correlation_heatmap.png"
    shell:
        "python scripts/analyze_data.py"
