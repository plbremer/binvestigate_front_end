import pathlib

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import json
from dash import html
from dash import callback_context
import pandas
import networkx as nx
import itertools
from pprint import pprint

from app import app

cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#load the base organ network
organ_json_address=DATA_PATH.joinpath('cyto_format_organ.json')
temp_json_file=open(organ_json_address,'r')
organ_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
organ_elements_starting_from=set()
for temp_element in organ_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name organ
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'
    #print(temp_element)
    organ_elements_starting_from.add(temp_element['data']['id'])

#organ_elements_starting=list()

#load the base organ network
organ_json_address=DATA_PATH.joinpath('cyto_format_organ.json')
temp_json_file=open(organ_json_address,'r')
organ_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
organ_elements_starting_to=set()
for temp_element in organ_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name organ
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'
    organ_elements_starting_to.add(temp_element['data']['id'])


#defines the map between the various boxes and the node ids
checklist_hashmap_organ_from={
    'some random plants': ['4081','29760','3760','3656','4081','3694'],
    'some random bacteria':['45133','33196','3705','5007','5476','9397','3052','47906','3055','3081','3075','3076','554065','3077','3041','535','1485','1502','13442','5207','3046','3038','853'],
    'monkeyish things':['9606','9544','9598','9557']
}
checklist_hashmap_organ_to={
    'some random plants': ['4081','29760','3760','3656','4081','3694'],
    'some random bacteria':['45133','33196','3705','5007','5476','9397','3052','47906','3055','3081','3075','3076','554065','3077','3041','535','1485','1502','13442','5207','3046','3038','853'],
    'monkeyish things':['9606','9544','9598','9557']
}



basic_stylesheet=[
    {
        'selector':'node',
        'style':{
            'content':'data(label)',
            'text-wrap':'wrap',
            'text-max-width':100,
            'font-size':13
        }
    },
    {
        'selector':'.selected',
        'style':{
            'background-color':'red'
        }
    },
    {
        'selector':'.not_selected',
        'style':{
            'background-color':'grey'
        }
    }
]



layout=html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.Br()
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H5('Pre-selected common groups of individuals')
                            ],
                            width={'size':4,'offset':0},
                            #align='center'
                        ),
                        dbc.Col(
                            children=[
                                html.H5('Pre-selected common groups of individuals')
                            ],
                            width={'size':4,'offset':8},
                            #align='center'
                        )
                    ],
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Checklist(
                                    id='checklist_from_organ',
                                    options=[
                                        {'label': i, 'value': i} for i in checklist_hashmap_organ_from.keys()
                                    ]
                                )
                            ],
                            width={'size':4,'offset':0},
                            align='center'
                        ),
                        dbc.Col(
                            children=[
                                dcc.Checklist(
                                    id='checklist_to_organ',
                                    options=[
                                        {'label': i, 'value': i} for i in checklist_hashmap_organ_from.keys()
                                    ]
                                )
                            ],
                            width={'size':4,'offset':8},
                            align='center'
                        )
                    ],

                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H5('Typable Dropdown with all selections')
                            ],
                            width={'size':4,'offset':0},
                            align='center'
                        ),
                        dbc.Col(
                            children=[
                                html.H5('Typable Dropdown with all selections')
                            ],
                            width={'size':4,'offset':8},
                            align='center'
                        )
                    ],
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    id='dropdown_from_organ',
                                    options=[
                                        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes']
                                    ],
                                    multi=True
                                )
                            ],
                            width={'size':4,'offset':0},
                        ),
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    id='dropdown_to_organ',
                                    options=[
                                        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes']
                                    ],
                                    multi=True
                                )
                            ],
                            width={'size':4,'offset':8},
                        )
                    ]
                )
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.Button(
                                    'Reset selections',
                                    id='button_from_organ',
                                )
                            ],
                            width={'size':4,'offset':0},
                        ),
                        dbc.Col(
                            children=[
                                html.Button(
                                    'Reset selections',
                                    id='button_to_organ',
                                )
                            ],
                            width={'size':4,'offset':8},
                        )
                    ]
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H5('Visualization of Selections. Zoomable and clickable.')
                            ],
                            width={'size':4,'offset':0},
                            align='center'
                        ),
                        dbc.Col(
                            children=[
                                html.H5('Visualization of Selections. Zoomable and clickable.')
                            ],
                            width={'size':4,'offset':8},
                            align='center'
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Card(
                            cyto.Cytoscape(
                                id='cytoscape_from_organ',
                                layout={'name':'klay','fit':False},
                                elements=organ_network_dict_from['elements'],
                                minZoom=0.15,
                                maxZoom=5,
                                stylesheet=basic_stylesheet,
                                style={'width': '700px','height':'1000px'}
                            )
                        )
                    ),
                    dbc.Col(
                        html.H1('VS'),
                        width={'size':2,'offset':0}
                    ),
                    dbc.Col(
                        cyto.Cytoscape(
                            id='cytoscape_to_organ',
                            layout={'name':'klay','fit':False},
                            elements=organ_network_dict_to['elements'],
                            minZoom=0.15,
                            maxZoom=5,
                            stylesheet=basic_stylesheet,
                            style={'width': '700px','height':'1000px'}
                        )
                    ),
                ]
            )
        ),
    ]
)



