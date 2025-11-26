from pymongo import MongoClient
import sql_server_controller as ssc
import pandas as pd
from dotenv import load_dotenv
import os
import pyodbc as pyodbc
import time

def get_mongo_database():
    load_dotenv()
    mongo_uri=os.getenv("MONGO_URI")
    CONNECTION_STRING = mongo_uri
    client = MongoClient(CONNECTION_STRING)
    return client['HospitalSystem']

def get_sql_database():
    load_dotenv()
    connection_string = os.getenv("CONNECTION_STRING")
    connection = pyodbc.connect(connection_string)
    return connection

def test():
    sql_results=[]
    sql_times=[]
    mongo_results=[]
    mongo_time=[]
    sql_database=get_sql_database()
    mongo_database=get_mongo_database()

    #Query 3.4
    start_time=time.time()
    sql_result=pd.read_sql("""  select * from Patients p
                                where exists (Select a.patient_id, a.discharge_location from Admissions a
                                where p.patient_id=a.patient_id and a.discharge_location = 'HOME');""", sql_database)
    end_time=time.time()
    sql_results.append(sql_result)
    sql_times.append(end_time-start_time)

    start_time=time.time()
    home_ids=mongo_database["admissions"].distinct("patient_id", {"discharge_location":"HOME"})
    mongo_result=mongo_database["patients"].find({"_id":{"$in":home_ids}})
    end_time=time.time()
    mongo_results.append(pd.DataFrame(list(mongo_result)))
    mongo_time.append(end_time-start_time)

    #Query 3.13
    start_time=time.time()
    sql_result=pd.read_sql("""  SELECT TOP 5 d.icd_code, COUNT(*) AS TotalDiagnoses
                                FROM Diagnoses d
                                GROUP BY d.icd_code
                                ORDER BY TotalDiagnoses DESC;""", sql_database)
    end_time=time.time()
    sql_results.append(sql_result)
    sql_times.append(end_time-start_time)

    start_time=time.time()
    mongo_result=mongo_database["diagnoses"].aggregate([
        {
            "$group": {
                "_id": "$icd_code",
                "TotalDiagnoses": { "$sum": 1 }
            }
        },
        {
            "$project": {
                "_id": 0,
                "icd_code": "$_id",
                "TotalDiagnoses": 1
            }
        },
        {
            "$sort": { "TotalDiagnoses": -1 }
        },
        {
            "$limit": 5
        }
    ])
    end_time=time.time()
    mongo_results.append(pd.DataFrame(list(mongo_result)))
    mongo_time.append(end_time-start_time)

    #Query 3.20
    start_time=time.time()
    sql_result=pd.read_sql("""  SELECT 
                                p.patient_id,
                                COALESCE(num_a.num_admissions, 0) AS num_admissions, 
                                COALESCE(num_i.num_icustays, 0) AS num_icustays, 
                                COALESCE(num_d.num_diagnoses, 0) AS num_diagnoses
                            FROM Patients p  
                            LEFT JOIN (
                                SELECT patient_id, COUNT(*) AS num_admissions 
                                FROM Admissions
                                GROUP BY patient_id
                            ) AS num_a 
                            ON num_a.patient_id = p.patient_id
                            LEFT JOIN(
                                SELECT patient_id, COUNT(*) AS num_icustays
                                FROM ICU
                                GROUP BY patient_id
                            ) AS num_i
                            ON num_i.patient_id = p.patient_id
                            LEFT JOIN(
                                SELECT patient_id, COUNT(*) as num_diagnoses
                                FROM Diagnoses
                                GROUP BY patient_id
                            ) AS num_d 
                            ON num_d.patient_id = p.patient_id
                            WHERE p.patient_id = 2225;""", sql_database)
    end_time=time.time()
    sql_results.append(sql_result)
    sql_times.append(end_time-start_time)

    start_time=time.time()
    patient_id = 2225

    num_admissions = mongo_database["admissions"].count_documents({"patient_id": patient_id})
    num_icustays   = mongo_database["icu"].count_documents({"patient_id": patient_id})
    num_diagnoses  = mongo_database["diagnoses"].count_documents({"patient_id": patient_id})

    mongo_result = [{
        "patient_id": patient_id,
        "num_admissions": num_admissions,
        "num_icustays": num_icustays,
        "num_diagnoses": num_diagnoses
    }]
    end_time=time.time()
    mongo_results.append(pd.DataFrame(list(mongo_result)))
    mongo_time.append(end_time-start_time)

    with open("output.txt", "w") as f:
        for i in range(3):
            print("\n------------------------------------------------------\n", file=f)
            print("Execution Time: "+str(sql_times[i]), file=f)
            print("\n", file=f)
            print(sql_results[i], file=f)
            print("\n------------------------------------------------------\n", file=f)
            print("Execution Time: "+str(mongo_time[i]), file=f)
            print("\n", file=f)
            print(mongo_results[i], file=f)


test()