import dash_bootstrap_components as dbc
from dash import html
from dash_labs.plugins import register_page
from app_dataframe import total

register_page(
    __name__,
    path="/",
    top_nav=True,
    order=2
    )

#text intro
texto1 = 'Homicides in Colombia represent a structural phenomenon that needs to be addressed from a proactive perspective because of the problems that produce for the administration of the justice system, the levels of life quality and the security of people in Colombia. In this project we explore the distributions of homicide trends from different fronts: homicides in men and women, in geographic zones, by type of weapon, by seasonality, among others, throughout the years 2010 to 2021 in Colombia.'
texto2 = 'The number of homicides is one of the most important indicators of violence, in this context, Colombia is in the top 10 of homicides in Latin America with 22.64 deaths per 100.000 habitants. The typification of homicides is important because it recognizes and evidences a specific type of violence that arises from a structural and systematic problem in Colombia. The analysis of murders is important because it allows us to create data structures to get better policies of prevention and security. With this model, the public and private institutions may create action plans to focus the politics of prevention of homicides in Colombia. '

card_content_1 = [
    dbc.CardBody(
        [
            html.H6("Country Ranking", className="card-title"),
            html.H1("16th in the world",className="card-text"),
            html.H6('By www.indexmundi.com', className='card-text'),
        ]
    ),
]

card_content_2 = [
    dbc.CardBody(
        [
            html.H6("Latinoamerica Ranking", className="card-title"),
            html.H2("8th in Latinoamérica",className="card-text"),
            html.H6('By www.indexmundi.com', className='card-text'),
        ]
    ),
]

card_content_3 = [
    dbc.CardBody(
        [
            html.H6("Total homicides", className="card-title"),
            html.H1(total,className="card-text"),
            html.H6('between years 2011-2020', className='card-text'),
        ]
    ),
]

#layout
layout = html.Div(
    [
        dbc.Card(dbc.CardBody(texto1),className="mb-3",),
        dbc.Card(dbc.CardBody(texto2),className="mb-3",),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content_1, color="primary", inverse=True), width=4),
                dbc.Col(dbc.Card(card_content_2, color="info", inverse=True), width=4),
                dbc.Col(dbc.Card(card_content_3, color="secondary", inverse=True), width=4),
            ],
            className="mb-4",
        ),  
    ]
)