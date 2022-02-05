import dash_table as dt
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

#things for api#
import requests
import pandas
base_url='http://127.0.0.1:5000/'
################

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
        html.Br(),
        html.H4('Where there is a non-null value for every field from all of the preceding pages, this table fills. Otherwise, it remains as an empty table.'),
        html.H4('At the moment, results render with back-end encoding. Updates coming soon :)')
        html.Br(),
        html.Br(),

        #resulting table
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        dt.DataTable(
                            id='subsetted_table',
                            columns=[{'name': 'temp', 'id': 'temp'}],
                            data=[],
                            page_current=0,
                            page_size=10,
                            page_action='custom',
                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white'
                                },
                                style_data={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                }
                        )
                    ]
                ),
                width='auto'
            )
        ),
        html.Br(),
        html.Br(),
        # dbc.Row(
        #     dbc.Col(
        #         html.Div(
        #             children=[
        #                 #a header
        #                 html.Button(
        #                     'Click button to slice/filter dataset',
        #                     id='button_perform_slice',
        #                     n_clicks=0
        #                 )
        #             ]
        #         ),
        #         width='auto'
        #     )
        # )
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
    #[Input(component_id='button_perform_slice',component_property='n_clicks'),
    [Input(component_id='subsetted_table',component_property='page_current'),
    Input(component_id='subsetted_table',component_property='page_size')],
    [State(component_id='store_compound',component_property='data'),
    State(component_id='store_from_species',component_property='data'),
    State(component_id='store_to_species',component_property='data'),
    State(component_id='store_from_organ',component_property='data'),
    State(component_id='store_to_organ',component_property='data'),
    State(component_id='store_from_disease',component_property='data'),
    State(component_id='store_to_disease',component_property='data'),
    State(component_id='store_additional',component_property='data'),
    State(component_id='store_result',component_property='data')]
)
def slice_database(
    #button_perform_slice_n_clicks,
    table_page_current,
    table_page_size,
    store_compound_data,
    store_from_species_data,
    store_to_species_data,
    store_from_organ_data,
    store_to_organ_data,
    store_from_disease_data,
    store_to_disease_data,
    store_additional_data,
    store_result_data
):

    store_result_data={
        'page_size':table_page_size,
        'page_current':table_page_current
    }

    #print(button_perform_slice_n_clicks)
    print(store_compound_data)
    print(store_from_species_data)
    print(store_to_species_data)
    print(store_from_organ_data)
    print(store_to_organ_data)
    print(store_from_disease_data)
    print(store_to_disease_data)
    print(store_additional_data)
    print(store_result_data)

    total_json_output={
        'store_compound':store_compound_data,
        'store_from_species':store_from_species_data,
        'store_to_species':store_to_species_data,
        'store_from_organ':store_from_organ_data,
        'store_to_organ':store_to_organ_data,
        'store_from_disease':store_from_disease_data,
        'store_to_disease':store_to_disease_data,
        'store_additional':store_additional_data,
        'store_result':store_result_data
    }



    response=requests.post(base_url+'/foldchangetable/',json=total_json_output)
    #temp=pandas.read_json(response.json(),orient='records')
    #print(temp)
    print(response.json())
    
    temp=pandas.read_json(response.json(),orient='records')
    column_dict_list=[
        {'name':temp_col,'id':temp_col} for temp_col in temp.columns
    ]

    return column_dict_list,temp.to_dict(orient='records')
