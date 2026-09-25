from sqlalchemy import text
from db import get_engine


def run_query(conn, title, query):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    result = conn.execute(text(query))

    rows = result.fetchall()

    for row in rows:
        print(row)

    return rows


def main():

    engine = get_engine()

    with engine.connect() as conn:

        run_query(
            conn,
            "TOTAL JOBS",
            """
            SELECT COUNT(*) AS total_jobs
            FROM fact_job_postings;
            """
        )

        run_query(
            conn,
            "JOBS BY CATEGORY",
            """
            SELECT
                COALESCE(category, 'Unknown') AS category,
                COUNT(*) AS total_jobs
            FROM fact_job_postings
            GROUP BY category
            ORDER BY total_jobs DESC;
            """
        )

        run_query(
            conn,
            "JOBS BY LOCATION",
            """
            SELECT
                l.city,
                COUNT(*) AS total_jobs
            FROM fact_job_postings f
            JOIN dim_location l
                ON f.location_id = l.location_id
            GROUP BY l.city
            ORDER BY total_jobs DESC;
            """
        )

        run_query(
            conn,
            "TOP COMPANIES",
            """
            SELECT
                c.company_name,
                COUNT(*) AS total_jobs
            FROM fact_job_postings f
            JOIN dim_company c
                ON f.company_id = c.company_id
            GROUP BY c.company_name
            ORDER BY total_jobs DESC
            LIMIT 20;
            """
        )

        run_query(
            conn,
            "TOP SKILLS",
            """
            SELECT
                TRIM(skill) AS skill,
                COUNT(*) AS job_count
            FROM fact_job_postings,
            LATERAL unnest(
                string_to_array(raw_skills, ',')
            ) AS skill
            WHERE TRIM(skill) <> ''
            GROUP BY TRIM(skill)
            ORDER BY job_count DESC
            LIMIT 30;
            """
        )


if __name__ == "__main__":
    main()