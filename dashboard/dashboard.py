import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
day_df = pd.read_csv(r"C:\submission 1\data\day.csv")

# Konversi kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mapping untuk musim dan kondisi cuaca
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Cerah/Berawan',
    2: 'Kabut/Awan',
    3: 'Hujan Ringan/Salju Ringan',
    4: 'Cuaca Ekstrem'
})

# Sidebar untuk filter rentang waktu
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter dataset berdasarkan rentang waktu
filtered_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

st.header("Bike Sharing Analysis Dashboard 🚴")

# 1. Analisis Tren Penyewaan Sepeda
st.subheader("Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_df["dteday"], filtered_df["cnt"], marker='o', linestyle='-', color="#29B5DA")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda Harian")
plt.xticks(rotation=45)
st.pyplot(fig)

# 2. Analisis Pengaruh Cuaca
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_df, x='temp', y='cnt', hue='weathersit', palette='coolwarm', alpha=0.7, ax=ax)
ax.set_title("Hubungan Temperatur dan Penyewaan Sepeda")
ax.set_xlabel("Temperatur (Normalisasi)")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# 3. Perbandingan Pengaruh Cuaca untuk Casual vs Registered
st.subheader("Pengaruh Cuaca terhadap Jenis Pengguna")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_df, x='temp', y='casual', color='red', label='Casual', alpha=0.6, ax=ax)
sns.scatterplot(data=filtered_df, x='temp', y='registered', color='blue', label='Registered', alpha=0.6, ax=ax)
ax.set_title("Perbandingan Casual vs Registered")
ax.set_xlabel("Temperatur")
ax.set_ylabel("Jumlah Penyewaan")
ax.legend()
st.pyplot(fig)

st.caption("Dashboard dibuat dengan Streamlit, Pandas, Matplotlib, dan Seaborn.")
