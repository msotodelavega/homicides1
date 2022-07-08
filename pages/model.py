from dash import dcc, html, Input, Output, callback
from dash_labs.plugins import register_page

import dash_bootstrap_components as dbc
import pandas as pd
import pickle
import plotly.graph_objects as go

from app_dataframe import df_hom

register_page(
    __name__,
    top_nav=True,
    order=5
    )

#sarimax funtion
def sarimax_forecast_city(SARIMAX_model, df, periods):
    # Forecast
    n_periods = periods

    forecast_df = pd.DataFrame({"month_index":pd.date_range(df.index[-1], periods = n_periods, freq='MS').month},
                    index = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods = n_periods, freq='MS'))

    fitted, confint = SARIMAX_model.predict(n_periods=n_periods, 
                                            return_conf_int=True,
                                            exogenous=forecast_df[['month_index']])
    index_of_fc = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods = n_periods, freq='MS')

    # make series for plotting purpose
    fitted_series = pd.Series(fitted, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)
    return fitted_series, lower_series, upper_series

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

#callback figure
@callback(
    Output("fore_fig", "figure"),
    Input("city_dropdown", "value"),
)

# make figure
def graficar(city_dropdown):

    df = df_hom[['fecha','cantidad','municipio']]

    #change city
    city = city_dropdown
    if city == 'MEDELLÍN':
        df = df[df['municipio']=='MEDELLÍN'][['fecha','cantidad']]
        df_fitted = pd.read_excel('data/pred_med.xlsx')
    elif city == 'BOGOTÁ, D.C.':
        df = df[df['municipio']=='BOGOTÁ, D.C.'][['fecha','cantidad']]
        df_fitted = pd.read_excel('data/pred_bog.xlsx')
    elif city == 'CALI':
        df = df[df['municipio']=='CALI'][['fecha','cantidad']]
        df_fitted = pd.read_excel('data/pred_cal.xlsx')
    else:
        df = df[['fecha','cantidad']]
        df_fitted = pd.read_excel('data/pred_tot.xlsx')

    df_fitted.columns = ['index','fecha','total','lower','upper']
    df_fitted = df_fitted.drop(columns='index')

    df = df.set_index('fecha')
    df = df.resample('M').sum()
    df = df.reset_index()

    #make figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(df.fecha), y=list(df.cantidad)))
    fig.update_layout(
        title_text='Trend of homicides in Colombia',
        xaxis_title="date",
        yaxis_title="homicides",
        )
    
    """fig2.add_trace(go.Scatter(x=df_fitted['fecha'], y=df_fitted['total'],
                        #mode='lines',
                        name='fitted'))
    fig2.add_trace(go.Scatter(x=df_fitted['fecha'], y=df_fitted['upper'],
                        #mode='lines',
                        name='upper_series',
                        line_color='rgba(200,200,200,0.2)',
                        showlegend=False,))
    fig2.add_trace(go.Scatter(x=df_fitted['fecha'], y=df_fitted['lower'],
                        #mode='lines',
                        name='lower',
                        fill='tonexty',
                        line_color='rgba(200,200,200,0.2)',
                        showlegend=False,))"""
    
    return fig