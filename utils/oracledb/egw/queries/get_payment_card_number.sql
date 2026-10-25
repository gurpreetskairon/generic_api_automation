SELECT  TO_CHAR(gap) FROM (SELECT  CARDNUMBER + 8 AS gap FROM egw.PaymentCard mo
    WHERE NOT EXISTS (SELECT NULL FROM egw.paymentcard mi
        WHERE   mi.CARDNUMBER = mo.CARDNUMBER + 8)
    ORDER BY CARDNUMBER)
    WHERE   rownum = 1