from dash import dcc, html, Input, Output, callback
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc
import plotly.express as px

from datetime import datetime as dt
from app_dataframe import df_hom, geojson

register_page(
    __name__,
    top_nav=True,
    order=4
    )

df = df_hom
center_dicts = {'ANTIOQUIA': [6.7, -75.4], 'VALLE': [3.8, -76.3], 'CUNDINAMARCA': [4.8, -74.0] }

def layout():
    return dbc.Row([
        dbc.Col(html.P("Ver:"), width=12),
        dbc.Col(dcc.Dropdown(
            id="state_dropdown",
            options=['ANTIOQUIA','VALLE','CUNDINAMARCA'],
            value='CUNDINAMARCA',
            multi=False
            ), width = 6),
        dbc.Col(dcc.DatePickerRange(
            id='date_picker',
            min_date_allowed=dt(2010, 1, 1),
            max_date_allowed=dt(2020, 12, 31),
            start_date=dt(2010,1,1).date(),
            end_date=dt(2020, 12, 31).date()
            ), width = 6),
        dbc.Col(dcc.Graph(id='Col_map'), width=12),
    ])

#callback maps
@callback(
    Output("Col_map", "figure"),
    [
        Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ]
)

#make chart
def graficar(state_dropdown,start_date,end_date):
    df2 = df[df['departamento'] == state_dropdown]
    df2 = df2[(df2['fecha'] >= start_date) & (df['fecha'] < end_date)]
    df2 = df2.groupby('municipio').sum().reset_index()
    fig2 = px.choropleth_mapbox(df2,
        locations='municipio',
        color='cantidad',
        geojson=geojson,
        zoom=6,
        mapbox_style="open-street-map",
        center={"lat": center_dicts[state_dropdown][0], "lon": center_dicts[state_dropdown][1]},
        opacity=0.5,
        labels={'cantidad':'homicides'})
    fig2.update_layout()
    return fig2