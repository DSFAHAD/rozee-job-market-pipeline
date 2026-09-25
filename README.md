# 📊 Rozee.pk Job Market Data Engineering Pipeline

> **End-to-end Data Engineering pipeline for collecting, cleaning, validating, transforming, storing, analyzing, and visualizing Pakistan's tech job-market data from Rozee.pk.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)](https://plotly.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)](https://github.com/features/actions)

---

## 🚀 Live Dashboard

Explore the deployed dashboard:

### 🌐 [Open Rozee Job Market Dashboard](https://rozee-job-market-pipeline.streamlit.app/)

The dashboard provides interactive insights into Pakistan's technology job market, including:

* 📈 Total job postings
* 🏢 Companies hiring
* 🛠️ Skills in demand
* 📍 Jobs by city
* 📂 Job categories
* 📋 Raw processed job-market data
* ⬇️ Downloadable CSV dataset

---

# 🎯 Project Overview

This project demonstrates how a real-world job-market dataset can be transformed into a structured and analytics-ready data platform.

The pipeline follows an end-to-end Data Engineering workflow:

```text
Rozee.pk
    │
    ▼
┌───────────────┐
│    Extract    │
│ Python / HTTP │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Transform   │
│ Clean / Parse │
│ Deduplicate   │
└───────┬───────┘
        │
        ▼
┌────────────────────┐
│      PostgreSQL    │
│                    │
│ Dimension Tables   │
│ Fact Table         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Data Quality Tests │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Analytics / Export │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Processed CSV      │
│                    │
│ ML / DS Ready      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Streamlit Dashboard│
└────────────────────┘
```

---

# 🏗️ Architecture

```text
                 ┌──────────────────┐
                 │     Rozee.pk     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Python Extractor │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Transformation   │
                 │ Pandas / Python  │
                 └────────┬─────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │       PostgreSQL        │
              │                         │
              │  dim_company            │
              │  dim_location           │
              │  dim_skill              │
              │  fact_job_postings      │
              └────────────┬────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌─────────────────┐      ┌─────────────────┐
      │ Data Quality    │      │ SQL Analytics   │
      │ Validation      │      │                 │
      └────────┬────────┘      └────────┬────────┘
               │                        │
               └───────────┬────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Processed CSV   │
                  └────────┬────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
       ┌─────────────────┐   ┌──────────────────┐
       │ Streamlit       │   │ Data Scientists  │
       │ Dashboard       │   │ / ML Engineers   │
       └─────────────────┘   └──────────────────┘
```

---

# 🛠️ Technologies Used

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Pipeline development               |
| Pandas         | Data transformation and processing |
| Requests       | Data extraction                    |
| BeautifulSoup  | Web data extraction                |
| PostgreSQL     | Data warehouse/database            |
| SQLAlchemy     | Database interaction               |
| SQL            | Analytics and validation           |
| Streamlit      | Interactive dashboard              |
| Plotly         | Data visualization                 |
| GitHub Actions | CI/CD                              |
| python-dotenv  | Environment configuration          |

---

# 📂 Project Structure

```text
rozee-job-market-pipeline/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── db.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── analytics.py
│   ├── validate.py
│   ├── export_csv.py
│   ├── sample_data.py
│   └── backfill_category.py
│
├── tests/
│   └── data_quality.py
│
├── sql/
│   └── analytics.sql
│
└── data/
    ├── raw/
    ├── sample/
    │   └── jobs.json
    │
    ├── processed/
    │   └── job_market.csv
    │
    └── exports/
```

---

# 🔄 Pipeline Workflow

## 1. Extract

Python extracts job-market information such as:

* Job title
* Company
* Location
* Category
* Salary
* Skills
* Source URL
* Posting information

Raw extraction files are stored locally and are excluded from GitHub.

---

## 2. Transform

The transformation layer uses Python and Pandas to:

* Remove invalid records
* Remove duplicates
* Clean company names
* Clean job titles
* Normalize locations
* Handle missing categories
* Process skills
* Convert skills into a usable format
* Validate source URLs

---

## 3. Load

Cleaned data is loaded into PostgreSQL.

The database follows a dimensional structure:

### Dimension Tables

```text
dim_company
dim_location
dim_skill
```

### Fact Table

```text
fact_job_postings
```

This structure allows analytical SQL queries while reducing repeated company and location information.

---

# 🧪 Data Quality

The project contains automated data-quality checks.

Current checks include:

```text
✓ Job table is not empty
✓ No duplicate source URLs
✓ No empty job titles
✓ No NULL company IDs
✓ No NULL location IDs
✓ No orphan company IDs
✓ No orphan location IDs
✓ No empty source URLs
```

Example:

```text
==============================
QUALITY CHECK SUMMARY
==============================

PASS: All data quality checks passed.
```

---

# ⚙️ CI/CD

GitHub Actions automatically runs the pipeline validation process.

The CI workflow:

```text
Push / Pull Request
        │
        ▼
Install Python dependencies
        │
        ▼
Start PostgreSQL
        │
        ▼
Initialize database
        │
        ▼
Load sample dataset
        │
        ▼
Run data quality checks
        │
        ▼
PASS / FAIL
```

This ensures that pipeline changes can be tested automatically before being considered valid.

---

# 📊 Dashboard

The project includes an interactive Streamlit dashboard.

### Dashboard Features

