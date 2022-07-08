from dash import dcc, html, Input, Output, callback
from dash_labs.plugins import register_page

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from app_dataframe import df_hom

register_page(
    __name__,
    top_nav=True,
    order=5
    )

def layout():
    return dbc.Row([
        dbc.Col(html.P("View:"), width=12),
        dbc.Col(dcc.Dropdown(
            id="city_dropdown",
            options=['TOTAL','BOGOTÁ, D.C.','MEDELLÍN','CALI'],
            value='TOTAL',
            multi=False
            ), width = 12),
        dbc.Col(dcc.Graph(id='fore_fig'), width=12),
    ])

@callback(
    Output("fore_fig", "figure"),
    Input("city_dropdown", "value"),
)

def graficar(city_dropdown):

    df = df_hom[['fecha','cantidad']]

    city = city_dropdown

    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=[3,4,5,6], y=[3,4,5,6],
                        #mode='lines',
                        name='original'))
    fig2.update_layout(
        showlegend=False,
        title_text='Forecasting homicides in '+city,
        xaxis_title='Date',
        yaxis_title='Homicides',
        )
    fig2.update_traces(mode='lines')
    return fig2