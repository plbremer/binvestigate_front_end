# 1
# 20
# [{'column_id': 'continent', 'direction': 'asc'}, {'column_id': 'lifeExp', 'direction': 'asc'}]
# {continent} scontains Asia && {lifeExp} s> 50

import json
import networkx as nx
from pprint import pprint
import pandas as pd

import dash
from dash import Dash
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bio as dashbio

from dash_table.Format import Format, Scheme, Group


#set in accordance with overall flask app
base_url = "http://127.0.0.1:4999/"
import requests

import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

operators = [
    ['ge ', '>='],
    ['le ', '<='],
    ['lt ', '<'],
    ['gt ', '>'],
    ['ne ', '!='],
    ['eq ', '='],
    ['contains ']
]

############### LOAD HIERARCHIES ##############
species_json_address = DATA_PATH.joinpath("cyto_format_species.json")
temp_json_file = open(species_json_address, "r")
species_network_dict_from = json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict_from["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["scientific_name"]
temp_json_file = open(species_json_address, "r")
species_network_dict_to = json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict_to["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["scientific_name"]

organ_json_address = DATA_PATH.joinpath("cyto_format_organ.json")
temp_json_file = open(organ_json_address, "r")
organ_network_dict_from = json.load(temp_json_file)
temp_json_file.close()
for temp_element in organ_network_dict_from["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["mesh_label"]
temp_json_file = open(organ_json_address, "r")
organ_network_dict_to = json.load(temp_json_file)
temp_json_file.close()
for temp_element in organ_network_dict_to["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["mesh_label"]

disease_json_address = DATA_PATH.joinpath("cyto_format_disease.json")
temp_json_file = open(disease_json_address, "r")
disease_network_dict_from = json.load(temp_json_file)
temp_json_file.close()
for temp_element in disease_network_dict_from["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["mesh_label"]
temp_json_file = open(disease_json_address, "r")
disease_network_dict_to = json.load(temp_json_file)
temp_json_file.close()
for temp_element in disease_network_dict_to["elements"]["nodes"]:
    temp_element["data"]["label"] = temp_element["data"]["mesh_label"]
###########################################


######### HELPER FUNCTIONS ################
def remove_unmapped_nodes(temp_network_dict, temp_mapped_to_dict):
    """
    here we completely ignore the edges in the dict

    create an empty list
    go through every dict in 'nodes'
    if we map to it, then add that temp_dict the empty dict
    """
    only_mapped_to_nodes = [
        temp_data
        for temp_data in temp_network_dict["elements"]["nodes"]
        if temp_mapped_to_dict[temp_data["data"]["id"]] == "Yes"
    ]
    temp_network_dict["elements"]["nodes"] = only_mapped_to_nodes
    return temp_network_dict


def remove_redundant_options(temp_network_dict):
    """
    because of the way the organ and disease MeSH hierarchies work, things like "plasma" can
    appear in multple places (they are fluids, blood components, etc)

    redundancies are due to the same mesh label not id

    this function removes things that appear more than once

    so the individual nodes that appear are someone "random". we just keep the first unique of each label
    """
    only_appeared_once_mesh_label = list()
    mesh_labels_added = set()
    for temp_data in temp_network_dict["elements"]["nodes"]:
        if temp_data["data"]["mesh_label"] not in mesh_labels_added:
            mesh_labels_added.add(temp_data["data"]["mesh_label"])
            only_appeared_once_mesh_label.append(temp_data)
    temp_network_dict["elements"]["nodes"] = only_appeared_once_mesh_label
    return temp_network_dict
########################################


#############Load pandas for data selection options ##########
table_species_address = DATA_PATH.joinpath("table_species_dash.bin")
table_organ_address = DATA_PATH.joinpath("table_organ_dash.bin")
table_disease_address = DATA_PATH.joinpath("table_disease_dash.bin")

species_map_panda = pd.read_pickle(table_species_address)
species_map_dict = {
    temp_tup[0]: temp_tup[1]
    for temp_tup in list(
        zip(species_map_panda.node_id.to_list(), species_map_panda.we_map_to.to_list())
    )
}
organ_map_panda = pd.read_pickle(table_organ_address)
organ_map_dict = {
    temp_tup[0]: temp_tup[1]
    for temp_tup in list(
        zip(organ_map_panda.node_id.to_list(), organ_map_panda.we_map_to.to_list())
    )
}
disease_map_panda = pd.read_pickle(table_disease_address)
disease_map_dict = {
    temp_tup[0]: temp_tup[1]
    for temp_tup in list(
        zip(disease_map_panda.node_id.to_list(), disease_map_panda.we_map_to.to_list())
    )
}

#to swap species names on metadata query
species_networkx_address=DATA_PATH.joinpath("species_networkx.bin")
species_networkx=nx.readwrite.read_gpickle(species_networkx_address)
swap_dict_species={
    species_networkx.nodes[temp_node]['ncbi_number']:species_networkx.nodes[temp_node]['scientific_name'] for temp_node in species_networkx.nodes
}
########################################


#####Read in panda for filtering options after one is selected######
index_panda_address=DATA_PATH.joinpath("index_panda.bin")
index_panda=pd.read_pickle(index_panda_address)
index_panda=index_panda.sort_index()
####################################################################


############Update pandas for data selection#################
species_network_dict_from = remove_unmapped_nodes(
    species_network_dict_from, species_map_dict
)
organ_network_dict_from = remove_unmapped_nodes(organ_network_dict_from, organ_map_dict)
organ_network_dict_from = remove_redundant_options(organ_network_dict_from)
disease_network_dict_from = remove_unmapped_nodes(
    disease_network_dict_from, disease_map_dict
)
disease_network_dict_from = remove_redundant_options(disease_network_dict_from)

species_network_dict_to = remove_unmapped_nodes(
    species_network_dict_to, species_map_dict
)
organ_network_dict_to = remove_unmapped_nodes(organ_network_dict_to, organ_map_dict)
organ_network_dict_to = remove_redundant_options(organ_network_dict_to)
disease_network_dict_to = remove_unmapped_nodes(
    disease_network_dict_to, disease_map_dict
)
disease_network_dict_to = remove_redundant_options(disease_network_dict_to)
#############################################


#####################Structure of app#################
app.layout=html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Metadata Group Comparator", className='text-center'),
                        html.Br(),
                    ],
                    width={'size':6}
                )
            ],
            justify='center'
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Br(),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Available Species")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_species',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Available Organs")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_organ',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Available Diseases")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        html.Br(),
                    ],
                    width={'size':4}
                ),
                dbc.Col(
                    children=[

                    ],
                    width={'size':2}
                ),
                dbc.Col(
                    children=[
                        html.Br(),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Available Species")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_species',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Available Organs")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_organ',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Available Diseases")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        html.Br(),
                    ],
                    width={'size':4}
                ),
            ],
            justify='around'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Br(),
                        html.H2("Describe Comparison", className='text-center'),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                html.Button(
                                                    'Describe Groups',
                                                    id='query_metadata',
                                                ),
                                                width={'size':2}
                                            ),
                                        ],
                                        justify='center'
                                    ),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                dbc.Card(
                                                    dt.DataTable(
                                                        id='table_query_summary_from',
                                                        columns=[
                                                            {'name': 'Triplet List', 'id': 'unique_triplet_list_real_from'}, 
                                                            {'name': 'Triplet Count', 'id': 'triplet_count_from'}, 
                                                            {'name': 'Sample Count List', 'id': 'sample_count_list_from'}, 
                                                            {'name': 'Sample Count Min', 'id': 'min_sample_count_from'}, 
                                                            {'name': 'Sample Count Sum', 'id': 'sum_sample_count_from'}
                                                        ],
                                                        data=[],
                                                        style_header={
                                                            'backgroundColor': 'rgb(30, 30, 30)',
                                                            'color': 'white'
                                                        },
                                                        style_data={
                                                            'backgroundColor': 'rgb(50, 50, 50)',
                                                            'color': 'white',
                                                        },
                                                        style_cell={"whiteSpace": "pre-line"},
                                                    )
                                                ),
                                                width={'size':6}
                                            ),
                                            dbc.Col(
                                                dbc.Card(
                                                    dt.DataTable(
                                                        id='table_query_summary_to',
                                                        columns=[
                                                            {'name': 'Triplet List', 'id': 'unique_triplet_list_real_to'}, 
                                                            {'name': 'Triplet Count', 'id': 'triplet_count_to'}, 
                                                            {'name': 'Sample Count List', 'id': 'sample_count_list_to'}, 
                                                            {'name': 'Sample Count Min', 'id': 'min_sample_count_to'}, 
                                                            {'name': 'Sample Count Sum', 'id': 'sum_sample_count_to'}
                                                        ],
                                                        data=[],
                                                        style_header={
                                                            'backgroundColor': 'rgb(30, 30, 30)',
                                                            'color': 'white'
                                                        },
                                                        style_data={
                                                            'backgroundColor': 'rgb(50, 50, 50)',
                                                            'color': 'white'
                                                        },
                                                        style_cell={"whiteSpace": "pre-line"},
                                                    )
                                                ),
                                                width={'size':6}
                                            )
                                        ],
                                        justify='around'
                                    )
                                ],
                            )
                        )
                    ],
                    width={'size':12}
                )
            ],
            justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Br(),
                        html.H2("Results - Individual Compounds", className='text-center'),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dcc.Checklist(
                                        id='checklist_query',
                                        options={
                                            'Classes':'Classes',
                                            'Knowns':'Knowns',
                                            'Unknowns':'Unknowns'
                                        }
                                    ),
                                    html.Button(
                                        'Get Results',
                                        id='button_query',
                                    )
                                ]
                            )
                        )
                    ],
                    width={'size':3}
                )
            ],
            justify='center'
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4(
                                            "Welch p-Value vs. Average Fold", className='text-center')
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_average_welch'
                                        )
                                    ),
                                ]
                            )
                        )
                    ]
                ),                
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4(
                                            "Mann Whitney p-Value vs. Median Fold", className='text-center')
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_median_mw',
                                        )
                                    ),
                                ]
                            )
                        )
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Card(
                    dt.DataTable(
                        id='table',
                        columns=[
                            {"name": "English Name", "id": "english_name"},
                            {"name": "Fold Average", "id": "fold_average"},
                            {"name": "Significance Welch", "id": "sig_welch"},
                            {"name": "Fold Median", "id": "fold_median"},
                            {"name": "Significance MWU", "id": "sig_mannwhit"}
                        ],
                        data=[],
                        page_current=0,
                        page_size=50,
                        page_action='custom',
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },

                        sort_action='custom',
                        sort_mode='multi',
                        sort_by=[],

                        filter_action='custom',
                        filter_query=''
                    )
                ),
            ],
            justify='center'
        ),
    ]
)
######################################################

