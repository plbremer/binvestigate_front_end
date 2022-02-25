
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import dash_bio as dashbio

import json
import pathlib
import pandas as pd



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#load the base species network
species_json_address=DATA_PATH.joinpath('cyto_format_species.json')
temp_json_file=open(species_json_address,'r')
species_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
#species_elements_starting_from=set()
for temp_element in species_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name species
    temp_element['data']['label']=temp_element['data']['scientific_name']
    # temp_element['classes']='not_selected'
    #species_elements_starting_from.add(temp_element['data']['id'])
temp_json_file=open(species_json_address,'r')
species_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
#species_elements_starting_to=set()
for temp_element in species_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name species
    temp_element['data']['label']=temp_element['data']['scientific_name']
    # temp_element['classes']='not_selected'
    #species_elements_starting_to.add(temp_element['data']['id'])

organ_json_address=DATA_PATH.joinpath('cyto_format_organ.json')
temp_json_file=open(organ_json_address,'r')
organ_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
#organ_elements_starting_from=set()
for temp_element in organ_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name organ
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    #temp_element['classes']='not_selected'
    #print(temp_element)
    #organ_elements_starting_from.add(temp_element['data']['id'])
temp_json_file=open(organ_json_address,'r')
organ_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
#organ_elements_starting_to=set()
for temp_element in organ_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name organ
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    #temp_element['classes']='not_selected'
    #organ_elements_starting_to.add(temp_element['data']['id'])

disease_json_address=DATA_PATH.joinpath('cyto_format_disease.json')
temp_json_file=open(disease_json_address,'r')
disease_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
#disease_elements_starting_from=set()
for temp_element in disease_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name disease
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    #temp_element['classes']='not_selected'
    #print(temp_element)
    #disease_elements_starting_from.add(temp_element['data']['id'])
temp_json_file=open(disease_json_address,'r')
disease_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
#disease_elements_starting_to=set()
for temp_element in disease_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name disease
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    #temp_element['classes']='not_selected'
    #disease_elements_starting_to.add(temp_element['data']['id'])



def remove_unmapped_nodes(temp_network_dict,temp_mapped_to_dict):
    '''
    here we completely ignore the edges in the dict

    create an empty list
    go through every dict in 'nodes'
    if we map to it, then add that temp_dict the empty dict
    '''
    only_mapped_to_nodes=[
        temp_data for temp_data in temp_network_dict['elements']['nodes'] if temp_mapped_to_dict[temp_data['data']['id']]=='Yes'
    ]
    temp_network_dict['elements']['nodes']=only_mapped_to_nodes
    return temp_network_dict

def remove_redundant_options(temp_network_dict):
    '''
    because of the way the organ and disease MeSH hierarchies work, things like "plasma" can
    appear in multple places (they are fluids, blood components, etc)

    redundancies are due to the same mesh label not id

    this function removes things that appear more than once

    so the individual nodes that appear are someone "random". we just keep the first unique of each label
    '''
    only_appeared_once_mesh_label=list()
    mesh_labels_added=set()
    for temp_data in temp_network_dict['elements']['nodes']:
        if temp_data['data']['mesh_label'] not in mesh_labels_added:
            mesh_labels_added.add(temp_data['data']['mesh_label'])
            only_appeared_once_mesh_label.append(temp_data)
    temp_network_dict['elements']['nodes']=only_appeared_once_mesh_label
    return temp_network_dict
    







