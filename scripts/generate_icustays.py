import pandas as pd

raw_icu_df = pd.read_csv("../csv_tables/ICUSTAYS_random.csv")

cleaned_icu_df = raw_icu_df[['ICUSTAY_ID', 'HADM_ID', 'SUBJECT_ID', 'INTIME', 'OUTTIME', 
                             'FIRST_CAREUNIT', 'LAST_CAREUNIT', 'FIRST_WARDID', 'LAST_WARDID']].copy()

icu_column_map = {
    'ICUSTAY_ID': 'icu_id',
    'HADM_ID': 'admission_id',
    'SUBJECT_ID': 'patient_id',
    'INTIME': 'entry_date',
    'OUTTIME': 'exit_date',
    'FIRST_CAREUNIT': 'first_careunit',
    'LAST_CAREUNIT': 'last_careunit',
    'FIRST_WARDID': 'first_wardid',
    'LAST_WARDID': 'last_wardid'
}
cleaned_icu_df.rename(columns=icu_column_map, inplace=True)

cleaned_icu_df = cleaned_icu_df.where(pd.notnull(cleaned_icu_df), None)

icu_list = cleaned_icu_df.to_dict(orient='records')

with open("icu_dict.py", "w", encoding="utf-8") as f:
    f.write("icu_data = [\n")
    for item in icu_list:
        f.write(f"    {item},\n")
    f.write("]\n")

print("icu_dict.py has been created with icu_data!")
