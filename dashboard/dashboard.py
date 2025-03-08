import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
day_df = pd.read_csv(r"C:\submission 1\data\day.csv")

# Feature Engineering
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['year'] = day_df['dteday'].dt.year
day_df['month'] = day_df['dteday'].dt.strftime('%B')
day_df['day_of_week'] = day_df['dteday'].dt.strftime('%A')

# Streamlit Dashboard
st.title("Dashboard Penyewaan Sepeda")
st.markdown("Analisis pola penyewaan sepeda berdasarkan dataset Bike Sharing.")

# Sidebar Filter
year_option = st.sidebar.selectbox("Pilih Tahun", day_df['year'].unique())
filtered_df = day_df[day_df['year'] == year_option]

# Visualisasi 1: Penyewaan Sepeda per Bulan
st.subheader("Jumlah Penyewaan Sepeda per Bulan")
monthly_demand = filtered_df.groupby('month')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=monthly_demand, x='month', y='cnt', ax=ax, order=
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualisasi 2: Penyewaan Sepeda Harian
st.subheader("Jumlah Penyewaan Sepeda Harian")
daily_demand = filtered_df.groupby('day_of_week')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=daily_demand, x='day_of_week', y='cnt', ax=ax, order=
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-rata Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualisasi 3: Pengaruh Suhu terhadap Penyewaan
st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='temp', y='cnt', ax=ax)
ax.set_xlabel("Suhu Normalisasi")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Visualisasi 4: Pengaruh Cuaca terhadap Penyewaan
st.subheader("Jumlah Penyewaan berdasarkan Situasi Cuaca")
weather_sit_demand = filtered_df.groupby('weathersit')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=weather_sit_demand, x='weathersit', y='cnt', ax=ax)
ax.set_xlabel("Situasi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticklabels(['Clear', 'Mist', 'Light Rain', 'Heavy Rain'])
st.pyplot(fig)
