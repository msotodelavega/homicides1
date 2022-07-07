import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
from .side_bar import sidebar


#---

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
df["dia"] = df["fecha"].dt.day_name
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

# AJUSTES A LOS NOMBRES DE LOS MUNICIPIOS
#cod_dane.columns = cod_dane.columns.str.replace(' ','_')
#cod_dane = cod_dane.replace(',','', regex=True)
cod_dane['Código Centro Poblado'] = cod_dane['Código Centro Poblado'].astype(int)
df_hom['codigo'] = df_hom['codigo'].astype(int)
df_hom['municipio'] = df_hom.municipio.str.replace('(CT)', '')
df_hom['municipio'] = df_hom.municipio.str.replace('[(+*)]', '')
df_hom['municipio'] = df_hom.municipio.str.replace('\s', '')

# CARGA GEOJSON MUNICIPIOS
f = open("data/MunicipiosVeredas19MB.json", encoding="utf8")
geojson = json.load(f)
json_names = []
for loc in geojson['features']:
    loc['id'] = loc['properties']['MPIO_CNMBR']
    json_names.append(loc['id'])

# Aca se cambian los nombres en el DF para que sean como los del json
df_names = list(df_hom.municipio.unique())
dict_mun ={}
dist_list = []
min_dist = 1000
match = ''
for name in df_names:
    for name2 in json_names:
        dist = jellyfish.levenshtein_distance(name, name2)
        if dist < min_dist:
            min_dist = dist
            match = name2
        
    dist_list.append(min_dist)
    dict_mun[name] = match
    min_dist = 1000
    
df_hom['municipio'] = df_hom.municipio.replace(dict_mun)

#---

register_page(
    __name__,
    name='Time series',
    top_nav=True,
    order = 3
)

# Create figure
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

def layout():
    return dbc.Row([dbc.Col(sidebar(), width=12),
        dbc.Col(graficar(), width=12)
        ])
