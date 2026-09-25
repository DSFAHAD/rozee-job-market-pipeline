import requests
import json
import os
import time
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Search multiple related terms
SEARCH_TERMS = {
    "data-science": "Data Science",
    "machine-learning": "Machine Learning",
    "data-engineering": "Data Engineering",
    "data-engineer": "Data Engineering",
    "data-scientist": "Data Science",
    "machine-learning-engineer": "Machine Learning",
    "ai-engineer": "Artificial Intelligence",
    "artificial-intelligence": "Artificial Intelligence",
    "data-analyst": "Data Analytics",
    "data-analytics": "Data Analytics",
}

# How many pages to collect for each search term
MAX_PAGES = 20

# ROZEE pagination appears in increments of 20
PAGE_SIZE = 20

session = requests.Session()
session.headers.update(HEADERS)


def fetch_page(url, retries=3):

    for attempt in range(retries + 1):

        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            return response.text

        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as e:

            if attempt < retries:

                wait = 5 * (attempt + 1)

                print(
                    f"Failed ({e}), retrying in "
                    f"{wait}s... ({attempt + 1}/{retries})"
                )

                time.sleep(wait)

            else:
                raise


def extract_json_blob(html):

    marker = "var apResp = "

    idx = html.find(marker)

    if idx == -1:
        raise ValueError(
            "Could not find apResp JSON blob. "
            "ROZEE page structure may have changed."
        )

    json_start = idx + len(marker)

    decoder = json.JSONDecoder()

    data, _ = decoder.raw_decode(html[json_start:])

    return data


def parse_jobs(data, category):

    jobs = []

    job_lists = data.get("response", {}).get("jobs", {})

    all_raw_jobs = (
        job_lists.get("basic", [])
        + job_lists.get("sponsored", [])
    )

    for j in all_raw_jobs:

        title = j.get("title")

        if not title:
            continue

        company = (
            j.get("company_name")
            or j.get("company")
            or "Unknown"
        )

        city = j.get("city", "Unknown")

        skills = j.get("skills", [])

        perma_link = (
            j.get("rozeePermaLink")
            or j.get("permaLink")
        )

        link = (
            f"https://www.rozee.pk/{perma_link}"
            if perma_link
            else None
        )

        jobs.append({

            "title": title,

            "company": company,

            "location": city,

            "link": link,

            "experience": j.get("experience_text"),

            "skills": skills,

            "salary": j.get("salaryTHide_exact"),

            "posted": j.get("created"),

            "category": category,
        })

    return jobs


def save_raw(jobs):

    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filepath = f"data/raw/jobs_{timestamp}.json"

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(
            jobs,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print(f"Saved {len(jobs)} jobs")
    print(f"File: {filepath}")
    print("=" * 60)

    return filepath


def get_job_key(job):

    # Prefer the actual job link as unique identifier
    if job.get("link"):
        return job["link"]

    # Fallback if link doesn't exist
    return (
        job.get("title"),
        job.get("company"),
        job.get("location"),
    )


if __name__ == "__main__":

    all_jobs = []

    print("=" * 60)
    print("JOB MARKET DATA EXTRACTION")
    print("=" * 60)

    for term, category_label in SEARCH_TERMS.items():

        print()
        print(f"SEARCH: {category_label}")
        print("-" * 60)

        for page in range(MAX_PAGES):

            fpn = page * PAGE_SIZE

            url = (
                f"https://www.rozee.pk/job/jsearch/"
                f"q/{term}?fpn={fpn}"
            )

            print(
                f"Page {page + 1}/{MAX_PAGES} "
                f"(fpn={fpn})..."
            )

            try:

                html = fetch_page(url)

                data = extract_json_blob(html)

                jobs = parse_jobs(
                    data,
                    category_label
                )

                print(
                    f"   Found {len(jobs)} jobs"
                )

                # If page contains no jobs,
                # stop this search term.
                if not jobs:

                    print(
                        "   No more jobs found."
                    )

                    break

                all_jobs.extend(jobs)

            except Exception as e:

                print(
                    f"   Error: {e}"
                )

                break

            # Don't hit the website too quickly
            time.sleep(3)

    print()
    print("=" * 60)
    print(f"RAW JOBS COLLECTED: {len(all_jobs)}")
    print("=" * 60)

    # Remove duplicates
    seen = set()

    unique_jobs = []

    for job in all_jobs:

        key = get_job_key(job)

        if key not in seen:

            seen.add(key)

            unique_jobs.append(job)

    print(
        f"UNIQUE JOBS: {len(unique_jobs)}"
    )

    print(
        f"DUPLICATES REMOVED: "
        f"{len(all_jobs) - len(unique_jobs)}"
    )

    save_raw(unique_jobs)