# Standard Imports
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar
from app_dataframe import df_dpto_day, df_dpto_month, df_dpto_year

register_page(
    __name__,
    name='homicides by period and area',
    )

# ======================== Plotly Graphs

dias_semana = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def graficar1():
    fig = px.bar(df_dpto_day, x="dia", y="cantidad", barmode="group", facet_col="departamento", category_orders={'dia': dias_semana}, color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per departamento and day',
        xaxis_title='Day',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270, tickmode='linear')
    grafica = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return grafica

def graficar2():
    fig = px.bar(df_dpto_month, x="mes", y="cantidad", barmode="group", facet_col="departamento", color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per departamento and month',
        xaxis_title='Month',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270, tickmode='linear')
    grafica = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return grafica

def graficar3():
    fig = px.bar(df_dpto_year, x="ano", y="cantidad", barmode="group", facet_col="departamento", color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per departamento and year',
        xaxis_title='Year',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270, tickmode='linear')
    grafica = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return grafica

# ======================== App Layout

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
                    dbc.Col(graficar3(), width=12),
                    dbc.Col(graficar2(), width=12),
                    dbc.Col(graficar1(), width=12),
                    ])
