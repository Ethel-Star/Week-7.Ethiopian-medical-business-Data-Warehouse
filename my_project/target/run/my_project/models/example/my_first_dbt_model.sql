
  
    

  create  table "Ethio_Medical_Database"."public"."my_first_dbt_model__dbt_tmp"
  
  
    as
  
  (
    

with source_data as (
    select 
        id,
        text,
        youtube_links,
        channel,
        image_path,
        contains_emoji,
        has_youtube_link,
        date
    from public.medical_database -- Use your actual table name
),

cleaned_data as (
    -- Remove emojis from the text field
    select
        id,
        -- Remove non-ASCII characters (emojis) and store cleaned text
        regexp_replace(text, '[^\x00-\x7F]+', '', 'g') as text,
        youtube_links,
        channel,
        image_path,
        -- Check for emojis and store a flag
        case 
            when text ~ '[^\x00-\x7F]' then 'Yes'  -- Contains emojis
            else 'No'  -- Does not contain emojis
        end as contains_emoji,
        -- Check if there's a YouTube link (non-null youtube_links)
        case 
            when youtube_links is not null and youtube_links != '' then 'Yes'
            else 'No'
        end as has_youtube_link,
        date
    from source_data
)

-- Final selection with the transformations
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
from cleaned_data
where id is not null
  );
  