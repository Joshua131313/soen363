USE HospitalSystem;
-- Admissions (you must manually configure the FROM URL)
DROP TABLE IF EXISTS Staging_Admissions;

IF OBJECT_ID('dbo.Admissions', 'U') IS NULL
BEGIN
    CREATE TABLE Admissions (
        admission_id INT PRIMARY KEY,
        patient_id INT NOT NULL,
        reason_of_visit VARCHAR(50) NOT NULL,
        death_during_stay BIT DEFAULT 0,
        insurance VARCHAR(25) NULL,
        marital_status VARCHAR(25) NULL,
        admission_date DATETIME NOT NULL,
        discharge_date DATETIME NULL
    );
END
GO
CREATE TABLE Staging_Admissions (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ADMITTIME DATETIME,
    DISCHTIME DATETIME,
    DEATHTIME DATETIME NULL,  
    ADMISSION_TYPE VARCHAR(50),
    ADMISSION_LOCATION VARCHAR(100),
    DISCHARGE_LOCATION VARCHAR(100),
    INSURANCE VARCHAR(100),
    LANGUAGE VARCHAR(50),
    RELIGION VARCHAR(50),
    MARITAL_STATUS VARCHAR(50),
    ETHNICITY VARCHAR(100),
    EDREGTIME DATETIME NULL,
    EDOUTTIME DATETIME NULL,
    DIAGNOSIS VARCHAR(255),
    HOSPITAL_EXPIRE_FLAG VARCHAR(500),
    HAS_CHARTEVENTS_DATA VARCHAR(500)
);

-- CHANGE path here to patients csv file

BULK INSERT Staging_Admissions 
FROM 'C:\Users\josht\Documents\COMP345\soen363\csv_tables\ADMISSIONS_random.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
SELECT * FROM Staging_Admissions;
INSERT INTO Admissions (
    admission_id, 
    admission_date, 
    death_during_stay, 
    discharge_date, 
    insurance,
    marital_status,
    patient_id,
    reason_of_visit
)
SELECT 
    HADM_ID,
    ADMITTIME,
    CASE 
        WHEN LTRIM(RTRIM(HOSPITAL_EXPIRE_FLAG)) IN ('1','0') THEN CAST(LTRIM(RTRIM(HOSPITAL_EXPIRE_FLAG)) AS BIT)
        ELSE NULL 
    END AS death_during_stay,    
    DISCHTIME,
    INSURANCE,
    MARITAL_STATUS,
    SUBJECT_ID,
    ADMISSION_TYPE
FROM Staging_Admissions;

DROP TABLE Staging_Admissions;
