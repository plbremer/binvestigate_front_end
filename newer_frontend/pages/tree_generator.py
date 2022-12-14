import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio
from . import hierarchical_differential_analysis_helper
import networkx as nx
from . import venn_helper

from pprint import pprint
dash.register_page(__name__)

#base_url_api = f"http://api_alias:4999/"
base_url_api = f"http://127.0.0.1:4999/"

########get things from helper script########
species_networkx,species_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_species()
organ_networkx,organ_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_organ()
disease_networkx,disease_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_disease()
index_panda=pd.read_pickle('../newer_datasets/index_panda.bin')
index_panda=index_panda.sort_index()
index_panda['species']=index_panda['species'].astype(str)


unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
##############################################


layout=html.Div(
    children=[
    # dbc.Row(
    #     children=[
    #         dbc.Col(
    #             children=[
    #                 html.H2("Venn Comparator", className='text-center'),
    #                 html.Br(),
    #             ],
    #             width={'size':6}
    #         )
    #     ],
    #     #justify='center'
    # ),
        dbc.Row(
            children=[
                #dbc.Col(width=5),
                #dbc.Col(
                #    children=[
                html.H2('Step 1: Choose Triplets and Options'),
                #    ],
                    #width=(4)
                #),
                #dbc.Col(width=3)
            ],
            #align='center',
            style={'textAlign': 'center'}
        ),
        dbc.Row(
            children=[
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        #html.H2("From Triplet", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_species',
                            options=sorted([
                                {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select species ontology node'
                        ),  
                        dcc.Dropdown(
                            id='dropdown_organ',
                            options=sorted([
                                {'label':organ_node_dict[temp], 'value':temp} for temp in organ_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select organ ontology node'
                        ), 
                        dcc.Dropdown(
                            id='dropdown_disease',
                            options=sorted([
                                {'label':disease_node_dict[temp], 'value':temp} for temp in disease_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select disease ontology node'
                        ), 
                        html.Br(),
                    ],
                    width={'size':3}
                ),


                dbc.Col(
                    children=[
                        #html.H2("From Triplet", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_triplet_selection',
                            options=sorted([
                                {'label': temp, 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                            ],key=lambda x:x['label']),
                            multi=True,
                            placeholder='Select Triplet'
                            #maxHeight=300
                            #style={ "overflow-y":"scroll", "height": "100px"}
                            #style = {'max-height': '280px', 'overflow-y': 'auto'}
                            # style={
                            #     'color': '#212121',
                            #     'background-color': '#3EB489',
                            # }
                        ),  
                        html.Br(),
                    ],
                    width={'size':4}
                ),






            ]
        
        ),



        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=3),
                dbc.Col(
                    children=[
                        html.H2("Step 2: Express Chosen Triplets", className='text-center'),
                        html.Div(
                            dbc.Button(
                                'Get Results',
                                id='tree_metadata_query',
                            ),
                            className="d-grid gap-2 col-3 mx-auto",
                        ),
                        #html.H2("Venn Comparator", className='text-center'),
                        dash_table.DataTable(
                            id='tree_table_metadata',
                            columns=[
                                #{'name': 'From or To', 'id': 'from_or_to'},
                                {'name': 'Triplet ID', 'id': 'triplet_id'}, 
                                {'name': 'Sample Count', 'id': 'sample_count'}
                            ],
                            data=[],
                            page_current=0,
                            page_size=10,
                            #page_action='custom',
                            page_action='native',
                            #sort_action='custom',
                            sort_action='native',
                            sort_mode='multi',
                            #sort_by=[],
                            #filter_action='custom',
                            filter_action='native',
                            #filter_query='',
                            style_cell={
                                'fontSize': 17,
                                'padding': '8px',
                                'textAlign': 'center'
                            },
                            style_header={
                                'font-family': 'arial',
                                'fontSize': 15,
                                'fontWeight': 'bold',
                                'textAlign': 'center'
                            },
                            style_data={
                                'textAlign': 'center',
                                'fontWeight': 'bold',
                                'font-family': 'Roboto',
                                'fontSize': 15,
                            },
                            row_deletable=True,
                        )
                    ],
                    #width={'size':3}
                ),
                dbc.Col(width=3),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width={'size':2}),
                dbc.Col(
                    children=[
                        html.H2("Step 3: Perform Differential Analysis", className='text-center'),
                        html.Div(
                            dbc.Button(
                                'Get Results',
                                id='tree_query',
                            ),
                            className="d-grid gap-2 col-3 mx-auto",
                        ),
                    ],
                    width={'size':8}
                ),
                dbc.Col(width={'size':2}),
            ],
            #justify='center'
        ),



    ]
)


