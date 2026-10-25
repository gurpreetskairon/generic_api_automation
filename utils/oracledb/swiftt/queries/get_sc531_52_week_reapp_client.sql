SELECT *
FROM (
    SELECT DISTINCT
        r.swn,
        b.servcde,
        b.servstatus,
        r.expirycde,
        r.rsntcde,
        r.actionind,
        TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.expirydt AS expiry_date,
        TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.effectdt AS effect_date
    FROM sexpr r
    INNER JOIN sexpt t ON t.expirycde = r.expirycde
    INNER JOIN sben b ON b.swn = r.swn AND b.servcde = r.servcde
    INNER JOIN clint c ON c.swn = b.swn
    WHERE b.maints != 'D'
      AND r.maints != 'D'
      AND b.servstatus = 3
      AND b.servcde IN (365)
      AND (
            r.expirycde IN (111, 112)
            OR (r.expirycde = 113 AND r.rsntcde != 293)
          )
      AND TRUNC(TO_DATE('01/01/1800', 'DD/MM/YYYY') + r.effectdt)
          BETWEEN TRUNC(CURRENT_DATE) AND TRUNC(CURRENT_DATE) + 35
      AND ((CURRENT_DATE - TO_DATE('01/01/1800', 'DD/MM/YYYY') - c.dob) + 1/24) / 365 < 64
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 2
