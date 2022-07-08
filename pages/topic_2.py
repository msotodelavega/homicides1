# Standard Imports
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar
from app_dataframe import df_yearly, df_monthly,df_daily

register_page(__name__,name='Homicides by periodicity')

# ======================== Plotly Graphs

def get_bar_chart1():
    #colors = np.random.rand(1,1000)
    #color_discrete_sequence=colors
    fig = px.bar(df_yearly, x='ano', y='cantidad', title='Homicidios por año', color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per year',
        xaxis_title='Year',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270, tickmode='linear')
    barChart1 = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return barChart1

def get_bar_chart2():
    fig = px.bar(df_monthly, x='mes', y='cantidad', title='Homicidios por mes', color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per month',
        xaxis_title='Month',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=0, tickmode='linear')
    barChart2 = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return barChart2

def get_bar_chart3():
    fig = px.bar(df_daily, x='dia', y='cantidad', title='Homicidios por día', color='cantidad', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=False,
        title_text='Homicides per day',
        xaxis_title='Day',
        yaxis_title='Homicides',
        )
    fig.update_xaxes(tickangle=270, tickmode='linear', categoryarray=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    barChart3 = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '60vh', 'display': 'inline-block'})
    return barChart3

# ======================== App Layout

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
                    dbc.Col(get_bar_chart1(), width=4),
                    dbc.Col(get_bar_chart2(), width=4),
                    dbc.Col(get_bar_chart3(), width=4)])

