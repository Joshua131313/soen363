-- Task 3.10: Show the first 10 discharge summaries recorded in the database
-- Table: NoteEvents
-- note_type = 'Discharge summary'
-- note_timestamp = chart/store time depending on dataset

SELECT TOP (10)
    n.patient_id,
    n.admission_id,
    n.note_type,
    n.note_timestamp,
    LEFT(CAST(n.note_text AS VARCHAR(MAX)), 200) AS preview_text  -- show first 200 chars
FROM NoteEvents AS n
WHERE n.note_type = 'Discharge summary'
ORDER BY n.note_timestamp ASC;