@app.callback(
    [
        Output(component_id="table_query_summary_from", component_property="columns"),
        Output(component_id="table_query_summary_from", component_property="data"),
        Output(component_id="table_query_summary_to", component_property="columns"),
        Output(component_id="table_query_summary_to", component_property="data"),
    ],
    [
        Input(component_id="query_metadata", component_property="n_clicks"),
    ],
    [
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),
    ],
)
def perform_metadata_query(
    query,
    from_species_value,
    from_organ_value,
    from_disease_value,
    to_species_value,
    to_organ_value,
    to_disease_value,
):
    '''
    describes the query that the user makes
    '''
    ################metadata query######################
    #prepare json for api
    metadata_json_output = {
        "from_species": from_species_value,
        "from_organ": from_organ_value,
        "from_disease": from_disease_value,
        "to_species": to_species_value,
        "to_organ": to_organ_value,
        "to_disease": to_disease_value,
    }
    #obtain results from api
    response = requests.post(base_url + "/metadataresource/", json=metadata_json_output)
    total_panda = pd.read_json(response.json(), orient="records")

    pre_swap_from=total_panda.at[0,'unique_triplet_list_real_from']
    post_swap_from=[
        [temp[0],swap_dict_species[temp[1]],temp[2]] for temp in pre_swap_from
    ]
    total_panda.at[0,'unique_triplet_list_real_from']=post_swap_from
    pre_swap_to=total_panda.at[0,'unique_triplet_list_real_to']
    post_swap_to=[
        [temp[0],swap_dict_species[temp[1]],temp[2]] for temp in pre_swap_to
    ]
    total_panda.at[0,'unique_triplet_list_real_to']=post_swap_to 

    #prepare column list for table
    query_summary_column_list_from = [
        {"name": temp_col, "id": temp_col} for temp_col in total_panda.columns if "from" in temp_col
    ]
    query_summary_column_list_to = [
        {"name": temp_col, "id": temp_col} for temp_col in total_panda.columns if "from" not in temp_col
    ]

    #prepare data for table
    query_summary_data_from = total_panda.to_dict(orient="records")
    for temp_key in query_summary_data_from[0]:
        query_summary_data_from[0][temp_key] = str(query_summary_data_from[0][temp_key])
    query_summary_data_to = total_panda.to_dict(orient="records")
    for temp_key in query_summary_data_to[0]:
        query_summary_data_to[0][temp_key] = str(query_summary_data_to[0][temp_key])

    query_summary_data_from[0]['unique_triplet_list_real_from']=query_summary_data_from[0]['unique_triplet_list_real_from'].replace('], [','],\n[')
    query_summary_data_from[0]['sample_count_list_from']=query_summary_data_from[0]['sample_count_list_from'].replace(', ',',\n')
    query_summary_data_to[0]['unique_triplet_list_real_to']=query_summary_data_to[0]['unique_triplet_list_real_to'].replace('], [','],\n[')
    query_summary_data_to[0]['sample_count_list_to']=query_summary_data_to[0]['sample_count_list_to'].replace(', ',',\n')
    
    new_names=['Triplet List','Triplet Count','Sample Count List','Sample Count Min','Sample Count Sum']
    query_summary_column_list_from = [
        {"name": new_names[i], "id": query_summary_column_list_from[i]['id']} for i in range(len(query_summary_column_list_from))
    ]

    return query_summary_column_list_from,query_summary_data_from,query_summary_column_list_to,query_summary_data_to
        
    #####################################################


