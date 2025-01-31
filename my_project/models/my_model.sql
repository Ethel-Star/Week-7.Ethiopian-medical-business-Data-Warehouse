
select
  id,
  text,
  {{ get_current_date() }} as current_date
from
  {{ source('raw', 'medical_database') }}
