from dash import html
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc
from .app_dataframe import df_year_month

register_page(
    __name__,
    name='About Us',
    top_nav=True,
    order=6
    )

texto1 = open("assets/texto1.txt", mode='r')
texto2 = open("assets/texto2.txt", mode='r')
texto3 = open("assets/texto3.txt", mode='r')
texto4 = open("assets/texto4.txt", mode='r')
texto5 = open("assets/texto5.txt", mode='r')

imagen1 = '/assets/alexis.jpg'
imagen2 = '/assets/buitrago.jpg'
imagen3 = '/assets/carlos.jpg'
imagen4 = '/assets/montaño.jpg'
imagen5 = '/assets/manuel.jpg'

card_1 = dbc.Card(
    [
        dbc.CardImg(src=imagen1, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Alexis Berrio", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go profile", color="primary"),
            ]
        ),
    ],
    style={"higth": "18rem"},
)

card_2 = dbc.Card(
    [
        dbc.CardImg(src=imagen2, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Oscar Buitrago", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go profile", color="primary"),
            ]
        ),
    ],
    style={"higth": "18rem"},
)

card_3 = dbc.Card(
    [
        dbc.CardImg(src=imagen3, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Carlos Lopez", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go profile", color="primary"),
            ]
        ),
    ],
    style={"higth": "18rem"},
)

card_4 = dbc.Card(
    [
        dbc.CardImg(src=imagen4, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Oscar Montaño", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go profile", color="primary"),
            ]
        ),
    ],
    style={"higth": "18rem"},
)

card_5 = dbc.Card(
    [
        dbc.CardImg(src=imagen5, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Manuel Soto", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go profile", color="primary"),
            ]
        ),
    ],
    style={"higth": "18rem"},
)

layout = dbc.Row(
    [
        dbc.Col(card_1),
        dbc.Col(card_2),
        dbc.Col(card_3),
        dbc.Col(card_4),
        dbc.Col(card_5),
    ]
)
