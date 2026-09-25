from sqlalchemy import text

from db import get_engine
from transform import run as get_clean_data


def get_company_id(conn, company_name):

    # Check whether company already exists
    result = conn.execute(
        text("""
            SELECT company_id
            FROM dim_company
            WHERE company_name = :company_name
        """),
        {
            "company_name": company_name
        }
    ).fetchone()

    if result:
        return result[0]

    # Insert new company
    result = conn.execute(
        text("""
            INSERT INTO dim_company (company_name)
            VALUES (:company_name)
            RETURNING company_id
        """),
        {
            "company_name": company_name
        }
    )

    return result.fetchone()[0]


def get_location_id(conn, location):

    # Check whether location already exists
    result = conn.execute(
        text("""
            SELECT location_id
            FROM dim_location
            WHERE city = :location
        """),
        {
            "location": location
        }
    ).fetchone()

    if result:
        return result[0]

    # Insert new location
    result = conn.execute(
        text("""
            INSERT INTO dim_location (city)
            VALUES (:location)
            RETURNING location_id
        """),
        {
            "location": location
        }
    )

    return result.fetchone()[0]


def job_exists(conn, source_url):

    result = conn.execute(
        text("""
            SELECT posting_id
            FROM fact_job_postings
            WHERE source_url = :source_url
        """),
        {
            "source_url": source_url
        }
    ).fetchone()

    return result is not None


def load_jobs(df):

    engine = get_engine()

    inserted = 0
    skipped = 0

    with engine.begin() as conn:

        for _, row in df.iterrows():

            source_url = row["link"]

            # --------------------------------
            # 1. Check if job already exists
            # --------------------------------

            if job_exists(conn, source_url):

                print(
                    f"SKIP: {row['title']} | "
                    f"{row['company']}"
                )

                skipped += 1

                continue

            # --------------------------------
            # 2. Get company ID
            # --------------------------------

            company_id = get_company_id(
                conn,
                row["company"]
            )

            # --------------------------------
            # 3. Get location ID
            # --------------------------------

            location_id = get_location_id(
                conn,
                row["location"]
            )

            # --------------------------------
            # 4. Insert job
            # --------------------------------

            conn.execute(
                text("""
                    INSERT INTO fact_job_postings
                    (
                        job_title,
                        company_id,
                        location_id,
                        category,
                        raw_skills,
                        source_url
                    )
                    VALUES
                    (
                        :job_title,
                        :company_id,
                        :location_id,
                        :category,
                        :raw_skills,
                        :source_url
                    )
                """),
                {
                    "job_title": row["title"],
                    "company_id": company_id,
                    "location_id": location_id,
                    "category": row["category"],
                    "raw_skills": row["raw_skills"],
                    "source_url": source_url
                }
            )

            print(
                f"INSERT: {row['title']} | "
                f"{row['company']}"
            )

            inserted += 1

    print("\n==============================")
    print("LOAD COMPLETE")
    print("==============================")
    print(f"Inserted : {inserted}")
    print(f"Skipped  : {skipped}")
    print(f"Total    : {inserted + skipped}")


def run():

    print("Starting transformation...")

    df = get_clean_data()

    print(
        f"Loaded {len(df)} cleaned jobs."
    )

    print("\nStarting database load...")

    load_jobs(df)


if __name__ == "__main__":
    run()