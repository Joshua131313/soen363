select * from Admissions a
where exists (select * from Diagnoses d
where d.admission_id = a.admission_id
and d.icd_code='4019');