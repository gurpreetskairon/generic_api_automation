SELECT swn
FROM (
    SELECT swn
    FROM (
        SELECT DISTINCT s.swn AS swn
        FROM sben s

        JOIN clint cl
            ON cl.swn = s.swn

        LEFT JOIN (
            SELECT DISTINCT
                pa.swn,
                'Y' AS payesInd
            FROM payes pa
            WHERE pa.paytcde IN (1,2,3,4,5,6,7,8,9,10)
              AND pa.servcde = 675
        ) J
            ON s.swn = J.swn

        JOIN (
            SELECT
                sben.swn,
                incm.effectdt,
                incm.incmnbr,
                incms.incmcde,
                incms.amount,
                RANK() OVER (
                    PARTITION BY sben.swn
                    ORDER BY incm.effectdt DESC,
                             incm.incmnbr,
                             incms.amount
                ) AS rnk
            FROM sben
            JOIN incm
                ON sben.swn = incm.swn
            LEFT JOIN incms
                ON incm.incmnbr = incms.incmnbr
            WHERE sben.servstatus = 3
              AND sben.servcde = 675
        ) F
            ON s.swn = F.swn

        WHERE cl.marstatus = 1
          AND s.servcde = 675
          AND s.servstatus = 3
          AND s.srtetcde = 4
          AND J.payesInd IS NULL
          AND cl.securedind = 'N'
          AND F.rnk = 1
          AND F.incmcde = 1
          AND F.amount > 0
    )
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 2
