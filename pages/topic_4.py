# Standard Imports
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar
from app_dataframe import df_departamento,df_municipio

register_page(
    __name__,
    name='homicides by zones',
    )

lista = df_departamento.departamento.unique()

def get_box_chart_departamento():
    fig = px.violin(df_departamento, x='departamento', y='cantidad', box=True, color='departamento')
    fig.update_layout(
        showlegend=False,
        title_text='BoxPlot Homicides per state',
        xaxis_title='State',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270)
    grafica = dcc.Graph(figure=fig, style={'width': '100%', 'height': '80vh', 'display': 'inline-block'})
    return grafica

def layout():
    return dbc.Row([
        dbc.Col(sidebar(), width=12), 
        dbc.Col('', width=6),
        dbc.Col('View:', width=6),
        dbc.Col('', width=6),
        dbc.Col(dcc.Checklist(id='checklist1',options=lista,value=lista), width=6),
        dbc.Col(get_box_chart_departamento(), width=6),
        dbc.Col(dcc.Graph(id='graph_box1'), width=6, style={'height': '80vs'}),
        ])

@callback(
    Output('graph_box1', 'figure'), 
    Input('checklist1', 'value'))

def get_box_chart_municipio(dpto):
    mask = df_municipio.departamento.isin(dpto)
    fig = px.strip(df_municipio[mask],x='municipio', y='cantidad', color='departamento')
    fig.update_layout(
        showlegend=False,
        title_text='StripPlot Homicides per borough',
        xaxis_title='Borough',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270)
    return fig