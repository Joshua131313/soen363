import pandas as pd
import json

raw_patients_df = pd.read_csv("../csv_tables/PATIENTS_random.csv")

cleaned_patients_df = raw_patients_df[['SUBJECT_ID', 'DOB', 'GENDER', 'EXPIRE_FLAG']].copy()

patients_column_map = {
    'SUBJECT_ID': 'patient_id',
    'DOB': 'date_of_birth',
    'GENDER': 'gender',
    'EXPIRE_FLAG': 'life_status'
}

cleaned_patients_df.rename(columns=patients_column_map, inplace=True)

patient_dict = cleaned_patients_df.to_dict(orient="records")

python_literal = f"patients = {json.dumps(patient_dict, indent=4)}\n"

with open("patients_dict.py", "w") as f:
    f.write(python_literal)

print("Generated patients_dict.py")