networkx_address_organ=DATA_PATH.joinpath('organ_networkx.bin')
networkx_organ=nx.readwrite.gpickle.read_gpickle(networkx_address_organ)
networkx_address_species=DATA_PATH.joinpath('species_networkx.bin')
networkx_species=nx.readwrite.gpickle.read_gpickle(networkx_address_species)
networkx_address_disease=DATA_PATH.joinpath('disease_networkx.bin')
networkx_disease=nx.readwrite.gpickle.read_gpickle(networkx_address_disease)

table_species_address=DATA_PATH.joinpath('table_species_dash.bin')
species_map_panda=pandas.read_pickle(table_species_address)
species_map_to_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(species_map_panda.node_id.to_list(),species_map_panda.we_map_to.to_list()))}
table_disease_address=DATA_PATH.joinpath('table_disease_dash.bin')
disease_map_panda=pandas.read_pickle(table_disease_address)
disease_map_to_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(disease_map_panda.node_id.to_list(),disease_map_panda.we_map_to.to_list()))}

index_panda_address=DATA_PATH.joinpath('index_panda.bin')
index_panda=pandas.read_pickle(index_panda_address)

def compile_set_of_valid_selections(temp_store_species,temp_store_disease):

    if temp_store_species is not None:
        #for each store, we get a list of mapped-to descendants
        total_descendant_set_species=set()
        for temp_element in temp_store_species['species']:
            total_descendant_set_species=total_descendant_set_species.union(nx.algorithms.dag.descendants(networkx_species,temp_element))
            total_descendant_set_species.add(temp_element)
        descendants_that_we_map_to_species=set()
        for temp_element in total_descendant_set_species:
            if species_map_to_dict[temp_element]=='Yes':
                descendants_that_we_map_to_species.add(temp_element)
    
    if temp_store_disease is not None:
        #do the same thing for disease
        total_descendant_set_disease=set()
        for temp_element in temp_store_disease['disease']:
            total_descendant_set_disease=total_descendant_set_disease.union(nx.algorithms.dag.descendants(networkx_disease,temp_element))
            total_descendant_set_disease.add(temp_element)
        descendants_that_we_map_to_disease=set()
        for temp_element in total_descendant_set_disease:
            if disease_map_to_dict[temp_element]=='Yes':
                descendants_that_we_map_to_disease.add(temp_element)

    if ( ((temp_store_disease is None) or (len(temp_store_disease['disease'])==0)) and ((temp_store_species is None) or (len(temp_store_species['species'])==0)) ):
        return [temp_element for temp_element in networkx_organ.nodes]

    elif (temp_store_disease is None) and (temp_store_species is not None):
        valid_base_organ_choices=list(set(index_panda.loc[index_panda.species.isin(descendants_that_we_map_to_species)].organ.to_list()))

    elif (temp_store_disease is not None) and (temp_store_species is None):
        valid_base_organ_choices=list(set(index_panda.loc[index_panda.disease.isin(descendants_that_we_map_to_disease)].organ.to_list()))
    elif (temp_store_disease is not None) and (temp_store_species is not None):
        #filter the index panda to get a list of organ that are valid choices
        valid_base_organ_choices=list(set(index_panda.loc[index_panda.species.isin(descendants_that_we_map_to_species) & index_panda.disease.isin(descendants_that_we_map_to_disease)].organ.to_list()))
    a=[i for i in valid_base_organ_choices if (pandas.isna(i)==False)]
    valid_base_organ_choices=a


    #create the list of nodes that are valid selections from the mapped-to-organ
    #step 1 find the lowest common ancestor
    #step 2 find all nodes along each path from every mapped-to-organ to LCA
    #step 3 return this. this result is used for the update on the cyto, dropdown, and checkboxes
    #step 1
    temp_lca=''
    if len(valid_base_organ_choices)==1:
        return set(valid_base_organ_choices)
    else:
        #the basic idea is that we test the first two nodes, get a lca, then test the current lca against each other node. it either goes up or stays
        print(valid_base_organ_choices)
        for i,temp_element in enumerate(valid_base_organ_choices):
            print(temp_element)
            if i==0:
                temp_tuple_tuple=((valid_base_organ_choices[0],valid_base_organ_choices[1],),)
                temp_lca=next(nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(G=networkx_organ,pairs=temp_tuple_tuple))[1]
            else:
                temp_tuple_tuple=((temp_lca,temp_element,),)
                temp_lca=next(nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(G=networkx_organ,pairs=temp_tuple_tuple))[1]
    #step 2
    nodes_for_subgraph_set=set()
    for temp_element in valid_base_organ_choices:
        nodes_to_lca=nx.algorithms.shortest_paths.unweighted.bidirectional_shortest_path(G=networkx_organ,source=temp_lca,target=temp_element)
        nodes_for_subgraph_set=nodes_for_subgraph_set.union(set(nodes_to_lca))

    return nodes_for_subgraph_set
    
