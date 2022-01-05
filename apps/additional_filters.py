from dash import html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import callback_context
import dash_daq as daq

import pathlib

from app import app


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


layout=html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Additional Result Filters", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    children=[
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Fold Change Minimum",className="card-title"),
                                                    html.H6("The minimum absolute value of fold change in shown results. There is greater confidence in large fold changes", className="card-subtitle"),
                                                    html.Br(),
                                                    dcc.Input(
                                                        id='fold_change_input',
                                                        placeholder='Min. fold change mag.',
                                                        value=1,
                                                        debounce=True
                                                    )
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Sample Count Minimum, Single Metadata Group",className="card-title"),
                                                    html.H6("The minimum number of samples that any metadata group can have in a result.", className="card-subtitle"),
                                                    html.Br(),
                                                    dcc.Input(
                                                        id='min_count_input',
                                                        placeholder='',
                                                        value=1,
                                                        debounce=True
                                                    )
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Sample Count Minimum, All Metadata Groups Summed",className="card-title"),
                                                    html.H6("The minimum number of samples that all metadata groups in a result have in total.", className="card-subtitle"),
                                                    html.Br(),
                                                    dcc.Input(
                                                        id='total_count_input',
                                                        placeholder='',
                                                        value=1,
                                                        debounce=True
                                                    )
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Number of Metadata Groups Minimum",className="card-title"),
                                                    html.H6("The minimum number of distinct metadata groups that a result can contain.", className="card-subtitle"),
                                                    html.Br(),
                                                    dcc.Input(
                                                        id='min_triplet_input',
                                                        placeholder='',
                                                        value=1,
                                                        debounce=True
                                                    )
                                                ]
                                            )
                                        ),

                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Maximum Distance From Root",className="card-title"),
                                                    html.H6("The furthest distance that a grouping of metadata can be from the root. Smaller numbers means only larger groupings are returned.", className="card-subtitle"),
                                                    html.Br(),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(
                                                                children=[
                                                                    html.H5('Compounds'),
                                                                    html.H5('Species'),
                                                                    html.H5('Organs'),
                                                                    html.H5('Diseases')
                                                                ],
                                                                width={'size':6}
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    dcc.Input(
                                                                        id='max_root_dist_compounds',
                                                                        placeholder='',
                                                                        value=10,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='max_root_dist_species',
                                                                        placeholder='',
                                                                        value=10,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='max_root_dist_organs',
                                                                        placeholder='',
                                                                        value=10,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='max_root_dist_diseases',
                                                                        placeholder='',
                                                                        value=10,
                                                                        debounce=True
                                                                    ),                                                      
                                                                ],
                                                                width={'size':6}
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Minimum Distance From Leaves",className="card-title"),
                                                    html.H6("The smallest distance that a grouping can be from the leaves.", className="card-subtitle"),
                                                    html.Br(),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(
                                                                children=[
                                                                    html.H5('Compounds'),
                                                                    html.H5('Species'),
                                                                    html.H5('Organs'),
                                                                    html.H5('Diseases')
                                                                ],
                                                                width={'size':6}
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    dcc.Input(
                                                                        id='min_leaf_dist_compounds',
                                                                        placeholder='',
                                                                        value=-1,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='min_leaf_dist_species',
                                                                        placeholder='',
                                                                        value=-1,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='min_leaf_dist_organs',
                                                                        placeholder='',
                                                                        value=-1,
                                                                        debounce=True
                                                                    ),                                                      
                                                                    dcc.Input(
                                                                        id='min_leaf_dist_diseases',
                                                                        placeholder='',
                                                                        value=-1,
                                                                        debounce=True
                                                                    ),                                                      
                                                                ],
                                                                width={'size':6}
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    width={'size':4}#,
                    #align='center'
                )
            ],
            justify='center'
        ),
    ]
)



