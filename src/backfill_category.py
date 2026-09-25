import json
import glob
import os

def guess_category(title, skills):
    text = (title + " " + " ".join(skills)).lower()

    if "data engineer" in text or "etl" in text or "data pipeline" in text or "airflow" in text or "data engineering" in text:
        return "Data Engineering"
    if "machine learning" in text or "ml engineer" in text or "deep learning" in text or "computer vision" in text or "nlp" in text:
        return "Machine Learning"
    if "data scien" in text:
        return "Data Science"
    return "General"


def run():
    files = glob.glob("data/raw/*.json")
    if not files:
        print("No raw files found")
        return

    latest = max(files, key=os.path.getctime)
    print(f"Backfilling category in {latest}")

    with open(latest, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    updated = 0
    for job in jobs:
        if not job.get("category"):
            job["category"] = guess_category(job.get("title", ""), job.get("skills", []))
            updated += 1

    with open(latest, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"Backfilled category on {updated} jobs, saved back to {latest}")


if __name__ == "__main__":
    run()