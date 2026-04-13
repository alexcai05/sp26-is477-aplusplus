import os
import hashlib
import argparse
import requests
import pandas as pd

# Output directories
RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# College Scorecard API settings
SCORECARD_BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

# Variables to fetch from the College Scorecard API.
# Format: <category>.<variable_name>
SCORECARD_FIELDS = [
    "id",                                               # UNITID
    "school.name",                                      # Institution name
    "latest.cost.tuition.in_state",                     # In-state tuition
    "latest.cost.tuition.out_of_state",                 # Out-of-state tuition
    "latest.earnings.10_yrs_after_entry.median",        # Median earnings 10yr after entry
    "latest.aid.median_debt.completers.overall",        # Median debt for completers
    "latest.completion.rate_suppressed.four_year",      # 4-year graduation rate
    "latest.student.size",                              # Total undergraduate enrollment
]

# IPEDS CSV settings
# HD2024: IPEDS Institutional Characteristics directory file (most recent year)
IPEDS_URL = "https://nces.ed.gov/ipeds/datacenter/data/HD2024.zip"
IPEDS_FILENAME = "HD2024.csv"
IPEDS_OUTPUT = os.path.join(RAW_DIR, "ipeds_hd2024.csv")

# SHA-256 checksums
EXPECTED_CHECKSUMS = {
    "ipeds": "dc01e1522d85a10d2dabcbd53197a19804d44b330377b6a1189491f4c53f7df6",       
    "scorecard": "25f4de04450b69c5f99466df424d4661379e1a58ef372a60ffa0707a82b2fd5c",     
}

def compute_sha256(filepath):
    """Compute and return the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_checksum(filepath, expected, label):
    """Verify file checksum against expected value. Print result."""
    actual = compute_sha256(filepath)
    print(f"\n[Checksum] {label}")
    print(f"  SHA-256: {actual}")
    if expected is None:
        print("No expected checksum provided. Record the above value in EXPECTED_CHECKSUMS.")
    elif actual == expected:
        print("Checksum verified.")
    else:
        print("WARNING: Checksum mismatch! File may be corrupted or changed.")
        print(f"Expected: {expected}")
    return actual


# Dataset 1: College Scorecard — API acquisition

def fetch_scorecard(api_key):
    """
    Get College Scorecard data from the U.S. Dept. of Education API.
    Paginates through all results and saves a CSV to data/raw/.
    """
    print("\nCollege Scorecard API")
    print("Getting data from College Scorecard API...")

    all_results = []
    page = 0
    per_page = 100  # Max allowed by the API

    while True:
        params = {
            "api_key": api_key,
            "fields": ",".join(SCORECARD_FIELDS),
            "per_page": per_page,
            "page": page,
        }

        response = requests.get(SCORECARD_BASE_URL, params=params)

        if response.status_code != 200:
            print(f"  ERROR: API request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            break  # No more pages

        all_results.extend(results)
        total = data.get("metadata", {}).get("total", "?")
        print(f"  Fetched page {page + 1} — {len(all_results)} / {total} records")
        page += 1

    if not all_results:
        print("  No data retrieved. Check your API key and parameters.")
        return

    # The API returns each result as a flat dict with dotted keys
    # (e.g. {"latest.cost.tuition.in_state": 12000, "id": 123, ...})
    # Extract only the fields we requested to avoid any nested objects.
    rows = []
    for record in all_results:
        row = {field: record.get(field, None) for field in SCORECARD_FIELDS}
        rows.append(row)

    df = pd.DataFrame(rows)

    output_path = os.path.join(RAW_DIR, "scorecard_raw.csv")
    df.to_csv(output_path, index=False)
    print(f"\n  Saved {len(df)} records to: {output_path}")

    verify_checksum(output_path, EXPECTED_CHECKSUMS["scorecard"], "College Scorecard")


# Dataset 2: IPEDS — CSV download

def fetch_ipeds():
    """
    Download the IPEDS HD2024 institutional characteristics file.
    The file is distributed as a ZIP; we extract the relevant CSV.
    """
    import zipfile
    import io

    print("\n IPEDS CSV Download")
    print(f"Downloading IPEDS HD2024 from:\n  {IPEDS_URL}")

    response = requests.get(IPEDS_URL, stream=True)

    if response.status_code != 200:
        print(f"ERROR: Download failed with status {response.status_code}")
        return

    # Extract CSV from ZIP in memory
    zip_bytes = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_bytes) as z:
        # The ZIP contains multiple files; find the main data CSV
        csv_files = [name for name in z.namelist()
                     if name.upper() == IPEDS_FILENAME.upper()]
        if not csv_files:
            # Fallback: list available files and pick the first CSV
            print("Available files in ZIP:")
            for name in z.namelist():
                print(f"    {name}")
            csv_files = [name for name in z.namelist() if name.endswith(".csv")]

        if not csv_files:
            print("ERROR: No CSV found in ZIP archive.")
            return

        target = csv_files[0]
        print(f"Extracting: {target}")
        with z.open(target) as f:
            df = pd.read_csv(f, encoding="utf-8-sig", low_memory=False)

    # Keep only the columns relevant to our project
    cols_to_keep = ["UNITID", "INSTNM", "CONTROL", "LOCALE"]
    available = [col for col in cols_to_keep if col in df.columns]
    missing = [col for col in cols_to_keep if col not in df.columns]

    if missing:
        print(f"WARNING: These expected columns were not found: {missing}")

    df = df[available]
    df.to_csv(IPEDS_OUTPUT, index=False)
    print(f"\n  Saved {len(df)} records to: {IPEDS_OUTPUT}")

    verify_checksum(IPEDS_OUTPUT, EXPECTED_CHECKSUMS["ipeds"], "IPEDS HD2024")

# Main

def main():
    parser = argparse.ArgumentParser(
        description="Acquire College Scorecard (API) and IPEDS (CSV) datasets."
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Your College Scorecard API key. Get one at https://collegescorecard.ed.gov/data/documentation/",
    )
    args = parser.parse_args()

    print("Data Acquisition: College Characteristics & Graduate Earnings")


    fetch_scorecard(args.api_key)
    fetch_ipeds()

    print("Acquisition complete.")
    print(f"Raw data saved to: {os.path.abspath(RAW_DIR)}")


if __name__ == "__main__":
    main()