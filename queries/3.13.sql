--By: Joshua Bitton
--ID: 40273378

USE HospitalSystem;

SELECT TOP 5 d.icd_code, COUNT(*) AS TotalDiagnoses
FROM Diagnoses d
GROUP BY d.icd_code
ORDER BY TotalDiagnoses DESC;
