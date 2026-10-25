select * from (select distinct r.swn, (to_date('01/01/1800','DD/MM/YYYY') + c.DOB)+1/24 as Date_of_birth
from sexpr r
inner join sexpt t on t.expirycde = r.expirycde
inner join sben b on b.swn = r.swn
inner join clint c on c.swn = b.swn
where r.servcde = b.servcde
and b.servstatus in 3
and b.servcde in (675) --(675,607,611,313,370,365,603,839,180)
and r.maints != 'D'
and ((t.expirycde in (111,112)) or (t.expirycde=113 and r.rsntcde!=293)) -- 52 week reapp
and (to_date('01/01/1800','DD/MM/YYYY') + r.effectdt)+1/24 between current_date and current_date+35
and ((CURRENT_DATE - to_date('01/01/1800','DD/MM/YYYY') - c.dob)+1/24)/365 < 64
order by dbms_random.value)
where rownum = 1