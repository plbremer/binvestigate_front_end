#in this app we dont filter the dropdowns based on other selections in the dropdowns
#because the "different chain locations" in a single dropdown selection
#each have their own set of corresponding other properties
#for example, a chain like banana->plant->root
#has an organ set for banana, set for plant, set for root
#it is nto clear which should be used for filtering
#by the time you get to organism, then you have every possibility

import json
import networkx as nx
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt

from dash import Dash
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bio as dashbio
from dash_table.Format import Format, Scheme, Group


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

######### Load networkx hierarchies########
compound_nx_address = DATA_PATH.joinpath("compounds_networkx.bin")
compound_nx=nx.readwrite.read_gpickle(compound_nx_address)
for temp_node in compound_nx.nodes:
    if compound_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
        compound_nx.nodes[temp_node]['name']=compound_nx.nodes[temp_node]['common_name']
species_nx_address = DATA_PATH.joinpath("species_networkx.bin")
species_nx=nx.readwrite.read_gpickle(species_nx_address)
# nx.draw(compound_nx,with_labels=True)
# plt.show()
organ_nx_address = DATA_PATH.joinpath("organ_networkx.bin")
organ_nx=nx.readwrite.read_gpickle(organ_nx_address)
disease_nx_address = DATA_PATH.joinpath("disease_networkx.bin")
disease_nx=nx.readwrite.read_gpickle(disease_nx_address)
###########################################

######### HELPER FUNCTIONS ################
def create_hierarchical_selection_labels_compound(temp_compound_dict,compound_nx):
    #{'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']
    compound_dropdown_options=list()
    for temp_node in temp_compound_dict['elements']['nodes']:
        #we only do "from binvestigate" because we only want full paths
        if temp_node['data']['type_of_node']=='from_binvestigate':
            # if bool(re.search('^([\s\d]+)$',temp_node['data']['common_name'])):
            #     compound_dropdown_options.append(
            #         {'label': 'Unknown: Bin ID '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
            #     )
            # else:
            #     compound_dropdown_options.append(
            #         {'label': 'Known: '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
            #     )
            #create the path from the networkx
            temp_path_list=nx.bidirectional_shortest_path(compound_nx,'CHEMONTID:9999999',int(temp_node['data']['id']))
            #temp_string_list=[compound_nx.nodes[temp_path_list[i]]['name'] for i in range(len(temp_path_list)-1,-1)]
            #print(temp_path_list)
            #print(reversed(temp_path_list))
            temp_string_list=[compound_nx.nodes[x]['name'] for x in reversed(temp_path_list)]
            temp_string=' -> '.join(temp_string_list)
            #print(range(len(temp_path_list)-1,-1))
            #print(temp_path_list)
            #print(temp_string_list)
            #print(temp_string)
            compound_dropdown_options.append(
                {'label': temp_string,'value':temp_node['data']['label']}
            )
        # else:
        #     compound_dropdown_options.append(
        #         {'label': 'Class: '+temp_node['data']['name'], 'value': temp_node['data']['label']}
        #     )            
    return compound_dropdown_options

def create_hierarchical_selection_labels_species(species_nx):
    #{'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']
    species_dropdown_options=list()
    for temp_node in species_nx.nodes:
        if len(nx.descendants(species_nx,temp_node))==0:
            temp_path_list=nx.bidirectional_shortest_path(species_nx,'1',temp_node)
            temp_string_list=[species_nx.nodes[x]['scientific_name'] for x in reversed(temp_path_list)]
            temp_string=' -> '.join(temp_string_list)
            species_dropdown_options.append(
                {'label': temp_string,'value':temp_node}
            )
    return species_dropdown_options

def create_hierarchical_selection_labels_organ(organ_nx):
    #{'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']
    organ_dropdown_options=list()
    for temp_node in organ_nx.nodes:
        if len(nx.descendants(organ_nx,temp_node))==0:
            temp_path_list=nx.bidirectional_shortest_path(organ_nx,'organ',temp_node)
            temp_string_list=[organ_nx.nodes[x]['mesh_label'] for x in reversed(temp_path_list)]
            temp_string=' -> '.join(temp_string_list)
            organ_dropdown_options.append(
                {'label': temp_string,'value':temp_node}
            )
    return organ_dropdown_options

