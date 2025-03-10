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

# Pertanyaan 1: Kapan saja penyewaan sepeda sangat ramai atau sepi di luar perkiraan? Apa penyebabnya?
st.subheader("📊 Tren Penyewaan Sepeda per Jam")

hourly_rentals = hour_df.groupby('hr')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_rentals, x='hr', y='cnt', marker='o', color='#29B5DA')
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda per Jam")
st.pyplot(fig)

st.subheader("📅 Jumlah Penyewaan Sepeda Harian")
daily_demand = day_df.groupby('weekday')['cnt'].sum().reset_index()
daily_demand['weekday'] = daily_demand['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=daily_demand, x='weekday', y='cnt', palette='Blues')
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda Harian")
st.pyplot(fig)

st.subheader("📆 Jumlah Penyewaan Sepeda per Bulan")
monthly_demand = day_df.groupby('mnth')['cnt'].sum().reset_index()
monthly_demand['mnth'] = monthly_demand['mnth'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'})
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_demand, x='mnth', y='cnt', marker='o', color='#29B5DA')
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda per Bulan")
st.pyplot(fig)

st.subheader("📊 Pengaruh Hari Libur dan Hari Kerja")
holiday_demand = day_df.groupby('holiday')['cnt'].sum().reset_index()
workingday_demand = day_df.groupby('workingday')['cnt'].sum().reset_index()
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.barplot(data=holiday_demand, x='holiday', y='cnt', ax=axes[0], palette='coolwarm')
axes[0].set_title("Penyewaan Holiday vs Non-Holiday")
axes[0].set_xticklabels(['Non-Holiday', 'Holiday'])
axes[0].set_xlabel("Holiday")
axes[0].set_ylabel("Jumlah Penyewaan")
sns.barplot(data=workingday_demand, x='workingday', y='cnt', ax=axes[1], palette='coolwarm')
axes[1].set_title("Penyewaan Working Day vs Non-Working Day")
axes[1].set_xticklabels(['Non-Working Day', 'Working Day'])
axes[1].set_xlabel("Working Day")
axes[1].set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Pertanyaan 2: Seberapa besar pengaruh cuaca terhadap jumlah penyewaan sepeda? Apakah pengaruhnya sama untuk semua jenis pengguna?
st.subheader("🔬 Korelasi Faktor Cuaca dengan Penyewaan Sepeda")
correlation_matrix = day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
ax.set_title("Korelasi Faktor Cuaca dan Penyewaan Sepeda")
st.pyplot(fig)

st.subheader("🌦️ Situasi Cuaca vs Permintaan")
weather_sit_demand = day_df.groupby('weathersit')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_sit_demand, x='weathersit', y='cnt', palette='Blues')
ax.set_title("Jumlah Penyewaan berdasarkan Situasi Cuaca")
ax.set_xlabel("Situasi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("🌡️ Pengaruh Faktor Cuaca terhadap Penyewaan Sepeda")
weather_features = ['temp', 'hum', 'windspeed']
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, feature in enumerate(weather_features):
    sns.scatterplot(data=day_df, x=feature, y='cnt', ax=axes[i], color='#FF5733')
    axes[i].set_title(f"Penyewaan vs {feature}")
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("👥 Pengaruh Cuaca terhadap Jenis Pengguna")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, feature in enumerate(weather_features):
    sns.scatterplot(data=day_df, x=feature, y='casual', ax=axes[i], label='Casual Users', color='#29B5DA')
    sns.scatterplot(data=day_df, x=feature, y='registered', ax=axes[i], label='Registered Users', color='#FF5733')
    axes[i].set_title(f"Penyewaan vs {feature} berdasarkan Jenis Pengguna")
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Jumlah Penyewaan")
    axes[i].legend()
st.pyplot(fig)

st.caption("© 2025 - Bike Sharing Analysis Dashboard")
