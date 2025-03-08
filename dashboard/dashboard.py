import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama untuk desain dashboard
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF"

# Load data
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

# Konversi tanggal
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Konfigurasi Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("📊 Bike Sharing Data Analysis")

# Sidebar Filter
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df["dteday"].min(), day_df["dteday"].max()])

# Pertanyaan 1: Kapan penyewaan ramai atau sepi di luar perkiraan? Apa penyebabnya?
st.header("📌 Tren Waktu: Kapan Penyewaan Sepeda Ramai atau Sepi?")

# Visualisasi pola penyewaan per jam
hourly_rentals = hour_df.groupby("hr")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=hourly_rentals, x="hr", y="cnt", marker='o', color=PRIMARY_COLOR, linewidth=2)
ax.set_title("Jumlah Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

# Pola harian
daily_demand = day_df.groupby(day_df["dteday"].dt.dayofweek)["cnt"].mean().reset_index()
daily_demand.columns = ["Hari", "Jumlah Penyewaan"]
daily_demand["Hari"] = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=daily_demand, x="Hari", y="Jumlah Penyewaan", palette="Blues")
ax.set_title("Jumlah Penyewaan Sepeda Harian")
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# Pertanyaan 2: Bagaimana cuaca mempengaruhi jumlah penyewaan?
st.header("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Heatmap korelasi
correlation_matrix = day_df[["temp", "hum", "windspeed", "cnt"]].corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
ax.set_title("Korelasi Faktor Cuaca dengan Jumlah Penyewaan")
st.pyplot(fig)

# Penyewaan berdasarkan kondisi cuaca
weather_sit_demand = day_df.groupby("weathersit")["cnt"].mean().reset_index()
weather_sit_demand["weathersit"] = weather_sit_demand["weathersit"].map({
    1: "Cerah",
    2: "Kabut",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
})
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=weather_sit_demand, x="weathersit", y="cnt", palette="Blues")
ax.set_title("Jumlah Penyewaan berdasarkan Situasi Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

st.caption("Dashboard ini dibuat menggunakan Streamlit, Matplotlib, dan Seaborn.")
