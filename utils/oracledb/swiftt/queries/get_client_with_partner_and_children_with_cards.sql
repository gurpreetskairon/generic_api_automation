select distinct cl.ptnrswn as swn, cl.swn as ptnrswn, sd.servcde, sd.servstatus, sb.apprtind, cl.sname, cl.givenames
from clint cl, sdet sd, sben sb

where sd.servstatus in (3,4,5) 

and cl.swn = sd.swn 
and cl.securedind <> 'Y'
and cl.swn < 450000000
and cl.ptnrswn > 0 
and cl.ptnrswn < 450000000 
and sb.servcde = sd.servcde and sb.swn = sd.swn 
and sb.sben_id = (select max(sben_id) from sben where sben.swn = sd.swn and sben.servcde = sd.servcde)
and sb.apprtind = 2

and exists (select * from sdet sdc where sdc.swn = cl.ptnrswn and sdc.servcde in (340,344) and sdc.servstatus in (3,4,5))
order by sd.servcde, sd.servstatus desc