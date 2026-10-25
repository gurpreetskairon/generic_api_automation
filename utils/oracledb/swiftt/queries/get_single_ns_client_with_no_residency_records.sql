select distinct s.swn
from sben s
-- Select current NS with no residency records
-- *** Contraints after all the joins ****
where   s.servcde = 180
  and   s.servstatus = 3
  and   s.sben_id = (select max (sben_id) from sben where sben.swn = s.swn and sben.servcde = s.servcde)
  and not exists (select * from SORR where sorr.swn = s.swn)

  order by s.swn