def delete_node_reconnect_cyto_elements(temp_elements,temp_tapnode):
    #scroll through nodes and delete the element where [data][id] is the tempnode[id]
    #scroll through the edges
    #there are some number of edges where the element in question is a source
    #some number of edges where the element in question is a target
    #both need to be deleted
    #make an edge between each source and each target instance

    targets_when_node_is_source=list()
    sources_when_node_is_target=list()
    indices_to_keep=list()
    for i,temp_edge in enumerate(temp_elements['edges']):
        if temp_edge['data']['source']==temp_tapnode:
            targets_when_node_is_source.append(temp_edge['data']['target'])
        elif temp_edge['data']['target']==temp_tapnode:
            sources_when_node_is_target.append(temp_edge['data']['source'])
        else:
            indices_to_keep.append(i)
    
    new_edges=list()

    for i in range(len(targets_when_node_is_source)):
        for j in range(len(sources_when_node_is_target)):
            new_edges.append(
                {
                    'data':{
                        'key':0,
                        'source':sources_when_node_is_target[j],
                        'target':targets_when_node_is_source[i]
                    }
                }
            )

    updated_edges=list()
    for i in indices_to_keep:
        updated_edges.append(temp_elements['edges'][i])
    updated_edges=updated_edges+new_edges
    temp_elements['edges']=updated_edges

    #find the node and remove it
    temp_node_index=0
    for i, temp_node in enumerate(temp_elements['nodes']):
        if temp_node['data']['id']==temp_tapnode:
            temp_node_index=i
            break

    temp_elements['nodes'].pop(temp_node_index)

    return temp_elements


