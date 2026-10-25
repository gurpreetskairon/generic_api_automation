insert into egw.paymentcard (oid, cardNumber, expiryDate, paymentCardDescription_code, dateOfManufacture, version)
values (:card_id, :card_no, to_Date('2050-12-31','yyyy-MM-dd'), 'MAG1', to_Date('2009-08-11','yyyy-MM-dd'), 0)
