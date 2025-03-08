import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Load dataset using relative path
day_df = pd.read_csv(os.path.join("data", "day.csv"))
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mapping season names
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_mapping)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard Penggunaan Sepeda"),
    
    # Dropdown for month selection
    dcc.Dropdown(
        id='month-filter',
        options=[{'label': f'Bulan {i}', 'value': i} for i in range(1, 13)],
        placeholder="Pilih Bulan"
    ),
    
    # Dropdown for season selection
    dcc.Dropdown(
        id='season-filter',
        options=[{'label': season, 'value': season} for season in day_df['season'].unique()],
        placeholder="Pilih Musim"
    ),
    
    dcc.Graph(id='usage-trend'),
    dcc.Graph(id='casual-registered'),
    dcc.Graph(id='weather-impact')
])

# Callbacks for interactivity
@app.callback(
    [dash.dependencies.Output('usage-trend', 'figure'),
     dash.dependencies.Output('casual-registered', 'figure'),
     dash.dependencies.Output('weather-impact', 'figure')],
    [dash.dependencies.Input('month-filter', 'value'),
     dash.dependencies.Input('season-filter', 'value')]
)
def update_graphs(selected_month, selected_season):
    filtered_df = day_df.copy()
    if selected_month:
        filtered_df = filtered_df[filtered_df['dteday'].dt.month == selected_month]
    if selected_season:
        filtered_df = filtered_df[filtered_df['season'] == selected_season]
    
    fig_usage_trend = px.line(filtered_df, x='dteday', y='cnt', title='Tren Penggunaan Sepeda Harian')
    fig_casual_registered = px.bar(filtered_df, x='dteday', y=['casual', 'registered'], title='Casual vs Registered Users', barmode='stack')
    fig_weather = px.box(filtered_df, x='weathersit', y='cnt', title='Pengaruh Cuaca terhadap Penggunaan Sepeda')
    
    return fig_usage_trend, fig_casual_registered, fig_weather

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)  # Disable reloader