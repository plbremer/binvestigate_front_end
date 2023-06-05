

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
                        html.H5('(Ontologically Grouped) Differential Analysis: Walkthrough'),
                        dp.DashPlayer(
                            id="player_1",
                            url="https://youtu.be/ipSUX9JzXSI",
                            controls=True,
                            width="100%",
                            height="350px",
                        ),
                        html.Br(),
                        html.H5('How is Ontologically Grouped Differential Analysis Calculated?'),
                        dp.DashPlayer(
                            id="player_2",
                            url="https://youtu.be/NvQDmvGIcH8",
                            controls=True,
                            width="100%",
                            height="350px",
                        ),
                        html.Br(),
                        html.H5('BinDiscover: Overview of Components'),
                        dp.DashPlayer(
                            id="player_3",
                            url="https://youtu.be/WkEt7WolqVs",
                            controls=True,
                            width="100%",
                            height="350px",
                        ),
                        html.Br(),
                        html.H5('Exploring Bacteria and Squalene'),
                        dp.DashPlayer(
                            id="player_4",
                            url="https://youtu.be/9opzdOdNMSY",
                            controls=True,
                            width="100%",
                            height="350px",
                        ),
                    ],
                    width=5
                ),
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        html.H4('Frequently Asked Questions'),
                        html.Br(),

                        html.H6('Where can I find more information?'),
                        html.P(
                            [
                                'Please see our publication ',
                                html.A("Publication Link Here", href = "https://google.com"),
                                '.'
                            ]
                        ),
                            
                        
                        html.Hr(),

                        html.H6('Can I access the underlying distributions?'),
                        html.P(
                            [
                                'Yes, the full underlying distributions are available at ',
                                html.A("Zenodo", href = "https://zenodo.org/record/7982901"),
                                '.'
                            ]
                        ),
                        html.Hr(),

                        html.H6('Is there an API for public use?'),
                        html.P(
                            [
                                'Yes, please see the full ',
                                html.A("API documentation", href = "https://metabolomics-us.github.io/bindiscover/"),
                                '.'
                            ]
                            ),
                        html.Hr(),

                        html.H6('Can I download the .msp files of compounds?'),
                        html.P('Yes, please download these using the buttons on the BinBrowser component.'),
                        html.Hr(),

                        html.H6('Why are there multiple entries for an organ or disease in OGDA/Phylo?'),
                        html.P('In the MeSH hierarchy, organs and disease can have multiple locations in the hierarchy based on context. For example, fruit is part of a plant but also a type of food. ( https://meshb.nlm.nih.gov/record/ui?ui=D005638 )'),
                        html.Hr(),

                    ],
                    width=4
                ),
                dbc.Col(width=1)
            ]
        )
    ],
)