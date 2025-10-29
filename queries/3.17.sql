USE HospitalSystem;

SELECT DISTINCT *
FROM Patients p
LEFT JOIN NoteEvents n on n.patient_id=p.patient_id
WHERE note_type="Radiology" AND upper(note_text) like "%chest%"
