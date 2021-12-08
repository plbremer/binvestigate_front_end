import dash_table as dt
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State



import pathlib


from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



layout=html.Div(

    children=[
        #Table title
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H1('Backend Dataset')
                    ]
                ),
                width='auto',
            ),
            justify='center'
        ),
        #resulting table
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        dt.DataTable(
                            id='subsetted_table',
                            columns=[{'name': 'temp', 'id': 'temp'}],
                            data=[]
                        )
                    ]
                ),
                width='auto'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.Button(
                            'Click button to slice/filter dataset',
                            id='button_perform_slice',
                            n_clicks=0
                        )
                    ]
                ),
                width='auto'
            )
        )
    ]
)



#there should be one callback
#upon the button click, it
#1) forms the json
#2) calls the api
#3) renders the api's reply