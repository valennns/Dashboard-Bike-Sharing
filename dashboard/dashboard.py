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

# Perbandingan Penyewaan Holiday vs Non-Holiday
with st.expander("🏖️ Penyewaan pada Hari Libur vs Non-Libur"):
    holiday_rentals = hour_df.groupby('holiday')['cnt'].sum().reset_index()
    holiday_rentals['holiday'] = holiday_rentals['holiday'].map({0: 'Non-Holiday', 1: 'Holiday'})
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=holiday_rentals, x='holiday', y='cnt', ax=ax)
    ax.set_title("Perkiraan Jumlah Penyewaan Holiday vs Non-Holiday")
    ax.set_xlabel("Holiday (1=Holiday, 0=Non-Holiday)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Perbandingan Penyewaan Working Day vs Non-Working Day
with st.expander("📅 Penyewaan pada Hari Kerja vs Hari Libur"):
    workingday_rentals = hour_df.groupby('workingday')['cnt'].sum().reset_index()
    workingday_rentals['workingday'] = workingday_rentals['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'})
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=workingday_rentals, x='workingday', y='cnt', ax=ax)
    ax.set_title("Perkiraan Jumlah Penyewaan Working Day vs Non-Working Day")
    ax.set_xlabel("Working Day (1=Working Day, 0=Non-Working Day)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Heatmap Korelasi
with st.expander("📊 Korelasi Faktor Cuaca dan Penyewaan"):
    correlation_matrix = hour_df[['temp', 'hum', 'windspeed', 'weathersit', 'cnt', 'casual', 'registered']].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title("Correlation Matrix of Weather Features and Rental Counts")
    st.pyplot(fig)

# Penyewaan Berdasarkan Situasi Cuaca
with st.expander("🌤️ Penyewaan Berdasarkan Situasi Cuaca"):
    weather_rentals = hour_df.groupby('weathersit')['cnt'].sum().reset_index()
    weather_rentals['weathersit'] = weather_rentals['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'})
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weather_rentals, x='weathersit', y='cnt', ax=ax)
    ax.set_title("Jumlah Penyewaan berdasarkan Situasi Cuaca")
    ax.set_xlabel("Situasi Cuaca (1=Clear, 2=Mist, 3=Light Rain, 4=Heavy Rain)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Penyewaan Berdasarkan Faktor Cuaca
with st.expander("🌤️ Penyewaan Berdasarkan Faktor Cuaca"):
    weather_features = ['temp', 'hum', 'windspeed']
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for i, feature in enumerate(weather_features):
        sns.scatterplot(data=hour_df, x=feature, y='cnt', ax=axes[0, i])
        axes[0, i].set_title(f'Rental Count vs {feature}')
        axes[0, i].set_xlabel(feature)
        axes[0, i].set_ylabel('Rental Count')
        
        sns.scatterplot(data=hour_df, x=feature, y='casual', label='Casual Users', ax=axes[1, i])
        sns.scatterplot(data=hour_df, x=feature, y='registered', label='Registered Users', ax=axes[1, i])
        axes[1, i].set_title(f'Rental Count vs {feature} by User Type')
        axes[1, i].set_xlabel(feature)
        axes[1, i].set_ylabel('Rental Count')
        axes[1, i].legend()
    plt.tight_layout()
    st.pyplot(fig)



st.caption("© 2025 - Bike Sharing Analysis Dashboard")
