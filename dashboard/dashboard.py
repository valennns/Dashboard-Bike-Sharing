import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv(r"C:\submission 1\data\day.csv")

# Feature Engineering
day_df['year'] = pd.to_datetime(day_df['dteday']).dt.year
day_df['month'] = pd.to_datetime(day_df['dteday']).dt.month_name()
day_df['day_of_week'] = pd.to_datetime(day_df['dteday']).dt.day_name()

# Streamlit Dashboard
st.title("Dashboard Penyewaan Sepeda")

# Section: Daily Demand Pattern
st.header("Jumlah Penyewaan Sepeda Harian")
daily_demand = day_df.groupby('day_of_week')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=daily_demand, x='day_of_week', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Harian')
ax.set_xlabel('Hari')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section: Monthly Demand Pattern
st.header("Jumlah Penyewaan Sepeda per Bulan")
monthly_demand = day_df.groupby('month')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_demand, x='month', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Section: Temperature Binning
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
