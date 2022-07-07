from dash import dcc, html, Input, Output, callback
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc
import plotly.express as px

from datetime import datetime as dt
from app_dataframe import df_mun, geojson

df = df_mun
center_dicts = {'ANTIOQUIA': [6,-75.8], 'VALLE': [3.2, -76.3], 'CUNDINAMARCA': [4.3,-74], 'NARIÑO': [1.1, -77] }
register_page(
    __name__,
    top_nav=True,
    order=4
    )

def layout():
    return dbc.Row([
        dbc.Col(html.P("Ver:"), width=12),
        dbc.Col(dcc.Dropdown(
            id="state_dropdown",
            options=['ANTIOQUIA','VALLE','CUNDINAMARCA', 'NARIÑO'],
            value='CUNDINAMARCA',
            multi=False
            ), width = 6),
        dbc.Col(dcc.DatePickerRange(
            id='date_picker',
            min_date_allowed=dt(2010, 1, 1),
            max_date_allowed=dt(2020, 12, 31),
            start_date=dt(2016,1,1).date(),
            end_date=dt(2017, 1, 1).date()
            ), width = 6),
        dbc.Col(dcc.Graph(id='Col_map'), width=12),
    ])

@callback(
    Output("Col_map", "figure"),
    [
        Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ]
)

def graficar(state_dropdown,start_date,end_date):
    df2 = df[df['departamento'] == state_dropdown]
    df2 = df2[(df2['fecha'] >= start_date) & (df['fecha'] < end_date)]
    df2 = df2.groupby('municipio').sum().reset_index()
    fig2 = px.choropleth_mapbox(df_mun,                         #Data
        locations='municipio',                   #Column containing the identifiers used in the GeoJSON file
        color='HOMIC_por_POB',                            #Column giving the color intensity of the region
        geojson=geojson,                          #The GeoJSON file
        zoom=6,                                   #Zoom
        mapbox_style="open-street-map",            #Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 6, "lon": -75.8}, #Center
        opacity=0.5 ) "lon": -75},
        opacity=0.5 )
    fig2.update_layout()
    return fig2