* Total postings
* Unique companies
* Unique cities
* Top hiring companies
* Most frequently appearing skills
* Job distribution by city
* Category-based filtering
* Raw dataset exploration
* CSV download

### Live Dashboard

🌐 **https://rozee-job-market-pipeline.streamlit.app/**

---

# 🧠 Dataset for Data Science & Machine Learning

One of the goals of this project is to make the processed job-market data useful beyond the dashboard.

The processed dataset is available here:

```text
data/processed/job_market.csv
```

The dashboard also provides a **Download Job Market CSV** button.

### 👨‍💻 For Data Scientists

The dataset can be downloaded and used for:

* Exploratory Data Analysis
* Skill-demand analysis
* Salary analysis
* Job-market trends
* Feature engineering
* Statistical analysis
* Visualization
* NLP experiments

Example:

```python
import pandas as pd

df = pd.read_csv(
    "job_market.csv"
)

print(df.head())
print(df.shape)
```

### 🤖 For ML Engineers

The dataset can also serve as a starting point for machine-learning experiments.

Possible projects include:

* Salary prediction
* Job-category classification
* Job-title classification
* Skill-demand prediction
* Job clustering
* Job recommendation systems
* NLP-based job similarity
* Skill extraction
* Employment trend analysis

For example, an ML engineer could create a model that predicts a salary range based on:

```text
Job Title
Company
City
Category
Skills
```

The dataset is therefore designed to be **ML/DS-ready after additional task-specific preprocessing and feature engineering**.

> **Important:** The CSV is an analytics/ML starting dataset. A specific ML task will still require appropriate preprocessing, feature engineering, target selection, train/test splitting, and validation.

---

# 📥 Download Dataset

You can download the processed dataset directly from the repository:

**[`data/processed/job_market.csv`](data/processed/job_market.csv)**

Or use the download button available inside the live dashboard.

### Dataset Fields

| Column         | Description                    |
| -------------- | ------------------------------ |
| `posting_id`   | Unique job posting ID          |
| `job_title`    | Job title                      |
| `company_name` | Hiring company                 |
| `city`         | Job location                   |
| `category`     | Job category                   |
| `salary_min`   | Minimum salary when available  |
| `salary_max`   | Maximum salary when available  |
| `posted_date`  | Job posting date               |
| `raw_skills`   | Skills associated with the job |
| `source_url`   | Original job posting URL       |
| `scraped_at`   | Extraction timestamp           |

---

# 🔬 Possible Data Science Projects

This dataset can be extended into several Data Science projects.

### Salary Prediction

```text
Skills + Job Title + City + Category
                 ↓
          ML Regression
                 ↓
        Salary Prediction
```

### Job Classification

```text
Job Title + Skills
       ↓
Text Processing / NLP
       ↓
Classification Model
       ↓
Job Category
```

### Skill Demand Analysis

```text
Job Postings
      ↓
Skill Extraction
      ↓
Frequency Analysis
      ↓
Most Requested Skills
```

### Job Recommendation

```text
Candidate Skills
       +
Job Requirements
       ↓
Similarity Model
       ↓
Recommended Jobs
```

---

# ▶️ Run Locally

Clone the repository:

```bash
git clone https://github.com/DSFAHAD/rozee-job-market-pipeline.git
```

Move into the project:

```bash
cd rozee-job-market-pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DB_URL=postgresql://postgres:postgres@localhost:5432/job_market_db
```

Initialize the database:

```bash
python src/db.py
```

Run the pipeline:

```bash
python src/load.py
```

Run data-quality checks:

```bash
python tests/data_quality.py
```

Run the dashboard:

```bash
streamlit run app.py
```

---

# 🔐 Environment Variables

Database credentials should be stored in `.env` and should **never be committed to GitHub**.

Example:

```env
DB_URL=postgresql://username:password@localhost:5432/database_name
```

The `.env` file is included in `.gitignore`.

---

# 📈 Future Improvements

Planned improvements include:

* Automated scheduled scraping
* Incremental data ingestion
* Historical job tracking
* Salary normalization
* Advanced SQL analytics
* More comprehensive data-quality tests
* Airflow orchestration
* Docker containerization
* Cloud database deployment
* Automated dataset refresh
* NLP-based skill extraction
* Machine-learning models
* Job recommendation system
* Time-series job-market analysis

---

# 🎓 What This Project Demonstrates

This project demonstrates practical experience with:

```text
Python
   ↓
Data Extraction
   ↓
Data Cleaning
   ↓
Data Transformation
   ↓
PostgreSQL
   ↓
Dimensional Modeling
   ↓
SQL Analytics
   ↓
Data Quality
   ↓
CI/CD
   ↓
CSV Data Product
   ↓
Streamlit Dashboard
   ↓
Data Science / ML
```

It combines **Data Engineering, Analytics, Data Science, and ML-ready data preparation** into one end-to-end project.

---

# 👨‍💻 Author

**Fahad**

Computer Science Student
Aspiring Data Scientist / ML & Data Engineering

GitHub:
https://github.com/DSFAHAD

---

# ⭐ If You Find This Project Useful

If this project helps you learn about Data Engineering, Data Science, or Machine Learning, consider giving the repository a ⭐ on GitHub.

---

## 📜 Disclaimer

This project is intended for educational, portfolio, and analytical purposes. The availability and contents of job postings may change over time. Always respect the source website's terms, policies, and applicable laws when collecting or using web data.
