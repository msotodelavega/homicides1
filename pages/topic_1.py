import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar

#------------------

# Standard Imports
import pandas as pd
import numpy as np
import json
import jellyfish

# Import data
cod_dane= pd.read_csv('data/cod_dane.csv')

datos_col = pd.read_csv('data/homicidios_policia.csv',
                        sep=';',
                        parse_dates=["FECHA HECHO"],
                        dayfirst=True
                       );

datos_col.columns = ['departamento','municipio','codigo','arma','fecha','genero', 'edad_grupo', 'cantidad']

#clearing cod_dane
cod_dane['Código Centro Poblado']=cod_dane['Código Centro Poblado'].apply(lambda x: x.replace(',',''))
cod_dane['Código Centro Poblado'] = cod_dane['Código Centro Poblado'].astype(int)

#clearing dotos_col
df = datos_col.copy()
keep_values =  ["ANTIOQUIA","VALLE","CUNDINAMARCA"]
df = df[df["departamento"].isin(keep_values)]
df['edad_grupo'].replace(' ', np.nan, inplace=True)
df = df.dropna()

dict_values =  {
"ARMA BLANCA / CORTOPUNZANTE":"ARMA BLANCA",
"ARMA DE FUEGO":"ARMA DE FUEGO",
"CORTANTES":"ARMA BLANCA",
"PUNZANTES":"ARMA BLANCA",
"CONTUNDENTES":"OTRAS ARMAS",
"ARTEFACTO EXPLOSIVO/CARGA DINAMITA":"OTRAS ARMAS",
"MINA ANTIPERSONA":"OTRAS ARMAS",
"CUERDA/SOGA/CADENA":"OTRAS ARMAS",
"COMBUSTIBLE":"OTRAS ARMAS",
"BOLSA PLASTICA":"OTRAS ARMAS",
"MOTO BOMBA":"OTRAS ARMAS",
"GRANADA DE MANO":"OTRAS ARMAS",
"PAQUETE BOMBA":"OTRAS ARMAS",
"SUSTANCIAS TOXICAS":"OTRAS ARMAS",
"SIN EMPLEO DE ARMAS":"OTRAS ARMAS",
"JERINGA":"OTRAS ARMAS",
"CARRO BOMBA":"OTRAS ARMAS",
"NO REPORTADO":"OTRAS ARMAS",
"PERSONA BOMBA":"OTRAS ARMAS",
"CINTAS/CINTURON":"OTRAS ARMAS",
"ESCOPOLAMINA":"OTRAS ARMAS",
"ALMOHADA":"OTRAS ARMAS",
"CILINDRO BOMBA":"OTRAS ARMAS",
"ARTEFACTO INCENDIARIO":"OTRAS ARMAS",
"VENENO":"OTRAS ARMAS",
"ROCKET":"OTRAS ARMAS",
"QUIMICOS":"OTRAS ARMAS",
"OLLA BOMBA":"OTRAS ARMAS",
"GASES":"OTRAS ARMAS",
"NO REPORTADA":"OTRAS ARMAS",
"GRANADA DE MORTERO":"OTRAS ARMAS",
"CASA BOMBA":"OTRAS ARMAS",
"MEDICAMENTOS":"OTRAS ARMAS",
"ACIDO":"OTRAS ARMAS",
"POLVORA(FUEGOS PIROTECNICOS)":"OTRAS ARMAS",
"PRENDAS DE VESTIR":"OTRAS ARMAS",
"LIQUIDOS":"OTRAS ARMAS"
}

df = df.replace({"arma": dict_values})

df['ano'] = df['fecha'].dt.year
df["dia"] = df["fecha"].dt.day_name(locale="es")
df = df.reindex(columns=['fecha','ano','dia','departamento','municipio','codigo', 'arma', 'genero', 'edad_grupo', 'cantidad'])

#para grafica por año
df_yearly = df.groupby("ano")['cantidad'].sum()
df_yearly = df_yearly.to_frame().reset_index()

#para grafica por mes
df['mes'] = df['fecha'].dt.month
df_monthly = df.groupby("mes")['cantidad'].sum()
df_monthly = df_monthly.to_frame().reset_index()

#para grafica por dia
df_daily = df.groupby("dia")['cantidad'].sum()
df_daily = df_daily.to_frame().reset_index()

#para grafica de serie
df['ano_mes'] = df['fecha'].dt.to_period('M').astype(dtype=str)
df_year_month = df.groupby("ano_mes")['cantidad'].sum()
df_year_month = df_year_month.to_frame().reset_index()

#para grafica de rangos de edad
df_age = df.groupby("edad_grupo")['cantidad'].sum()
df_age = df_age.to_frame().reset_index()

#para grafico por genero
df_gen = df.groupby("genero")['cantidad'].sum()
df_gen = df_gen.to_frame().reset_index()

#para grafico por tipo de arma
df_weapon = df.groupby("arma")['cantidad'].sum()
df_weapon = df_weapon.to_frame().reset_index()

#para grafica box plot por departamento
df['week'] = df['fecha'].dt.to_period('M')
df_departamento = df.groupby(["departamento","week"])['cantidad'].sum()
df_departamento = df_departamento.to_frame().reset_index()

#para grafica box plot municipio
df['week'] = df['fecha'].dt.to_period('M')
df_municipio = df.groupby(["municipio","week","departamento"])['cantidad'].sum()
df_municipio = df_municipio.to_frame().reset_index()
df_municipio = df_municipio.sort_values(by='cantidad', ascending=False)
df_municipio = df_municipio[df_municipio['cantidad'] > 20]

#para grafico departamento x año
df_dpto_year = df.groupby(["ano","departamento"])['cantidad'].sum()
df_dpto_year = df_dpto_year.reset_index()

#para grafico departamento x mes
df_dpto_month = df.groupby(["mes","departamento"])['cantidad'].sum()
df_dpto_month = df_dpto_month.reset_index()

#para grafico departamento x día
df_dpto_day = df.groupby(["dia","departamento"])['cantidad'].sum()
df_dpto_day = df_dpto_day.reset_index()

df_hom = pd.merge(df, cod_dane[['Código Centro Poblado','Tipo Centro Poblado', 'Longitud', 'Latitud']],
                  left_on='codigo', 
                  right_on='Código Centro Poblado', 
                  how='left')

df_hom = df_hom.drop(columns=["Código Centro Poblado"])

#------------------

register_page(
    __name__,
    name='Time series',
    top_nav=True,
    order = 3
)

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
        dbc.Col('hola', width=12)
        ])
