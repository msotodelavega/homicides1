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
