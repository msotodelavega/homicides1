# Standard Imports
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar
from app_dataframe import df

register_page(
    __name__,
    name='homicides by characteristics',
    )

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
                    dbc.Col(html.P("View:"), width=12),
                    dbc.Col(dcc.Dropdown(id='names',options=['genero', 'arma','edad_grupo','departamento'],value='genero',style={'width': '100%'}), width=12),
                    dbc.Col(dcc.Graph(id="graph_pie",style={'width': '100%', 'height': '60vh'}), width=12)])
   
@callback(
    Output("graph_pie", "figure"), 
    Input("names", "value"))

def generate_chart(names):
    fig = px.pie(df, values='cantidad', names=names, hole=.3)
    return fig