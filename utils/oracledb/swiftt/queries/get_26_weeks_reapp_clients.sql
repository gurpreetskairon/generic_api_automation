select * from (select distinct r.swn, (to_date('01/01/1800','DD/MM/YYYY') + c.DOB)+1/24 as Date_of_birth
from sexpr r
inner join sexpt t on t.expirycde = r.expirycde
inner join sben b on b.swn = r.swn
inner join clint c on c.swn = b.swn
where r.servcde = b.servcde
--delete conditon below
--and r.swn in ( 523602533, 523602656, 523602664, 523602672, 523602779, 523602787, 523602795, 523602576, 523603151, 523603194, 523603231,
--523603274, 523603311, 523603354, 523603960, 523603928, 523604001, 523604001, 523604044,523608780, 523608828, 523608860, 523608908, 523608940,
--523608983, 523609024, 523609067, 523609104, 523609163, 523609200, 523609243, 523609307, 523609342, 523609382, 523609422)
and b.servstatus in 3
and b.servcde in (675) --(675,607,611,313,370,365,603,839,180)
and r.maints != 'D'
and ((t.expirycde in (149,150)) or (t.expirycde=113 and r.rsntcde=293)) -- 26 week reapp
and (to_date('01/01/1800','DD/MM/YYYY') + r.effectdt)+1/24 between current_date and current_date+35
and ((CURRENT_DATE - to_date('01/01/1800','DD/MM/YYYY') - c.dob)+1/24)/365 < 64
order by dbms_random.value)
where rownum = 1