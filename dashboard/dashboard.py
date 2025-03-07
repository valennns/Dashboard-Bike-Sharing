import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load dataset
day_df = pd.read_csv("dashboard/day.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Pengguna Sepeda"),
    
    dcc.Graph(id='trend-chart'),
    
    dcc.Dropdown(
        id='season-filter',
        options=[
            {'label': 'Spring', 'value': 1},
            {'label': 'Summer', 'value': 2},
            {'label': 'Fall', 'value': 3},
            {'label': 'Winter', 'value': 4}
        ],
        multi=True,
        placeholder='Pilih musim...'
    ),
    
    dcc.Graph(id='weather-chart'),
    
    dcc.Slider(
        id='year-slider',
        min=day_df['dteday'].dt.year.min(),
        max=day_df['dteday'].dt.year.max(),
        value=day_df['dteday'].dt.year.min(),
        marks={str(year): str(year) for year in day_df['dteday'].dt.year.unique()},
        step=None
    )
])

@app.callback(
    Output('trend-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_trend_chart(selected_seasons, selected_year):
    df_filtered = day_df[day_df['dteday'].dt.year == selected_year]
    if selected_seasons:
        df_filtered = df_filtered[df_filtered['season'].isin(selected_seasons)]
    
    fig = px.line(df_filtered, x='dteday', y='cnt', title='Tren Pengguna Sepeda', labels={'cnt': 'Jumlah Pengguna'})
    return fig

@app.callback(
    Output('weather-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_weather_chart(selected_seasons, selected_year):
    df_filtered = day_df[day_df['dteday'].dt.year == selected_year]
    if selected_seasons:
        df_filtered = df_filtered[df_filtered['season'].isin(selected_seasons)]
    
    fig = px.box(df_filtered, x='weathersit', y='cnt', title='Distribusi Pengguna Sepeda berdasarkan Cuaca', labels={'cnt': 'Jumlah Pengguna', 'weathersit': 'Kondisi Cuaca'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
