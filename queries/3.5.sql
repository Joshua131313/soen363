--By: Yifu Li
--ID: 40286100

USE HospitalSystem;
-- Task 3-5: List of all the patients who have private insurance
SELECT DISTINCT a.patient_id
FROM Admissions AS a
WHERE a.insurance = 'Private'
ORDER BY a.patient_id;
