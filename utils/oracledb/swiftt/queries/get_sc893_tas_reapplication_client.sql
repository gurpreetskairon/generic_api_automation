SELECT *
FROM (
    SELECT DISTINCT
           b.swn,
           b.servcde AS parent_servcde,
           CASE b.servcde
                WHEN 365 THEN 'Sole Parent Support'
                WHEN 370 THEN 'Supported Living Payment'
                WHEN 675 THEN 'Jobseeker Support'
                ELSE 'Other'
           END AS parent_service,
           b.servstatus AS parent_servstatus,
           s.supservcde,
           s.servstatus AS tas_servstatus,
           s.typind,
           r.expirycde,
           t.expdesc,
           r.rsntcde,
           r.actionind,
           TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.expirydt AS expiry_date,
           TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.effectdt AS effect_date,
           (TO_DATE('01/01/1800', 'DD/MM/YYYY') + c.dob) + 1/24 AS dob,
           c.securedind,
           c.marstatus
    FROM ssup s
    INNER JOIN sben b
        ON b.swn = s.swn
    INNER JOIN clint c
        ON c.swn = b.swn
    INNER JOIN sexpr r
        ON r.swn = b.swn
       AND r.servcde = b.servcde
    INNER JOIN sexpt t
        ON t.expirycde = r.expirycde
    WHERE b.maints <> 'D'
      AND s.maints <> 'D'
      AND c.maints <> 'D'
      AND r.maints <> 'D'
      AND b.servstatus = 3
      AND b.servcde IN (365, 370, 675)
      AND s.supservcde = 450
      AND s.servstatus = 3
      AND s.typind = 1
      AND c.securedind = 'N'
      AND r.expirycde IN (100, 105)
      AND TRUNC(TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.effectdt)
          BETWEEN TRUNC(CURRENT_DATE) AND TRUNC(CURRENT_DATE) + 28
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 2
