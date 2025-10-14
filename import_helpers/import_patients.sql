USE HospitalSystem;
DROP TABLE IF EXISTS Staging_Patients;
-- Patients (you must manually configure the FROM URL)
IF OBJECT_ID('dbo.Patients', 'U') IS NULL
BEGIN
    CREATE TABLE Patients (
        patient_id INT PRIMARY KEY,
        date_of_birth DATETIME NOT NULL,
        gender VARCHAR(10) NOT NULL 
            CHECK (gender IN ('M', 'F')),
        life_status BIT NOT NULL DEFAULT 1
    );
END
GO

CREATE TABLE Staging_Patients (
    ROW_ID INT,
    SUBJECT_ID INT,
    GENDER CHAR(1),
    DOB DATETIME2 NULL,
    DOD DATETIME2 NULL,
    DOD_HOSP DATETIME2 NULL,
    DOD_SSN DATETIME2 NULL,
    EXPIRE_FLAG TINYINT -- since only 0 or 1
);
-- CHANGE path here to patients csv file
BULK INSERT Staging_Patients 
FROM 'C:\Users\josht\Documents\COMP345\soen363\csv_tables\PATIENTS_random.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT * FROM Staging_Patients;
INSERT INTO Patients (patient_id, date_of_birth, gender, life_status)
SELECT 
    SUBJECT_ID,
    DOB,
    GENDER, 
    EXPIRE_FLAG
FROM Staging_Patients;

DROP TABLE Staging_Patients;