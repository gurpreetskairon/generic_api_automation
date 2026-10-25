select distinct s.swn
from    clint cl,
        sben s

-- Add payee indicator
left outer join (select distinct pa.SWN, 'Y' AS payesInd
from    payes pa
where   pa.PAYTCDE  in  (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
and   pa.SERVCDE = 675 ) J on s.swn = J.swn

-- Add debt indicator
left outer join (select swn,'Y' as DEBTind  from debt
where swn in (SELECT SWN FROM DEBT WHERE CHANGEDT=0
GROUP BY SWN
HAVING COUNT(SWN)<3)
AND maints not in ('D', 'I') AND DEBTSTATUS in (1,2)
AND RECOVAMT != 0
AND TODT != 0
and servcde = 675
) C on s.swn = C.swn

-- *** Contraints after all the joins ****
where   s.swn = cl.swn
  and   s.servstatus = 3
  and   s.srtetcde = 4
  and   cl.securedind = 'N'
  and   C.DEBTind = 'Y'
  and   s.sben_id = (select max (sben_id) from sben where sben.swn = s.swn and sben.servcde = s.servcde)