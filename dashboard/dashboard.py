import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF"

# Load dataset
day_df = pd.read_csv("data/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Konfigurasi Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♂️ Bike Sharing Dashboard")
st.markdown("Analisis tren penyewaan sepeda berdasarkan waktu dan faktor lingkungan.")

# Sidebar untuk filter tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df['dteday'].min(), day_df['dteday'].max()])
day_df = day_df[(day_df['dteday'] >= pd.to_datetime(date_range[0])) & (day_df['dteday'] <= pd.to_datetime(date_range[1]))]

# Tren Penyewaan Sepeda Harian
st.subheader("📅 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(day_df['dteday'], day_df['cnt'], marker='o', linestyle='-', color=PRIMARY_COLOR)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda Harian")
ax.grid()
st.pyplot(fig)

# Analisis Musiman
st.subheader("🌤️ Pengaruh Musim terhadap Penyewaan Sepeda")
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_season = day_df.groupby("season")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=df_season, palette='coolwarm', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
st.pyplot(fig)

# Analisis Cuaca
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
day_df['weathersit'] = day_df['weathersit'].map({1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan', 4: 'Cuaca Ekstrem'})
df_weather = day_df.groupby("weathersit")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='cnt', data=df_weather, palette='viridis', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)

# Korelasi Faktor Cuaca dengan Penyewaan
st.subheader("📈 Korelasi Faktor Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(day_df[['temp', 'hum', 'windspeed', 'cnt']].corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Korelasi Faktor Cuaca terhadap Penyewaan Sepeda")
st.pyplot(fig)

# Pengaruh Cuaca terhadap Jenis Pengguna
st.subheader("👥 Pengaruh Cuaca terhadap Jenis Pengguna")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, feature in enumerate(['temp', 'hum', 'windspeed']):
    sns.scatterplot(data=day_df, x=feature, y='casual', ax=axes[i], label='Casual Users', color='#FF5733')
    sns.scatterplot(data=day_df, x=feature, y='registered', ax=axes[i], label='Registered Users', color=PRIMARY_COLOR)
    axes[i].set_title(f"Penyewaan vs {feature} berdasarkan Jenis Pengguna")
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Jumlah Penyewaan")
    axes[i].legend()
st.pyplot(fig)

st.caption("© 2025 - Bike Sharing Analysis Dashboard")