@app.callback(
    [Output(component_id='cytoscape_from_organ',component_property='elements'),
    Output(component_id='checklist_from_organ',component_property='value'),
    Output(component_id='dropdown_from_organ',component_property='value'),
    Output(component_id='store_from_organ',component_property='data'),
    
    Output(component_id='dropdown_from_organ',component_property='options'),
    Output(component_id='checklist_from_organ',component_property='options'),

    Output(component_id='cytoscape_from_organ',component_property='zoom'),
    Output(component_id='cytoscape_from_organ',component_property='pan')
    ],
    
    [Input(component_id='cytoscape_from_organ',component_property='tapNodeData'),
    Input(component_id='checklist_from_organ',component_property='value'),
    Input(component_id='dropdown_from_organ',component_property='value'),
    Input(component_id='button_from_organ',component_property='n_clicks')],
    
    [State(component_id='cytoscape_from_organ',component_property='elements'),
   
    State(component_id='store_from_organ',component_property='data'),
    State(component_id='store_from_species',component_property='data'),
    State(component_id='store_from_disease',component_property='data'),

    State(component_id='dropdown_from_organ',component_property='options'),
    State(component_id='checklist_from_organ',component_property='options'),
    State(component_id='cytoscape_from_organ',component_property='zoom'),
    State(component_id='cytoscape_from_organ',component_property='pan')
    ]
)
def callback_aggregate_from(
    cytoscape_from_organ_tapnodedata,
    checklist_from_organ_value,
    dropdown_from_organ_value,
    button_from_organ_value,

    cytoscape_from_organ_elements,

    store_from_organ_data,
    store_from_species_data,
    store_from_disease_data,

    dropdown_from_organ_options,
    checklist_from_organ_options,

    cytoscape_from_organ_zoom,
    cytoscape_from_organ_pan

):
    if (len(callback_context.triggered)>1) and (store_from_organ_data is None):
        store_from_organ_data={
            'organ':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_from_organ_value=list()

        ###modifying the layout based on species/disease
        valid_organ_selections=compile_set_of_valid_selections(store_from_species_data,store_from_disease_data)
        dropdown_from_organ_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes'] if (temp_node['data']['id'] in valid_organ_selections)
        ]
        checklist_from_organ_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_organ_from.keys() if (set(checklist_hashmap_organ_from[i]).issubset(valid_organ_selections))
        ]
        temp_nodes_to_remove_organ=organ_elements_starting_from.difference(valid_organ_selections)
        for temp_node in temp_nodes_to_remove_organ:
            cytoscape_from_organ_elements=delete_node_reconnect_cyto_elements(cytoscape_from_organ_elements,temp_node)
        cytoscape_from_organ_zoom=5/len(valid_organ_selections)
        cytoscape_from_organ_pan={'x':600,'y':1}
        
        return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

    elif (len(callback_context.triggered)>1) and (store_from_organ_data is not None):
        
        ###modifying the layout based on species/disease
        valid_organ_selections=compile_set_of_valid_selections(store_from_species_data,store_from_disease_data)
        dropdown_from_organ_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_from['elements']['nodes'] if (temp_node['data']['id'] in valid_organ_selections)
        ]
        checklist_from_organ_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_organ_from.keys() if (set(checklist_hashmap_organ_from[i]).issubset(valid_organ_selections))
        ]
        temp_nodes_to_remove_organ=organ_elements_starting_from.difference(valid_organ_selections)
        for temp_node in temp_nodes_to_remove_organ:
            cytoscape_from_organ_elements=delete_node_reconnect_cyto_elements(cytoscape_from_organ_elements,temp_node)
        cytoscape_from_organ_zoom=5/len(valid_organ_selections)
        cytoscape_from_organ_pan={'x':600,'y':1}

        for temp_node in cytoscape_from_organ_elements['nodes']:
            if temp_node['data']['id'] in store_from_organ_data['organ']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
        dropdown_from_organ_value=store_from_organ_data['organ']
        checklist_from_organ_value=store_from_organ_data['checkboxes']
        #dont do anthing to store_from_organ_data
        return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_from_organ.tapNodeData'):
        this_click=set()
        this_click.add(cytoscape_from_organ_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_from_organ_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store organ
        new_organ_list=list()
        for temp_node in cytoscape_from_organ_elements['nodes']:
            if temp_node['classes']=='selected':
                new_organ_list.append(temp_node['data']['id'])        
        store_from_organ_data['organ']=new_organ_list

        #dropdown
        dropdown_from_organ_value=store_from_organ_data['organ']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_organ_from.keys():
            #if every node id is in the store
            if all([(i in store_from_organ_data['organ']) for i in checklist_hashmap_organ_from[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_from_organ_value=new_checkbox_values

        #store checkboxes        
        store_from_organ_data['checkboxes']=checklist_from_organ_value

        return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_from_organ.value'):

        if (len(store_from_organ_data['checkboxes']) < len(checklist_from_organ_value)):

            box_we_clicked=list(set(checklist_from_organ_value).difference(set(store_from_organ_data['checkboxes'])))[0]
            #elements
            for temp_node in cytoscape_from_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ_from[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_organ_data['checkboxes'].append(box_we_clicked)
            store_from_organ_data['organ']=list(set(store_from_organ_data['organ']).union(set(checklist_hashmap_organ_from[box_we_clicked])))

            #dropdown
            dropdown_from_organ_value=store_from_organ_data['organ']
            
            return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan
           
        elif len(store_from_organ_data['checkboxes']) > len(checklist_from_organ_value):

            box_we_unclicked=list(set(store_from_organ_data['checkboxes']).difference(set(checklist_from_organ_value)))[0]

            #elements
            for temp_node in cytoscape_from_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ_from[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_organ_data['checkboxes'].remove(box_we_unclicked)
            store_from_organ_data['organ']=list(set(store_from_organ_data['organ']).difference(set(checklist_hashmap_organ_from[box_we_unclicked])))

            #dropdown
            dropdown_from_organ_value=store_from_organ_data['organ']

            return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_from_organ.value'):

        if len(store_from_organ_data['organ']) < len(dropdown_from_organ_value):

            organ_we_added=list(set(dropdown_from_organ_value).difference(set(store_from_organ_data['organ'])))[0]

            #elements
            for temp_node in cytoscape_from_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_organ_data['organ'].append(organ_we_added)

            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ_from.keys() if (organ_we_added in checklist_hashmap_organ_from[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #if the set of organ implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of organ is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_organ_from[temp_checkbox]).difference(set(dropdown_from_organ_value)))==0:
                    store_from_organ_data['checkboxes'].append(temp_checkbox)
                    checklist_from_organ_value.append(temp_checkbox)

            return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

        elif len(store_from_organ_data['organ']) > len(dropdown_from_organ_value):

            organ_we_lost=list(set(store_from_organ_data['organ']).difference(set(dropdown_from_organ_value)))[0]

            #elements
            for temp_node in cytoscape_from_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_organ_data['organ'].remove(organ_we_lost)

            #checklist
            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ_from.keys() if (organ_we_lost in checklist_hashmap_organ_from[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_organ_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_from_organ_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_from_organ.n_clicks'):

        store_from_organ_data={
            'organ':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_from_organ_elements['nodes']:
            temp_node['classes']='not_selected'  
        checklist_from_organ_value=list()
        dropdown_from_organ_value=None

        return cytoscape_from_organ_elements, checklist_from_organ_value, dropdown_from_organ_value,store_from_organ_data, dropdown_from_organ_options,checklist_from_organ_options,cytoscape_from_organ_zoom,cytoscape_from_organ_pan

@app.callback(
    [Output(component_id='cytoscape_to_organ',component_property='elements'),
    Output(component_id='checklist_to_organ',component_property='value'),
    Output(component_id='dropdown_to_organ',component_property='value'),
    Output(component_id='store_to_organ',component_property='data'),
    
    Output(component_id='dropdown_to_organ',component_property='options'),
    Output(component_id='checklist_to_organ',component_property='options'),

    Output(component_id='cytoscape_to_organ',component_property='zoom'),
    Output(component_id='cytoscape_to_organ',component_property='pan')
    ],
    
    [Input(component_id='cytoscape_to_organ',component_property='tapNodeData'),
    Input(component_id='checklist_to_organ',component_property='value'),
    Input(component_id='dropdown_to_organ',component_property='value'),
    Input(component_id='button_to_organ',component_property='n_clicks')],
    
    [State(component_id='cytoscape_to_organ',component_property='elements'),
   
    State(component_id='store_to_organ',component_property='data'),
    State(component_id='store_to_species',component_property='data'),
    State(component_id='store_to_disease',component_property='data'),

    State(component_id='dropdown_to_organ',component_property='options'),
    State(component_id='checklist_to_organ',component_property='options'),
    State(component_id='cytoscape_to_organ',component_property='zoom'),
    State(component_id='cytoscape_to_organ',component_property='pan')
    ]
)
def callback_aggregate_to(
    cytoscape_to_organ_tapnodedata,
    checklist_to_organ_value,
    dropdown_to_organ_value,
    button_to_organ_value,

    cytoscape_to_organ_elements,

    store_to_organ_data,
    store_to_species_data,
    store_to_disease_data,

    dropdown_to_organ_options,
    checklist_to_organ_options,

    cytoscape_to_organ_zoom,
    cytoscape_to_organ_pan

):
    if (len(callback_context.triggered)>1) and (store_to_organ_data is None):
        store_to_organ_data={
            'organ':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_to_organ_value=list()

        ###modifying the layout based on species/disease
        valid_organ_selections=compile_set_of_valid_selections(store_to_species_data,store_to_disease_data)
        dropdown_to_organ_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_to['elements']['nodes'] if (temp_node['data']['id'] in valid_organ_selections)
        ]
        checklist_to_organ_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_organ_to.keys() if (set(checklist_hashmap_organ_to[i]).issubset(valid_organ_selections))
        ]
        temp_nodes_to_remove_organ=organ_elements_starting_to.difference(valid_organ_selections)
        for temp_node in temp_nodes_to_remove_organ:
            cytoscape_to_organ_elements=delete_node_reconnect_cyto_elements(cytoscape_to_organ_elements,temp_node)
        cytoscape_to_organ_zoom=5/len(valid_organ_selections)
        cytoscape_to_organ_pan={'x':600,'y':1}
        
        return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

    elif (len(callback_context.triggered)>1) and (store_to_organ_data is not None):
        
        ###modifying the layout based on species/disease
        valid_organ_selections=compile_set_of_valid_selections(store_to_species_data,store_to_disease_data)
        dropdown_to_organ_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict_to['elements']['nodes'] if (temp_node['data']['id'] in valid_organ_selections)
        ]
        checklist_to_organ_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_organ_to.keys() if (set(checklist_hashmap_organ_to[i]).issubset(valid_organ_selections))
        ]
        temp_nodes_to_remove_organ=organ_elements_starting_to.difference(valid_organ_selections)
        for temp_node in temp_nodes_to_remove_organ:
            cytoscape_to_organ_elements=delete_node_reconnect_cyto_elements(cytoscape_to_organ_elements,temp_node)
        cytoscape_to_organ_zoom=5/len(valid_organ_selections)
        cytoscape_to_organ_pan={'x':600,'y':1}

        for temp_node in cytoscape_to_organ_elements['nodes']:
            if temp_node['data']['id'] in store_to_organ_data['organ']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
        dropdown_to_organ_value=store_to_organ_data['organ']
        checklist_to_organ_value=store_to_organ_data['checkboxes']
        #dont do anthing to store_to_organ_data
        return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_to_organ.tapNodeData'):
        this_click=set()
        this_click.add(cytoscape_to_organ_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_to_organ_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store organ
        new_organ_list=list()
        for temp_node in cytoscape_to_organ_elements['nodes']:
            if temp_node['classes']=='selected':
                new_organ_list.append(temp_node['data']['id'])        
        store_to_organ_data['organ']=new_organ_list

        #dropdown
        dropdown_to_organ_value=store_to_organ_data['organ']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_organ_to.keys():
            #if every node id is in the store
            if all([(i in store_to_organ_data['organ']) for i in checklist_hashmap_organ_to[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_to_organ_value=new_checkbox_values

        #store checkboxes        
        store_to_organ_data['checkboxes']=checklist_to_organ_value

        return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_to_organ.value'):

        if (len(store_to_organ_data['checkboxes']) < len(checklist_to_organ_value)):

            box_we_clicked=list(set(checklist_to_organ_value).difference(set(store_to_organ_data['checkboxes'])))[0]
            #elements
            for temp_node in cytoscape_to_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ_to[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_to_organ_data['checkboxes'].append(box_we_clicked)
            store_to_organ_data['organ']=list(set(store_to_organ_data['organ']).union(set(checklist_hashmap_organ_to[box_we_clicked])))

            #dropdown
            dropdown_to_organ_value=store_to_organ_data['organ']
            
            return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan
           
        elif len(store_to_organ_data['checkboxes']) > len(checklist_to_organ_value):

            box_we_unclicked=list(set(store_to_organ_data['checkboxes']).difference(set(checklist_to_organ_value)))[0]

            #elements
            for temp_node in cytoscape_to_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ_to[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_to_organ_data['checkboxes'].remove(box_we_unclicked)
            store_to_organ_data['organ']=list(set(store_to_organ_data['organ']).difference(set(checklist_hashmap_organ_to[box_we_unclicked])))

            #dropdown
            dropdown_to_organ_value=store_to_organ_data['organ']

            return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_to_organ.value'):

        if len(store_to_organ_data['organ']) < len(dropdown_to_organ_value):

            organ_we_added=list(set(dropdown_to_organ_value).difference(set(store_to_organ_data['organ'])))[0]

            #elements
            for temp_node in cytoscape_to_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_to_organ_data['organ'].append(organ_we_added)

            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ_to.keys() if (organ_we_added in checklist_hashmap_organ_to[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #if the set of organ implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of organ is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_organ_to[temp_checkbox]).difference(set(dropdown_to_organ_value)))==0:
                    store_to_organ_data['checkboxes'].append(temp_checkbox)
                    checklist_to_organ_value.append(temp_checkbox)

            return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

        elif len(store_to_organ_data['organ']) > len(dropdown_to_organ_value):

            organ_we_lost=list(set(store_to_organ_data['organ']).difference(set(dropdown_to_organ_value)))[0]

            #elements
            for temp_node in cytoscape_to_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_to_organ_data['organ'].remove(organ_we_lost)

            #checklist
            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ_to.keys() if (organ_we_lost in checklist_hashmap_organ_to[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_to_organ_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_to_organ_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_to_organ.n_clicks'):

        store_to_organ_data={
            'organ':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_to_organ_elements['nodes']:
            temp_node['classes']='not_selected'  
        checklist_to_organ_value=list()
        dropdown_to_organ_value=None

        return cytoscape_to_organ_elements, checklist_to_organ_value, dropdown_to_organ_value,store_to_organ_data, dropdown_to_organ_options,checklist_to_organ_options,cytoscape_to_organ_zoom,cytoscape_to_organ_pan
