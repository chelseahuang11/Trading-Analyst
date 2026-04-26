with source as (
    select * from {{ source('raw', 'fred_observations') }}
)

select
    series_id,
    observation_date::date as observation_date,
    value::float         as value,
    loaded_at
from source
