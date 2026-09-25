import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

DB_URL = os.getenv("DB_URL")


def get_engine():
    """
    Create and return the PostgreSQL SQLAlchemy engine.
    """

    if not DB_URL:
        raise ValueError(
            "DB_URL not found, check your .env file"
        )

    # Explicitly use psycopg2 because requirements.txt
    # contains psycopg2-binary.
    database_url = DB_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://"
    )

    return create_engine(database_url)


def init_tables():
    """
    Create all database tables if they do not already exist.
    """

    engine = get_engine()

    with engine.connect() as conn:

        # --------------------------------
        # Company dimension
        # --------------------------------

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_company (
                company_id SERIAL PRIMARY KEY,
                company_name TEXT UNIQUE NOT NULL
            );
        """))

        # --------------------------------
        # Location dimension
        # --------------------------------

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_location (
                location_id SERIAL PRIMARY KEY,
                city TEXT UNIQUE NOT NULL
            );
        """))

        # --------------------------------
        # Skill dimension
        # --------------------------------

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_skill (
                skill_id SERIAL PRIMARY KEY,
                skill_name TEXT UNIQUE NOT NULL
            );
        """))

        # --------------------------------
        # Job postings fact table
        # --------------------------------

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_job_postings (
                posting_id SERIAL PRIMARY KEY,

                job_title TEXT NOT NULL,

                company_id INT
                    REFERENCES dim_company(company_id),

                location_id INT
                    REFERENCES dim_location(location_id),

                category TEXT,

                salary_min NUMERIC,

                salary_max NUMERIC,

                posted_date DATE,

                scraped_at TIMESTAMP DEFAULT NOW(),

                raw_skills TEXT,

                source_url TEXT UNIQUE
            );
        """))

        conn.commit()

    print("Tables ready.")


def reset_tables():
    """
    Delete all pipeline tables and recreate them.
    """

    engine = get_engine()

    with engine.connect() as conn:

        conn.execute(text(
            "DROP TABLE IF EXISTS fact_job_postings CASCADE;"
        ))

        conn.execute(text(
            "DROP TABLE IF EXISTS dim_company CASCADE;"
        ))

        conn.execute(text(
            "DROP TABLE IF EXISTS dim_location CASCADE;"
        ))

        conn.execute(text(
            "DROP TABLE IF EXISTS dim_skill CASCADE;"
        ))

        conn.commit()

    print("Tables dropped.")

    init_tables()


if __name__ == "__main__":
    init_tables()