"""Streamlit app."""

import os

import duckdb
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

DATABASE = os.environ.get("DB_NAME")

con = duckdb.connect(database=f"md:{DATABASE}")

st.title("FinGrid Power Generation")

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
