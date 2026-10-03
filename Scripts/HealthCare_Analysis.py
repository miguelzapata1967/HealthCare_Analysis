from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# HEALTHCARE PATIENT SURVEY
# DATA PROFILING AND CONSERVATIVE CLEANING
# ============================================================

PROJECT_ROOT = Path(
    r"C:\Users\mexar\OneDrive\DE_Academy\HealthCare_Analysis"
)

SOURCE_FILE = (
    PROJECT_ROOT
    / "Data"
    / "Health Care_Patient_survey_source.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "Data" / "Analysis_Outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_FILE = OUTPUT_DIR / "Health_Care_Patient_Survey_Cleaned.csv"
PROFILE_FILE = OUTPUT_DIR / "column_profile.csv"
DUPLICATE_FILE = OUTPUT_DIR / "exact_duplicate_rows.csv"
MISSING_FILE = OUTPUT_DIR / "missing_values_summary.csv"
UNIQUE_FILE = OUTPUT_DIR / "unique_values_summary.csv"


# ============================================================
# 1. LOAD SOURCE DATA
# ============================================================

print("\n" + "=" * 70)
print("HEALTHCARE PATIENT SURVEY - DATA VALIDATION")
print("=" * 70)

if not SOURCE_FILE.exists():
    raise FileNotFoundError(
        f"\nSource file was not found:\n{SOURCE_FILE}"
    )

df = pd.read_csv(SOURCE_FILE, low_memory=False)

print("\nSOURCE FILE")
print(SOURCE_FILE)

print("\nDATASET SHAPE")
print(f"Rows:    {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# ============================================================
# 2. ORIGINAL COLUMN NAMES
# ============================================================

print("\n" + "=" * 70)
print("ORIGINAL COLUMNS")
print("=" * 70)

for number, column in enumerate(df.columns, start=1):
    print(f"{number:>3}. {column}")


# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================
# This changes formatting only:
# "Hospital Name" -> "hospital_name"
# It does NOT change the underlying data.

original_columns = df.columns.tolist()

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^\w]+", "_", regex=True)
    .str.strip("_")
)

print("\n" + "=" * 70)
print("STANDARDIZED COLUMN NAMES")
print("=" * 70)

for old, new in zip(original_columns, df.columns):
    print(f"{old}  -->  {new}")


# ============================================================
# 4. REMOVE LEADING/TRAILING SPACES FROM TEXT
# ============================================================

text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].apply(
        lambda value: value.strip()
        if isinstance(value, str)
        else value
    )


# ============================================================
# 5. IDENTIFY BLANK TEXT VALUES
# ============================================================

blank_summary = []

for column in text_columns:

    blank_count = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    blank_summary.append(
        {
            "column": column,
            "blank_text_values": int(blank_count)
        }
    )

blank_df = pd.DataFrame(blank_summary)


# ============================================================
# 6. MISSING VALUES
# ============================================================

missing_summary = pd.DataFrame(
    {
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percent":
            (df.isna().mean().values * 100).round(2)
    }
)

missing_summary = missing_summary.merge(
    blank_df,
    on="column",
    how="left"
)

missing_summary["blank_text_values"] = (
    missing_summary["blank_text_values"]
    .fillna(0)
    .astype(int)
)

missing_summary.to_csv(MISSING_FILE, index=False)

print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

print(
    missing_summary[
        (missing_summary["missing_count"] > 0)
        | (missing_summary["blank_text_values"] > 0)
    ].to_string(index=False)
)


# ============================================================
# 7. EXACT DUPLICATE ROWS
# ============================================================

duplicate_mask = df.duplicated(keep=False)
duplicate_rows = df[duplicate_mask].copy()

duplicate_count = df.duplicated().sum()

print("\n" + "=" * 70)
print("EXACT DUPLICATE CHECK")
print("=" * 70)

print(f"Exact duplicate rows: {duplicate_count:,}")

if not duplicate_rows.empty:
    duplicate_rows.to_csv(DUPLICATE_FILE, index=False)

    print(
        f"Duplicate records were NOT deleted.\n"
        f"They were exported for review:\n{DUPLICATE_FILE}"
    )
else:
    print("No exact duplicate rows were identified.")


# ============================================================
# 8. UNIQUE VALUES PER COLUMN
# ============================================================

unique_summary = pd.DataFrame(
    {
        "column": df.columns,
        "unique_values": [
            df[column].nunique(dropna=True)
            for column in df.columns
        ]
    }
)

unique_summary.to_csv(UNIQUE_FILE, index=False)

print("\n" + "=" * 70)
print("UNIQUE VALUE COUNTS")
print("=" * 70)

print(unique_summary.to_string(index=False))


# ============================================================
# 9. DATA TYPE PROFILE
# ============================================================

profile_rows = []

for column in df.columns:

    non_null = df[column].dropna()

    sample_values = (
        non_null.astype(str)
        .drop_duplicates()
        .head(5)
        .tolist()
    )

    profile_rows.append(
        {
            "column": column,
            "data_type": str(df[column].dtype),
            "rows": len(df),
            "non_null": df[column].notna().sum(),
            "nulls": df[column].isna().sum(),
            "unique_values": df[column].nunique(dropna=True),
            "sample_values": " | ".join(sample_values)
        }
    )

profile_df = pd.DataFrame(profile_rows)

profile_df.to_csv(PROFILE_FILE, index=False)


# ============================================================
# 10. SEARCH FOR ASSIGNMENT-RELATED COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("POTENTIAL STAR-SCHEMA COLUMNS")
print("=" * 70)

