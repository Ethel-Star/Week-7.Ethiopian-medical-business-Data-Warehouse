
      
  
    

  create  table "Ethio_Medical_Database"."analytics"."medical_data_snapshot"
  
  
    as
  
  (
    
    

    select *,
        md5(coalesce(cast(id as varchar ), '')
         || '|' || coalesce(cast(now()::timestamp without time zone as varchar ), '')
        ) as dbt_scd_id,
        now()::timestamp without time zone as dbt_updated_at,
        now()::timestamp without time zone as dbt_valid_from,
        
  
  coalesce(nullif(now()::timestamp without time zone, now()::timestamp without time zone), null)
  as dbt_valid_to
from (
        



select
  id,
  text,
  youtube_links,
  -- Label for YouTube link status
  case 
      when youtube_links is not null and youtube_links != '' then 'Has Link'
      else 'No Link'
  end as link_status,
  channel,
  image_path,
  contains_emoji,
  has_youtube_link,
  date
from "Ethio_Medical_Database"."public"."medical_database"  -- Uses the source defined in sources.yml

    ) sbq



  );
  
  