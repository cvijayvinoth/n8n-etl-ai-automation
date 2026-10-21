#!/usr/bin/env python3
"""
Python ETL Pipeline matching the updated n8n pipeline logic:
- Cleans whitespace & standardizes data
- Validates emails using regex
- Normalizes fee payment values
- Filters students from Chennai with valid email addresses
- Exports output to Excel (.xlsx)
"""

import re
import argparse
import pandas as pd

def to_title_case(val):
    if pd.isna(val) or not str(val).strip():
        return ""
    return " ".join(word.capitalize() for word in str(val).strip().split())

def is_valid_email(email):
    if pd.isna(email):
        return False
    regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(regex, str(email).strip()))

def normalize_fee_paid(val):
    if pd.isna(val):
        return "No"
    clean = str(val).strip().lower()
    if clean in ["yes", "y", "true", "paid", "1"]:
        return "Yes"
    return "No"

def normalize_course(course):
    if pd.isna(course) or not str(course).strip():
        return ""
    c = str(course).strip().lower()
    if c == "python":
        return "Python"
    if c in ["ml", "machine learning"]:
        return "Machine Learning"
    if c in ["ds", "data science"]:
        return "Data Science"
    return to_title_case(c)

def clean_phone(phone):
    if pd.isna(phone):
        return "Invalid/Missing"
    p = str(phone).strip()
    return p if len(p) == 10 and p.isdigit() else "Invalid/Missing"

def run_etl(input_file: str, output_file: str):
    df = pd.read_csv(input_file)

    # 1. Clean & Standardize fields
    df["Name"] = df["Name"].apply(to_title_case)
    df["Email"] = df["Email"].fillna("").astype(str).str.strip().str.lower()
    df["City"] = df["City"].apply(to_title_case).replace("", "Not Provided")
    df["Course"] = df["Course"].apply(normalize_course)
    df["Fee_Paid"] = df["Fee_Paid"].apply(normalize_fee_paid)
    df["Phone"] = df["Phone"].apply(clean_phone)
    
    # 2. Email Validation
    df["is_valid_email"] = df["Email"].apply(is_valid_email)

    # 3. Filter: City == 'Chennai' AND is_valid_email == True
    filtered_df = df[
        (df["City"].str.lower() == "chennai") & 
        (df["is_valid_email"] == True)
    ].copy()

    # 4. Export to Excel (.xlsx)
    filtered_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"ETL completed successfully: {len(filtered_df)} of {len(df)} records exported to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Student Enrollment ETL Pipeline")
    parser.add_argument("--input", default="../data/sample_students.csv", help="Input CSV path")
    parser.add_argument("--output", default="../data/chennai_verified_students.xlsx", help="Output Excel (.xlsx) path")
    args = parser.parse_args()

    run_etl(args.input, args.output)
