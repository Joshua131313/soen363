--By: Joshua Bitton
--ID: 40273378

USE HospitalSystem;

SELECT DISTINCT p.*
FROM NoteEvents ne
INNER JOIN Patients p
ON ne.patient_id = p.patient_id
WHERE note_type LIKE '%radiology%' OR note_type LIKE '%ecg%';
