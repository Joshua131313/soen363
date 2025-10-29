--By: Liam Daigle
--ID: 40207583
USE HospitalSystem;

SELECT *
FROM Patients p
WHERE p.patient_id NOT IN (
    SELECT DISTINCT patient_id
    FROM ICU
);