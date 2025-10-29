--By: Liam Daigle
--ID: 40207583
USE HospitalSystem;

SELECT admission_id, COUNT(*) as NumberOfNotes
FROM NoteEvents
GROUP BY admission_id;