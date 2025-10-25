USE HospitalSystem;

SELECT 
    p.patient_id,
    COALESCE(num_a.num_admissions, 0) AS num_admissions, 
    COALESCE(num_i.num_icustays, 0) AS num_icustays, 
    COALESCE(num_d.num_diagnoses, 0) AS num_diagnoses
FROM Patients p  
LEFT JOIN (
    SELECT patient_id, COUNT(*) AS num_admissions 
    FROM Admissions
    GROUP BY patient_id
) AS num_a 
ON num_a.patient_id = p.patient_id
LEFT JOIN(
    SELECT patient_id, COUNT(*) AS num_icustays
    FROM ICU
    GROUP BY patient_id
) AS num_i
ON num_i.patient_id = p.patient_id
LEFT JOIN(
    SELECT patient_id, COUNT(*) as num_diagnoses
    FROM Diagnoses
    GROUP BY patient_id
) AS num_d 
ON num_d.patient_id = p.patient_id;