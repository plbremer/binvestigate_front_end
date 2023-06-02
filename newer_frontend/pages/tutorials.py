

import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_player as dp

dash.register_page(__name__, path='/tutorials')

layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        html.H3('Tutorial Videos'),
                        html.Br(),
                        html.H6('Title'),
                        dp.DashPlayer(
                            id="player",
                            url="https://www.youtube.com/watch?v=KCzwyFHSMdY",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                        html.Br(),
                        html.H6('Title'),
                        dp.DashPlayer(
                            id="player",
                            url="https://www.youtube.com/watch?v=KCzwyFHSMdY",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                        html.Br(),
                        html.H6('Title'),
                        dp.DashPlayer(
                            id="player",
                            url="https://www.youtube.com/watch?v=KCzwyFHSMdY",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                        html.Br(),
                        html.H6('Title'),
                        dp.DashPlayer(
                            id="player",
                            url="https://www.youtube.com/watch?v=KCzwyFHSMdY",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                    ],
                    width=5
                ),
                dbc.Col(
                    children=[
                        html.H4('faq goes here'),
                        html.Br(),
                        html.H6('Here is an example question'),
                        html.P('here is an example answer'),
                        html.Hr(),
                        html.H6('Why are there multiple entries for an organ or disease?'),
                        html.P('here is an example answer'),
                        html.Hr(),
                    ],
                    width=5
                ),
                dbc.Col(width=2)
            ]
        )
    ],
)