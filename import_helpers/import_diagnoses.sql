USE HospitalSystem;
DROP TABLE IF EXISTS Staging_Diagnoses;
IF OBJECT_ID('dbo.Diagnoses', 'U') IS NULL 
BEGIN 
    CREATE TABLE Diagnoses (
        diagnosis_id INT PRIMARY KEY,
        admission_id INT,
        patient_id INT,
        icd_code VARCHAR(10),
        priority FLOAT
    );
END
GO
CREATE TABLE Staging_Diagnoses (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    SEQ_NUM FLOAT,
    ICD9_CODE VARCHAR(10)
);

BULK INSERT Staging_Diagnoses
FROM 'C:\Users\josht\Documents\COMP345\soen363\csv_tables\DIAGNOSES_ICD_random.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK,
    FIELDQUOTE = '"'  
);


INSERT INTO Diagnoses (
    diagnosis_id,
    patient_id,
    admission_id,
    priority,
    icd_code
)
SELECT 
    ROW_ID,
    SUBJECT_ID,
    HADM_ID,
    SEQ_NUM,
    ICD9_CODE
FROM Staging_Diagnoses;

DROP TABLE Staging_Diagnoses;
