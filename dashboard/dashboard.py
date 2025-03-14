import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema utama
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Memuat data
@st.cache
def load_data():
    day_df = pd.read_csv(r"C:\submission 1\data\day.csv")
    hour_df = pd.read_csv(r"C:\submission 1\data\hour.csv")
    # Tambahkan kolom 'day_of_week'
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df['day_of_week'] = day_df['dteday'].dt.day_name()
    return day_df, hour_df

day_df, hour_df = load_data()

# Menampilkan informasi dataset
if st.sidebar.checkbox("Tampilkan Info Dataset"):
    st.subheader("Informasi Dataset Hari")
    st.write(day_df.info())
    st.subheader("Informasi Dataset Jam")
    st.write(hour_df.info())

# Analisis Penyewaan Sepeda
st.header("Analisis Penyewaan Sepeda")
option = st.selectbox("Pilih Analisis", ["Pola Penyewaan Harian", "Pola Penyewaan Jam"])

if option == "Pola Penyewaan Harian":
    daily_demand = day_df.groupby('day_of_week')['cnt'].mean().reset_index()
    peak_days = daily_demand.sort_values(by='cnt', ascending=False).head(3)
    off_peak_days = daily_demand.sort_values(by='cnt', ascending=True).head(3)

    st.subheader("Hari Puncak Penyewaan")
    st.write(peak_days)

    st.subheader("Hari Sepi Penyewaan")
    st.write(off_peak_days)

    # Visualisasi Pola Penyewaan Harian
    plt.figure(figsize=(10, 5))
    sns.barplot(data=daily_demand, x='day_of_week', y='cnt', palette='viridis')
    plt.title("Rata-rata Penyewaan Sepeda per Hari")
    plt.xticks(rotation=45)
    st.pyplot(plt)

elif option == "Pola Penyewaan Jam":
    hourly_demand = hour_df.groupby('hour')['cnt'].mean().reset_index()
    peak_hours = hourly_demand.sort_values(by='cnt', ascending=False).head(5)
    off_peak_hours = hourly_demand.sort_values(by='cnt', ascending=True).head(5)

    st.subheader("Jam Puncak Penyewaan")
    st.write(peak_hours)

    st.subheader("Jam Sepi Penyewaan")
    st.write(off_peak_hours)

    # Visualisasi Pola Penyewaan Jam
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_demand, x='hour', y='cnt', marker='o')
    plt.title("Rata-rata Penyewaan Sepeda per Jam")
    plt.xticks(range(0, 24))
    st.pyplot(plt)

# Analisis Pengaruh Cuaca
st.header("Pengaruh Cuaca Terhadap Penyewaan Sepeda")
weather_option = st.selectbox("Pilih Fitur Cuaca", ["Suhu", "Kelembaban", "Kecepatan Angin", "Kondisi Cuaca"])

if weather_option == "Suhu":
    sns.scatterplot(data=day_df, x='temp', y='cnt', hue='season', palette='coolwarm')
    plt.title("Pengaruh Suhu Terhadap Penyewaan Sepeda")
    st.pyplot(plt)

elif weather_option == "Kelembaban":
    sns.scatterplot(data=day_df, x='hum', y='cnt', hue='season', palette='coolwarm')
    plt.title("Pengaruh Kelembaban Terhadap Penyewaan Sepeda")
    st.pyplot(plt)

elif weather_option == "Kecepatan Angin":
    sns.scatterplot(data=day_df, x='windspeed', y='cnt', hue='season', palette='coolwarm')
    plt.title("Pengaruh Kecepatan Angin Terhadap Penyewaan Sepeda")
    st.pyplot(plt)

elif weather_option == "Kondisi Cuaca":
    sns.boxplot(data=day_df, x='weathersit', y='cnt')
    plt.title("Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda")
    st.pyplot(plt)

# Kesimpulan
st.header("Kesimpulan")
st.write("Dashboard ini memberikan wawasan mengenai pola penyewaan sepeda berdasarkan waktu dan pengaruh cuaca terhadap jumlah penyewaan.")

# Menampilkan footer
st.caption('Copyright (c) Dicoding 2023')
