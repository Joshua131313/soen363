import pandas as pd

raw_noteevents_df = pd.read_csv("../csv_tables/NOTEEVENTS_random.csv")

cleaned_noteevents_df = raw_noteevents_df[["ROW_ID", "HADM_ID", "SUBJECT_ID", "CGID", "CATEGORY", "TEXT", "ISERROR", "CHARTDATE", "CHARTTIME", "STORETIME"]].copy()

noteevents_column_map = {
    "ROW_ID": "note_id", 
    "HADM_ID": "admission_id", 
    "SUBJECT_ID": "patient_id", 
    "CGID": "author", 
    "CATEGORY": "note_type", 
    "TEXT": "note_text", 
    "ISERROR": "has_error",
}
cleaned_noteevents_df.rename(columns=noteevents_column_map, inplace=True)

cleaned_noteevents_df['note_timestamp'] = cleaned_noteevents_df['CHARTTIME'].combine_first(cleaned_noteevents_df['CHARTDATE'])

cleaned_noteevents_df.drop(['CHARTDATE', 'CHARTTIME', 'STORETIME'], axis=1, inplace=True)

cleaned_noteevents_df = cleaned_noteevents_df.where(pd.notnull(cleaned_noteevents_df), None)

noteevents_list = cleaned_noteevents_df.to_dict(orient='records')

with open("noteevents_dict.py", "w", encoding="utf-8") as f:
    f.write("noteevents_data = [\n")
    for item in noteevents_list:
        f.write(f"    {item},\n")
    f.write("]\n")

print("noteevents_dict.py has been created with noteevents_data!")
