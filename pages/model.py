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

@callback(
    Output("fore_fig", "figure"),
    Input("city_dropdown", "value"),
)

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
        name = 'model/SARIMAX_med.pkl'
    elif city == 'BOGOTÁ, D.C.':
        name = 'model/SARIMAX_bog.pkl'
    elif city == 'CALI':
        name = 'model/SARIMAX_cal.pkl'
    else:
        name = 'model/SARIMAX_total.pkl'

    with open(name, 'rb') as pkl:
        SARIMA_model = pickle.load(pkl)
        fitted_series, lower_series ,upper_series = sarimax_forecast_city(SARIMA_model,df, 5)

    df = df.reset_index()
    df_fitted = fitted_series.to_frame().reset_index()
    df_fitted.columns = ['fecha','total']
    lower_series = lower_series.to_frame().reset_index()
    lower_series.columns = ['fecha','total']
    upper_series = upper_series.to_frame().reset_index()
    upper_series.columns = ['fecha','total']

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['fecha'], y=df['total'],
                        #mode='lines',
                        name='original'))
    fig2.add_trace(go.Scatter(x=df_fitted['fecha'], y=df_fitted['total'],
                        #mode='lines',
                        name='fitted'))
    fig2.add_trace(go.Scatter(x=upper_series['fecha'], y=upper_series['total'],
                        #mode='lines',
                        name='upper_series',
                        line_color='rgba(200,200,200,0.2)',
                        showlegend=False,))
    fig2.add_trace(go.Scatter(x=lower_series['fecha'], y=lower_series['total'],
                        #mode='lines',
                        name='lower',
                        fill='tonexty',
                        line_color='rgba(200,200,200,0.2)',
                        showlegend=False,))
    fig2.update_layout(
        showlegend=False,
        title_text='Forecasting homicides in '+city,
        xaxis_title='Date',
        yaxis_title='Homicides',
        )
    fig2.update_traces(mode='lines')
    return fig2