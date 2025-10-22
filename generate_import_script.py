# %%
#Imports
import pandas as pd
import math

# %%
#Patients
raw_patients_df = pd.read_csv("csv_tables\PATIENTS_random.csv")

cleaned_patients_df = raw_patients_df[['SUBJECT_ID', 'DOB', 'GENDER', 'EXPIRE_FLAG']]
patients_column_map = {
    'SUBJECT_ID': 'patient_id',
    'DOB': 'date_of_birth',
    'GENDER': 'gender',
    'EXPIRE_FLAG': 'life_status'
}
cleaned_patients_df.rename(columns=patients_column_map, inplace=True)

cleaned_patients_df['date_of_birth'] = "'" + cleaned_patients_df['date_of_birth'].astype(str) + "'"
cleaned_patients_df['gender'] = "'" + cleaned_patients_df['gender'].astype(str) + "'"


# %%
#Admissions
raw_admissions_df = pd.read_csv("csv_tables\ADMISSIONS_random.csv")

cleaned_admissions_df = raw_admissions_df[['HADM_ID', 'SUBJECT_ID', 'ADMISSION_TYPE', 'HOSPITAL_EXPIRE_FLAG', 'INSURANCE', 'MARITAL_STATUS', 'ADMITTIME', 'ADMISSION_LOCATION', 'DISCHTIME', 'DISCHARGE_LOCATION', 'DIAGNOSIS']]
admission_column_map = {
    'HADM_ID':'admission_id',
    'SUBJECT_ID': 'patient_id',
    'ADMISSION_TYPE': 'reason_of_visit',
    'HOSPITAL_EXPIRE_FLAG': 'death_during_stay',
    'INSURANCE': 'insurance',
    'MARITAL_STATUS': 'marital_status',
    'ADMITTIME': 'admission_date',
    'ADMISSION_LOCATION': 'admission_location',
    'DISCHTIME': 'discharge_date',
    'DISCHARGE_LOCATION': 'discharge_location',
    'DIAGNOSIS': 'diagnosis'
    }
cleaned_admissions_df.rename(columns=admission_column_map, inplace=True)

#filter out any entries that have an invalid patient_id
cleaned_admissions_df = cleaned_admissions_df[cleaned_admissions_df['patient_id'].isin(cleaned_patients_df['patient_id'])] 

#Make all the existing apostrophes doubled so SQL knows it is in the text, not the start of a string
cleaned_admissions_df['diagnosis'] = cleaned_admissions_df['diagnosis'].str.replace("'", "''")

cleaned_admissions_df['admission_date'] = "'" + cleaned_admissions_df['admission_date'].astype(str) + "'"
cleaned_admissions_df['reason_of_visit'] = "'" + cleaned_admissions_df['reason_of_visit'].astype(str) + "'"
cleaned_admissions_df['discharge_date'] = "'" + cleaned_admissions_df['discharge_date'].astype(str) + "'"
cleaned_admissions_df['insurance'] = "'" + cleaned_admissions_df['insurance'].astype(str) + "'"
cleaned_admissions_df['marital_status'] = "'" + cleaned_admissions_df['marital_status'].astype(str) + "'"
cleaned_admissions_df['admission_location'] = "'" + cleaned_admissions_df['admission_location'].astype(str) + "'"
cleaned_admissions_df['discharge_location'] = "'" + cleaned_admissions_df['discharge_location'].astype(str) + "'"
cleaned_admissions_df['diagnosis'] = "'" + cleaned_admissions_df['diagnosis'].astype(str) + "'"


# %%
#ICDCodes
raw_icdcodes_df = pd.read_csv("csv_tables\D_ICD_DIAGNOSES.csv")

icdcodes_column_map = {
    'ICD9_CODE': 'icd_code',
    'LONG_TITLE': 'description'
}

cleaned_icdcodes_df = raw_icdcodes_df[['ICD9_CODE', 'LONG_TITLE']]
cleaned_icdcodes_df.rename(columns=icdcodes_column_map, inplace=True)

cleaned_icdcodes_df['description'] = cleaned_icdcodes_df['description'].str.replace("'", "''")

cleaned_icdcodes_df['icd_code'] = "'" + cleaned_icdcodes_df['icd_code'].astype(str) + "'"
cleaned_icdcodes_df['description'] = "'" + cleaned_icdcodes_df['description'].astype(str) + "'"


