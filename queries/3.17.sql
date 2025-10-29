--By Kevin Ung
--ID:49259218

USE HospitalSystem;

SELECT DISTINCT p.*
FROM Patients p
LEFT JOIN NoteEvents n on n.patient_id=p.patient_id
WHERE n.note_type='Radiology' AND upper(CAST(n.note_text AS VARCHAR(MAX))) like '%chest%';