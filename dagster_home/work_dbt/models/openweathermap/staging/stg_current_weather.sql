select
    created_at,
    place,
    lat,
    lon,
    sunrise_at,
    sunset_at,
    temp_celcius,
    temp_feels_like_celcius,
    temp_celcius_min,
    temp_celcius_max,
    humidity_percent as humidity_pct,
    sea_level_pressure_hpa,
    wind_speed_ms,
    wind_dir_degree,
    cloudiness_percent as cloudiness_pct,
    date_trunc('day', created_at) as created_at_dt
from {{ source('openweathermap', 'raw_current_weather') }}
