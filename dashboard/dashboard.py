import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
day_df = pd.read_csv(r"C:\submission 1\data\day.csv")
hour_df = pd.read_csv(r"C:\submission 1\data\hour.csv")

# Feature Engineering (repeat feature engineering for code completeness)
day_df['year'] = pd.to_datetime(day_df['dteday']).dt.year
day_df['month'] = pd.to_datetime(day_df['dteday']).dt.month_name()
day_df['day_of_week'] = pd.to_datetime(day_df['dteday']).dt.day_name()
hour_df['hour'] = pd.to_datetime(hour_df['dteday']).dt.hour
hour_df['year'] = pd.to_datetime(hour_df['dteday']).dt.year
hour_df['month'] = pd.to_datetime(hour_df['dteday']).dt.month_name()
hour_df['day_of_week'] = pd.to_datetime(hour_df['dteday']).dt.day_name()

# Streamlit Dashboard
st.title("Dashboard Penyewaan Sepeda")

# Section for Hourly Rentals
st.header("Jumlah Penyewaan Sepeda per Jam")
hourly_rentals = hour_df.groupby('hour')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_rentals, x='hour', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section for Daily Demand Pattern
st.header("Jumlah Penyewaan Sepeda Harian")
daily_demand = day_df.groupby('day_of_week')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=daily_demand, x='day_of_week', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Harian')
ax.set_xlabel('Hari')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section for Monthly Demand Pattern
st.header("Jumlah Penyewaan Sepeda per Bulan")
monthly_demand = day_df.groupby('month')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_demand, x='month', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section for Weather Impact
st.header("Jumlah Penyewaan berdasarkan Situasi Cuaca")
weather_sit_demand = hour_df.groupby('weathersit')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=weather_sit_demand, x='weathersit', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan berdasarkan Situasi Cuaca')
ax.set_xlabel('Situasi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks([0, 1, 2, 3], ['Clear', 'Mist', 'Light Rain', 'Heavy Rain'])
st.pyplot(fig)

# Section for Rental Time Groups
st.header("Rata-rata Penyewaan Sepeda Berdasarkan Kelompok Waktu")
def categorize_rental_time(hour):
    if 7 <= hour < 9 or 16 <= hour < 18:
        return "Jam Sibuk (Peak Hours)"
    elif 10 <= hour < 15:
        return "Tengah Hari (Midday)"
    elif 18 <= hour < 22:
        return "Malam Hari (Evening)"
    else:
        return "Luar Jam Sibuk (Off-Peak Hours)"

hour_df['rental_time_group'] = hour_df['hour'].apply(categorize_rental_time)
rental_time_demand = hour_df.groupby('rental_time_group')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=rental_time_demand, x='rental_time_group', y='cnt', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kelompok Waktu')
ax.set_xlabel('Kelompok Waktu Penyewaan')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section for Temperature Binning
st.header("Rata-rata Penyewaan Berdasarkan Kelompok Suhu")
bins = [float('-inf'), 0.25, 0.6, float('inf')]
labels = ["Dingin", "Sejuk", "Hangat"]
day_df['temp_bin'] = pd.cut(day_df['temp'], bins=bins, labels=labels, right=False)
temp_bin_demand = day_df.groupby('temp_bin')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=temp_bin_demand, x='temp_bin', y='cnt', ax=ax)
ax.set_title('Rata-rata Penyewaan Berdasarkan Kelompok Suhu')
ax.set_xlabel('Kelompok Suhu')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(fig)

# Section for Humidity Binning
st.header("Rata-rata Penyewaan Berdasarkan Kelompok Kelembaban")
bins_hum = [float('-inf'), 0.6, 0.8, float('inf')]
labels_hum = ["Rendah", "Sedang", "Tinggi"]
day_df['hum_bin'] = pd.cut(day_df['hum'], bins=bins_hum, labels=labels_hum, right=False)
hum_bin_demand = day_df.groupby('hum_bin')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=hum_bin_demand, x='hum_bin', y='cnt', ax=ax)
ax.set_title('Rata-rata Penyewaan Berdasarkan Kelompok Kelembaban')
ax.set_xlabel('Kelompok Kelembaban')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(fig)