search_groups = {

    "COUNTRY / GEOGRAPHY": [
        "country",
        "county",
        "state",
        "city",
        "zip",
        "location"
    ],

    "HOSPITAL": [
        "hospital",
        "facility",
        "provider"
    ],

    "MEASURE": [
        "measure"
    ],

    "SURVEY": [
        "survey",
        "question",
        "answer"
    ],

    "RATING": [
        "rating",
        "star"
    ],

    "RESPONSE": [
        "response",
        "percent"
    ],

    "DATE": [
        "date",
        "start",
        "end"
    ]
}

for group, keywords in search_groups.items():

    matches = [
        column
        for column in df.columns
        if any(keyword in column for keyword in keywords)
    ]

    print(f"\n{group}")

    if matches:
        for match in matches:
            print(f"  - {match}")
    else:
        print("  No obvious matching columns found.")


# ============================================================
# 11. NUMERIC COLUMN VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("NUMERIC COLUMN SUMMARY")
print("=" * 70)

numeric_columns = df.select_dtypes(include=np.number).columns

if len(numeric_columns) > 0:

    numeric_summary = (
        df[numeric_columns]
        .describe()
        .transpose()
    )

    print(numeric_summary.to_string())

    numeric_summary.to_csv(
        OUTPUT_DIR / "numeric_summary.csv"
    )

else:
    print(
        "No columns are currently recognized by Pandas "
        "as numeric."
    )


# ============================================================
# 12. DATE-LIKE COLUMN REVIEW
# ============================================================
# We only IDENTIFY possible date columns here.
# We do not convert them automatically.

date_candidates = [
    column
    for column in df.columns
    if any(
        keyword in column
        for keyword in ["date", "start", "end"]
    )
]

print("\n" + "=" * 70)
print("POSSIBLE DATE COLUMNS")
print("=" * 70)

if date_candidates:

    for column in date_candidates:

        print(f"\n{column}")

        samples = (
            df[column]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        for value in samples:
            print(f"  {value}")

else:
    print("No obvious date columns identified.")


# ============================================================
# 13. POSSIBLE PERCENTAGE COLUMNS
# ============================================================

percentage_candidates = [
    column
    for column in df.columns
    if "percent" in column
    or "percentage" in column
    or "rate" in column
]

print("\n" + "=" * 70)
print("POSSIBLE RATE / PERCENTAGE COLUMNS")
print("=" * 70)

for column in percentage_candidates:
    print(f"  - {column}")


# ============================================================
# 14. SAVE CONSERVATIVELY CLEANED DATA
# ============================================================
# At this stage we have only:
# - standardized column names
# - trimmed leading/trailing text spaces
#
# We have NOT:
# - removed duplicates
# - removed nulls
# - filled missing values
# - changed survey values
# - changed ratings
# - changed response rates
# - inferred dates

df.to_csv(CLEAN_FILE, index=False)


# ============================================================
# 15. FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

print(f"""
Original rows:       {len(df):,}
Original columns:    {len(df.columns):,}
Exact duplicates:    {duplicate_count:,}

Files created:

Cleaned working CSV:
{CLEAN_FILE}

Column profile:
{PROFILE_FILE}

Missing-value summary:
{MISSING_FILE}

Unique-value summary:
{UNIQUE_FILE}
""")

if not duplicate_rows.empty:
    print(f"Duplicate review file:\n{DUPLICATE_FILE}")

print("""
IMPORTANT:
No questionable records were automatically deleted.

Review the findings before making additional cleaning decisions
or creating the Power BI dimension and fact tables.
""")
# ============================================================
# 16. INVESTIGATE HOSPITAL IDENTIFIERS
# ============================================================

print("\n" + "=" * 70)
print("HOSPITAL NAME / PROVIDER ID INVESTIGATION")
print("=" * 70)

hospital_lookup = (
    df[
        [
            "provider_id",
            "hospital_name",
            "address",
            "city",
            "state",
            "zip_code"
        ]
    ]
    .drop_duplicates()
    .sort_values(["hospital_name", "provider_id"])
)

name_counts = (
    hospital_lookup
    .groupby("hospital_name")["provider_id"]
    .nunique()
)

shared_names = name_counts[name_counts > 1]

print(f"Unique providers: {df['provider_id'].nunique():,}")
print(f"Unique hospital names: {df['hospital_name'].nunique():,}")
print(
    f"Hospital names associated with multiple provider IDs: "
    f"{len(shared_names):,}"
)

if not shared_names.empty:

    shared_hospitals = hospital_lookup[
        hospital_lookup["hospital_name"].isin(shared_names.index)
    ]

    print("\nHospitals requiring review:")
    print(shared_hospitals.to_string(index=False))

    shared_hospitals.to_csv(
        OUTPUT_DIR / "hospital_name_provider_review.csv",
        index=False
    )


# ============================================================
# 17. INVESTIGATE ANALYTICAL VALUES
# ============================================================

print("\n" + "=" * 70)
print("ANALYTICAL VALUE INVESTIGATION")
print("=" * 70)

analysis_columns = [
    "patient_survey_star_rating",
    "answer_percent",
    "linear_mean_value",
    "number_of_completed_surveys",
    "survey_response_rate_percent"
]

for column in analysis_columns:

    print("\n" + "-" * 70)
    print(column.upper())
    print("-" * 70)

    counts = (
        df[column]
        .value_counts(dropna=False)
        .head(30)
    )

    print(counts.to_string())


# ============================================================
# 18. INVESTIGATE FOOTNOTE VALUES
# ============================================================

print("\n" + "=" * 70)
print("FOOTNOTE VALUE INVESTIGATION")
print("=" * 70)

footnote_columns = [
    column
    for column in df.columns
    if "footnote" in column
]

for column in footnote_columns:

    print("\n" + "-" * 70)
    print(column.upper())
    print("-" * 70)

    print(
        df[column]
        .value_counts(dropna=False)
        .head(30)
        .to_string()
    )