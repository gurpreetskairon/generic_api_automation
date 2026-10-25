
SELECT
    x.swn
FROM (
    SELECT DISTINCT
        s.swn
    FROM clint cl
    JOIN sben s
      ON s.swn = cl.swn
    WHERE s.servstatus IN (3,4,5,6)
      AND s.maints <> 'D'
      AND cl.maints <> 'D'
      AND cl.securedind = 'N'
      AND cl.dob IS NOT NULL
      AND trim(cl.givenamef) IS NOT NULL
      AND trim(cl.snamef) IS NOT NULL
      AND LENGTH(TRIM(s.swn)) = 9
) x
WHERE rownum <= 10000
ORDER BY x.swn
