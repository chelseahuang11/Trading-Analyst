with observations as (
    select * from {{ ref('stg_fred_observations') }}
),

dates as (
    select * from {{ ref('dim_date') }}
),

indicators as (
    select * from {{ ref('dim_indicator') }}
)

select
    o.observation_date,
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    o.series_id,
    i.name             as indicator_name,
    i.category         as indicator_category,
    i.unit,
    i.frequency,
    o.value,
    o.loaded_at
from observations o
inner join dates      d on o.observation_date = d.full_date
inner join indicators i on o.series_id        = i.series_id
