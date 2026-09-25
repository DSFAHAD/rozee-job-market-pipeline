from db import get_engine
from sqlalchemy import text


def run_checks():
    engine = get_engine()

    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM fact_job_postings")).scalar()
        null_titles = conn.execute(text("SELECT COUNT(*) FROM fact_job_postings WHERE job_title IS NULL")).scalar()
        null_skills = conn.execute(text("SELECT COUNT(*) FROM fact_job_postings WHERE raw_skills = ''")).scalar()

        dup_check = conn.execute(text("""
            SELECT job_title, company_id, COUNT(*) as c
            FROM fact_job_postings
            GROUP BY job_title, company_id
            HAVING COUNT(*) > 1
        """)).fetchall()

    print("---- Data Quality Report ----")
    print(f"Total postings: {total}")
    print(f"Null titles: {null_titles}")
    print(f"Postings with no skills matched: {null_skills}")
    print(f"Duplicate groups found: {len(dup_check)}")
    print("------------------------------")


if __name__ == "__main__":
    run_checks()
