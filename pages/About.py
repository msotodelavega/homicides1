from dash import html
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    name='About Us',
    top_nav=True,
    order=6
    )

#images
imagen1 = '/assets/alexis.jpg'
imagen2 = '/assets/buitrago.jpg'
imagen3 = '/assets/carlos.jpg'
imagen4 = '/assets/montaño.jpg'
imagen5 = '/assets/manuel.jpg'

#presentation cards
card_1 = dbc.Card(
    [
        dbc.CardImg(src=imagen1, top=True, style={'higth':'10rem'}),
        dbc.CardBody(
            [
                html.H4("Alexis Berrio", className="card-title"),
                html.P(
                    "Electronic Engineer | Data Analyst "
                    "Universidad de Antioquía. "
                    "Data Analyst Bancolombia "
                    ".                        ",
                    className="card-text",
                ),
                dbc.Button("Go Linkedin", color="primary",external_link=True,href="https://www.linkedin.com/in/johan-alexis-berrio-arenas-8368731bb/",),
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
                    "Business Administrator & specialist in Senior "
                    "Management. "
                    "Analista Arquitectura de Aplicaciones de TI.",
                    className="card-text",
                ),
                dbc.Button("Go Linkedin", color="primary",external_link=True,href="https://www.linkedin.com/in/oscar-buitrago-21081531/",),
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
                    "Data Scientist with experience in the venture capital "
                    "and startup environment. Skilled in Python, SQL and DAX. "
                    "Data Scientist at ADDI",
                    className="card-text",
                ),
                dbc.Button("Go Linkedin", color="primary",external_link=True,href="https://www.linkedin.com/in/carlos-d-lopez/",),
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
                    "Systems engineer, master in computer science, developer "
                    "in vuejs, nuxt, react, Laravel, SQL, and noSQL. "
                    "Xi'an University of Technology",
                    className="card-text",
                ),
                dbc.Button("Go Linkedin", color="primary",external_link=True,href="https://www.linkedin.com/in/oscar-eduardo-monta%C3%B1o-lopez-84199b72/",),
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
                    "Industrial enginering / Universidad de Córdoba. "
                    "Master / Universidad de los Andes. "
                    "Professor Universidad Tecnológia de Bolívar",
                    className="card-text",
                ),
                dbc.Button("Go Linkedin", color="primary",external_link=True,href="https://www.linkedin.com/in/manuel-soto-de-la-vega-23163220b/",),
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