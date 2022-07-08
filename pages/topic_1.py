import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar
from app_dataframe import df_year_month

register_page(
    __name__,
    name='Time series',
    top_nav=True,
    order = 3
)

# ======================== Plotly Graphs

def graficar():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(df_year_month.ano_mes), y=list(df_year_month.cantidad)))
    fig.update_layout(
        title_text='Trend of homicides in Colombia',
        xaxis_title="date",
        yaxis_title="homicides",
        )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(count=2,
                        label="2y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    grafica = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '80vh', 'display': 'inline-block'})
    return grafica

# ======================== App Layout

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
        dbc.Col(graficar(), width=12)
        ])
