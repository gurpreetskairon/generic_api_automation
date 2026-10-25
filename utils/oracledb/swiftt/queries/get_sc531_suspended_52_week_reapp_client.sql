SELECT *
FROM (
    SELECT DISTINCT
        se.swn,
        se.servcde,
        sb.servstatus,
        se.expirycde,
        se.rsntcde,
        se.actionind,
        TO_DATE('01/01/1800', 'DD/MM/YYYY') + se.effectdt AS effect_date,
        TO_DATE('01/01/1800', 'DD/MM/YYYY') + se.expirydt AS expiry_date,
        st.expdesc
    FROM sben sb
    INNER JOIN sexpr se
        ON sb.swn = se.swn
       AND sb.servcde = se.servcde
    INNER JOIN sexpt st
        ON se.expirycde = st.expirycde
    WHERE sb.maints != 'D'
      AND se.maints != 'D'
      AND st.maint != 'D'
      AND sb.servstatus = 4
      AND (
            se.expirycde IN (111, 112, 115)
            OR (se.expirycde = 113 AND se.rsntcde != 293)
          )
      AND TRUNC(TO_DATE('01/01/1800', 'DD/MM/YYYY') + se.effectdt)
          BETWEEN TRUNC(CURRENT_DATE) AND TRUNC(CURRENT_DATE) + 35
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 2
