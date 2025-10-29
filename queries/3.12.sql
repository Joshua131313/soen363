--By: Liam Daigle
--ID: 40207583
USE HospitalSystem;

SELECT d.patient_id, d.icd_code, i.description
FROM Diagnoses d
INNER JOIN ICDCode i
ON d.icd_code = i.icd_code
WHERE patient_id = 262;