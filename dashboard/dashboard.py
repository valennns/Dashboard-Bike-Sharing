import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
day_df = pd.read_csv("data/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Inisialisasi aplikasi Dash
app = dash.Dash(__name__)

# Layout dashboard
app.layout = html.Div([
    html.H1('Dashboard Analisis Penyewaan Sepeda', style={'textAlign': 'center'}),
    
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Tren Waktu Penyewaan', value='tab1'),
        dcc.Tab(label='Pengaruh Cuaca', value='tab2')
    ]),
    
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def update_tab(tab):
    if tab == 'tab1':
        fig_hourly = px.line(df, x='hour', y='rental_count', title='Jumlah Penyewaan Sepeda per Jam')
        fig_daily = px.bar(df, x='day_of_week', y='rental_count', title='Jumlah Penyewaan Sepeda Harian')
        
        return html.Div([
            dcc.Graph(figure=fig_hourly),
            dcc.Graph(figure=fig_daily)
        ])
    
    elif tab == 'tab2':
        fig_weather = px.scatter(df, x='temperature', y='rental_count', color='weather_condition',
                                 title='Pengaruh Cuaca terhadap Penyewaan Sepeda')
        
        return html.Div([
            dcc.Graph(figure=fig_weather)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
