#!/usr/bin/env python3
"""
Production Python ETL Pipeline matching the n8n data transformation logic.
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

def normalize_course(course):
    if pd.isna(course) or not str(course).strip():
        return ""
    c = str(course).strip().lower()
    if c == "python":
        return "Python"
    if c in ["ml", "machine learning"]:
        return "Machine Learning"
    return to_title_case(c)

def clean_phone(phone):
    if pd.isna(phone):
        return "Invalid/Missing"
    p = str(phone).strip()
    return p if len(p) == 10 and p.isdigit() else "Invalid/Missing"

def run_etl(input_file: str, output_file: str):
    df = pd.read_csv(input_file)

    # 1. Clean basic fields
    df["Name"] = df["Name"].apply(to_title_case)
    df["Email"] = df["Email"].fillna("").astype(str).str.strip().str.lower()
    df["City"] = df["City"].apply(to_title_case).replace("", "Not Provided")
    df["Course"] = df["Course"].apply(normalize_course)
    df["Fee_Paid"] = df["Fee_Paid"].fillna("").astype(str).str.strip().apply(
        lambda x: "Yes" if x.lower() == "yes" else "No"
    )
    df["Phone"] = df["Phone"].apply(clean_phone)
    
    # 2. Validation flag
    df["is_valid_email"] = df["Email"].apply(is_valid_email)

    # 3. Filter condition: is_valid_email == True OR Fee_Paid == 'Yes'
    filtered_df = df[(df["is_valid_email"] == True) | (df["Fee_Paid"] == "Yes")].copy()

    # 4. Save to output CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"ETL pipeline executed successfully: {len(filtered_df)} records written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute ETL pipeline on student data")
    parser.add_argument("--input", default="data/sample-students.csv", help="Input CSV path")
    parser.add_argument("--output", default="data/processed-students.csv", help="Output CSV path")
    args = parser.parse_args()

    run_etl(args.input, args.output)
