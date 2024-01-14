import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import openmeteo_requests
import requests_cache
from datetime import date
from retry_requests import retry

st.set_page_config(
        page_title="San Francisco Rainfall",
)

st.title("San Francisco Rainfall")

DATE_RANGE = st.date_input("Time range", value=[date(2020, 10, 1), date.today()])

def get_season_from_date(datetime):
    date = datetime.date()
    season = date.year if date.month > 9 else date.year - 1
    return season

def get_season_start_date_from_season(season):
    return date(season, 10, 1)

def get_day_season_rank(datetime):
    date = datetime.date()
    delta = date - get_season_start_date_from_season(get_season_from_date(datetime))
    return delta.days

def get_day_in_season(datetime):
    return datetime.strftime("%b %d")


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 37.7749,
	"longitude": -122.4194,
	"start_date": DATE_RANGE[0],
	"end_date": DATE_RANGE[1],
	"daily": "precipitation_sum",
    "precipitation_unit": "inch",
	"timezone": "America/Los_Angeles"
}

responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

daily = response.Daily()
daily_precipitation_sum = daily.Variables(0).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["precipitation_sum"] = daily_precipitation_sum

daily_dataframe = pd.DataFrame(data = daily_data)
daily_dataframe["date"] = daily_dataframe["date"].apply(lambda x: pd.to_datetime(x))
daily_dataframe["x_rank"] = daily_dataframe["date"].apply(get_day_season_rank)
daily_dataframe["Day"] = daily_dataframe["date"].apply(get_day_in_season)
daily_dataframe["season"] = daily_dataframe["date"].apply(lambda x: str(get_season_from_date(x)))
daily_dataframe["Cumulative Rainfall (Inches)"] = daily_dataframe.groupby('season')['precipitation_sum'].cumsum()
daily_dataframe["14 Day Rolling Rainfall (Inches)"] = daily_dataframe.groupby('season')['precipitation_sum'].rolling(window=14,min_periods=14).sum().reset_index(0,drop=True)

st.altair_chart(alt.Chart(daily_dataframe, height=700, width=700, title="Cumulative Seasonal Rainfall")
    .mark_line().encode(
    x=alt.X('Day', sort=alt.EncodingSortField(field="x_rank", op="min")),
    y='Cumulative Rainfall (Inches)',
    color='season',
    )
)

st.altair_chart(alt.Chart(daily_dataframe, height=700, width=700, title="14 Day Rolling Rainfall")
    .mark_line().encode(
    x=alt.X('Day', sort=alt.EncodingSortField(field="x_rank", op="min")),
    y='14 Day Rolling Rainfall (Inches)',
    color='season',
    )
)
