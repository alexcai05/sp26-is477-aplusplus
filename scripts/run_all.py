import subprocess
import sys

SCRIPTS = [
    "scripts/acquire_data.py",
    "scripts/profile_data.py",
    "scripts/clean_data.py",
    "scripts/merge_data.py",
    "scripts/analyze_data.py",
]

for script in SCRIPTS:
    print(f"Running {script}...")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\nError: {script} failed. Stopping pipeline.")
        sys.exit(1)

print("\nPipeline complete.")