def create_hierarchical_selection_labels_disease(disease_nx):
    #{'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']
    disease_dropdown_options=list()
    for temp_node in disease_nx.nodes:
        if len(nx.descendants(disease_nx,temp_node))==0:
            temp_path_list=nx.bidirectional_shortest_path(disease_nx,'disease',temp_node)
            temp_string_list=[disease_nx.nodes[x]['mesh_label'] for x in reversed(temp_path_list)]
            temp_string=' -> '.join(temp_string_list)
            disease_dropdown_options.append(
                {'label': temp_string,'value':temp_node}
            )
    return disease_dropdown_options
    # for temp_node in temp_species_dict['elements']['nodes']:
    #     #we only do "from binvestigate" because we only want full paths
    #     if temp_node['data']['type_of_node']=='from_binvestigate':
    #         # if bool(re.search('^([\s\d]+)$',temp_node['data']['common_name'])):
    #         #     compound_dropdown_options.append(
    #         #         {'label': 'Unknown: Bin ID '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
    #         #     )
    #         # else:
    #         #     compound_dropdown_options.append(
    #         #         {'label': 'Known: '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
    #         #     )
    #         #create the path from the networkx
    #         temp_path_list=nx.bidirectional_shortest_path(compound_nx,'CHEMONTID:9999999',int(temp_node['data']['id']))
    #         #temp_string_list=[compound_nx.nodes[temp_path_list[i]]['name'] for i in range(len(temp_path_list)-1,-1)]
    #         #print(temp_path_list)
    #         #print(reversed(temp_path_list))
    #         temp_string_list=[compound_nx.nodes[x]['name'] for x in reversed(temp_path_list)]
    #         temp_string=' -> '.join(temp_string_list)
    #         #print(range(len(temp_path_list)-1,-1))
    #         #print(temp_path_list)
    #         #print(temp_string_list)
    #         #print(temp_string)
    #         compound_dropdown_options.append(
    #             {'label': temp_string,'value':temp_node['data']['label']}
    #         )
    #     # else:
    #     #     compound_dropdown_options.append(
    #     #         {'label': 'Class: '+temp_node['data']['name'], 'value': temp_node['data']['label']}
    #     #     )            
    