# %%
#Diagnoses
raw_diagnoses_df = pd.read_csv("csv_tables\DIAGNOSES_ICD_random.csv")

diagnoses_column_map = {
    'ROW_ID' : 'diagnosis_id',
    'HADM_ID' : 'admission_id',
    'SUBJECT_ID' : 'patient_id',
    'ICD9_CODE' : 'icd_code',
    'SEQ_NUM' : 'priority'
}
cleaned_diagnoses_df = raw_diagnoses_df.rename(columns=diagnoses_column_map)

#Retrieve the columns of the DataFrame
diagnoses_columns = list(cleaned_diagnoses_df.columns)

#Find indexes of the columns that need to move to match those defined in the database
admission_id_index = diagnoses_columns.index('admission_id')
icd_code_index = diagnoses_columns.index('icd_code')

if admission_id_index > 0:
    diagnoses_columns[admission_id_index - 1], diagnoses_columns[admission_id_index] = diagnoses_columns[admission_id_index], diagnoses_columns[admission_id_index - 1]

if icd_code_index > 0:
    diagnoses_columns[icd_code_index - 1], diagnoses_columns[icd_code_index] = diagnoses_columns[icd_code_index], diagnoses_columns[icd_code_index - 1]

cleaned_diagnoses_df = cleaned_diagnoses_df[diagnoses_columns]

cleaned_diagnoses_df['icd_code'] = "'" + cleaned_diagnoses_df['icd_code'].astype(str) + "'"

#Filter out any entries that have an invalid icd_code, patient_id or admission_id
cleaned_diagnoses_df = cleaned_diagnoses_df[cleaned_diagnoses_df['icd_code'].isin(cleaned_icdcodes_df['icd_code'])]

cleaned_diagnoses_df = cleaned_diagnoses_df[cleaned_diagnoses_df['patient_id'].isin(cleaned_patients_df['patient_id'])]
cleaned_diagnoses_df = cleaned_diagnoses_df[cleaned_diagnoses_df['admission_id'].isin(cleaned_admissions_df['admission_id'])]


# %%
#ICU
raw_icu_df = pd.read_csv("csv_tables\ICUSTAYS_random.csv")

cleaned_icu_df = raw_icu_df[['ICUSTAY_ID', 'HADM_ID', 'SUBJECT_ID', 'INTIME', 'OUTTIME', 'FIRST_CAREUNIT', 'LAST_CAREUNIT', 'FIRST_WARDID', 'LAST_WARDID']]

icu_column_map = {
    'ICUSTAY_ID' : 'icu_id', 
    'HADM_ID' : 'admission_id',
    'SUBJECT_ID': 'patient_id',
    'INTIME' : 'entry_date', 
    'OUTTIME' : 'exit_date',
    'FIRST_CAREUNIT': 'first_careunit', 
    'LAST_CAREUNIT' : 'last_careunit',
    'FIRST_WARDID': 'first_wardid',
    'LAST_WARDID' : 'last_wardid'
}
cleaned_icu_df.rename(columns= icu_column_map, inplace=True)

icu_columns = list(cleaned_icu_df.columns)

exit_date_index = icu_columns.index('exit_date')
last_wardid_index = icu_columns.index('last_wardid')

if exit_date_index > 0:
    icu_columns[exit_date_index - 1], icu_columns[exit_date_index] = icu_columns[exit_date_index], icu_columns[exit_date_index - 1]

if last_wardid_index > 0:
    icu_columns[last_wardid_index - 1], icu_columns[last_wardid_index] = icu_columns[last_wardid_index], icu_columns[last_wardid_index - 1]

cleaned_icu_df = cleaned_icu_df[icu_columns]

#Filter out any entries with an invalid admission_id
cleaned_icu_df = cleaned_icu_df[cleaned_icu_df['admission_id'].isin(cleaned_admissions_df['admission_id'])]

cleaned_icu_df['entry_date'] = "'" + cleaned_icu_df['entry_date'].astype(str) + "'"
cleaned_icu_df['exit_date'] = "'" + cleaned_icu_df['exit_date'].astype(str) + "'"
cleaned_icu_df['first_careunit'] = "'" + cleaned_icu_df['first_careunit'].astype(str) + "'"
cleaned_icu_df['last_careunit'] = "'" + cleaned_icu_df['last_careunit'].astype(str) + "'"



