# Standard Imports
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar

register_page(__name__,name='word cloud')

# ======================== Plotly Graphs
imagen = '/assets/wordcloud.png'

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
                    dbc.Col(html.Img(src=imagen, height="520px"), width=12),
                    ])
