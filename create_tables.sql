--  go directly to import helpers for creating tables
USE HospitalSystem;

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    date_of_birth DATETIME NOT NULL,
    gender VARCHAR(10) NOT NULL 
        CHECK (gender IN ('M', 'F')),
    life_status BIT NOT NULL DEFAULT 1
);
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
-- add foreign key constraint admission_id
CREATE TABLE ICU (
    icu_id INT PRIMARY KEY,
    admission_id INT NOT NULL,
    exit_date DATETIME NULL,
    entry_date DATETIME NOT NULL,
    ward_location INT NOT NULL,
    icu_type VARCHAR(10)
);
--  add foreign key constraints for admission_id
CREATE TABLE NoteEvents (
    note_id INT PRIMARY KEY,
    admission_id INT,
    patient_id INT,
    author INT NULL,
    note_type VARCHAR(50),
    note_text TEXT,
    has_error BIT DEFAULT 0,
    note_timestamp DATETIME NOT NULL
);
-- add foreign key constraint for admission_id, patient_id, icd_code
CREATE TABLE Diagnoses (
    diagnosis_id INT PRIMARY KEY,
    admission_id INT,
    patient_id INT,
    icd_code VARCHAR(10),
    priority FLOAT
);
CREATE TABLE ICDCode (
    icd_code VARCHAR(10) PRIMARY KEY,
    description VARCHAR(500)
);
-- Ignore constraints for now
-- set constraints
-- Admissions 
ALTER TABLE Admissions 
ADD CONSTRAINT FK_Admissions_Patient
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id);

-- ICU 
ALTER TABLE ICU 
ADD CONSTRAINT FK_ICU_Admission
FOREIGN KEY (admission_id) REFERENCES Admissions(admission_id);

-- NoteEvents 

ALTER TABLE NoteEvents 
ADD CONSTRAINT FK_NoteEvents_Admission
FOREIGN KEY (admission_id) REFERENCES Admissions(admission_id);

ALTER TABLE NoteEvents 
ADD CONSTRAINT FK_NoteEvents_Patient
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id);

-- Diagnoses 

ALTER TABLE Diagnoses 
ADD CONSTRAINT FK_Diagnoses_Admission
FOREIGN KEY (admission_id) REFERENCES Admissions(admission_id);

ALTER TABLE Diagnoses 
ADD CONSTRAINT FK_Diagnoses_Patient 
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id);

ALTER TABLE Diagnoses 
ADD CONSTRAINT FK_Diagnoses_ICDCODE
FOREIGN KEY (icd_code) REFERENCES ICDCode(icd_code);
