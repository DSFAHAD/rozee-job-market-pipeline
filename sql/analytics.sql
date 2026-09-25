SELECT COUNT(*) AS total_jobs
FROM fact_job_postings;

SELECT COUNT(*) AS total_companies
FROM dim_company;

SELECT COUNT(*) AS total_locations
FROM dim_location;

SELECT
    COALESCE(category, 'Unknown') AS category,
    COUNT(*) AS total_jobs
FROM fact_job_postings
GROUP BY category
ORDER BY total_jobs DESC;

SELECT
    l.city,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city
ORDER BY total_jobs DESC;

SELECT
    c.company_name,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_company c
    ON f.company_id = c.company_id
GROUP BY c.company_name
ORDER BY total_jobs DESC
LIMIT 20;

SELECT
    c.company_name,
    f.category,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_company c
    ON f.company_id = c.company_id
GROUP BY c.company_name, f.category
ORDER BY total_jobs DESC;

SELECT
    job_title,
    COUNT(*) AS total_jobs
FROM fact_job_postings
GROUP BY job_title
ORDER BY total_jobs DESC
LIMIT 20;

SELECT COUNT(*) AS data_science_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%data scientist%'
   OR LOWER(category) LIKE '%data science%';

SELECT COUNT(*) AS data_engineering_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%data engineer%'
   OR LOWER(category) LIKE '%data engineer%';

SELECT COUNT(*) AS machine_learning_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%machine learning%'
   OR LOWER(job_title) LIKE '%ml engineer%'
   OR LOWER(category) LIKE '%machine learning%';

SELECT COUNT(*) AS python_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%python%'
   OR LOWER(raw_skills) LIKE '%python%';

SELECT COUNT(*) AS sql_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%sql%'
   OR LOWER(raw_skills) LIKE '%sql%';

SELECT COUNT(*) AS python_sql_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%python%'
  AND LOWER(raw_skills) LIKE '%sql%';

SELECT COUNT(*) AS python_ml_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%python%'
  AND (
      LOWER(raw_skills) LIKE '%machine learning%'
      OR LOWER(raw_skills) LIKE '%machine-learning%'
  );

SELECT COUNT(*) AS data_engineering_skill_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%airflow%'
   OR LOWER(raw_skills) LIKE '%spark%'
   OR LOWER(raw_skills) LIKE '%kafka%'
   OR LOWER(raw_skills) LIKE '%etl%'
   OR LOWER(raw_skills) LIKE '%data engineering%'
   OR LOWER(raw_skills) LIKE '%data engineer%';

SELECT COUNT(*) AS cloud_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%aws%'
   OR LOWER(raw_skills) LIKE '%azure%'
   OR LOWER(raw_skills) LIKE '%gcp%'
   OR LOWER(raw_skills) LIKE '%google cloud%'
   OR LOWER(raw_skills) LIKE '%cloud%';

SELECT COUNT(*) AS powerbi_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%power bi%'
   OR LOWER(raw_skills) LIKE '%powerbi%';

SELECT COUNT(*) AS tableau_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%tableau%';

SELECT COUNT(*) AS excel_jobs
FROM fact_job_postings
WHERE LOWER(raw_skills) LIKE '%excel%';

SELECT
    c.company_name,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_company c
    ON f.company_id = c.company_id
WHERE LOWER(f.job_title) LIKE '%data scientist%'
GROUP BY c.company_name
ORDER BY total_jobs DESC
LIMIT 20;

SELECT
    l.city,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE LOWER(f.job_title) LIKE '%data scientist%'
   OR LOWER(f.category) LIKE '%data science%'
GROUP BY l.city
ORDER BY total_jobs DESC;

SELECT
    l.city,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE LOWER(f.job_title) LIKE '%data engineer%'
   OR LOWER(f.category) LIKE '%data engineer%'
GROUP BY l.city
ORDER BY total_jobs DESC;

SELECT
    l.city,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE LOWER(f.job_title) LIKE '%machine learning%'
   OR LOWER(f.job_title) LIKE '%ml engineer%'
GROUP BY l.city
ORDER BY total_jobs DESC;

SELECT COUNT(*) AS jobs_with_salary
FROM fact_job_postings
WHERE salary_min IS NOT NULL
   OR salary_max IS NOT NULL;

SELECT AVG(salary_min) AS average_min_salary
FROM fact_job_postings
WHERE salary_min IS NOT NULL
  AND salary_min > 0;

SELECT AVG(salary_max) AS average_max_salary
FROM fact_job_postings
WHERE salary_max IS NOT NULL
  AND salary_max > 0;

SELECT
    MIN(salary_min) AS lowest_salary,
    MAX(salary_max) AS highest_salary,
    AVG(salary_min) AS average_min_salary,
    AVG(salary_max) AS average_max_salary
FROM fact_job_postings
WHERE salary_min > 0
   OR salary_max > 0;

SELECT
    CASE
        WHEN salary_max IS NULL OR salary_max = 0 THEN 'No Salary'
        WHEN salary_max < 50000 THEN 'Below 50K'
        WHEN salary_max < 100000 THEN '50K - 100K'
        WHEN salary_max < 200000 THEN '100K - 200K'
        WHEN salary_max < 300000 THEN '200K - 300K'
        ELSE '300K+'
    END AS salary_range,
    COUNT(*) AS total_jobs
