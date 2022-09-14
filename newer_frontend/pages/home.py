

import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, path='/')

#df = px.data.gapminder()

layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),

])