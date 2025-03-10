import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
day_df = pd.read_csv("data/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Inisialisasi aplikasi Dash
app = dash.Dash(__name__)

# Layout Dashboard
app.layout = html.Div([
    html.H1("Dashboard Penyewaan Sepeda"),
    
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Tren Penyewaan Sepeda', value='tab1'),
        dcc.Tab(label='Pengaruh Cuaca', value='tab2')
    ]),
    
    html.Div(id='tabs-content')
])

# Callback untuk memperbarui konten berdasarkan tab yang dipilih
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def update_tab(tab_name):
    if tab_name == 'tab1':
        fig_hourly = px.line(day_df, x='hour', y='count', title='Jumlah Penyewaan Sepeda per Jam')
        fig_daily = px.bar(day_df, x='day_of_week', y='count', title='Jumlah Penyewaan Sepeda Harian')
        fig_monthly = px.line(day_df, x='month', y='count', title='Jumlah Penyewaan Sepeda per Bulan')
        return html.Div([
            dcc.Graph(figure=fig_hourly),
            dcc.Graph(figure=fig_daily),
            dcc.Graph(figure=fig_monthly)
        ])
    elif tab_name == 'tab2':
        fig_weather = px.bar(day_df, x='weather', y='count', title='Jumlah Penyewaan berdasarkan Situasi Cuaca')
        fig_corr = px.imshow(day_df.corr(), title='Matriks Korelasi antara Cuaca dan Penyewaan')
        return html.Div([
            dcc.Graph(figure=fig_weather),
            dcc.Graph(figure=fig_corr)
        ])

# Jalankan server
if __name__ == '__main__':
    app.run_server(debug=True)

