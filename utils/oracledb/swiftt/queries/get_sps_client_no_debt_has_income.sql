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
        (select sum(debtamt) from debt where swn = c.swn and fromdt > 0) -
        (select sum(recovamt) from debt where swn = c.swn and fromdt > 0)) < 1000
    and (
        select count(*) from (
            select * from (
                select (to_date('01/01/1800','DD/MM/YYYY')+effectdt) effective_date,
                    amount, incmhours from incm i left join incms s on i.incmnbr = s.incmnbr
                where i.swn = c.swn
                order by effective_date desc)
            where rownum = 1) f
        where f.amount > 0
            ) > 0
    order by dbms_random.value)
where rownum = 1