select * from Patients p
where exists (select * from NoteEvents n
where n.patient_id = p.patient_id
and n.note_type = 'Discharge summary');