if temp_app_name=="basic_query":
    table_species_address=DATA_PATH.joinpath('table_species_dash.bin')
    table_organ_address=DATA_PATH.joinpath('table_organ_dash.bin')
    table_disease_address=DATA_PATH.joinpath('table_disease_dash.bin')

    species_map_panda=pd.read_pickle(table_species_address)
    species_map_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(species_map_panda.node_id.to_list(),species_map_panda.we_map_to.to_list()))}
    organ_map_panda=pd.read_pickle(table_organ_address)
    organ_map_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(organ_map_panda.node_id.to_list(),organ_map_panda.we_map_to.to_list()))}
    disease_map_panda=pd.read_pickle(table_disease_address)
    disease_map_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(disease_map_panda.node_id.to_list(),disease_map_panda.we_map_to.to_list()))}

    species_network_dict_from=remove_unmapped_nodes(species_network_dict_from,species_map_dict)
    organ_network_dict_from=remove_unmapped_nodes(organ_network_dict_from,organ_map_dict)
    organ_network_dict_from=remove_redundant_options(organ_network_dict_from)
    disease_network_dict_from=remove_unmapped_nodes(disease_network_dict_from,disease_map_dict)
    disease_network_dict_from=remove_redundant_options(disease_network_dict_from)

    species_network_dict_to=remove_unmapped_nodes(species_network_dict_to,species_map_dict)
    organ_network_dict_to=remove_unmapped_nodes(organ_network_dict_to,organ_map_dict)
    organ_network_dict_to=remove_redundant_options(organ_network_dict_to)
    disease_network_dict_to=remove_unmapped_nodes(disease_network_dict_to,disease_map_dict)
    disease_network_dict_to=remove_redundant_options(disease_network_dict_to)

temp_layout=html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Blah", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Blah", className='text-center')
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
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Blah", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(html.H4("Blah")),
                                    dbc.Card(
                                        html.Button(
                                            'Reset selections',
                                            id='button_from_species',
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_species',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_organ',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                # children=[                    
                                #     dbc.Card(html.H4("Use these checkboxes to select multiple species at once. Selecting multiple species will compare each individually. Choosing their parent will aggregate them.")),
                                #     dbc.Card(
                                #         dcc.Checklist(
                                #             id='checklist_from_species',
                                #             options=[
                                #                 {'label': i, 'value': i} for i in checklist_hashmap_species_from.keys()
                                #             ],
                                #             labelStyle={'display':'block'}
                                #         )
                                #     ),

                                # ]
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
                        html.H2('blah', className='text-center')
                    ],
                    width={'size':2}
                ),
                dbc.Col(
                    children=[
                        
                        html.H2("Blah", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(html.H4("Blah")),
                                    dbc.Card(
                                        html.Button(
                                            'Reset selections',
                                            id='button_to_species2',
                                        )
                                    ),


                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_species',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_organ',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                    dbc.Card(html.H4("blah")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes']
                                            ],
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#212121',
                                            }
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                # children=[                    
                                #     dbc.Card(html.H4("Use these checkboxes to select multiple species at once. Selecting multiple species will compare each individually. Choosing their parent will aggregate them.")),
                                #     dbc.Card(
                                #         dcc.Checklist(
                                #             id='checklist_to_species',
                                #             options=[
                                #                 {'label': i, 'value': i} for i in checklist_hashmap_species_to.keys()
                                #             ],
                                #             labelStyle={'display':'block'}
                                #         )
                                #     ),
                                # ]
                            )
                        ),
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
                        html.H2("Other options", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Blah", className='text-center')
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
                        html.H2("Execute query", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4("Blah", className='text-center')
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
                        html.H2("Results", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(
                                        html.H4(
                                            "Query Summary", className='text-center')
                                    ),
                                    dbc.Card(
                                        dt.DataTable(
                                            id='table_query_summary',
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
                        )
                    ]
                )
            ]
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
                                            "Blah", className='text-center')
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_average_welch_bins',
                                        )
                                    ),
                                    dbc.Card(
                                        dt.DataTable(
                                            id='table_average_welch_bins',
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
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_average_welch_classyfire',
                                        )
                                    ),
                                    dbc.Card(
                                        dt.DataTable(
                                            id='table_average_welch_classyfire',
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
                                            "Blah", className='text-center')
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_median_mw_bins',
                                        )
                                    ),
                                    dbc.Card(
                                        dt.DataTable(
                                            id='table_median_mw_bins',
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
                                    ),
                                    dbc.Card(
                                        dcc.Graph(
                                            id='volcano_median_mw_classyfire',
                                        )
                                    ),
                                    dbc.Card(
                                        dt.DataTable(
                                            id='table_median_mw_classyfire',
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
                        )
                    ],
                    width={'size':4}
                )
            ]
        )
    ]
)


if __name__ == "__main__":
    pass