SELECT swn
FROM (
    SELECT DISTINCT s.swn
    FROM sben s
    WHERE s.maints <> 'D'
      AND s.servstatus = 3
      AND s.servcde = 675
      AND EXISTS (
          SELECT 1
          FROM sben d
          WHERE d.swn = s.swn
            AND d.maints <> 'D'
            AND TRIM(d.debtind) = 'Y'
      )
    ORDER BY s.swn
)
WHERE ROWNUM = 1
