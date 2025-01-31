
  create view "Ethio_Medical_Database"."public"."my_model__dbt_tmp"
    
    
  as (
    select
  id,
  text,
  
  current_date
 as current_date
from
  "Ethio_Medical_Database"."public"."medical_database"
  );