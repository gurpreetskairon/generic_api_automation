select swn
from (
    select distinct sb.swn
    from sben sb
    join wami w
        on w.swn = sb.swn
    join srte r
        on r.swn = sb.swn
       and r.servcde = 365

    where sb.maints <> 'D'
      and sb.servstatus = 3
      and sb.servcde = 365

      and w.maints <> 'D'
      and w.wtind = 'P'

      -- Client must not already have a sanction
      and trim(w.sanctcde) is null
      and nvl(w.sanctgrdn, 0) = 0
      and nvl(w.sanctpctg, 0) = 0
      and nvl(w.sanctamt, 0) = 0
      and nvl(w.sanctdt, 0) = 0

      -- No recompliance
      and trim(w.recompcde) is null
      and nvl(w.recompdt, 0) = 0
      and nvl(w.exrsncde, 0) = 0

      -- Latest WAMI row
      and w.inputdt + (nvl(w.inputti, 0) / 1000000000) =
          (
              select max(
                  w2.inputdt +
                  (nvl(w2.inputti, 0) / 1000000000)
              )
              from wami w2
              where w2.swn = w.swn
                and w2.maints <> 'D'
          )

      -- Latest SRTE row
      and r.srte_id =
          (
              select max(r2.srte_id)
              from srte r2
              where r2.swn = r.swn
                and r2.servcde = 365
                and r2.maints <> 'D'
          )

      -- Confirmed positive candidate type
      and r.changetyp = 454

    order by dbms_random.value
)
where rownum <= 2
