SELECT
TRIM(weekdag) as weekdag,
TRIM(datum) as datum,
ID,
TRIM(maaltijdnaam) as maaltijdnaam,
TRIM(link) as link
from {{ source('recipes', 'raw_daily_recipes') }}
