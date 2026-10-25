SELECT swn,
       next_effective_date
FROM (
    SELECT se.swn,

           CASE
               WHEN MAX(
                   TO_DATE('01/01/1800', 'dd/mm/yyyy') + i.effectdt
               ) IS NULL
               THEN TRUNC(SYSDATE)

               WHEN MAX(
                   TO_DATE('01/01/1800', 'dd/mm/yyyy') + i.effectdt
               ) >= TRUNC(SYSDATE)
               THEN MAX(
                   TO_DATE('01/01/1800', 'dd/mm/yyyy') + i.effectdt
               ) + 7

               ELSE
                   MAX(
                       TO_DATE('01/01/1800', 'dd/mm/yyyy') + i.effectdt
                   )
                   +
                   (
                       7 * CEIL(
                           (
                               TRUNC(SYSDATE)
                               -
                               MAX(
                                   TO_DATE('01/01/1800', 'dd/mm/yyyy')
                                   + i.effectdt
                               )
                           ) / 7
                       )
                   )
           END AS next_effective_date

    FROM sben sb

    JOIN sexpr se
        ON sb.swn = se.swn
       AND sb.servcde = se.servcde

    JOIN sexpt st
        ON se.expirycde = st.expirycde

    LEFT JOIN incm i
        ON i.swn = sb.swn

    WHERE sb.maints != 'D'
      AND se.maints != 'D'
      AND st.maint != 'D'
      AND sb.servstatus = 3

      AND se.servcde IN (
          675,
          370,
          365,
          607,
          603
      )

      AND se.expirycde IN (
          111,
          112,
          113,
          115
      )

      AND NOT EXISTS (
          SELECT 1
          FROM ssup su
          WHERE su.swn = sb.swn
            AND su.supservcde = 830
            AND su.servstatus IN (3, 4, 5)
      )

    GROUP BY se.swn
    ORDER BY se.swn
)
WHERE ROWNUM <= 2
