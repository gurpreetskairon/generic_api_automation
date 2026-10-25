select * from (select b.swn,(to_date('01/01/1800','DD/MM/YYYY') + c.dob)+1/24
from servt a, sben b, clint c
where a.servcde=b.servcde
and b.swn=c.swn
and b.servstatus in (4,6)
and a.servcde in (20,21,320,367,600,601,667)
and b.swn in
(select swn from sben
where servcde in (20,21,320,367,600,601,667)
and servstatus in (4,6)
 minus
select swn from sben
where servstatus not in (4,6) )
order by dbms_random.value)
where rownum = 1
