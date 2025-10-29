--By: Omar Hammodan
--ID: 40246598

USE HospitalSystem;
select * from Patients p
where exists (select * from NoteEvents n
where n.patient_id = p.patient_id
and n.note_type = 'Discharge summary');