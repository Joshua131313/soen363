import pandas as pd
import json

raw_admissions_df = pd.read_csv("../csv_tables/ADMISSIONS_random.csv")

cleaned_admissions_df = raw_admissions_df[
    [
        "SUBJECT_ID",
        "HADM_ID",
        "ADMITTIME",
        "DISCHTIME",
        "DEATHTIME",
        "ADMISSION_TYPE",
        "ADMISSION_LOCATION",
        "DISCHARGE_LOCATION",
        "INSURANCE",
        "LANGUAGE",
        "RELIGION",
        "MARITAL_STATUS",
        "ETHNICITY",
        "DIAGNOSIS"
    ]
].copy()

admissions_column_map = {
    "SUBJECT_ID": "patient_id",
    "HADM_ID": "admission_id",
    "ADMITTIME": "admit_time",
    "DISCHTIME": "discharge_time",
    "DEATHTIME": "death_time",
    "ADMISSION_TYPE": "admission_type",
    "ADMISSION_LOCATION": "admission_location",
    "DISCHARGE_LOCATION": "discharge_location",
    "INSURANCE": "insurance",
    "LANGUAGE": "language",
    "RELIGION": "religion",
    "MARITAL_STATUS": "marital_status",
    "ETHNICITY": "ethnicity",
    "DIAGNOSIS": "diagnosis"
}

cleaned_admissions_df.rename(columns=admissions_column_map, inplace=True)

admissions_dict = cleaned_admissions_df.to_dict(orient="records")

python_literal = f"admissions = {json.dumps(admissions_dict, indent=4)}\n"

with open("admissions_dict.py", "w") as f:
    f.write(python_literal)

print("Generated admissions_dict.py")
