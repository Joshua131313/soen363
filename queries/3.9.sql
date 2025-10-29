USE HospitalSystem;
--ID chosen:171662
SELECT author, note_type, note_text, has_error, note_timestamp
FROM NoteEvents
Where admission_id="171662";
