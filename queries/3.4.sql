USE HospitalSystem;
select * from Patients p
where exists (Select a.patient_id, a.discharge_location from Admissions a
where p.patient_id=a.patient_id and a.discharge_location = 'HOME');