############create selection options################
compound_dropdown_options=create_hierarchical_selection_labels_compound(compound_dict,compound_nx)
species_dropdown_options=create_hierarchical_selection_labels_species(species_nx)
organ_dropdown_options=create_hierarchical_selection_labels_organ(organ_nx)
disease_dropdown_options=create_hierarchical_selection_labels_disease(disease_nx)
#############################################################

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
                        html.H2("Single Compound Explorer", className='text-center'),
                        html.Br(),
                        html.Br(),
                        # dbc.Card(
                        #     children=[
                        #         dbc.CardBody(
                        #             html.H4(
                        #                 "Single Compound Explorer", className='text-center')
                        #         )
                        #     ]
                        # )
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
                        #html.H2("Choose compound stuff here", className='text-center'),
                        html.H2("OPTIONAL Compound Filters", className='text-center'),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Choose Compound", className='text-center')
                                )
                            ]
                        ),
                        # dbc.Card(
                        #     # dbc.CardBody(
                        #     #     dcc.Slider(0,root_dist_max_compound,1,value=0,id='slider_compound')
                        #     # )
                        # ),
                        dbc.Card(
                            dcc.Dropdown(
                                id='dropdown_compound',
                                # options=[
                                #     {'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']# if (temp_node['data']['type_of_node']=='from_binvestigate')#species_network_dict_from['elements']['nodes']
                                # ],
                                options=compound_dropdown_options,
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
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("OPTIONAL From Filters", className='text-center'),
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
                        #html.Br(),
                        # dbc.Card(
                        #     dbc.CardBody(
                        #         # children=[
                        #         #     dcc.Slider(0,root_dist_max_species,1,value=0,id='slider_from_species'),
                        #         #     dcc.Slider(0,root_dist_max_organ,1,value=0,id='slider_from_organ'),
                        #         #     dcc.Slider(0,root_dist_max_disease,1,value=0,id='slider_from_disease'),
                        #         # ]
                        #     )
                        # ),
                        #html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Filter Species")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_species',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            options=species_dropdown_options,
                                            #value='Any',
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Filter Organs")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_organ',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            options=organ_dropdown_options,
                                            ##value='Any',
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Filter Diseases")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_disease',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            #value='Any',
                                            options=disease_dropdown_options,
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
                # dbc.Col(
                #     children=[
                #         #dbc.Card(
                #         #    html.H4("lorem ipsum")
                #         #)
                #         html.H2('get compared to', className='text-center')
                #     ],
                #     width={'size':2}
                # ),
                dbc.Col(
                    children=[
                        
                        html.H2("OPTIONAL To Filters", className='text-center'),
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
                        #html.Br(),
                        # dbc.Card(
                        #     dbc.CardBody(
                        #         # children=[
                        #         #     dcc.Slider(0,root_dist_max_species,1,value=0,id='slider_to_species'),
                        #         #     dcc.Slider(0,root_dist_max_organ,1,value=0,id='slider_to_organ'),
                        #         #     dcc.Slider(0,root_dist_max_disease,1,value=0,id='slider_to_disease'),
                        #         # ]
                        #     )
                        # ),
                        #html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Filter Species")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_species',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_to['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            options=species_dropdown_options,
                                            #value='Any',
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Filter Organs")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_organ',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_to['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            options=organ_dropdown_options,
                                            #value='Any',
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("Filter Diseases")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_disease',
                                            # options=[
                                            #     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes']
                                            # ],#+[{'label': 'Any', 'value': 'Any'}],
                                            options=disease_dropdown_options,
                                            #value='Any',
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
        # dbc.Row(
        #     children=[
        #         dbc.Col(
        #             children=[
        #                 html.H2("Other options", className='text-center'),
        #                 html.Br(),
        #                 dbc.Card(
        #                     children=[
        #                         dbc.CardBody(
        #                             html.H4(
        #                                 "Node distance, count filters coming soon", className='text-center')
        #                         )
        #                     ]
        #                 )
        #             ],
        #             width={'size':4}#,
        #             #align='center'
        #         )
        #     ],
        #     justify='center'
        # ),
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
        dbc.Row(
            children=[
                dbc.Card(
                    dt.DataTable(
                        id='table',
                        # columns=[
                        #     {"name": "English Name", "id": "english_name"},
                        #     {"name": "Fold Average", "id": "fold_average"},
                        #     {"name": "Significance Welch", "id": "sig_welch"},
                        #     {"name": "Fold Median", "id": "fold_median"},
                        #     {"name": "Significance MWU", "id": "sig_mannwhit"}
                        # ],
                        columns=[{'name': 'temp', 'id': 'temp'}],
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

                        style_cell={
                            'textOverflow':'ellipsis',
                            'maxWidth':190
                        },
                        style_table={'overflowX': 'auto'},
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
)#
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
        Output(component_id="table", component_property="columns"),
        Output(component_id="table", component_property="data"),
        # Output(component_id="table_median_mw_classyfire", component_property="columns"),
        # Output(component_id="table_median_mw_classyfire", component_property="data"),
        Output(component_id="volcano_average_welch", component_property="figure"),
        Output(component_id="volcano_median_mw", component_property="figure"),
        # Output(
        #     component_id="volcano_average_welch_classyfire", component_property="figure"
        # ),
        # Output(
        #     component_id="volcano_median_mw_classyfire", component_property="figure"
        # ),
    ],
    [
        Input(component_id="button_query", component_property="n_clicks"),
        Input(component_id="table", component_property="page_current"),
        Input(component_id="table", component_property="page_size"),
        Input(component_id="table", component_property="sort_by"),
        Input(component_id="table", component_property="filter_query"),
    ],
    [
        State(component_id="dropdown_compound",component_property="value"),
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),

        # State(component_id="slider_compound",component_property="value"),
        # State(component_id="slider_from_species", component_property="value"),
        # State(component_id="slider_from_organ", component_property="value"),
        # State(component_id="slider_from_disease", component_property="value"),
        # State(component_id="slider_to_species", component_property="value"),
        # State(component_id="slider_to_organ", component_property="value"),
        # State(component_id="slider_to_disease", component_property="value"),        
    ],
)
def perform_volcano_query(
    query,
    page_current,
    page_size,
    sort_by,
    filter_query,   
    dropdown_compound_value,
    dropdown_from_species_value,
    dropdown_from_organ_value,
    dropdown_from_disease_value,
    dropdown_to_species_value,
    dropdown_to_organ_value,
    dropdown_to_disease_value,

    # slider_compound_value,
    # slider_from_species_value,
    # slider_from_organ_value,
    # slider_from_disease_value,
    # slider_to_species_value,
    # slider_to_organ_value,
    # slider_to_disease_value,
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
    root_distance_json_output = {
        "compound": dropdown_compound_value,
        "from_species": dropdown_from_species_value,
        "from_organ": dropdown_from_organ_value,
        "from_disease": dropdown_from_disease_value,
        "to_species": dropdown_to_species_value,
        "to_organ": dropdown_to_organ_value,
        "to_disease": dropdown_to_disease_value,
        "page_current":page_current,
        "page_size":page_size,
        "sort_by":sort_by,
        "filter_query":filter_query,

        # 'compound_dfr':slider_compound_value,
        # 'species_from_dfr':slider_from_species_value,
        # 'organ_from_dfr':slider_from_organ_value,
        # 'disease_from_dfr':slider_from_disease_value,
        # 'species_to_dfr':slider_to_species_value,
        # 'organ_to_dfr':slider_to_organ_value,
        # 'disease_to_dfr':slider_to_disease_value,
        
        # 'page_size':50,
        # 'page_current':0
    }

    # root_distance_json_output = {
    #     "compound":2,
    #     "from_species":562,
    #     "from_organ":"A15.145.846",
    #     "from_disease":"No",
    #     "to_species":314146,
    #     "to_organ":"A12.207.270.695",
    #     "to_disease":"No",

    #     "compound_dfr":2,
    #     "species_from_dfr": 8,
    #     "organ_from_dfr":8,
    #     "disease_from_dfr":8,
    #     "species_to_dfr": 8,
    #     "organ_to_dfr":8,
    #     "disease_to_dfr":8,
        
    #     "page_size":50,
    #     "page_current":0
    # }




    #call api
    response = requests.post(base_url + "/rootdistanceresource/", json=root_distance_json_output)
    total_panda = pd.read_json(response.json(), orient="records")
    total_panda=total_panda.drop_duplicates(subset=['species_from','organ_from','disease_from','species_to','organ_to','disease_to','compound'],ignore_index=True)
    print(total_panda)

    total_panda['from']=total_panda['species_from'].astype(str)+', '+total_panda['organ_from']+', '+total_panda['disease_from']
    total_panda['to']=total_panda['species_to'].astype(str)+', '+total_panda['organ_to']+', '+total_panda['disease_to']

    #print(total_panda.columns)
    column_list=[
        #{'name':temp_col,'id':temp_col} for temp_col in total_panda.columns
        {"name": "From Species", "id": "species_from"},
        {"name": "Root. Dist.", "id": "root_dist_species_from"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_species_from"},
        {"name": "From Organ", "id": "organ_from"},
        {"name": "Root. Dist.", "id": "root_dist_organ_from"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_organ_from"},
        {"name": "From Disease", "id": "disease_from"},
        {"name": "Root. Dist.", "id": "root_dist_disease_from"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_disease_from"},
        {"name": "To Species", "id": "species_to"},
        {"name": "Root. Dist.", "id": "root_dist_species_to"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_species_to"},
        {"name": "To Organ", "id": "organ_to"},
        {"name": "Root. Dist.", "id": "root_dist_organ_to"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_organ_to"},
        {"name": "To Disease", "id": "disease_to"},
        {"name": "Root. Dist.", "id": "root_dist_disease_to"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_disease_to"},   
        {"name": "Compound", "id": "compound"},
        {"name": "Root. Dist.", "id": "root_dist_compound"},
        {"name": "Leaf. Dist.", "id": "leaf_dist_compound"}, 
        {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        {"name": "Sig. Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
        {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        {"name": "Sig. MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
    ]

    print(total_panda.columns.to_list())
    data=total_panda[
        ['species_from', 'root_dist_species_from', 'leaf_dist_species_from', 'organ_from', 
        'root_dist_organ_from', 'leaf_dist_organ_from', 'disease_from', 'root_dist_disease_from', 
        'leaf_dist_disease_from', 'species_to', 'root_dist_species_to', 'leaf_dist_species_to', 
        'organ_to', 'root_dist_organ_to', 'leaf_dist_organ_to', 'disease_to', 'root_dist_disease_to', 
        'leaf_dist_disease_to', 'compound', 'root_dist_compound', 'leaf_dist_compound', 'fold_average', 
        'fold_median', 'sig_mannwhit', 'sig_welch']
    ].to_dict(orient="records")

    #prepare figures for volcano plots
    volcano_average = dashbio.VolcanoPlot(
        dataframe=total_panda,
        #snp="english_name",
        snp='from',
        p="sig_welch",
        effect_size="fold_average",
        gene='to',
    )
    volcano_median = dashbio.VolcanoPlot(
        dataframe=total_panda,
        #snp="english_name",
        snp='from',
        p="sig_mannwhit",
        effect_size="fold_median",
        gene='to',
    )
    #################################################3

    return (
        column_list,
        data,
        volcano_average,
        volcano_median
    )





if __name__ == "__main__":

    app.run_server(debug=True)
