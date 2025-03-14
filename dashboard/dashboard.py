import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
df = pd.read_csv("C:\submission 1\data\day.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# Konfigurasi dashboard
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Header utama
st.title("📊 Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk filter
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['dteday'].min(), df['dteday'].max()])
df_filtered = df[(df['dteday'] >= pd.to_datetime(date_range[0])) & (df['dteday'] <= pd.to_datetime(date_range[1]))]

# Tren Penyewaan Sepeda
st.subheader("📅 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_filtered['dteday'], df_filtered['cnt'], marker='o', linestyle='-', color='blue')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda Harian")
ax.grid()
st.pyplot(fig)

# Analisis Musiman
st.subheader("🌤️ Pengaruh Musim terhadap Penyewaan Sepeda")
df_season = df.groupby("season")["cnt"].mean().reset_index()
df_season['season'] = df_season['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=df_season, palette='coolwarm', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
st.pyplot(fig)

# Analisis Cuaca
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
df_weather = df.groupby("weathersit")["cnt"].mean().reset_index()
df_weather['weathersit'] = df_weather['weathersit'].map({1: 'Cerah', 2: 'Mendung', 3: 'Hujan/Salju Ringan', 4: 'Cuaca Ekstrem'})
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='cnt', data=df_weather, palette='viridis', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)

# Korelasi Faktor Cuaca dengan Penyewaan
st.subheader("📈 Korelasi Faktor Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(df[['temp', 'hum', 'windspeed', 'cnt']].corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Korelasi Faktor Cuaca terhadap Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("**Sumber Data:** Dataset Penyewaan Sepeda")
