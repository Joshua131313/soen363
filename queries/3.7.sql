USE HospitalSystem;

SELECT p.patient_id, COUNT(i.icu_id) AS ICUStayCount
FROM Patients p
JOIN Admissions a ON p.patient_id = a.patient_id
JOIN ICU i ON a.admission_id = i.admission_id 
GROUP BY p.patient_id, a.admission_id
HAVING COUNT(i.icu_id) > 1;

