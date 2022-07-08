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

# Create figure
def graficar(city_dropdown):

    df = df_hom[['fecha','cantidad']]

    city = city_dropdown

    if city == 'MEDELLÍN':
        df = df_hom[df_hom['municipio']=='MEDELLÍN'][['fecha','cantidad']]
    elif city == 'BOGOTÁ, D.C.':
        df = df_hom[df_hom['municipio']=='BOGOTÁ, D.C.'][['fecha','cantidad']]
    elif city == 'CALI':
        df = df_hom[df_hom['municipio']=='CALI'][['fecha','cantidad']]
    else:
        df = df_hom[['fecha','cantidad']]
    
    df = df.set_index('fecha')
    df = df.resample('M').sum()
    df.columns = ['total']
    df['month_index'] = df.index.month

    if city == 'MEDELLÍN':
        pred_med = pd.read_excel('data/pred_med.xlsx')
    elif city == 'BOGOTÁ, D.C.':
        pred_med = pd.read_excel('data/pred_bog.xlsx')
    elif city == 'CALI':
        pred_med = pd.read_excel('data/pred_cal.xlsx')
    else:
        pred_med = pd.read_excel('data/pred_tot.xlsx')

    df = df.reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['fecha'], y=df['total'],
                        #mode='lines',
                        name='original'))
    fig2.add_trace(go.Scatter(x=pred_med['index'], y=pred_med[0],
                        #mode='lines',
                        name='fitted'))
    fig2.update_layout(
        showlegend=False,
        title_text='Forecasting homicides in '+city,
        xaxis_title='Date',
        yaxis_title='Homicides1',
        )
    fig2.update_traces(mode='lines')
    return fig2