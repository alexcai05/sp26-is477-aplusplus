# College Characteristics and Graduate Earnings
## Contributors
Bulleted list of contributors (with optional ORCIDs).
## Summary
[500-600 words]
Description of your project, motivation, research question(s), and any findings.
## Storage and Organization
To support reproducibility and traceability, we adopt the following directory structure:
```
data/
  raw/
    scorecard_raw.csv        # raw College Scorecard data from API
    ipeds_hd2024.csv         # raw IPEDS HD2024 institutional characteristics
  profiling/
    data_profile_report.json      # data quality profile of raw datasets
  cleaned/
    scorecard_cleaned.csv    # cleaned College Scorecard data
    ipeds_cleaned.csv        # cleaned IPEDS data
  merged/
    merged_cleaned.csv       # inner join of cleaned datasets on UNITID
    merge_stats.json         # merge match statistics
scripts/
  acquire_data.py            # fetches raw data and generates SHA-256 checksums
  profile_data.py            # profiles raw datasets
  clean_data.py              # cleans raw datasets
  merge_data.py              # merges cleaned datasets on UNITID
  analyze_data.py            # generates visualizations
  run_all.py                 # re-executes full pipeline
results/
  question1_tuition_vs_earnings.png
  question2_locale_vs_earnings.png
  question3_size_vs_earnings.png
  question4_tuition_vs_debt.png
  question5_tuition_vs_graduation.png
  correlation_heatmap.png
Snakefile                    # end-to-end workflow automation
requirements.txt             # Python dependencies
metadata.json                # DCAT project metadata
DataDictionary               # column descriptions for all datasets
DCAT                         # Machine Readable Descriptive metadata
LICENSE                      # MIT license
ProjectPlan.md               # Project plan
StatusReport.md              # Status report
README.md                    # project report
```
Raw files are preserved in data/raw/ and are never edited manually. All profiling, cleaning, merging, and analysis steps are performed by scripts in scripts/, and their outputs are written to the appropriate subdirectory under data/ or results/. This separation between raw and processed data makes it easy to track provenance and rerun the workflow from scratch.
## Data Profile
[max 2000 words] 
For each dataset used, describe its structure, content, and characteristics. Specify the location of the dataset files in your project repository. Discuss any ethical or legal constraints associated with the data and explain how the datasets relate to your questions
### College Scorecard
### IPEDS
## Data Quality
[500-1000 words] 
Summary of the quality assessment.
## Data Cleaning
[max 1000 words] 
Summarize the data cleaning operations you performed and explain how each operation addressed specific data quality issues in your datasets.
## Findings
[~500 words] 
Description of any findings including numeric results and/or visualizations.
## Future Work
[~500-1000 words] 
Brief discussion of any lessons learned and potential future work.
## Challenges
[~500 words] 
Discuss the main challenges you encountered while working on the project.
## Reproducing
Sequence of steps required for someone else to reproduce your results.
## References
Formatted citations for any papers, datasets, or software used in your project.