FROM fact_job_postings
GROUP BY
    CASE
        WHEN salary_max IS NULL OR salary_max = 0 THEN 'No Salary'
        WHEN salary_max < 50000 THEN 'Below 50K'
        WHEN salary_max < 100000 THEN '50K - 100K'
        WHEN salary_max < 200000 THEN '100K - 200K'
        WHEN salary_max < 300000 THEN '200K - 300K'
        ELSE '300K+'
    END
ORDER BY total_jobs DESC;

SELECT
    posted_date,
    COUNT(*) AS total_jobs
FROM fact_job_postings
WHERE posted_date IS NOT NULL
GROUP BY posted_date
ORDER BY posted_date DESC;

SELECT
    DATE_TRUNC('month', posted_date) AS month,
    COUNT(*) AS total_jobs
FROM fact_job_postings
WHERE posted_date IS NOT NULL
GROUP BY DATE_TRUNC('month', posted_date)
ORDER BY month;

SELECT
    DATE_TRUNC('week', posted_date) AS week,
    COUNT(*) AS total_jobs
FROM fact_job_postings
WHERE posted_date IS NOT NULL
GROUP BY DATE_TRUNC('week', posted_date)
ORDER BY week;

SELECT
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%data scientist%'
    ) AS data_scientist_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%data engineer%'
    ) AS data_engineer_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%machine learning%'
           OR LOWER(job_title) LIKE '%ml engineer%'
    ) AS machine_learning_jobs
FROM fact_job_postings;

SELECT
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%python%'
    ) AS python_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%sql%'
    ) AS sql_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%power bi%'
           OR LOWER(raw_skills) LIKE '%powerbi%'
    ) AS powerbi_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%tableau%'
    ) AS tableau_jobs
FROM fact_job_postings;

SELECT
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%airflow%'
    ) AS airflow_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%spark%'
    ) AS spark_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%kafka%'
    ) AS kafka_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%aws%'
    ) AS aws_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%azure%'
    ) AS azure_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%gcp%'
           OR LOWER(raw_skills) LIKE '%google cloud%'
    ) AS gcp_jobs
FROM fact_job_postings;

SELECT
    l.city,
    f.category,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.city, f.category
ORDER BY total_jobs DESC
LIMIT 50;

SELECT
    c.company_name,
    l.city,
    COUNT(*) AS total_jobs
FROM fact_job_postings f
JOIN dim_company c
    ON f.company_id = c.company_id
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY c.company_name, l.city
ORDER BY total_jobs DESC
LIMIT 50;

SELECT COUNT(*) AS remote_jobs
FROM fact_job_postings f
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE LOWER(l.city) LIKE '%remote%';

SELECT COUNT(*) AS hybrid_jobs
FROM fact_job_postings
WHERE LOWER(job_title) LIKE '%hybrid%'
   OR LOWER(raw_skills) LIKE '%hybrid%';

SELECT
    TRIM(skill) AS skill,
    COUNT(*) AS job_count
FROM fact_job_postings,
LATERAL unnest(string_to_array(raw_skills, ',')) AS skill
WHERE TRIM(skill) <> ''
GROUP BY TRIM(skill)
ORDER BY job_count DESC
LIMIT 30;

SELECT
    TRIM(skill) AS skill,
    COUNT(*) AS job_count
FROM fact_job_postings,
LATERAL unnest(string_to_array(raw_skills, ',')) AS skill
WHERE (
    LOWER(job_title) LIKE '%data scientist%'
    OR LOWER(category) LIKE '%data science%'
)
AND TRIM(skill) <> ''
GROUP BY TRIM(skill)
ORDER BY job_count DESC
LIMIT 20;

SELECT
    TRIM(skill) AS skill,
    COUNT(*) AS job_count
FROM fact_job_postings,
LATERAL unnest(string_to_array(raw_skills, ',')) AS skill
WHERE (
    LOWER(job_title) LIKE '%data engineer%'
    OR LOWER(category) LIKE '%data engineer%'
)
AND TRIM(skill) <> ''
GROUP BY TRIM(skill)
ORDER BY job_count DESC
LIMIT 20;

SELECT
    TRIM(skill) AS skill,
    COUNT(*) AS job_count
FROM fact_job_postings,
LATERAL unnest(string_to_array(raw_skills, ',')) AS skill
WHERE (
    LOWER(job_title) LIKE '%machine learning%'
    OR LOWER(job_title) LIKE '%ml engineer%'
)
AND TRIM(skill) <> ''
GROUP BY TRIM(skill)
ORDER BY job_count DESC
LIMIT 20;

SELECT
    COUNT(*) AS total_jobs,
    COUNT(DISTINCT company_id) AS total_companies,
    COUNT(DISTINCT location_id) AS total_locations,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%python%'
    ) AS python_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(raw_skills) LIKE '%sql%'
    ) AS sql_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%data scientist%'
    ) AS data_scientist_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%data engineer%'
    ) AS data_engineer_jobs,
    COUNT(*) FILTER (
        WHERE LOWER(job_title) LIKE '%machine learning%'
           OR LOWER(job_title) LIKE '%ml engineer%'
    ) AS machine_learning_jobs
FROM fact_job_postings;