with dates as (
    select
        dateadd(day, seq4(), '2000-01-01'::date) as full_date
    from table(generator(rowcount => 11323))
)

select
    full_date,
    year(full_date)          as year,
    quarter(full_date)       as quarter,
    month(full_date)         as month,
    monthname(full_date)     as month_name,
    day(full_date)           as day,
    dayofweekiso(full_date)  as day_of_week,
    dayname(full_date)       as day_name,
    case
        when dayofweekiso(full_date) in (6, 7) then true
        else false
    end                      as is_weekend
from dates
