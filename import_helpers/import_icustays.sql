USE HospitalSystem;
GO

-- 1) Create ICU table if it doesn't exist
IF OBJECT_ID('dbo.ICU', 'U') IS NULL
BEGIN
    CREATE TABLE ICU (
        icu_id INT PRIMARY KEY,
        admission_id INT NOT NULL,
        exit_date DATETIME NULL,
        entry_date DATETIME NOT NULL,
        ward_location INT NOT NULL,
        icu_type VARCHAR(10)
    );
END
GO

DROP TABLE IF EXISTS Staging_ICU;

CREATE TABLE Staging_ICU (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    DBSOURCE VARCHAR(50),
    FIRST_CAREUNIT VARCHAR(10),
    LAST_CAREUNIT VARCHAR(10),
    FIRST_WARDID INT,
    LAST_WARDID INT,
    INTIME DATETIME,
    OUTTIME DATETIME,
    LOS FLOAT
);
GO

BULK INSERT Staging_ICU
FROM 'C:\Users\josht\Documents\COMP345\soen363\csv_tables\ICUSTAYS_random.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\r\n',
    TABLOCK,
    FIELDQUOTE = '"'
);
GO
INSERT INTO ICU (
    icu_id,
    admission_id,
    entry_date,
    exit_date,
    icu_type,
    ward_location
)
SELECT 
    ICUSTAY_ID,
    HADM_ID,
    INTIME,
    OUTTIME,
    LAST_CAREUNIT,
    LAST_WARDID
FROM Staging_ICU s
WHERE NOT EXISTS (
    SELECT 1 FROM ICU i WHERE i.icu_id = s.ICUSTAY_ID
);
GO

-- 5) Drop staging table
DROP TABLE Staging_ICU;
GO
