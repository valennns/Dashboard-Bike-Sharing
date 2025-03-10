import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

# Convert date column
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Streamlit configuration
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♂️ Bike Sharing Dashboard")
st.markdown("Analisis tren penyewaan sepeda berdasarkan waktu dan faktor lingkungan.")

# Pertanyaan 1: Kapan saja penyewaan sepeda sangat ramai atau sepi di luar perkiraan?
st.subheader("📊 Tren Penyewaan Sepeda per Jam")

time_df = hour_df.groupby('hr').agg({'cnt': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=time_df['hr'], y=time_df['cnt'], marker='o', color='#29B5DA')
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
st.pyplot(fig)

st.markdown("**Insight:** Penyewaan memuncak pada jam sibuk (08:00 & 17:00), sementara lebih sepi pada malam hari.")

# Pertanyaan 2: Seberapa besar pengaruh cuaca terhadap jumlah penyewaan sepeda?
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_df = day_df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()
weather_df['weathersit'] = weather_df['weathersit'].map({
    1: 'Cerah/Berawan',
    2: 'Kabut/Awan',
    3: 'Hujan Ringan',
    4: 'Cuaca Ekstrem'
})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='cnt', data=weather_df, palette='Blues')
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("**Insight:** Penyewaan sepeda lebih rendah saat hujan atau cuaca ekstrem.")

# Visualisasi pengaruh suhu terhadap penyewaan
st.subheader("🌡️ Pengaruh Suhu terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x=day_df['temp'], y=day_df['cnt'], alpha=0.6, color='#FF5733')
ax.set_xlabel("Temperatur (Normalized)")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Hubungan antara Temperatur dan Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("**Insight:** Penyewaan meningkat pada suhu sedang, tetapi menurun pada suhu ekstrem.")

# Visualisasi pengaruh kelembapan terhadap penyewaan
st.subheader("💧 Pengaruh Kelembapan terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x=day_df['hum'], y=day_df['cnt'], alpha=0.6, color='#33A1FF')
ax.set_xlabel("Kelembapan (Normalized)")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Hubungan antara Kelembapan dan Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("**Insight:** Penyewaan cenderung menurun pada kelembapan yang sangat tinggi.")

# Visualisasi pengaruh kecepatan angin terhadap penyewaan
st.subheader("💨 Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x=day_df['windspeed'], y=day_df['cnt'], alpha=0.6, color='#2ECC71')
ax.set_xlabel("Kecepatan Angin (Normalized)")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Hubungan antara Kecepatan Angin dan Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("**Insight:** Kecepatan angin tidak terlalu mempengaruhi jumlah penyewaan secara signifikan.")

st.caption("© 2025 - Bike Sharing Analysis Dashboard")
