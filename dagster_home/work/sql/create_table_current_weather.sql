CREATE TABLE openweathermap.raw_current_weather (
    created_at timestamptz,
    place character(30),
    lat float,
    lon float,
    sunrise_at timestamptz,
    sunset_at timestamptz,
    temp_celcius float,
    temp_feels_like_celcius float,
    temp_celcius_min float,
    temp_celcius_max float,
    humidity_percent int,
    sea_level_pressure_hpa float,
    wind_speed_ms float,
    wind_dir_degree int,
    cloudiness_percent int
)
