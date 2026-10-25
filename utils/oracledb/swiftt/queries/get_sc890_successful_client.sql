SELECT *
FROM (
    SELECT DISTINCT
           cl.swn,

           TO_CHAR(
               TO_DATE('01/01/1800','dd/mm/yyyy') + a.contactdt,
               'YYYY-MM-DD'
           ) AS application_date

    FROM clint cl
    JOIN appc a
      ON a.swn = cl.swn

    WHERE cl.maints <> 'D'
      AND a.maints <> 'D'

      AND cl.ptnrswn = 0
      AND a.contactdt <> 0
      AND a.completedt <> 0

      AND (
            a.lapsedt = 0
            OR TO_DATE('01/01/1800','dd/mm/yyyy') + a.lapsedt
               >= TRUNC(SYSDATE)
          )

      AND NOT EXISTS (
            SELECT 1
            FROM sben sb
            WHERE sb.swn = cl.swn
              AND sb.maints <> 'D'
              AND sb.servcde = 675
          )

      AND NOT EXISTS (
            SELECT 1
            FROM relat r
            WHERE r.swn = cl.swn
              AND r.maints NOT IN ('D','I')
              AND r.servcde IN (340,344)
          )

    ORDER BY application_date DESC
)
WHERE ROWNUM = 1
