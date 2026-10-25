SELECT unique se.swn, cl.ptnrswn, sb.servstatus from sexpr se, clint cl, sben sb
where se.expirydt > 78417 
and se.servcde = 675 
and se.expirycde = 113
and se.rsntcde = 293
and se.maints != 'D' 
and se.actionind = ' '
and se.useract = ' '
and cl.swn = se.swn 
and cl.maints <> 'D'
and sb.servcde = se.servcde 
and sb.swn = se.swn 
and sb.servstatus = 3
and sb.sben_id = (select max(sben_id) from sben where sben.swn = se.swn and sben.servcde = se.servcde) 
and sb.apprtind != 1
and cl.securedind = 'N'
and cl.ptnrswn = 0
-- No children
and not exists(select * from relat r where r.servcde = se.servcde and r.maints <> 'D' and r.maints <> 'I' and r.swn in (se.swn)
and exists (select * from child_x ch where ch.childswn = r.childswn AND ch.maints <> 'D'))
-- Has Accommodation Sup
and exists (select * from ssup ss where
ss.servcde = se.servcde
and ss.swn = se.swn
and ss.supservcde = 471
and ss.servstatus = 3
and ss.maints <> 'D')
and cl.givenames not like '%TEST%'
and cl.sname not like '%TEST%'

-- Exclude expiries where the hours worked at renewal date is 30 or more
and not exists (select incms.incmhours from incms
    where incms.incmnbr =
        (select incm.incmnbr
        from incm
        where incm.effectdt =
            (select max (effectdt)
                from incm
                where incm.swn = se.swn
                and incm.servcde = se.servcde
                and incm.effectdt <= se.expirydt)
        and incm.swn = se.swn
        and incm.servcde = se.servcde
        and incms.incmhours > 29))

order by dbms_random.value
--order by se.swn desc