import json
import networkx as nx
from pprint import pprint
import pandas as pd

from dash import Dash
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bio as dashbio


base_url = "http://127.0.0.1:4999/"
import requests

import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


root_dist_max_compound=10
root_dist_max_species=10
root_dist_max_organ=10
root_dist_max_disease=10


############### LOAD HIERARCHIES ##############
compound_json_address = DATA_PATH.joinpath("cyto_format_compound.json")
temp_json_file = open(compound_json_address, "r")
compound_dict = json.load(temp_json_file)
temp_json_file.close()
for temp_element in compound_dict["elements"]["nodes"]:
    #options included 'id' 'inchikey' 'name' 'value'
    #also has property "type_of_node" (is it a leaf or not)
    temp_element["data"]["label"] = temp_element["data"]["id"]
# [(temp_element["data"]["label"] := temp_element["data"]["id"]) for temp_element in compound_dict["elements"]["nodes"]\
#     if temp_element['type_of_node']=='from_binvestigate']

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

############create compound selection options################
# no-- #i think that we will just have "if from_binvestigate== True in the load?"

#############################################################


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
########################################


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
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Select metadata and observe volcano plots below", className='text-center')
                                )
                            ]
                        )
                    ],
                    width={'size':4}#,
                    #align='center'
                )
            ],
            justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Choose compound stuff here", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "asdf", className='text-center')
                                )
                            ]
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Slider(0,root_dist_max_compound,1,value=0,id='slider_compound')
                            )
                        ),
                        dbc.Card(
                            dcc.Dropdown(
                                id='dropdown_compound',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes'] if (temp_node['data']['type_of_node']=='from_binvestigate')#species_network_dict_from['elements']['nodes']
                                ],
                                multi=False,
                                style={
                                    'color': '#212121',
                                    'background-color': '#3EB489',
                                }
                            )
                        ),
                    ],
                    width={'size':4}#,
                    #align='center'
                )
            ],
            justify='center'
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Selections here", className='text-center'),
                        html.Br(),
                        #dbc.Card(
                            #dbc.CardBody(
                            #    children=[
                            #        dbc.Card(html.H4("Blah")),
                            #        dbc.Card(
                            #            html.Button(
                            #                'Reset selections',
                            #                id='button_from_species',
                            #            )
                            #        ),
                            #    ]
                            #)
                        #),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dcc.Slider(0,root_dist_max_species,1,value=0,id='slider_from_species'),
                                    dcc.Slider(0,root_dist_max_organ,1,value=0,id='slider_from_organ'),
                                    dcc.Slider(0,root_dist_max_disease,1,value=0,id='slider_from_disease'),
                                ]
                            )
                        ),
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


                    ],
                    width={'size':4}
                ),
                dbc.Col(
                    children=[
                        #dbc.Card(
                        #    html.H4("lorem ipsum")
                        #)
                        html.H2('get compared to', className='text-center')
                    ],
                    width={'size':2}
                ),
                dbc.Col(
                    children=[
                        
                        html.H2("Selections here", className='text-center'),
                        html.Br(),
                        #dbc.Card(
                        #    dbc.CardBody(
                        #        children=[
                        #            dbc.Card(html.H4("Blah")),
                        #            dbc.Card(
                        #                html.Button(
                        #                    'Reset selections',
                        #                    id='button_to_species2',
                        #                )
                        #            ),3#
                        #  
                        # 
                        #        ]
                        #    )
                        #),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dcc.Slider(0,root_dist_max_species,1,value=0,id='slider_to_species'),
                                    dcc.Slider(0,root_dist_max_organ,1,value=0,id='slider_to_organ'),
                                    dcc.Slider(0,root_dist_max_disease,1,value=0,id='slider_to_disease'),
                                ]
                            )
                        ),
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
                        html.Br()
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
                        html.H2("Other options", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Node distance, count filters coming soon", className='text-center')
                                )
                            ]
                        )
                    ],
                    width={'size':4}#,
                    #align='center'
                )
            ],
            justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Br(),
                        html.H2("Execute query", className='text-center'),
                        #html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4("Click to query backend", className='text-center')
                                    ),
                                    dbc.Card(
                                        html.Button(
                                            'Execute Query',
                                            id='button_query',
                                        )
                                    )
                                ]
                            )
                        )
                    ],
                    width={'size':4}#,
                    #align='center'
                )
            ],
            justify='center'
        ),
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
                                            id='volcano_average_welch_bins',
                                        )
                                    ),
                                ]
                            )
                        )
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
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4(
                                            "Mann Whitney p-Value vs. Median Fold", className='text-center')
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_median_mw_bins',
                                        )
                                    )
                                ]
                            )
                        )
                    ],
                    width={'size':4}
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("result table", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    dt.DataTable(
                                            id='table_result',
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
                                )
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
######################################################


@app.callback(
    [
        # Output(component_id="table_query_summary", component_property="columns"),
        # Output(component_id="table_query_summary", component_property="data"),
        # Output(component_id="table_average_welch_bins", component_property="columns"),
        # Output(component_id="table_average_welch_bins", component_property="data"),
        # Output(component_id="table_median_mw_bins", component_property="columns"),
        # Output(component_id="table_median_mw_bins", component_property="data"),
        # Output(
        #     component_id="table_average_welch_classyfire", component_property="columns"
        # ),
        # Output(
        #     component_id="table_average_welch_classyfire", component_property="data"
        # ),
        Output(component_id="table_result", component_property="columns"),
        Output(component_id="table_result", component_property="data"),
        # Output(component_id="table_median_mw_classyfire", component_property="columns"),
        # Output(component_id="table_median_mw_classyfire", component_property="data"),
        Output(component_id="volcano_average_welch_bins", component_property="figure"),
        Output(component_id="volcano_median_mw_bins", component_property="figure"),
        # Output(
        #     component_id="volcano_average_welch_classyfire", component_property="figure"
        # ),
        # Output(
        #     component_id="volcano_median_mw_classyfire", component_property="figure"
        # ),
    ],
    [Input(component_id="button_query", component_property="n_clicks")],
    [
        State(component_id="dropdown_compound",component_property="value"),
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),

        State(component_id="slider_compound",component_property="value"),
        State(component_id="slider_from_species", component_property="value"),
        State(component_id="slider_from_organ", component_property="value"),
        State(component_id="slider_from_disease", component_property="value"),
        State(component_id="slider_to_species", component_property="value"),
        State(component_id="slider_to_organ", component_property="value"),
        State(component_id="slider_to_disease", component_property="value"),        
    ],
)
def perform_volcano_query(
    query,
    
    dropdown_compound_value,
    dropdown_from_species_value,
    dropdown_from_organ_value,
    dropdown_from_disease_value,
    dropdown_to_species_value,
    dropdown_to_organ_value,
    dropdown_to_disease_value,

    slider_compound_value,
    slider_from_species_value,
    slider_from_organ_value,
    slider_from_disease_value,
    slider_to_species_value,
    slider_to_organ_value,
    slider_to_disease_value,
):
    """
    The singular page callback
    """

    # ################metadata query######################
    # #prepare json for api
    # metadata_json_output = {
    #     "from_species": from_species_value,
    #     "from_organ": from_organ_value,
    #     "from_disease": from_disease_value,
    #     "to_species": to_species_value,
    #     "to_organ": to_organ_value,
    #     "to_disease": to_disease_value,
    # }
    # #obtain results from api
    # response = requests.post(base_url + "/metadataresource/", json=metadata_json_output)
    # total_panda = pd.read_json(response.json(), orient="records")

    # #prepare column list for table
    # query_summary_column_list = [
    #     {"name": temp_col, "id": temp_col} for temp_col in total_panda.columns
    # ]

    # #prepare data for table
    # query_summary_data = total_panda.to_dict(orient="records")
    # for temp_key in query_summary_data[0]:
    #     query_summary_data[0][temp_key] = str(query_summary_data[0][temp_key])
    # #####################################################


    ##################main query######################
    #prepare json for api
    # root_distance_json_output = {
    #     "from_species": dropdown_from_species_value,
    #     "from_organ": dropdown_from_organ_value,
    #     "from_disease": dropdown_from_disease_value,
    #     "to_species": dropdown_to_species_value,
    #     "to_organ": dropdown_to_organ_value,
    #     "to_disease": dropdown_to_disease_value,

    #     'compound_dfr':slider_compound_value,
    #     'species_from_dfr':slider_from_species_value,
    #     'organ_from_dfr':slider_from_organ_value,
    #     'disease_from_dfr':slider_from_disease_value,
    #     'species_to_dfr':slider_to_species_value,
    #     'organ_to_dfr':slider_to_organ_value,
    #     'disease_to_dfr':slider_to_disease_value,
        
    #     'page_size':50,
    #     'page_current':0
    # }

    root_distance_json_output = {
        "compound":2,
        "from_species":562,
        "from_organ":"A15.145.846",
        "from_disease":"No",
        "to_species":314146,
        "to_organ":"A12.207.270.695",
        "to_disease":"No",

        "compound_dfr":2,
        "species_from_dfr": 8,
        "organ_from_dfr":8,
        "disease_from_dfr":8,
        "species_to_dfr": 8,
        "organ_to_dfr":8,
        "disease_to_dfr":8,
        
        "page_size":50,
        "page_current":0
    }




    #call api
    response = requests.post(base_url + "/rootdistanceresource/", json=root_distance_json_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)

    result_table_column_list=[
        {'name':temp_col,'id':temp_col} for temp_col in total_panda.columns
    ]
    result_table_data=total_panda.to_dict(orient="records")

    #prepare figures for volcano plots
    volcano_average_bin = dashbio.VolcanoPlot(
        dataframe=total_panda,
        #snp="english_name",
        snp=None,
        p="sig_welch",
        effect_size="fold_average",
        gene=None,
    )
    volcano_median_bin = dashbio.VolcanoPlot(
        dataframe=total_panda,
        #snp="english_name",
        snp=None,
        p="sig_mannwhit",
        effect_size="fold_median",
        gene=None,
    )
    #################################################3

    return (
        result_table_column_list,
        result_table_data,
        volcano_average_bin,
        volcano_median_bin
    )





if __name__ == "__main__":

    app.run_server(debug=True)
