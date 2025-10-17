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

cleaned_admissions_df = raw_admissions_df[['HADM_ID', 'SUBJECT_ID', 'ADMISSION_TYPE', 'HOSPITAL_EXPIRE_FLAG', 'INSURANCE', 'MARITAL_STATUS', 'ADMITTIME', 'DISCHTIME']]
admission_column_map = {
    'HADM_ID':'admission_id',
    'SUBJECT_ID': 'patient_id',
    'ADMISSION_TYPE': 'reason_of_visit',
    'HOSPITAL_EXPIRE_FLAG': 'death_during_stay',
    'INSURANCE': 'insurance',
    'MARITAL_STATUS': 'marital_status',
    'ADMITTIME': 'admission_date',
    'DISCHTIME': 'discharge_date'
    }
cleaned_admissions_df.rename(columns=admission_column_map, inplace=True)

#filter out any entries that have an invalid patient_id
cleaned_admissions_df = cleaned_admissions_df[cleaned_admissions_df['patient_id'].isin(cleaned_patients_df['patient_id'])] 

cleaned_admissions_df['admission_date'] = "'" + cleaned_admissions_df['admission_date'].astype(str) + "'"
cleaned_admissions_df['reason_of_visit'] = "'" + cleaned_admissions_df['reason_of_visit'].astype(str) + "'"
cleaned_admissions_df['discharge_date'] = "'" + cleaned_admissions_df['discharge_date'].astype(str) + "'"
cleaned_admissions_df['insurance'] = "'" + cleaned_admissions_df['insurance'].astype(str) + "'"
cleaned_admissions_df['marital_status'] = "'" + cleaned_admissions_df['marital_status'].astype(str) + "'"


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

cleaned_icu_df = raw_icu_df[['ICUSTAY_ID', 'HADM_ID', 'INTIME', 'OUTTIME', 'LAST_CAREUNIT', 'LAST_WARDID']]

icu_column_map = {
    'ICUSTAY_ID' : 'icu_id', 
    'HADM_ID' : 'admission_id', 
    'INTIME' : 'entry_date', 
    'OUTTIME' : 'exit_date', 
    'LAST_CAREUNIT' : 'icu_type', 
    'LAST_WARDID' : 'ward_location'
}
cleaned_icu_df.rename(columns= icu_column_map, inplace=True)

icu_columns = list(cleaned_icu_df.columns)

exit_date_index = icu_columns.index('exit_date')
ward_location_index = icu_columns.index('ward_location')

if exit_date_index > 0:
    icu_columns[exit_date_index - 1], icu_columns[exit_date_index] = icu_columns[exit_date_index], icu_columns[exit_date_index - 1]

if ward_location_index > 0:
    icu_columns[ward_location_index - 1], icu_columns[ward_location_index] = icu_columns[ward_location_index], icu_columns[ward_location_index - 1]

cleaned_icu_df = cleaned_icu_df[icu_columns]

#Filter out any entries with an invalid admission_id
cleaned_icu_df = cleaned_icu_df[cleaned_icu_df['admission_id'].isin(cleaned_admissions_df['admission_id'])]

cleaned_icu_df['entry_date'] = "'" + cleaned_icu_df['entry_date'].astype(str) + "'"
cleaned_icu_df['exit_date'] = "'" + cleaned_icu_df['exit_date'].astype(str) + "'"
cleaned_icu_df['icu_type'] = "'" + cleaned_icu_df['icu_type'].astype(str) + "'"


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

# %%
raw_diagnoses_df


