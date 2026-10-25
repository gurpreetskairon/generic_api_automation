select * from (select s.swn, (to_date('01/01/1800','DD/MM/YYYY')+cl.DOB)+1/24 as DOB
    from clint cl, sben s left outer join (select distinct sp.swn, 'Y' AS suppInd from  ssup sp
    where sp.servstatus in (3,4)) B on s.swn = b.swn left outer join
        (select distinct pa.SWN, 'Y' AS payesInd from payes pa
        where pa.PAYTCDE  in  (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        and pa.SERVCDE = 675 ) J on s.swn = J.swn
where s.swn = cl.swn
and s.servcde = 675
and s.servstatus = 3
and s.srtetcde = 4
and J.payesInd is null
and cl.securedind = 'N'
and cl.marstatus = 1
Order by dbms_random.value)
where rownum = 1