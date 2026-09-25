import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL not found. Check your .env file.")

engine = create_engine(DB_URL)

query = """
SELECT
    f.posting_id,
    f.job_title,
    c.company_name,
    l.city AS location,
    f.category,
    f.salary_min,
    f.salary_max,
    f.posted_date,
    f.raw_skills,
    f.source_url
FROM fact_job_postings f
LEFT JOIN dim_company c
    ON f.company_id = c.company_id
LEFT JOIN dim_location l
    ON f.location_id = l.location_id
ORDER BY f.posting_id;
"""

df = pd.read_sql(query, engine)

output_path = "data/processed/job_market.csv"

df.to_csv(output_path, index=False)

print(f"Exported {len(df)} jobs.")
print(f"Saved to: {output_path}")