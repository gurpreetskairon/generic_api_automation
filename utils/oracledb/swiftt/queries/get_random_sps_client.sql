Select * from (select b.swn, (to_date('01/01/1800','DD/MM/YYYY')+c.DOB)+1/24 from ssup s
    inner join sben b on b.swn = s.swn
    inner join clint c on b.swn = c.swn
    where b.servstatus in (3)
    and b.servcde in (365)
    and s.supservcde in (471)
    and s.servstatus in (3)
    and s.typind in (1)
    and c.securedind = 'N'
    and (
        select count(swn) from debt
        where swn = c.swn
    ) = 0
    order by dbms_random.value)
where rownum = 1