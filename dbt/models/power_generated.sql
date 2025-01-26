WITH raw AS (
  SELECT start_time, end_time, value
  FROM fingrid_api_data.resource__data
  WHERE value IS NOT NULL
)
, upsampled AS (
  SELECT *
  FROM generate_series(
    (SELECT min(start_time) FROM raw),
    (SELECT max(end_time) FROM raw),
    INTERVAL '1 minute'
  ) g(generated_minute)
  JOIN raw d ON g.generated_minute BETWEEN d.start_time AND d.end_time
)
, downsampled AS (
  SELECT g.quarter_hour AS generated_at, avg(d.value) AS megawatts
  FROM generate_series(
    (SELECT date_trunc('hour', min(start_time)) FROM raw),
    (SELECT date_trunc('hour', max(end_time)) + INTERVAL '1 hour' FROM raw),
    INTERVAL '15 minutes'
  ) g(quarter_hour)
  LEFT JOIN upsampled d ON g.quarter_hour <= d.generated_minute AND g.quarter_hour + INTERVAL '15 minutes' > d.generated_minute 
  GROUP BY g.quarter_hour
)
, filled AS (
  SELECT
    generated_at,
    first_value(megawatts) OVER (PARTITION BY grp_megawatts) AS megawatts
  FROM (
    SELECT *, sum(CASE WHEN megawatts IS NOT NULL THEN 1 END) OVER (ORDER BY generated_at) AS grp_megawatts
    FROM downsampled
  )
)
SELECT
  generated_at,
  date_trunc('day', generated_at AT TIME ZONE 'Europe/Helsinki') AS generated_date,
  (generated_at AT TIME ZONE 'Europe/Helsinki')::time AS generated_time,
  megawatts,
  megawatts * 0.25 AS megawatt_hours
FROM filled