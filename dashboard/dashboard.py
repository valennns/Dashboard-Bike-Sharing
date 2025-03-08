import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
day_df = pd.read_csv(r"C:\submission 1\data\day.csv")

# Convert 'dteday' to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# 1. Overview
total_records = len(day_df)
date_range = (day_df['dteday'].min(), day_df['dteday'].max())

# 2. Key Metrics
total_rentals = day_df['cnt'].sum()
average_temp = day_df['temp'].mean()
average_humidity = day_df['hum'].mean()
average_windspeed = day_df['windspeed'].mean()

# 3. Monthly Breakdown
day_df['month'] = day_df['dteday'].dt.month
monthly_rentals = day_df.groupby('month')['cnt'].sum()

# 4. Seasonal Analysis
day_df['season'] = day_df['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
seasonal_rentals = day_df.groupby('season')['cnt'].sum()

# 5. Weather Impact
weather_impact = day_df['weathersit'].value_counts(normalize=True) * 100

# 6. User Engagement
total_casual_users = day_df['casual'].sum()
total_registered_users = day_df['registered'].sum()

# 7. Visualizations
plt.figure(figsize=(12, 6))

# Monthly Rentals
plt.subplot(2, 2, 1)
sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values)
plt.title('Monthly Rentals')
plt.xlabel('Month')
plt.ylabel('Number of Rentals')

# Seasonal Rentals
plt.subplot(2, 2, 2)
sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values)
plt.title('Seasonal Rentals')
plt.xlabel('Season')
plt.ylabel('Number of Rentals')

# Weather Impact
plt.subplot(2, 2, 3)
sns.barplot(x=weather_impact.index, y=weather_impact.values)
plt.title('Weather Impact on Rentals')
plt.xlabel('Weather Situation')
plt.ylabel('Percentage of Rentals')

# Show the plots
plt.tight_layout()
plt.show()

# Print the insights
print(f"Total Records: {total_records}")
print(f"Date Range: {date_range}")
print(f"Total Rentals: {total_rentals}")
print(f"Average Temperature: {average_temp:.2f}")
print(f"Average Humidity: {average_humidity:.2f}")
print(f"Average Windspeed: {average_windspeed:.2f}")
print(f"Total Casual Users: {total_casual_users}")
print(f"Total Registered Users: {total_registered_users}")