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
    scorecard_raw.csv                    # raw College Scorecard data from API
    ipeds_hd2024.csv                     # raw IPEDS HD2024 institutional characteristics
  profiling/
    data_profile_report.json             # data quality profile of raw datasets
  cleaned/
    scorecard_cleaned.csv                # cleaned College Scorecard data
    ipeds_cleaned.csv                    # cleaned IPEDS data
  merged/
    merged_cleaned.csv                   # inner join of cleaned datasets on UNITID
    merge_stats.json                     # merge match statistics
findings/
  question1_tuition_vs_earnings.png
  question2_locale_vs_earnings.png
  question3_size_vs_earnings.png
  question4_tuition_vs_debt.png
  question5_tuition_vs_graduation.png
  correlation_heatmap.png
project_milestones/
  ProjectPlan.md                         # project plan
  StatusReport.md                        # status report
scripts/
  acquire_data.py                        # fetches raw data and generates SHA-256 checksums
  profile_data.py                        # profiles raw datasets
  clean_data.py                          # cleans raw datasets
  merge_data.py                          # merges cleaned datasets on UNITID
  analyze_data.py                        # generates visualizations
  run_all.py                             # re-executes full pipeline
metadata.json                            # DCAT project metadata
DCAT                                     # Machine Readable Descriptive metadata
DataDictionary                           # column descriptions for all datasets
LICENSE                                  # MIT license
README.md                                # project report
Snakefile                                # end-to-end workflow automation
requirements.txt                         # Python dependencies
```
Raw files are preserved in `data/raw/` and are never edited manually. All profiling, cleaning, merging, and analysis steps are performed by scripts in `scripts/`, and their outputs are written to the appropriate subdirectory under `data/` or `results/`. This separation between raw and processed data makes it easy to track provenance and rerun the workflow from scratch.

## Data Profile
[max 2000 words] 
For each dataset used, describe its structure, content, and characteristics. Specify the location of the dataset files in your project repository. Discuss any ethical or legal constraints associated with the data and explain how the datasets relate to your questions

### Acquisition
 
Both datasets are publicly accessible online and can be reproduced by running `scripts/acquire_data.py`. A College Scorecard API key is required and can be obtained at https://api.data.gov/signup/.
 
```
python scripts/acquire_data.py --api-key YOUR_API_KEY
```
 
The script fetches College Scorecard data via the API with pagination and downloads the IPEDS HD2024 ZIP archive, extracting the relevant CSV. SHA-256 checksums are generated for both raw files and printed to the terminal for verification. Expected checksums are hardcoded in `acquire_data.py` and can be used to confirm file integrity.
 
| Dataset | File | SHA-256 |
|---|---|---|
| College Scorecard | `data/raw/scorecard_raw.csv` | `25f4de04450b69c5f99466df424d4661379e1a58ef372a60ffa0707a82b2fd5c` |
| IPEDS HD2024 | `data/raw/ipeds_hd2024.csv` | `dc01e1522d85a10d2dabcbd53197a19804d44b330377b6a1189491f4c53f7df6` |

### Dataset 1: College Scorecard
 
*alex fills in — source, coverage, format, variables, ethical/legal constraints*
 
### Dataset 2: IPEDS HD2024
 
*alex fills in — source, coverage, format, variables, ethical/legal constraints*
 
## Data Quality
[500-1000 words] 
Summary of the quality assessment.

## Data Cleaning
[max 1000 words] 
Summarize the data cleaning operations you performed and explain how each operation addressed specific data quality issues in your datasets.
 
Data was profiled using `scripts/profile_data.py` before any cleaning was performed. The profiling report saved to `data/profiling/data_profile_report.json` identified the following issues, which were addressed in `scripts/clean_data.py`.
 
### College Scorecard
 
Institutions with a student enrollment of 0 were dropped as these values are implausible. An active institution should not have zero enrolled students. There were 17 of these records. Rows were only dropped if they were missing values across all the relevant analysis columns simultaneously, rather than dropping any row with a single missing value. This preserved as much data as possible since some institutions don't want to disclose information like completion rate.
 
### IPEDS HD2024
 
The `CONTROL` and `LOCALE` columns use `-3` as a sentinel value that means "not applicable." These were turned into `NaN` to prevent them from being treated as valid numeric values during analysis. Human-readable labels were added for both columns. `CONTROL_LABEL` maps the numeric codes to Public, Private nonprofit, or Private for-profit, and `LOCALE_LABEL` maps locale codes to descriptions such as City: Large or Rural: Remote. A simplified `locale_broad` column was made using `LOCALE_LABEL` to group institutions into four broad categories: City, Suburb, Town, and Rural.
 
### Integration
 
The two datasets share the IPEDS Unit ID (`UNITID`) as a common identifier. College Scorecard uses this field as `id`, which is renamed to `UNITID` during the data cleaning step. The datasets are joined using an inner join in `scripts/merge_data.py`, keeping only institutions present in both sources.
 
```
SCORECARD                        IPEDS
---------                        -----
UNITID (primary key) ─────────── UNITID (primary key)
school_name                      CONTROL
tuition                          LOCALE
earnings
debt
completion_rate
student_size
```
 
**Merge Statistics**:
- Records in College Scorecard (cleaned): 4,839
- Records in IPEDS HD2024 (cleaned): 6,072
- Successfully matched: 4,839 (85.5% merge rate)
- Records in Scorecard only: 0
- Records in IPEDS only: 821
The 821 unmatched IPEDS institutions had no corresponding Scorecard entry, likely because they are not covered by the Scorecard program. Full match statistics are saved to `data/merged/merge_stats.json`.


## Findings
[~500 words] 
Description of any findings including numeric results and/or visualizations.

Visualizations were generated using `scripts/analyze_data.py` and saved to `results/`. The following plots address each research question:
 
| Research Question | Visualization |
|---|---|
| Do universities with higher tuition result in graduates with higher post-graduation earnings? | `question1_tuition_vs_earnings.png` |
| Do graduates from urban universities earn more than those from rural universities? | `question2_locale_vs_earnings.png` |
| Do larger universities produce higher-earning graduates? | `question3_size_vs_earnings.png` |
| Do students at universities with higher tuition graduate with more student debt? | `question4_tuition_vs_debt.png` |
| Do universities with higher tuition have higher graduation rates? | `question5_tuition_vs_graduation.png` |

Correlations across all variables is saved as `correlation_heatmap.png`.

*alex fill in the actual analysis*

## Future Work
[~500-1000 words] 
Brief discussion of any lessons learned and potential future work.

## Challenges
[~500 words] 
Discuss the main challenges you encountered while working on the project.
Challenges encountered while working on the project related to storage, missing data, and sentinel values. When the data was initially acquired, the file sizes for both the College Scorecard and IPEDS datasets were very large. Together, they took up 1.55 GB. This exceeded the Github file size limit of 50 MB and also resulted in low laptop storage warnings. After examining the CSV files, the root of the problem was that the datasets had an excessive number of columns, many of which were not required even need to answer our research questions. To address the storage challenge, it was decided that the best course of action would be to revise the data acquisition script so that it extracts only the columns relevant to the project from the College Scorecard and IPEDS datasets. The fix made a substantial difference. It solved the problem as the file sizes went from a combined 1.55 GB down to 698 KB.

Another challenge was debating what to do with the missing data. When the College Scorecard data was first retrieved, it was not anticipated that a majority of the records would have missing information. Options like imputation were considered, in which every piece of data missing either the tuition cost or postgraduate earnings (or both) would be imputed with the mean or median of the original data. However, it was decided that this approach might be inaccurate and impact the legitimacy of the conclusions. Thus, dropping missing data was the best course of action since sample size after cleaning was large enough to still be representative. Rather than blindly dropping any row with missing data since that would remove a lot of valuable data, only rows with missing values across all the relevant analysis columns were eliminated. The potential risks that might come along with a slightly smaller sample size were acknowledged, but the approach taken preserved as much of the orignal data as possible.

Another challenge was the presence of sentinal values in the IPEDS dataset. 

## Reproducing
Sequence of steps required for someone else to reproduce your results.

### System Requirements
- macOS, Linux, or Windows
- Python 3.8 or higher
- Internet access for initial data download
### Step 1: Clone the Repository
 
```
git clone https://github.com/alexcai05/sp26-is477-aplusplus.git
cd sp26-is477-aplusplus
```
 
### Step 2: Set Up the Python Environment
 
**Option A: Using pip**
```
pip install -r requirements.txt
```
 
**Option B: Using conda**
```
conda create -n is477-project python=3.10
conda activate is477-project
pip install -r requirements.txt
```
 
### Step 3: Obtain a College Scorecard API Key
 
Get a free API key at https://api.data.gov/signup/
 
### Step 4: Run the Pipeline
 
**Option A: Snakemake (recommended)**
```
snakemake run_all --cores 1 --config api_key=YOUR_API_KEY
```
 
**Option B: Run all at once**
```
python scripts/run_all.py
```
 
**Option C: Run each script individually**
```
python scripts/acquire_data.py --api-key YOUR_API_KEY
python scripts/profile_data.py
python scripts/clean_data.py
python scripts/merge_data.py
python scripts/analyze_data.py
```
 
### Step 5: Verify Outputs
 
After running the pipeline, make sure the following files exist:
 
```
data/profiling/data_profile_report.json
data/cleaned/scorecard_cleaned.csv
data/cleaned/ipeds_cleaned.csv
data/merged/merged_cleaned.csv
data/merged/merge_stats.json
results/question1_tuition_vs_earnings.png
results/question2_locale_vs_earnings.png
results/question3_size_vs_earnings.png
results/question4_tuition_vs_debt.png
results/question5_tuition_vs_graduation.png
results/correlation_heatmap.png
```
 
 
## Workflow
 
All processing and analysis steps are implemented as Python scripts in `scripts/`. Run the following commands in order from the repository root.
 
1. **Acquire raw data**
   ```
   python scripts/acquire_data.py --api-key YOUR_API_KEY
   ```
   Input: College Scorecard API, IPEDS HD2024 ZIP archive → Output: `data/raw/scorecard_raw.csv`, `data/raw/ipeds_hd2024.csv`
2. **Profile raw datasets**
   ```
   python scripts/profile_data.py
   ```
   Input: `data/raw/scorecard_raw.csv`, `data/raw/ipeds_hd2024.csv` → Output: `data/profiling/data_profile_report.json`
3. **Clean raw datasets**
   ```
   python scripts/clean_data.py
   ```
   Input: `data/raw/scorecard_raw.csv`, `data/raw/ipeds_hd2024.csv` → Output: `data/cleaned/scorecard_cleaned.csv`, `data/cleaned/ipeds_cleaned.csv`
4. **Merge cleaned datasets**
   ```
   python scripts/merge_data.py
   ```
   Input: `data/cleaned/scorecard_cleaned.csv`, `data/cleaned/ipeds_cleaned.csv` → Output: `data/merged/merged_cleaned.csv`, `data/merged/merge_stats.json`
5. **Generate visualizations**
   ```
   python scripts/analyze_data.py
   ```
   Input: `data/merged/merged_cleaned.csv` → Output: `results/question1_tuition_vs_earnings.png`, `results/question2_locale_vs_earnings.png`, `results/question3_size_vs_earnings.png`, `results/question4_tuition_vs_debt.png`, `results/question5_tuition_vs_graduation.png`, `results/correlation_heatmap.png`
For convenience, the full pipeline can also be run with a single command:
 
```
snakemake run_all --cores 1 --config api_key=YOUR_API_KEY
```
## References
Formatted citations for any papers, datasets, or software used in your project.
### Datasets
U.S. Department of Education. (2024). College Scorecard Data. Retrieved from https://collegescorecard.ed.gov/data/documentation/

National Center for Education Statistics. (2024). IPEDS HD2024: Institutional Characteristics. Integrated Postsecondary Education Data System. Retrieved from https://nces.ed.gov/ipeds/datacenter/data/HD2024.zip

### Software



## Licenses
### Code License
This project's code is released under the MIT License. See `LICENSE` in the repository root.

### Data License
**College Scorecard Dataset**
- Source: U.S. Department of Education
- License: Public Domain
- Terms: Freely available for use and redistribution
- Required citation: U.S. Department of Education. *College Scorecard Data, 2024.* https://collegescorecard.ed.gov/data/

**IPEDS Dataset**
- Source: National Center for Education Statistics
- License: Public Domain
- Terms: Freely available for use and redistribution
- Required citation: National Center for Education Statistics. *Integrated Postsecondary Education Data System (IPEDS), 2024.* https://nces.ed.gov/ipeds/use-the-data

### Third-Party Software
- **pandas**: BSD 3-Clause License
- **numpy**: BSD License
- **matplotlib**: PSF License
- **seaborn**: BSD 3-Clause License
- **jupyter**: BSD License
