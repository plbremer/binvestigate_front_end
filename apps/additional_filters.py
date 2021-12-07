


import pathlib

from app import app


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                children=[
                   html.H3('Minimum Fold Change Magnitude')
                ],
                width='auto',
                align='center'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
  
                    ]
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H3('Don\'t Include Presence/Absence ----- Include Presence/Absence')
                    ]
                ),
                width='auto',
            ),
            justify='center'
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        daq.ToggleSwitch(
                            id='toggleswitch_additional',
                            value=True
                        )
                    ]
                )
            )
        )
    ]
)