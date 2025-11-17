# generate_diagnoses_dict.py
import pandas as pd

# ICD Codes (generates for d icd)
raw_icdcodes_df = pd.read_csv("../csv_tables/D_ICD_DIAGNOSES.csv")
icdcodes_column_map = {'ICD9_CODE': 'icd_code', 'LONG_TITLE': 'description'}
cleaned_icdcodes_df = raw_icdcodes_df[['ICD9_CODE', 'LONG_TITLE']].copy()
cleaned_icdcodes_df.rename(columns=icdcodes_column_map, inplace=True)
cleaned_icdcodes_df = cleaned_icdcodes_df.where(pd.notnull(cleaned_icdcodes_df), None)

icd_list = cleaned_icdcodes_df.to_dict(orient='records')
with open("icd_dict.py", "w", encoding="utf-8") as f:
    f.write("icd_data = [\n")
    for item in icd_list:
        f.write(f"    {item},\n")
    f.write("]\n")
print("icd_dict.py has been created with icd_data!")

# Diagnoses (generates for diagnoses icd)
raw_diagnoses_df = pd.read_csv("../csv_tables/DIAGNOSES_ICD_random.csv")
diagnoses_column_map = {'ROW_ID': 'diagnosis_id', 'HADM_ID': 'admission_id', 'SUBJECT_ID': 'patient_id', 'ICD9_CODE': 'icd_code', 'SEQ_NUM': 'priority'}
cleaned_diagnoses_df = raw_diagnoses_df.rename(columns=diagnoses_column_map)
cleaned_diagnoses_df = cleaned_diagnoses_df.where(pd.notnull(cleaned_diagnoses_df), None)

valid_icd_codes = set(cleaned_icdcodes_df['icd_code'])
cleaned_diagnoses_df = cleaned_diagnoses_df[cleaned_diagnoses_df['icd_code'].isin(valid_icd_codes)]

diagnoses_list = cleaned_diagnoses_df.to_dict(orient='records')
with open("diagnoses_dict.py", "w", encoding="utf-8") as f:
    f.write("diagnoses_data = [\n")
    for item in diagnoses_list:
        f.write(f"    {item},\n")
    f.write("]\n")
print("diagnoses_dict.py has been created with diagnoses_data!")
