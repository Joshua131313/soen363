--By Kevin Ung
--ID:49259218
USE HospitalSystem;

SELECT *
FROM Patients
WHERE patient_id in (SELECT patient_id FROM ICU where first_careunit<>last_careunit);
