USE HospitalSystem;

DROP TABLE IF EXISTS Staging_ICDCode;

IF OBJECT_ID('dbo.ICDCode') IS NULL
BEGIN
    CREATE TABLE dbo.ICDCode (
        icd_code VARCHAR(20) PRIMARY KEY,
        description VARCHAR(MAX)
    );
END

CREATE TABLE Staging_ICDCode (
    ROW_ID INT,
    ICD9_CODE VARCHAR(20),
    SHORT_TITLE VARCHAR(255),
    LONG_TITLE VARCHAR(MAX)
);

BULK INSERT Staging_ICDCode
FROM 'C:\Users\josht\Documents\COMP345\soen363\csv_tables\D_ICD_DIAGNOSES.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK,
    FIELDQUOTE = '"'   -- handles commas in LONG_TITLE
);


INSERT INTO dbo.ICDCode (icd_code, description)
SELECT 
    s.ICD9_CODE,
    s.LONG_TITLE
FROM Staging_ICDCode s
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.ICDCode c
    WHERE c.icd_code = s.ICD9_CODE
);

DROP TABLE Staging_ICDCode;
