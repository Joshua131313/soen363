import pandas as pandas
import pyodbc as pyodbc
import os
from dotenv import load_dotenv
#gets the connection string from the .env file
def connection_string():
    load_dotenv()
    return os.getenv("CONNECTION_STRING")

#These functions return dictionary of the tables present in the SQL database
def get_patients():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from patients", connection)
    return df.to_dict(orient="records")

def get_admissions():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from admissions", connection)
    return df.to_dict(orient="records")

def get_diagnoses():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from diagnoses", connection)
    return df.to_dict(orient="records")

def get_icu():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from icu", connection)
    return df.to_dict(orient="records")

def get_icdcode():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from ICDCode", connection)
    return df.to_dict(orient="records")

def get_noteevents():
    connection = pyodbc.connect(connection_string())
    df = pandas.read_sql("Select * from NoteEvents", connection)
    return df.to_dict(orient="records")