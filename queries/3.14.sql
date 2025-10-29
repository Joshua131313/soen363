USE HospitalSystem;
select * from Admissions a
where exists (select * from ICU i
left join Diagnoses d
on i.admission_id = d.admission_id
where d.admission_id = a.admission_id
and d.icd_code='4019');