@app.callback(
    #[Output(component_id='slider_additional',component_property='value'),
    #Output(component_id='toggleswitch_additional',component_property='value'),
    [Output(component_id='store_additional',component_property='data'),
    Output(component_id='fold_change_input',component_property='value'),
    #Output(component_id='toggleswitch_presence_absence',component_property='value'),
    Output(component_id='min_count_input',component_property='value'),
    Output(component_id='total_count_input',component_property='value'),
    Output(component_id='min_triplet_input',component_property='value'),
    Output(component_id='max_root_dist_compounds',component_property='value'),
    Output(component_id='min_leaf_dist_compounds',component_property='value'),
    Output(component_id='max_root_dist_species',component_property='value'),
    Output(component_id='min_leaf_dist_species',component_property='value'),
    Output(component_id='max_root_dist_organs',component_property='value'),
    Output(component_id='min_leaf_dist_organs',component_property='value'),
    Output(component_id='max_root_dist_diseases',component_property='value'),
    Output(component_id='min_leaf_dist_diseases',component_property='value')
    ],
    
    [Input(component_id='fold_change_input',component_property='value'),
    #Input(component_id='toggleswitch_presence_absence',component_property='value'),
    Input(component_id='min_count_input',component_property='value'),
    Input(component_id='total_count_input',component_property='value'),
    Input(component_id='min_triplet_input',component_property='value'),
    Input(component_id='max_root_dist_compounds',component_property='value'),
    Input(component_id='min_leaf_dist_compounds',component_property='value'),
    Input(component_id='max_root_dist_species',component_property='value'),
    Input(component_id='min_leaf_dist_species',component_property='value'),
    Input(component_id='max_root_dist_organs',component_property='value'),
    Input(component_id='min_leaf_dist_organs',component_property='value'),
    Input(component_id='max_root_dist_diseases',component_property='value'),
    Input(component_id='min_leaf_dist_diseases',component_property='value'),
    ],

    [State(component_id='store_additional',component_property='data')]
)
def callback_additional(
    fold_change_input_value,
    #toggleswitch_presence_absence_value,
    min_count_input_value,
    total_count_input_value,
    min_triplet_input_value,
    max_root_dist_compounds_value,
    min_leaf_dist_compounds_value,
    max_root_dist_species_value,
    min_leaf_dist_species_value,
    max_root_dist_organs_value,
    min_leaf_dist_organs_value,
    max_root_dist_diseases_value,
    min_leaf_dist_diseases_value,
    store_additional_data
):
    #it was noticed that upon initial load, the  callback context had length >1
    #like
    #[{'prop_id': 'slider_additional.value', 'value': 0}, {'prop_id': 'toggleswitch_additional.value', 'value': True}]
    #this only works if the number of buttons is >1, but thats the case, so be it

    #therefore, we load from store if the callback context length is >1 and the store is not none
    # print('-------------')
    # print(callback_context.triggered)
    # print(slider_additional_value)
    # print(toggleswitch_additional_value)
    # print(store_additional_data)

    if (len(callback_context.triggered)>1) and (store_additional_data is None):
        store_additional_data={
            # 'slider_additional':slider_additional_value,
            # 'toggleswitch_additional':toggleswitch_additional_value,
            'fold_change_input': fold_change_input_value,
            'toggleswitch_presence_absence': 'obsolete?',#toggleswitch_presence_absence_value,
            'min_count_input': min_count_input_value,
            'total_count_input': total_count_input_value,
            'min_triplet_input': min_triplet_input_value,
            'max_root_dist_compounds': max_root_dist_compounds_value,
            'min_leaf_dist_compounds': min_leaf_dist_compounds_value,
            'max_root_dist_species': max_root_dist_species_value,
            'min_leaf_dist_species': min_leaf_dist_species_value,
            'max_root_dist_organs': max_root_dist_organs_value,
            'min_leaf_dist_organs': min_leaf_dist_organs_value,
            'max_root_dist_diseases': max_root_dist_diseases_value,
            'min_leaf_dist_diseases': min_leaf_dist_diseases_value,
        }
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value


    elif (len(callback_context.triggered)>1) and (store_additional_data is not None):
        
        fold_change_input_value=store_additional_data['fold_change_input']
        toggleswitch_presence_absence_value=store_additional_data['toggleswitch_presence_absence']
        min_count_input_value=store_additional_data['min_count_input']
        total_count_input_value=store_additional_data['total_count_input']
        min_triplet_input_value=store_additional_data['min_triplet_input']
        max_root_dist_compounds_value=store_additional_data['max_root_dist_compounds']
        min_leaf_dist_compounds_value=store_additional_data['min_leaf_dist_compounds']
        max_root_dist_species_value=store_additional_data['max_root_dist_species']
        min_leaf_dist_species_value=store_additional_data['min_leaf_dist_species']
        max_root_dist_organs_value=store_additional_data['max_root_dist_organs']
        min_leaf_dist_organs_value=store_additional_data['min_leaf_dist_organs']
        max_root_dist_diseases_value=store_additional_data['max_root_dist_diseases']
        min_leaf_dist_diseases_value=store_additional_data['min_leaf_dist_diseases']

        return store_additional_data, fold_change_input_value,toggleswitch_presence_absence_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'fold_change_input.value'):
        store_additional_data['fold_change_input']=fold_change_input_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'toggleswitch_presence_absence.value'):
        store_additional_data['toggleswitch_presence_absence']='obsolete?'
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_count_input.value'):
        store_additional_data['min_count_input']=min_count_input_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'total_count_input.value'):
        store_additional_data['total_count_input']=total_count_input_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_triplet_input.value'):
        store_additional_data['min_triplet_input']=min_triplet_input_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'max_root_dist_compounds.value'):
        store_additional_data['max_root_dist_compounds']=max_root_dist_compounds_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_leaf_dist_compounds.value'):
        store_additional_data['min_leaf_dist_compounds']=min_leaf_dist_compounds_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'max_root_dist_species.value'):
        store_additional_data['max_root_dist_species']=max_root_dist_species_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_leaf_dist_species.value'):
        store_additional_data['min_leaf_dist_species']=min_leaf_dist_species_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
        
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'max_root_dist_organs.value'):
        store_additional_data['max_root_dist_organs']=max_root_dist_organs_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_leaf_dist_organs.value'):
        store_additional_data['min_leaf_dist_organs']=min_leaf_dist_organs_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'max_root_dist_diseases.value'):
        store_additional_data['max_root_dist_diseases']=max_root_dist_diseases_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'min_leaf_dist_diseases.value'):
        store_additional_data['min_leaf_dist_diseases']=min_leaf_dist_diseases_value
        return store_additional_data, fold_change_input_value,min_count_input_value,total_count_input_value,min_triplet_input_value,max_root_dist_compounds_value,min_leaf_dist_compounds_value,max_root_dist_species_value,min_leaf_dist_species_value,max_root_dist_organs_value,min_leaf_dist_organs_value,max_root_dist_diseases_value,min_leaf_dist_diseases_value
    
    
    
    
    # elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'slider_additional.value'):
    #     store_additional_data['slider_additional']=slider_additional_value
    #     return slider_additional_value,toggleswitch_additional_value,store_additional_data


    # elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'toggleswitch_additional.value'):
    #     store_additional_data['toggleswitch_additional']=toggleswitch_additional_value
    #     return slider_additional_value,toggleswitch_additional_value,store_additional_data
