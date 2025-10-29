--By: Yifu Li
--ID: 40286100

USE HospitalSystem;
-- Task 3.16: List patients who had at least one radiology report during admission
-- Note: Radiology reports are identified by note_type containing 'Radiology'
SELECT DISTINCT a.patient_id
FROM Admissions AS a
JOIN NoteEvents AS n
  ON n.admission_id = a.admission_id
WHERE n.note_type LIKE '%Radiology%'
ORDER BY a.patient_id;
