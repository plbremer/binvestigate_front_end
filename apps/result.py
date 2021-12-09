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


@app.callback(
    [Output(component_id='subsetted_table',component_property='columns'),
    Output(component_id='subsetted_table',component_property='data')],
    [Input(component_id='button_perform_slice',component_property='n_clicks')],
    [State(component_id='store_from_species',component_property='data'),
    State(component_id='store_to_species',component_property='data'),
    State(component_id='store_from_organ',component_property='data'),
    State(component_id='store_to_organ',component_property='data'),
    State(component_id='store_from_disease',component_property='data'),
    State(component_id='store_to_disease',component_property='data'),
    State(component_id='store_additional',component_property='data'),]
)
def slice_database(
    button_perform_slice_n_clicks,
    store_from_species_data,
    store_to_species_data,
    store_from_organ_data,
    store_to_organ_data,
    store_from_disease_data,
    store_to_disease_data,
    store_additional_data
):
    print(button_perform_slice_n_clicks)
    print(store_from_species_data)
    print(store_to_species_data)
    print(store_from_organ_data)
    print(store_to_organ_data)
    print(store_from_disease_data)
    print(store_to_disease_data)
    print(store_additional_data)



