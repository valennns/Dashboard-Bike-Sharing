import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv(r"C:\submission 1\data\day.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping season names
df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Mapping weather conditions
df['weathersit'] = df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
})

# Dashboard Title
st.title("Bike Sharing Analysis Dashboard 🚴‍♂️")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_season = st.sidebar.multiselect("Select Season", df['season'].unique(), default=df['season'].unique())
selected_weather = st.sidebar.multiselect("Select Weather Condition", df['weathersit'].unique(), default=df['weathersit'].unique())

# Filter data
df_filtered = df[(df['season'].isin(selected_season)) & (df['weathersit'].isin(selected_weather))]

# Trend Analysis
st.subheader("Daily Rental Trends")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=df_filtered, x='dteday', y='cnt', ax=ax, color='#007BFF')
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Impact of Weather
st.subheader("Weather Impact on Bike Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df_filtered, x='weathersit', y='cnt', palette='coolwarm', ax=ax)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")
st.pyplot(fig)

# Impact of Temperature
st.subheader("Effect of Temperature on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_filtered, x='temp', y='cnt', color='#FF5733', alpha=0.7)
ax.set_xlabel("Temperature (Normalized)")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Impact of Humidity
st.subheader("Effect of Humidity on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_filtered, x='hum', y='cnt', color='#1F77B4', alpha=0.7)
ax.set_xlabel("Humidity (Normalized)")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Impact of Wind Speed
st.subheader("Effect of Wind Speed on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_filtered, x='windspeed', y='cnt', color='#2CA02C', alpha=0.7)
ax.set_xlabel("Wind Speed (Normalized)")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Summary Insights
st.markdown("## Key Insights:")
st.markdown("- Bike rentals peak during warmer months and drop in winter.")
st.markdown("- Clear weather increases rentals, while heavy rain/snow reduces demand.")
st.markdown("- Rentals correlate positively with temperature up to a certain threshold.")
st.markdown("- Higher humidity levels may slightly reduce rentals.")
st.markdown("- Wind speed does not have a strong effect on rentals.")
