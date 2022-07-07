import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback

register_page(
    __name__,
    name='Time series',
    top_nav=True,
    order = 3
)

def layout():
    return dbc.Row([dbc.Col('hola', width=12),
        dbc.Col('prueba', width=12),
        ])
