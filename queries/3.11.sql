USE HospitalSystem;

SELECT admission_id, COUNT(*) as NumberOfNotes
FROM NoteEvents
GROUP BY admission_id;