--By: Joshua Bitton
--ID: 40273378

USE HospitalSystem;
-- SELECT TOP 10 * FROM Patients;
-- SELECT TOP 10 * FROM Admissions;

SELECT p.patient_id, COUNT(a.admission_id) AS AdmissionCount
FROM Patients p
JOIN Admissions a ON p.patient_id = a.patient_id
GROUP BY p.patient_id;