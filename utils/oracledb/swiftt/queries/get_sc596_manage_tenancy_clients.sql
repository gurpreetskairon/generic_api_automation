WITH eligible_clients AS (
    SELECT DISTINCT
           LPAD(TO_CHAR(c.swn), 9, '0') AS swn,
           TRIM(c.givenamef) AS given_name,
           TRIM(c.snamef) AS surname,
           c.marstatus,
           c.securedind,
           TO_CHAR(
               (TO_DATE('01/01/1800', 'DD/MM/YYYY') + c.dob) + 1/24,
               'YYYY-MM-DD'
           ) AS date_of_birth
    FROM clint c
    WHERE c.maints <> 'D'
      AND c.securedind = 'N'
      AND c.dob IS NOT NULL
      AND TRIM(c.givenamef) IS NOT NULL
      AND TRIM(c.snamef) IS NOT NULL

      -- Client must have at least one eligible service
      AND EXISTS (
          SELECT 1
          FROM sben s
          WHERE s.swn = c.swn
            AND s.maints <> 'D'
            AND s.servstatus IN (3, 4, 5)
            AND s.servcde IN (365, 370, 675, 180, 181)
      )

      -- Exclude apportioned partners
      AND NOT EXISTS (
          SELECT 1
          FROM sben s2
          WHERE s2.swn = c.swn
            AND s2.maints <> 'D'
            AND s2.servstatus IN (3, 4, 5)
            AND s2.servcde IN (365, 370, 675, 180, 181)
            AND s2.apprtind = 2
      )

      -- Exclude clients already registered as tenants
      AND NOT EXISTS (
          SELECT 1
          FROM tenant t
          WHERE t.tenant_swn = c.swn
            AND NVL(TRIM(t.maints), 'X') <> 'D'
      )

      -- Exclude clients already used as head/main clients
      AND NOT EXISTS (
          SELECT 1
          FROM tenant_cost tc
          WHERE tc.client_swn = c.swn
            AND NVL(TRIM(tc.maints), 'X') <> 'D'
      )

      -- Exclude clients with Accommodation Supplement or TAS records.
      -- 471 = Accommodation Supplement
      -- 450 = TAS
      -- These can cause SC596 outcome 12538 when tenant costs do not
      -- match the client's existing supplementary costs.
      AND NOT EXISTS (
          SELECT 1
          FROM ssup ss
          WHERE ss.swn = c.swn
            AND NVL(TRIM(ss.maints), 'X') <> 'D'
            AND ss.supservcde IN (450, 471)
      )
)

SELECT
    swn,
    given_name,
    surname,
    marstatus,
    securedind,
    date_of_birth
FROM (
    SELECT e.*
    FROM eligible_clients e
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 20
