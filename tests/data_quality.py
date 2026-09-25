import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

DB_URL = os.getenv("DB_URL")


def get_engine():
    if not DB_URL:
        raise ValueError(
            "DB_URL not found. Check your .env file."
        )

    # Explicitly use psycopg2 because
    # requirements.txt contains psycopg2-binary.
    database_url = DB_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://"
    )

    return create_engine(database_url)


def check_total_jobs(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings;
        """)
    ).scalar()

    print(f"Total jobs: {result}")

    return result > 0


def check_duplicate_urls(conn):
    result = conn.execute(
        text("""
            SELECT source_url, COUNT(*)
            FROM fact_job_postings
            GROUP BY source_url
            HAVING COUNT(*) > 1;
        """)
    ).fetchall()

    if result:
        print("FAIL: Duplicate source URLs found.")
        return False

    print("PASS: No duplicate source URLs.")
    return True


def check_null_titles(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings
            WHERE job_title IS NULL
               OR TRIM(job_title) = '';
        """)
    ).scalar()

    if result > 0:
        print(f"FAIL: {result} jobs have empty titles.")
        return False

    print("PASS: No empty job titles.")
    return True


def check_null_company_ids(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings
            WHERE company_id IS NULL;
        """)
    ).scalar()

    if result > 0:
        print(
            f"FAIL: {result} jobs have NULL company_id."
        )
        return False

    print("PASS: No NULL company IDs.")
    return True


def check_null_location_ids(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings
            WHERE location_id IS NULL;
        """)
    ).scalar()

    if result > 0:
        print(
            f"FAIL: {result} jobs have NULL location_id."
        )
        return False

    print("PASS: No NULL location IDs.")
    return True


def check_orphan_companies(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings f
            LEFT JOIN dim_company c
                ON f.company_id = c.company_id
            WHERE c.company_id IS NULL;
        """)
    ).scalar()

    if result > 0:
        print(
            f"FAIL: {result} orphan company IDs found."
        )
        return False

    print("PASS: All company IDs are valid.")
    return True


def check_orphan_locations(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings f
            LEFT JOIN dim_location l
                ON f.location_id = l.location_id
            WHERE l.location_id IS NULL;
        """)
    ).scalar()

    if result > 0:
        print(
            f"FAIL: {result} orphan location IDs found."
        )
        return False

    print("PASS: All location IDs are valid.")
    return True


def check_empty_urls(conn):
    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM fact_job_postings
            WHERE source_url IS NULL
               OR TRIM(source_url) = '';
        """)
    ).scalar()

    if result > 0:
        print(
            f"FAIL: {result} empty source URLs found."
        )
        return False

    print("PASS: All jobs have source URLs.")
    return True


def run_quality_checks():

    engine = get_engine()

    checks = []

    with engine.connect() as conn:

        print("\n==============================")
        print("DATA QUALITY CHECKS")
        print("==============================\n")

        checks.append(
            check_total_jobs(conn)
        )

        checks.append(
            check_duplicate_urls(conn)
        )

        checks.append(
            check_null_titles(conn)
        )

        checks.append(
            check_null_company_ids(conn)
        )

        checks.append(
            check_null_location_ids(conn)
        )

        checks.append(
            check_orphan_companies(conn)
        )

        checks.append(
            check_orphan_locations(conn)
        )

        checks.append(
            check_empty_urls(conn)
        )

    print("\n==============================")
    print("QUALITY CHECK SUMMARY")
    print("==============================")

    if all(checks):
        print("PASS: All data quality checks passed.")
        return True

    print("FAIL: One or more data quality checks failed.")
    return False


if __name__ == "__main__":

    success = run_quality_checks()

    if not success:
        raise SystemExit(1)