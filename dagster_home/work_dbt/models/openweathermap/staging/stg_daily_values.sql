select
  created_at_DT,
  place,
  lat,
  lon,
  sunrise_at,
  sunset_at,
  min(temp_celcius) as min_temp_celcius,
  max(temp_celcius) as max_temp_celcius,
  min(temp_feels_like_celcius) as min_feels_like_temp_celcius,
  max(temp_feels_like_celcius) as max_feels_like_temp_celcius
from {{ ref('stg_current_weather') }}
group by
  place,
  created_at_DT,
  lat,
  lon,
  sunrise_at,
  sunset_at