@app.callback(
    [
        Output(component_id="table", component_property="columns"),
        Output(component_id="table", component_property="data"),
        Output(component_id="volcano_average_welch", component_property="figure"),
        Output(component_id="volcano_median_mw", component_property="figure"),
    ],
    [
        Input(component_id="button_query", component_property="n_clicks"),
        Input(component_id="table", component_property="page_current"),
        Input(component_id="table", component_property="page_size"),
        Input(component_id="table", component_property="sort_by"),
        Input(component_id="table", component_property="filter_query"),
    ],
    [
        State(component_id="checklist_query",component_property="value"),
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),
    ],
)
def perform_volcano_query(
    query,
    page_current,
    page_size,
    sort_by,
    filter_query,
    checklist_query,
    from_species_value,
    from_organ_value,
    from_disease_value,
    to_species_value,
    to_organ_value,
    to_disease_value,
):
    """
    """
    print(page_current)
    print(page_size)
    print(sort_by)
    print(filter_query)


    print('before json')

    if "Classes" in checklist_query:
        include_classes='Yes'
    else:
        include_classes='No'
    if "Knowns" in checklist_query:
        include_knowns='Yes'
    else:
        include_knowns='No'
    if "Unknowns" in checklist_query:
        include_unknowns='Yes'
    else:
        include_unknowns='No'

    ##################volcano query######################
    #prepare json for api
    volcano_json_output = {
        "from_species": from_species_value,
        "from_organ": from_organ_value,
        "from_disease": from_disease_value,
        "to_species": to_species_value,
        "to_organ": to_organ_value,
        "to_disease": to_disease_value,
        "include_classes": include_classes,
        "include_knowns": include_knowns,
        "include_unknowns": include_unknowns,
        "page_current":page_current,
        "page_size":page_size,
        "sort_by":sort_by,
        "filter_query":filter_query,
    }

    print('after json before api')
    #call api
    response = requests.post(base_url + "/volcanoresource/", json=volcano_json_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)

    #prepare columns and data for the table
    column_list = [
        {"name": "English Name", "id": "english_name"},
        {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        {"name": "Significance Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
        {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        {"name": "Significance MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
    ]
    data = total_panda.to_dict(orient='records')

    #prepare figures for volcano plots
    volcano_average = dashbio.VolcanoPlot(
        dataframe=total_panda,#bins_panda,
        snp="english_name",
        p="sig_welch",
        effect_size="fold_average",
        gene=None,
        xlabel='log2 Fold Change',
        genomewideline_value=1e-2,
    )
    volcano_median = dashbio.VolcanoPlot(
        dataframe=total_panda,#bins_panda,
        snp="english_name",
        p="sig_mannwhit",
        effect_size="fold_median",
        gene=None,
        xlabel='log2 Fold Change',
        genomewideline_value=1e-2,
    )
    #################################################3

    return (
        column_list,
        data,
        volcano_average,
        volcano_median,
    )


@app.callback(
    [
        Output(component_id="dropdown_from_species", component_property="options"),
        Output(component_id="dropdown_from_organ", component_property="options"),
        Output(component_id="dropdown_from_disease", component_property="options"),
    ],
    [
        Input(component_id="dropdown_from_species", component_property="value"),
        Input(component_id="dropdown_from_organ", component_property="value"),
        Input(component_id="dropdown_from_disease", component_property="value"),
    ],
)
def update_input_options_from(
    from_species_value_input,
    from_organ_value_input,
    from_disease_value_input,
):
    '''
    this callback makes it so that if a user specifies a species, an organ, or a disease
    for "from", then the other options are filtered accordingly
    '''

    #determine valid species options
    temp_view=index_panda.copy()
    if from_species_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_species_choice=temp_view.loc[temp_view.species==from_species_value_input].index[0][1]
        temp_view=temp_view.loc[
            slice(None),
            slice(temp_species_choice,temp_species_choice),
            slice(None)
        ]
    if from_organ_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_organ_choice=temp_view.loc[temp_view.organ==from_organ_value_input].index[0][0]
        temp_view=temp_view.loc[
            slice(temp_organ_choice,temp_organ_choice),
            slice(None),
            slice(None)
        ]

    if from_disease_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_disease_choice=temp_view.loc[temp_view.disease==from_disease_value_input].index[0][2]
        temp_view=temp_view.loc[
            slice(None),
            slice(None),
            slice(temp_disease_choice,temp_disease_choice)
        ]
  
    valid_species=set(temp_view.species.values)
    
    species_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in species_network_dict_from['elements']['nodes'] \
                if temp_node['data']['id'] in valid_species
    ]
    valid_organ=set(temp_view.organ.values)

    organ_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in organ_network_dict_from['elements']['nodes'] \
                if temp_node['data']['id'] in valid_organ
    ]
    valid_disease=set(temp_view.disease.values)

    disease_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in disease_network_dict_from['elements']['nodes'] \
                if temp_node['data']['id'] in valid_disease
    ]

    return species_options,organ_options,disease_options

@app.callback(
    [
        Output(component_id="dropdown_to_species", component_property="options"),
        Output(component_id="dropdown_to_organ", component_property="options"),
        Output(component_id="dropdown_to_disease", component_property="options"),
    ],
    [
        Input(component_id="dropdown_to_species", component_property="value"),
        Input(component_id="dropdown_to_organ", component_property="value"),
        Input(component_id="dropdown_to_disease", component_property="value"),
    ],
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

    #determine valid species options
    temp_view=index_panda.copy()
    if to_species_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_species_choice=temp_view.loc[temp_view.species==to_species_value_input].index[0][1]
        temp_view=temp_view.loc[
            slice(None),
            slice(temp_species_choice,temp_species_choice),
            slice(None)
        ]
    if to_organ_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_organ_choice=temp_view.loc[temp_view.organ==to_organ_value_input].index[0][0]
        temp_view=temp_view.loc[
            slice(temp_organ_choice,temp_organ_choice),
            slice(None),
            slice(None)
        ]

    if to_disease_value_input!=None:
        #we have to do some hoop jump through hoops because of the mesh hierarchies
        #haveing multiple instances of things like "plasma"
        temp_disease_choice=temp_view.loc[temp_view.disease==to_disease_value_input].index[0][2]
        temp_view=temp_view.loc[
            slice(None),
            slice(None),
            slice(temp_disease_choice,temp_disease_choice)
        ]
  
    valid_species=set(temp_view.species.values)
    
    species_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in species_network_dict_to['elements']['nodes'] \
                if temp_node['data']['id'] in valid_species
    ]
    valid_organ=set(temp_view.organ.values)

    organ_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in organ_network_dict_to['elements']['nodes'] \
                if temp_node['data']['id'] in valid_organ
    ]
    valid_disease=set(temp_view.disease.values)

    disease_options=[
        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} \
            for temp_node in disease_network_dict_to['elements']['nodes'] \
                if temp_node['data']['id'] in valid_disease
    ]

    return species_options,organ_options,disease_options


if __name__ == "__main__":

    app.run_server(debug=True)