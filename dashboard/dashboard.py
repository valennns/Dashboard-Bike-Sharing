import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF"

# Load dataset
try:
    hour_df = pd.read_csv("data/hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
except FileNotFoundError:
    st.error("File tidak ditemukan. Pastikan file sudah diunggah dengan benar.")
    st.stop()

# Konfigurasi Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♂️ Bike Sharing Dashboard")
st.markdown("Analisis tren penyewaan sepeda berdasarkan waktu dan faktor lingkungan.")

# Sidebar untuk filter tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [hour_df['dteday'].min(), hour_df['dteday'].max()])
hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(date_range[0])) & (hour_df['dteday'] <= pd.to_datetime(date_range[1]))]

# Jumlah Penyewaan Sepeda per Jam
with st.expander("⏰ Jumlah Penyewaan Sepeda per Jam"):
    hourly_rentals = hour_df.groupby('hr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_rentals, x='hr', y='cnt', marker='o', color=PRIMARY_COLOR)
    ax.set_title("Jumlah Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid()
    st.pyplot(fig)

# Pola Permintaan Harian
with st.expander("📅 Pola Permintaan Harian"):
    daily_demand = hour_df.groupby('weekday')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=daily_demand, x='weekday', y='cnt', palette='coolwarm', ax=ax)
    ax.set_title("Jumlah Penyewaan Sepeda Harian")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid(axis='y')
    st.pyplot(fig)

# Pola Permintaan Bulanan
with st.expander("📆 Pola Permintaan Bulanan"):
    monthly_demand = hour_df.groupby('mnth')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_demand, x='mnth', y='cnt', marker='o', color=SECONDARY_COLOR)
    ax.set_title("Jumlah Penyewaan Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid()
    st.pyplot(fig)

# Matriks Korelasi Faktor Cuaca
with st.expander("📈 Korelasi Faktor Cuaca dengan Penyewaan Sepeda"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(hour_df[['temp', 'hum', 'windspeed', 'weathersit', 'cnt', 'casual', 'registered']].corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Matrix of Weather Features and Rental Counts")
    st.pyplot(fig)

# Perbandingan Penyewaan Hari Libur vs Non-Libur dan Hari Kerja vs Non-Kerja
with st.expander("🏖️ Perbandingan Penyewaan Holiday vs Non-Holiday & Working Day vs Non-Working Day"):
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    sns.barplot(x=hour_df['holiday'].map({0: 'Non-Holiday', 1: 'Holiday'}), y=hour_df['cnt'], ax=axes[0])
    axes[0].set_title("Perkiraan Jumlah Penyewaan Holiday vs Non-Holiday")
    axes[0].set_xlabel("Holiday (1=Holiday, 0=Non-Holiday)")
    axes[0].set_ylabel("Jumlah Penyewaan")
    
    sns.barplot(x=hour_df['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'}), y=hour_df['cnt'], ax=axes[1])
    axes[1].set_title("Perkiraan Jumlah Penyewaan Working Day vs Non-Working Day")
    axes[1].set_xlabel("Working Day (1=Working Day, 0=Non-Working Day)")
    axes[1].set_ylabel("Jumlah Penyewaan")
    
    st.pyplot(fig)

st.caption("© 2025 - Bike Sharing Analysis Dashboard")
