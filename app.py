"""Streamlit app."""

import os

import duckdb
import streamlit as st

from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.environ.get("DB_NAME")

con = duckdb.connect(database=f"md:{DATABASE}")

st.title("FinGrid Power Generation")
query = """
SELECT inserted_at
FROM fingrid_api_data._dlt_loads
ORDER BY inserted_at DESC
LIMIT 1;
"""
last_updated = con.execute(query).fetchone()[0]
last_updated_minutes_ago = (
    datetime.now(timezone.utc) - last_updated
).total_seconds() / 60
st.text(f"Last updated {last_updated_minutes_ago:.0f} minutes ago.")

# Cumulative megawatts per hour compared to yesterday
query = """
WITH generated AS (
  SELECT
    generated_time,
    SUM(megawatt_hours) FILTER(WHERE generated_date = current_date - 1) AS megawatt_hours_yesterday,
    SUM(megawatt_hours) FILTER(WHERE generated_date = current_date) AS megawatt_hours_today
  FROM dwh.power_generated
  GROUP BY generated_time
  ORDER BY generated_time
)
SELECT
  generated_time,
  megawatt_hours_today,
  SUM(megawatt_hours_yesterday) OVER (ORDER BY generated_time) AS yesterday,
  CASE WHEN megawatt_hours_today IS NULL THEN NULL ELSE SUM(megawatt_hours_today) OVER (ORDER BY generated_time) END AS today
FROM generated;
"""
df = con.execute(query).df()
df.generated_time = df.generated_time.astype(str)
st.subheader("Live Cumulative Generated Wind Power")
st.line_chart(
    data=df,
    x="generated_time",
    y=["yesterday", "today"],
    y_label="Megawatt Hours",
    x_label="Time",
)
st.bar_chart(
    data=df,
    x="generated_time",
    y="megawatt_hours_today",
    y_label="Megawatt Hours",
    x_label="Time",
)
