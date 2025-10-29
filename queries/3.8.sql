USE HospitalSystem;
-- Task 3.8: List all patients who were in the ICU
-- where both the first and last care units are "MICU"
SELECT DISTINCT
    a.patient_id,
    i.admission_id,
    i.first_careunit,
    i.last_careunit
FROM ICU AS i
JOIN Admissions AS a
    ON a.admission_id = i.admission_id
WHERE i.first_careunit = 'MICU'
  AND i.last_careunit  = 'MICU'
ORDER BY a.patient_id;
