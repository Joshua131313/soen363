from pymongo import MongoClient
import sql_server_controller as ssc
import pandas as pd
from dotenv import load_dotenv
import os

#Connects to the MongoDB using the connection string in the .env
def get_database():
   load_dotenv()
   mongo_uri=os.getenv("MONGO_URI")
 
   CONNECTION_STRING = mongo_uri
 
   client = MongoClient(CONNECTION_STRING)
 
   return client['HospitalSystem']

#These functions insert the contents of the SQL database into MongoDB
def insert_patients():
  db=get_database()
  collection=db["patients"]
  record_list=ssc.get_patients()
  for record in record_list:
     record["_id"]=record.pop("patient_id")
     collection.insert_one(record)

def insert_admissions():
  db=get_database()
  collection=db["admissions"]
  record_list=ssc.get_admissions()
  for record in record_list:
     record["_id"]=record.pop("admission_id")
     collection.insert_one(record)

def insert_diagnoses():
  db=get_database()
  collection=db["diagnoses"]
  record_list=ssc.get_diagnoses()
  for record in record_list:
     record["_id"]=record.pop("diagnosis_id")
     collection.insert_one(record)

def insert_icu():
  db=get_database()
  collection=db["icu"]
  record_list=ssc.get_icu()
  for record in record_list:
     record["_id"]=record.pop("icu_id")
     collection.insert_one(record)

def insert_icdcode():
  db=get_database()
  collection=db["icdCode"]
  record_list=ssc.get_icdcode()
  for record in record_list:
     record["_id"]=record.pop("icd_code")
     collection.insert_one(record)

def insert_noteevents():
  db=get_database()
  collection=db["noteEvents"]
  record_list=ssc.get_noteevents()
  for record in record_list:
     record["_id"]=record.pop("note_id")
     collection.insert_one(record)


#This function inserts the records from NoteEvents that were not added to the SQL database (around 153k records only)
def insert_rest_noteevents():

    #------------------- Cleaning NoteEvents CSV  (code copied from import generator script)----------------------#
    raw_noteevents_df = pd.read_csv(
        "csv_tables/NOTEEVENTS_random.csv",
        low_memory=False
    )

    # Select needed columns and force a COPY to avoid SettingWithCopyWarning
    cleaned_noteevents_df = raw_noteevents_df[
        ["ROW_ID", "HADM_ID", "SUBJECT_ID", "CGID", "CATEGORY", "TEXT", "ISERROR", "CHARTDATE", "CHARTTIME", "STORETIME"]
    ].copy()

    # Rename columns safely
    cleaned_noteevents_df.rename(columns={
        "ROW_ID": "_id",
        "HADM_ID": "admission_id",
        "SUBJECT_ID": "patient_id",
        "CGID": "author",
        "CATEGORY": "note_type",
        "TEXT": "note_text",
        "ISERROR": "has_error",
    }, inplace=True)

    # Drop unused date/time columns
    cleaned_noteevents_df.drop(['CHARTDATE', 'CHARTTIME', 'STORETIME'], axis=1, inplace=True)

    # Convert string-like fields to proper string dtype BEFORE inserting strings like "NULL"
    cleaned_noteevents_df["author"] = cleaned_noteevents_df["author"].astype("string")
    cleaned_noteevents_df["has_error"] = cleaned_noteevents_df["has_error"].astype("string")
    cleaned_noteevents_df["note_type"] = cleaned_noteevents_df["note_type"].astype("string")
    cleaned_noteevents_df["note_text"] = cleaned_noteevents_df["note_text"].astype("string")

    # Escape apostrophes
    cleaned_noteevents_df["note_text"] = cleaned_noteevents_df["note_text"].str.replace("'", "''")

    # Replace missing values with string "NULL"
    cleaned_noteevents_df.loc[cleaned_noteevents_df['author'].isna(), 'author'] = "NULL"
    cleaned_noteevents_df.loc[cleaned_noteevents_df['has_error'].isna(), 'has_error'] = "NULL"

    # Add surrounding quotes (like SQL literals)
    cleaned_noteevents_df["note_type"] = "'" + cleaned_noteevents_df["note_type"] + "'"
    cleaned_noteevents_df["note_text"] = "'" + cleaned_noteevents_df["note_text"] + "'"

    #---------------------------------------------- Insert rest of notes in MongoDB -----------------------------------#
    db=get_database()
    collection=db["noteEvents"]

    for _, row in cleaned_noteevents_df.iterrows():
        record = row.to_dict()

        try:
         collection.insert_one(record)
        except:
           print()

   


#These function calls insert the data (The data is already there so I commented them out to avoid someone accidentally running the script and making pointless insertions in the db).
'''
insert_patients()
insert_admissions()
insert_diagnoses()
insert_icdcode()
insert_icu()
insert_noteevents()
insert_rest_noteevents()
'''