# %%
#NoteEvents
raw_noteevents_df = pd.read_csv("csv_tables\\NOTEEVENTS_random.csv")

cleaned_noteevents_df = raw_noteevents_df[["ROW_ID", "HADM_ID", "SUBJECT_ID", "CGID", "CATEGORY", "TEXT", "ISERROR", "CHARTDATE", "CHARTTIME", "STORETIME"]]
cleaned_noteevents_df['note_timestamp'] = None

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

cleaned_noteevents_df = cleaned_noteevents_df[cleaned_noteevents_df['patient_id'].isin(cleaned_patients_df['patient_id'])]
cleaned_noteevents_df = cleaned_noteevents_df[cleaned_noteevents_df['admission_id'].isin(cleaned_admissions_df['admission_id'])]

#Iterate over the rows, check the type and assign note_timestamp with either CHARTDATE, CHARTTIME or STORETIME
#Then, delete CHARTDATE, CHARTTIME and STORETIME
nan_float = float('nan')
for index, row in cleaned_noteevents_df.iterrows():
    chart_time = row['CHARTTIME']
    chart_date = row['CHARTDATE']
    if pd.isna(chart_time):
        cleaned_noteevents_df.at[index, "note_timestamp"] = chart_date
    else:
        cleaned_noteevents_df.at[index, "note_timestamp"] = chart_time

cleaned_noteevents_df.drop(['CHARTDATE', 'CHARTTIME', 'STORETIME'], axis=1, inplace=True)

#Double all apostrophes for SQL
cleaned_noteevents_df['note_text'] = cleaned_noteevents_df['note_text'].str.replace("'", "''")

cleaned_noteevents_df.loc[cleaned_noteevents_df['author'].isna(), 'author'] = "NULL"
cleaned_noteevents_df.loc[cleaned_noteevents_df['has_error'].isna(), 'has_error'] = "NULL"


cleaned_noteevents_df['note_type'] = "'" + cleaned_noteevents_df['note_type'].astype(str) + "'"
cleaned_noteevents_df['note_text'] = "'" + cleaned_noteevents_df['note_text'].astype(str) + "'"
cleaned_noteevents_df['note_timestamp'] = "'" + cleaned_noteevents_df['note_timestamp'].astype(str) + "'"

# %%
def generateInsertStatement(dataframe: pd.DataFrame, table_name: str):
    dataframe_string = f"INSERT INTO {table_name} ("
    columns_list = dataframe.columns.tolist()
    column_list_size = len(columns_list)

    for index, column in enumerate(columns_list):
        if(index == column_list_size - 1):
            dataframe_string += f"{column})"
            continue

        dataframe_string += f"{column}, "
    
    dataframe_string += "\nVALUES\n"
    
    is_first_row = True
    for index, row in dataframe.iterrows():
        if(is_first_row):
            dataframe_string += "("
            is_first_row = False
        else:
            dataframe_string += ",\n("
        row_size = len(row)
        for el_index, element in enumerate(row):
            if(el_index == row_size - 1):
                dataframe_string += f"{element}"
                continue

            dataframe_string += f"{element}, "
        dataframe_string += ")"

    dataframe_string += ';'
    return dataframe_string

def separateInsertStatement(dataframe: pd.DataFrame, table_name: str):
    insert_string = ""

    number_of_entries = dataframe.shape[0]
    number_of_iterations = math.ceil(number_of_entries/1000)

    for i in range(number_of_iterations):
        starting_index = i * 1000
        end_index = starting_index + 1000
        insert_string += generateInsertStatement(dataframe.iloc[starting_index:end_index], table_name) + "\n"


    return insert_string

# %%
# print(separateInsertStatement(cleaned_patients_df, 'Patients'))
with open("insertvalues.sql", "w") as file:
    file.write("USE HospitalSystem;\n")
    file.write(separateInsertStatement(cleaned_patients_df, 'Patients') + "\n")
    file.write(separateInsertStatement(cleaned_admissions_df, 'Admissions') + "\n")
    file.write(separateInsertStatement(cleaned_icdcodes_df, 'ICDCode') + "\n")
    file.write(separateInsertStatement(cleaned_icu_df, 'ICU') + "\n")
    file.write(separateInsertStatement(cleaned_diagnoses_df, 'Diagnoses') + "\n")
    file.write(separateInsertStatement(cleaned_noteevents_df, 'NoteEvents') + "\n")


