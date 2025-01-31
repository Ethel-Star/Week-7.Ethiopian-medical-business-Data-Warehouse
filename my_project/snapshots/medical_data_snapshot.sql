{% snapshot medical_data_snapshot %}

{{ 
  config(
    target_schema='analytics',
    unique_key='id',
    strategy='check',
    check_cols=['text', 'youtube_links', 'image_path', 'contains_emoji', 'has_youtube_link']
  )
}}

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
from {{ source('raw', 'medical_database') }}  -- Uses the source defined in sources.yml

{% endsnapshot %}
