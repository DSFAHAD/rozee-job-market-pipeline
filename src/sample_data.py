import json
import glob
import os
import random


SAMPLE_SIZE = 50
OUTPUT_DIR = "data/sample"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "jobs.json")


def create_sample():
    files = glob.glob("data/raw/*.json")

    if not files:
        raise FileNotFoundError("No raw JSON files found.")

    latest_file = max(files, key=os.path.getctime)

    with open(latest_file, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    if len(jobs) <= SAMPLE_SIZE:
        sample = jobs
    else:
        random.seed(42)
        sample = random.sample(jobs, SAMPLE_SIZE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2, ensure_ascii=False)

    print(f"Created sample dataset: {OUTPUT_FILE}")
    print(f"Sample jobs: {len(sample)}")


if __name__ == "__main__":
    create_sample()