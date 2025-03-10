import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
day_df = pd.read_csv("data/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Streamlit dashboard setup
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♂️ Bike Sharing Dashboard")

# Sidebar controls
st.sidebar.header("Filter Data")
selected_year = st.sidebar.radio("Pilih Tahun:", options=[2011, 2012])
day_df = day_df[day_df['yr'] == (selected_year - 2011)]

# 1. Tren Penyewaan Sepeda Bulanan
st.subheader("📅 Tren Penyewaan Sepeda Bulanan")
monthly_usage = day_df.groupby(day_df['dteday'].dt.month)['cnt'].sum()
fig, ax = plt.subplots()
ax.plot(monthly_usage.index, monthly_usage.values, marker='o', linestyle='-', color='blue')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.set_ylabel("Total Penyewaan")
ax.set_xlabel("Bulan")
st.pyplot(fig)

# 2. Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x=day_df['weathersit'], y=day_df['cnt'], ax=ax, palette="coolwarm")
ax.set_xticklabels(["Cerah", "Mendung", "Hujan Ringan", "Cuaca Buruk"])
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# 3. Tren Penyewaan Sepeda Harian
st.subheader("🕒 Tren Penyewaan Sepeda per Jam")
hour_df = pd.read_csv("data/hour.csv")
avg_hourly_usage = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots()
ax.plot(avg_hourly_usage.index, avg_hourly_usage.values, marker='o', color='green')
ax.set_xticks(range(0, 24))
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel("Jam dalam Sehari")
st.pyplot(fig)

st.caption("📊 Dashboard ini menampilkan tren penyewaan sepeda berdasarkan waktu dan kondisi cuaca. Dibuat dengan Streamlit, Pandas, Matplotlib, dan Seaborn.")