@callback(
    [
        Output(component_id="dropdown_species", component_property="options"),
        Output(component_id="dropdown_organ", component_property="options"),
        Output(component_id="dropdown_disease", component_property="options"),
    ],
    [
        Input(component_id="dropdown_species", component_property="value"),
        Input(component_id="dropdown_organ", component_property="value"),
        Input(component_id="dropdown_disease", component_property="value"),
    ],
    prevent_initial_call=True
)
def update_input_options_to(
    to_species_value_input,
    to_organ_value_input,
    to_disease_value_input,
):

    '''
    this callback makes it so that if a user specifies a species, an organ, or a disease
    for "to", then the other options are filtered accordingly
    '''
    #print('here')
    #determine valid species options
    temp_view=index_panda.copy()
    if to_species_value_input!=None:
        temp_set=nx.algorithms.dag.descendants(species_networkx,to_species_value_input)
        temp_set.add(to_species_value_input)
        temp_view=temp_view.loc[
            temp_view.species.isin(temp_set)
        ]

    if to_organ_value_input!=None:
        temp_set=nx.algorithms.dag.descendants(organ_networkx,to_organ_value_input)
        temp_set.add(to_organ_value_input)
        temp_view=temp_view.loc[
            temp_view.organ.isin(temp_set)
        ]

    if to_disease_value_input!=None:
        #print(to_disease_value_input)
        temp_set=nx.algorithms.dag.descendants(disease_networkx,to_disease_value_input)
        temp_set.add(to_disease_value_input)
        temp_view=temp_view.loc[
            temp_view.disease.isin(temp_set)
        ]

    all_basic_species_options=set(temp_view.species.values)
    all_valid_species_options=all_basic_species_options
    [all_valid_species_options:=all_valid_species_options.union(nx.ancestors(species_networkx,temp_option)) for temp_option in all_basic_species_options]

    all_basic_organ_options=set(temp_view.organ.values)
    all_valid_organ_options=all_basic_organ_options
    [all_valid_organ_options:=all_valid_organ_options.union(nx.ancestors(organ_networkx,temp_option)) for temp_option in all_basic_organ_options]

    all_basic_disease_options=set(temp_view.disease.values)
    all_valid_disease_options=all_basic_disease_options
    [all_valid_disease_options:=all_valid_disease_options.union(nx.ancestors(disease_networkx,temp_option)) for temp_option in all_basic_disease_options]

    species_options=sorted([
        {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict if temp in all_valid_species_options
    ],key=lambda x:x['label'])

    organ_options=sorted([
        {'label':organ_node_dict[temp], 'value':temp} for temp in organ_node_dict if temp in all_valid_organ_options
    ],key=lambda x:x['label'])

    disease_options=sorted([
        {'label':disease_node_dict[temp], 'value':temp} for temp in disease_node_dict if temp in all_valid_disease_options
    ],key=lambda x:x['label'])

    return species_options,organ_options,disease_options



@callback(
    [
        #Output(component_id="leaf_table", component_property="columns"),
        Output(component_id="tree_table_metadata", component_property="data")
    ],
    [
        Input(component_id="tree_metadata_query", component_property="n_clicks"),
    ],
    [
        State(component_id="dropdown_species", component_property="value"),
        State(component_id="dropdown_organ", component_property="value"),
        State(component_id="dropdown_disease", component_property="value"),
        State(component_id="dropdown_triplet_selection", component_property="value"),
    ],
    prevent_initial_call=True
)
def perform_metadata_query(
    query_n_clicks,
    dropdown_species_value,
    dropdown_organ_value,
    dropdown_disease_value,
    dropdown_triplet_selection_value

):
    '''
    describes the query that the user makes
    '''
    ################metadata query######################
    #prepare json for api
    metadata_json_output = {
        "species": dropdown_species_value,
        "organ": dropdown_organ_value,
        "disease": dropdown_disease_value,
        "species_organ_disease":dropdown_triplet_selection_value
    }
    pprint(metadata_json_output)
    #obtain results from api
    response = requests.post(base_url_api + "/treemetadataresource/", json=metadata_json_output)
    total_panda = pd.read_json(response.json(), orient="records")

    print(total_panda)

    data = total_panda.to_dict(orient='records')

    return [data]