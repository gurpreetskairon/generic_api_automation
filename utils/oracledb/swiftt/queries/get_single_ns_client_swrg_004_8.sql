select s.swn
from    clint cl,
        sben s
  --Searching NS clients with income no supps/payees/osp single--

-- Add payee indicator
left outer join (select distinct pa.SWN, 'Y' AS payesInd
from  payes pa
where pa.PAYTCDE  in  (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
and   pa.SERVCDE = 180) J on s.swn = J.swn

-- Add a Supp Indicator
left outer join
  (select distinct sp.swn, 'Y' AS suppInd
    from  ssup sp
    where sp.servstatus in (3,4)
) B on s.swn = b.swn

-- add income
left outer join
  (select sben.swn, incm.effectdt, incm.incmnbr, incms.amount,
    RANK() OVER (PARTITION BY sben.swn
    ORDER By incm.effectdt desc, incm.incmnbr, incms.amount ) Rnk
      from    sben, incm
      left outer join incms on incm.incmnbr = incms.incmnbr
      where   sben.swn = incm.swn
      and   sben.servstatus in  (3)
      and   sben.SERVCDE = 180
      order by Rnk
      ) F on s.swn = F.swn

-- *** Contraints after all the joins ****
where   s.swn = cl.swn
  and   cl.marstatus = 1
  and   s.servcde = 180
  and   s.servstatus = 3
  and   s.rcsind = 0
  and   s.portcde = 0
  and   J.payesInd is null
  and   cl.securedind = 'N'
  and   cl.IRDNBR != 0
  and   cl.COUNTRYCDE != 0
  and   b.suppInd is null
  and   (f.amount = 0 or f.amount is null)
  and rnk = 1