import json
import pandas as pd
import glob
import os


def load_latest_raw():

    files = glob.glob("data/raw/*.json")

    if not files:
        raise FileNotFoundError(
            "No raw files found, run extract.py first"
        )

    latest = max(files, key=os.path.getctime)

    print(f"Loading {latest}")

    with open(latest, "r", encoding="utf-8") as f:
        data = json.load(f)

    return pd.DataFrame(data)


def clean(df):

    # Remove rows without required fields
    df = df.dropna(subset=["title", "company"])

    # Remove duplicates inside the current extraction
    df = df.drop_duplicates(
        subset=["title", "company", "location"]
    )

    # Clean text
    df["title"] = df["title"].astype(str).str.strip()

    df["company"] = df["company"].astype(str).str.strip()

    df["location"] = (
        df["location"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["category"] = (
        df["category"]
        .fillna("General")
        .astype(str)
        .str.strip()
    )

    # Skills
    df["skills"] = df["skills"].apply(
        lambda s: s if isinstance(s, list) else []
    )

    df["raw_skills"] = df["skills"].apply(
        lambda s: ", ".join(s)
    )

    # Salary
    df["salary"] = df["salary"].fillna(0)

    # Link
    df["link"] = df["link"].fillna("").astype(str).str.strip()

    # Remove rows without a source URL
    df = df[df["link"] != ""]

    return df.reset_index(drop=True)


def run():

    df = load_latest_raw()

    df = clean(df)

    print(f"{len(df)} rows after cleaning")

    return df


if __name__ == "__main__":

    result = run()

    print(
        result[
            [
                "title",
                "company",
                "category",
                "location",
                "link"
            ]
        ].head()
    )