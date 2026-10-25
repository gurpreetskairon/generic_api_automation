SELECT swn
FROM (
    SELECT LPAD(i.swn, 9, '0') AS swn
    FROM incm i
    JOIN servt s2
      ON s2.servcde = i.servcde
    WHERE i.maints != 'D'
      AND i.incmstat = 1
    GROUP BY i.swn
    ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM <= 20
