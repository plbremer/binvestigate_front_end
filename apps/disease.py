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

#load the base disease network
disease_json_address=DATA_PATH.joinpath('cyto_format_disease.json')
temp_json_file=open(disease_json_address,'r')
disease_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
disease_elements_starting_from=set()
for temp_element in disease_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name disease
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'
    #print(temp_element)
    disease_elements_starting_from.add(temp_element['data']['id'])

#disease_elements_starting=list()

#load the base disease network
disease_json_address=DATA_PATH.joinpath('cyto_format_disease.json')
temp_json_file=open(disease_json_address,'r')
disease_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
disease_elements_starting_to=set()
for temp_element in disease_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name disease
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'
    disease_elements_starting_to.add(temp_element['data']['id'])


#defines the map between the various boxes and the node ids
checklist_hashmap_disease_from={
    'Neoplasms': ['C04']
}
checklist_hashmap_disease_to={
    'Neoplasms': ['C04']
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
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Diseases", className='text-center'),
                        html.Br(),
                        dbc.Card(

                            children=[
                                dbc.CardBody(
                                    html.H4(
                                        "Select disease that you want to compare. For both *from* and *to*, the four selection options \
                                        update each other when one is updated. Moreover, selecting a disease on this page will filter invalid disease and Disease disease on their respective pages.", className='text-center')
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
                        html.H2("Diseases selected here", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(html.H4("Use this button to reset selection to nothing")),
                                    dbc.Card(
                                        html.Button(
                                            'Reset selections',
                                            id='button_from_disease',
                                        )
                                    ),

                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Use this dropdown to quickly choose (groups of) disease. You can type into it.")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_from_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes']
                                            ],
                                            multi=True,
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
                                children=[                    
                                    dbc.Card(html.H4("Use these checkboxes to select multiple disease at once. Selecting multiple disease will compare each individually. Choosing their parent will aggregate them.")),
                                    dbc.Card(
                                        dcc.Checklist(
                                            id='checklist_from_disease',
                                            options=[
                                                {'label': i, 'value': i} for i in checklist_hashmap_disease_from.keys()
                                            ],
                                            labelStyle={'display':'block'}
                                        )
                                    ),

                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Use this graph to visualize the selected (groups of) disease. Selections can be made by zooming/clicking nodes.")),
                                    dbc.Card(
                                        cyto.Cytoscape(
                                            id='cytoscape_from_disease',
                                            layout={'name':'klay'},#,'fit':True},
                                            elements=disease_network_dict_from['elements'],
                                            minZoom=0.15,
                                            maxZoom=3,
                                            #responsive=True,
                                            stylesheet=basic_stylesheet,
                                            style={'width':'100%','height':'1000px'}
                                            #style={'width': '200px','height':'1000px'}
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
                        #dbc.Card(
                        #    html.H4("lorem ipsum")
                        #)
                        html.H2('get compared to', className='text-center')
                    ],
                    width={'size':2}
                ),
                dbc.Col(
                    children=[
                        
                        html.H2("Diseases selected here", className='text-center'),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Card(html.H4("Use this button to reset selection to nothing")),
                                    dbc.Card(
                                        html.Button(
                                            'Reset selections',
                                            id='button_to_disease',
                                        )
                                    ),
                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Use this dropdown to quickly choose (groups of) disease. You can type into it.")),
                                    dbc.Card(
                                        dcc.Dropdown(
                                            id='dropdown_to_disease',
                                            options=[
                                                {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes']
                                            ],
                                            multi=True,
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
                                children=[                    
                                    dbc.Card(html.H4("Use these checkboxes to select multiple disease at once. Selecting multiple disease will compare each individually. Choosing their parent will aggregate them.")),
                                    dbc.Card(
                                        dcc.Checklist(
                                            id='checklist_to_disease',
                                            options=[
                                                {'label': i, 'value': i} for i in checklist_hashmap_disease_to.keys()
                                            ],
                                            labelStyle={'display':'block'}
                                        )
                                    ),

                                ]
                            )
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.CardBody(
                                children=[                    
                                    dbc.Card(html.H4("Use this graph to visualize the selected (groups of) disease. Selections can be made by zooming/clicking nodes.")),
                                    dbc.Card(
                                        cyto.Cytoscape(
                                            id='cytoscape_to_disease',
                                            layout={'name':'klay'},#,'fit':True},
                                            elements=disease_network_dict_to['elements'],
                                            minZoom=0.15,
                                            maxZoom=3,
                                            #responsive=True,
                                            stylesheet=basic_stylesheet,
                                            style={'width':'100%','height':'1000px'}
                                            #style={'width': '200px','height':'1000px'}
                                        )
                                    )
                                ]
                            )
                        )
                    ],
                    width={'size':4}
                ),
            ],
            justify='around'
        )
    ]
)



networkx_address_disease=DATA_PATH.joinpath('disease_networkx.bin')
networkx_disease=nx.readwrite.gpickle.read_gpickle(networkx_address_disease)
networkx_address_organ=DATA_PATH.joinpath('organ_networkx.bin')
networkx_organ=nx.readwrite.gpickle.read_gpickle(networkx_address_organ)
networkx_address_species=DATA_PATH.joinpath('species_networkx.bin')
networkx_species=nx.readwrite.gpickle.read_gpickle(networkx_address_species)

table_organ_address=DATA_PATH.joinpath('table_organ_dash.bin')
organ_map_panda=pandas.read_pickle(table_organ_address)
organ_map_to_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(organ_map_panda.node_id.to_list(),organ_map_panda.we_map_to.to_list()))}
table_species_address=DATA_PATH.joinpath('table_species_dash.bin')
species_map_panda=pandas.read_pickle(table_species_address)
species_map_to_dict={temp_tup[0]:temp_tup[1] for temp_tup in list(zip(species_map_panda.node_id.to_list(),species_map_panda.we_map_to.to_list()))}

index_panda_address=DATA_PATH.joinpath('index_panda.bin')
index_panda=pandas.read_pickle(index_panda_address)


def compile_set_of_valid_selections(temp_store_organ,temp_store_species):

    if temp_store_organ is not None:
        
        #if the store exists but is empty, then we need to make everything a valid choice
        if len(temp_store_organ['organ'])==0:
            total_descendant_set_organ=set()
            total_descendant_set_organ=total_descendant_set_organ.union(nx.algorithms.dag.descendants(networkx_organ,'organ'))
            total_descendant_set_organ.add('organ')
            descendants_that_we_map_to_organ=set()
            for temp_element in total_descendant_set_organ:
                if organ_map_to_dict[temp_element]=='Yes':
                    descendants_that_we_map_to_organ.add(temp_element)        

        #for each store, we get a list of mapped-to descendants
        total_descendant_set_organ=set()
        for temp_element in temp_store_organ['organ']:
            total_descendant_set_organ=total_descendant_set_organ.union(nx.algorithms.dag.descendants(networkx_organ,temp_element))
            total_descendant_set_organ.add(temp_element)
        descendants_that_we_map_to_organ=set()
        for temp_element in total_descendant_set_organ:
            if organ_map_to_dict[temp_element]=='Yes':
                descendants_that_we_map_to_organ.add(temp_element)
    
    if temp_store_species is not None:
        
        #if the store exists but is empty, then we need to make everything a valid choice
        if len(temp_store_species['species'])==0:
            total_descendant_set_species=set()
            total_descendant_set_species=total_descendant_set_species.union(nx.algorithms.dag.descendants(networkx_species,'1'))
            total_descendant_set_species.add('1')
            descendants_that_we_map_to_species=set()
            for temp_element in total_descendant_set_species:
                if species_map_to_dict[temp_element]=='Yes':
                    descendants_that_we_map_to_species.add(temp_element)  
        
        #do the same thing for species
        total_descendant_set_species=set()
        for temp_element in temp_store_species['species']:
            total_descendant_set_species=total_descendant_set_species.union(nx.algorithms.dag.descendants(networkx_species,temp_element))
            total_descendant_set_species.add(temp_element)
        descendants_that_we_map_to_species=set()
        for temp_element in total_descendant_set_species:
            if species_map_to_dict[temp_element]=='Yes':
                descendants_that_we_map_to_species.add(temp_element)

    if ( ((temp_store_species is None) or (len(temp_store_species['species'])==0)) and ((temp_store_organ is None) or (len(temp_store_organ['organ'])==0)) ):
        return [temp_element for temp_element in networkx_disease.nodes]

    elif (temp_store_species is None) and (temp_store_organ is not None):
        valid_base_disease_choices=list(set(index_panda.loc[index_panda.organ.isin(descendants_that_we_map_to_organ)].disease.to_list()))

    elif (temp_store_species is not None) and (temp_store_organ is None):
        valid_base_disease_choices=list(set(index_panda.loc[index_panda.species.isin(descendants_that_we_map_to_species)].disease.to_list()))
    elif (temp_store_species is not None) and (temp_store_organ is not None):
        #if one has checkboxes but the other doesnt
        if len(temp_store_species['species'])!=0 and len(temp_store_organ['organ'])==0:
            valid_base_disease_choices=list(set(index_panda.loc[index_panda.species.isin(descendants_that_we_map_to_species)].disease.to_list()))
        elif len(temp_store_species['species'])==0 and len(temp_store_organ['organ'])!=0:
            valid_base_disease_choices=list(set(index_panda.loc[index_panda.organ.isin(descendants_that_we_map_to_organ)].disease.to_list()))
        elif len(temp_store_species['species'])!=0 and len(temp_store_organ['organ'])!=0:
            valid_base_disease_choices=list(set(index_panda.loc[index_panda.organ.isin(descendants_that_we_map_to_organ) & index_panda.species.isin(descendants_that_we_map_to_species)].disease.to_list()))
                        
        #filter the index panda to get a list of disease that are valid choices
        #valid_base_disease_choices=list(set(index_panda.loc[index_panda.organ.isin(descendants_that_we_map_to_organ) & index_panda.species.isin(descendants_that_we_map_to_species)].disease.to_list()))
    a=[i for i in valid_base_disease_choices if (pandas.isna(i)==False)]
    valid_base_disease_choices=a
    
    #create the list of nodes that are valid selections from the mapped-to-disease
    #step 1 find the lowest common ancestor
    #step 2 find all nodes along each path from every mapped-to-disease to LCA
    #step 3 return this. this result is used for the update on the cyto, dropdown, and checkboxes
    #step 1
    temp_lca=''
    if len(valid_base_disease_choices)==1:
        return set(valid_base_disease_choices)
    else:
        #the basic idea is that we test the first two nodes, get a lca, then test the current lca against each other node. it either goes up or stays
        for i,temp_element in enumerate(valid_base_disease_choices):
            if i==0:
                temp_tuple_tuple=((valid_base_disease_choices[0],valid_base_disease_choices[1],),)
                temp_lca=next(nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(G=networkx_disease,pairs=temp_tuple_tuple))[1]
            else:
                temp_tuple_tuple=((temp_lca,temp_element,),)
                temp_lca=next(nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(G=networkx_disease,pairs=temp_tuple_tuple))[1]
    #step 2
    nodes_for_subgraph_set=set()
    for temp_element in valid_base_disease_choices:
        nodes_to_lca=nx.algorithms.shortest_paths.unweighted.bidirectional_shortest_path(G=networkx_disease,source=temp_lca,target=temp_element)
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
    [Output(component_id='cytoscape_from_disease',component_property='elements'),
    Output(component_id='checklist_from_disease',component_property='value'),
    Output(component_id='dropdown_from_disease',component_property='value'),
    Output(component_id='store_from_disease',component_property='data'),
    
    Output(component_id='dropdown_from_disease',component_property='options'),
    Output(component_id='checklist_from_disease',component_property='options'),

    #Output(component_id='cytoscape_from_disease',component_property='zoom'),
    #Output(component_id='cytoscape_from_disease',component_property='pan')
    ],
    
    [Input(component_id='cytoscape_from_disease',component_property='tapNodeData'),
    Input(component_id='checklist_from_disease',component_property='value'),
    Input(component_id='dropdown_from_disease',component_property='value'),
    Input(component_id='button_from_disease',component_property='n_clicks')],
    
    [State(component_id='cytoscape_from_disease',component_property='elements'),
   
    State(component_id='store_from_disease',component_property='data'),
    State(component_id='store_from_organ',component_property='data'),
    State(component_id='store_from_species',component_property='data'),

    State(component_id='dropdown_from_disease',component_property='options'),
    State(component_id='checklist_from_disease',component_property='options'),
    State(component_id='cytoscape_from_disease',component_property='zoom'),
    State(component_id='cytoscape_from_disease',component_property='pan')
    ]
)
def callback_aggregate_from(
    cytoscape_from_disease_tapnodedata,
    checklist_from_disease_value,
    dropdown_from_disease_value,
    button_from_disease_value,

    cytoscape_from_disease_elements,

    store_from_disease_data,
    store_from_organ_data,
    store_from_species_data,

    dropdown_from_disease_options,
    checklist_from_disease_options,

    cytoscape_from_disease_zoom,
    cytoscape_from_disease_pan

):
    if (len(callback_context.triggered)>1) and (store_from_disease_data is None):
        store_from_disease_data={
            'disease':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_from_disease_value=list()

        ###modifying the layout based on organ/species
        valid_disease_selections=compile_set_of_valid_selections(store_from_organ_data,store_from_species_data)
        dropdown_from_disease_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes'] if (temp_node['data']['id'] in valid_disease_selections)
        ]
        checklist_from_disease_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_disease_from.keys() if (set(checklist_hashmap_disease_from[i]).issubset(valid_disease_selections))
        ]
        temp_nodes_to_remove_disease=disease_elements_starting_from.difference(valid_disease_selections)
        for temp_node in temp_nodes_to_remove_disease:
            cytoscape_from_disease_elements=delete_node_reconnect_cyto_elements(cytoscape_from_disease_elements,temp_node)
        ##hot fix for internship applicaitons
        try:
            cytoscape_from_disease_zoom=5/len(valid_disease_selections)
        except ZeroDivisionError:
            cytoscape_from_disease_zoom=5/1
        ##
        cytoscape_from_disease_pan={'x':600,'y':1}
        
        return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

    elif (len(callback_context.triggered)>1) and (store_from_disease_data is not None):
        
        ###modifying the layout based on organ/species
        valid_disease_selections=compile_set_of_valid_selections(store_from_organ_data,store_from_species_data)
        dropdown_from_disease_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_from['elements']['nodes'] if (temp_node['data']['id'] in valid_disease_selections)
        ]
        checklist_from_disease_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_disease_from.keys() if (set(checklist_hashmap_disease_from[i]).issubset(valid_disease_selections))
        ]
        temp_nodes_to_remove_disease=disease_elements_starting_from.difference(valid_disease_selections)
        for temp_node in temp_nodes_to_remove_disease:
            cytoscape_from_disease_elements=delete_node_reconnect_cyto_elements(cytoscape_from_disease_elements,temp_node)
        ##hot fix for internship applicaitons
        try:
            cytoscape_from_disease_zoom=5/len(valid_disease_selections)
        except ZeroDivisionError:
            cytoscape_from_disease_zoom=5/1
        ##
        cytoscape_from_disease_pan={'x':600,'y':1}

        for temp_node in cytoscape_from_disease_elements['nodes']:
            if temp_node['data']['id'] in store_from_disease_data['disease']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
        dropdown_from_disease_value=store_from_disease_data['disease']
        checklist_from_disease_value=store_from_disease_data['checkboxes']
        #dont do anthing to store_from_disease_data
        return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_from_disease.tapNodeData'):
        this_click=set()
        this_click.add(cytoscape_from_disease_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_from_disease_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store disease
        new_disease_list=list()
        for temp_node in cytoscape_from_disease_elements['nodes']:
            if temp_node['classes']=='selected':
                new_disease_list.append(temp_node['data']['id'])        
        store_from_disease_data['disease']=new_disease_list

        #dropdown
        dropdown_from_disease_value=store_from_disease_data['disease']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_disease_from.keys():
            #if every node id is in the store
            if all([(i in store_from_disease_data['disease']) for i in checklist_hashmap_disease_from[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_from_disease_value=new_checkbox_values

        #store checkboxes        
        store_from_disease_data['checkboxes']=checklist_from_disease_value

        return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_from_disease.value'):

        if (len(store_from_disease_data['checkboxes']) < len(checklist_from_disease_value)):

            box_we_clicked=list(set(checklist_from_disease_value).difference(set(store_from_disease_data['checkboxes'])))[0]
            #elements
            for temp_node in cytoscape_from_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease_from[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_disease_data['checkboxes'].append(box_we_clicked)
            store_from_disease_data['disease']=list(set(store_from_disease_data['disease']).union(set(checklist_hashmap_disease_from[box_we_clicked])))

            #dropdown
            dropdown_from_disease_value=store_from_disease_data['disease']
            
            return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan
           
        elif len(store_from_disease_data['checkboxes']) > len(checklist_from_disease_value):

            box_we_unclicked=list(set(store_from_disease_data['checkboxes']).difference(set(checklist_from_disease_value)))[0]

            #elements
            for temp_node in cytoscape_from_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease_from[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_disease_data['checkboxes'].remove(box_we_unclicked)
            store_from_disease_data['disease']=list(set(store_from_disease_data['disease']).difference(set(checklist_hashmap_disease_from[box_we_unclicked])))

            #dropdown
            dropdown_from_disease_value=store_from_disease_data['disease']

            return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_from_disease.value'):

        if len(store_from_disease_data['disease']) < len(dropdown_from_disease_value):

            disease_we_added=list(set(dropdown_from_disease_value).difference(set(store_from_disease_data['disease'])))[0]

            #elements
            for temp_node in cytoscape_from_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_disease_data['disease'].append(disease_we_added)

            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease_from.keys() if (disease_we_added in checklist_hashmap_disease_from[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #if the set of disease implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of disease is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_disease_from[temp_checkbox]).difference(set(dropdown_from_disease_value)))==0:
                    store_from_disease_data['checkboxes'].append(temp_checkbox)
                    checklist_from_disease_value.append(temp_checkbox)

            return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

        elif len(store_from_disease_data['disease']) > len(dropdown_from_disease_value):

            disease_we_lost=list(set(store_from_disease_data['disease']).difference(set(dropdown_from_disease_value)))[0]

            #elements
            for temp_node in cytoscape_from_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_disease_data['disease'].remove(disease_we_lost)

            #checklist
            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease_from.keys() if (disease_we_lost in checklist_hashmap_disease_from[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_disease_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_from_disease_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_from_disease.n_clicks'):

        store_from_disease_data={
            'disease':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_from_disease_elements['nodes']:
            temp_node['classes']='not_selected'  
        checklist_from_disease_value=list()
        dropdown_from_disease_value=None

        return cytoscape_from_disease_elements, checklist_from_disease_value, dropdown_from_disease_value,store_from_disease_data, dropdown_from_disease_options,checklist_from_disease_options#,cytoscape_from_disease_zoom,cytoscape_from_disease_pan

@app.callback(
    [Output(component_id='cytoscape_to_disease',component_property='elements'),
    Output(component_id='checklist_to_disease',component_property='value'),
    Output(component_id='dropdown_to_disease',component_property='value'),
    Output(component_id='store_to_disease',component_property='data'),
    
    Output(component_id='dropdown_to_disease',component_property='options'),
    Output(component_id='checklist_to_disease',component_property='options'),

    #Output(component_id='cytoscape_to_disease',component_property='zoom'),
    #Output(component_id='cytoscape_to_disease',component_property='pan')
    ],
    
    [Input(component_id='cytoscape_to_disease',component_property='tapNodeData'),
    Input(component_id='checklist_to_disease',component_property='value'),
    Input(component_id='dropdown_to_disease',component_property='value'),
    Input(component_id='button_to_disease',component_property='n_clicks')],
    
    [State(component_id='cytoscape_to_disease',component_property='elements'),
   
    State(component_id='store_to_disease',component_property='data'),
    State(component_id='store_to_organ',component_property='data'),
    State(component_id='store_to_species',component_property='data'),

    State(component_id='dropdown_to_disease',component_property='options'),
    State(component_id='checklist_to_disease',component_property='options'),
    State(component_id='cytoscape_to_disease',component_property='zoom'),
    State(component_id='cytoscape_to_disease',component_property='pan')
    ]
)
def callback_aggregate_to(
    cytoscape_to_disease_tapnodedata,
    checklist_to_disease_value,
    dropdown_to_disease_value,
    button_to_disease_value,

    cytoscape_to_disease_elements,

    store_to_disease_data,
    store_to_organ_data,
    store_to_species_data,

    dropdown_to_disease_options,
    checklist_to_disease_options,

    cytoscape_to_disease_zoom,
    cytoscape_to_disease_pan

):
    if (len(callback_context.triggered)>1) and (store_to_disease_data is None):
        store_to_disease_data={
            'disease':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_to_disease_value=list()

        ###modifying the layout based on organ/species
        valid_disease_selections=compile_set_of_valid_selections(store_to_organ_data,store_to_species_data)
        dropdown_to_disease_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes'] if (temp_node['data']['id'] in valid_disease_selections)
        ]
        checklist_to_disease_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_disease_to.keys() if (set(checklist_hashmap_disease_to[i]).issubset(valid_disease_selections))
        ]
        temp_nodes_to_remove_disease=disease_elements_starting_to.difference(valid_disease_selections)
        for temp_node in temp_nodes_to_remove_disease:
            cytoscape_to_disease_elements=delete_node_reconnect_cyto_elements(cytoscape_to_disease_elements,temp_node)
        ##hot fix for internship applicaitons
        try:
            cytoscape_from_disease_zoom=5/len(valid_disease_selections)
        except ZeroDivisionError:
            cytoscape_from_disease_zoom=5/1
        ##
        cytoscape_to_disease_pan={'x':600,'y':1}
        
        return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

    elif (len(callback_context.triggered)>1) and (store_to_disease_data is not None):
        
        ###modifying the layout based on organ/species
        valid_disease_selections=compile_set_of_valid_selections(store_to_organ_data,store_to_species_data)
        dropdown_to_disease_options=[
            {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict_to['elements']['nodes'] if (temp_node['data']['id'] in valid_disease_selections)
        ]
        checklist_to_disease_options=[
            {'label': i, 'value': i} for i in checklist_hashmap_disease_to.keys() if (set(checklist_hashmap_disease_to[i]).issubset(valid_disease_selections))
        ]
        temp_nodes_to_remove_disease=disease_elements_starting_to.difference(valid_disease_selections)
        for temp_node in temp_nodes_to_remove_disease:
            cytoscape_to_disease_elements=delete_node_reconnect_cyto_elements(cytoscape_to_disease_elements,temp_node)
        ##hot fix for internship applicaitons
        try:
            cytoscape_from_disease_zoom=5/len(valid_disease_selections)
        except ZeroDivisionError:
            cytoscape_from_disease_zoom=5/1
        ##
        cytoscape_to_disease_pan={'x':600,'y':1}

        for temp_node in cytoscape_to_disease_elements['nodes']:
            if temp_node['data']['id'] in store_to_disease_data['disease']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
        dropdown_to_disease_value=store_to_disease_data['disease']
        checklist_to_disease_value=store_to_disease_data['checkboxes']
        #dont do anthing to store_to_disease_data
        return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_to_disease.tapNodeData'):
        this_click=set()
        this_click.add(cytoscape_to_disease_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_to_disease_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store disease
        new_disease_list=list()
        for temp_node in cytoscape_to_disease_elements['nodes']:
            if temp_node['classes']=='selected':
                new_disease_list.append(temp_node['data']['id'])        
        store_to_disease_data['disease']=new_disease_list

        #dropdown
        dropdown_to_disease_value=store_to_disease_data['disease']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_disease_to.keys():
            #if every node id is in the store
            if all([(i in store_to_disease_data['disease']) for i in checklist_hashmap_disease_to[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_to_disease_value=new_checkbox_values

        #store checkboxes        
        store_to_disease_data['checkboxes']=checklist_to_disease_value

        return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_to_disease.value'):

        if (len(store_to_disease_data['checkboxes']) < len(checklist_to_disease_value)):

            box_we_clicked=list(set(checklist_to_disease_value).difference(set(store_to_disease_data['checkboxes'])))[0]
            #elements
            for temp_node in cytoscape_to_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease_to[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_to_disease_data['checkboxes'].append(box_we_clicked)
            store_to_disease_data['disease']=list(set(store_to_disease_data['disease']).union(set(checklist_hashmap_disease_to[box_we_clicked])))

            #dropdown
            dropdown_to_disease_value=store_to_disease_data['disease']
            
            return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan
           
        elif len(store_to_disease_data['checkboxes']) > len(checklist_to_disease_value):

            box_we_unclicked=list(set(store_to_disease_data['checkboxes']).difference(set(checklist_to_disease_value)))[0]

            #elements
            for temp_node in cytoscape_to_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease_to[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_to_disease_data['checkboxes'].remove(box_we_unclicked)
            store_to_disease_data['disease']=list(set(store_to_disease_data['disease']).difference(set(checklist_hashmap_disease_to[box_we_unclicked])))

            #dropdown
            dropdown_to_disease_value=store_to_disease_data['disease']

            return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_to_disease.value'):

        if len(store_to_disease_data['disease']) < len(dropdown_to_disease_value):

            disease_we_added=list(set(dropdown_to_disease_value).difference(set(store_to_disease_data['disease'])))[0]

            #elements
            for temp_node in cytoscape_to_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_to_disease_data['disease'].append(disease_we_added)

            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease_to.keys() if (disease_we_added in checklist_hashmap_disease_to[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #if the set of disease implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of disease is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_disease_to[temp_checkbox]).difference(set(dropdown_to_disease_value)))==0:
                    store_to_disease_data['checkboxes'].append(temp_checkbox)
                    checklist_to_disease_value.append(temp_checkbox)

            return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

        elif len(store_to_disease_data['disease']) > len(dropdown_to_disease_value):

            disease_we_lost=list(set(store_to_disease_data['disease']).difference(set(dropdown_to_disease_value)))[0]

            #elements
            for temp_node in cytoscape_to_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_to_disease_data['disease'].remove(disease_we_lost)

            #checklist
            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease_to.keys() if (disease_we_lost in checklist_hashmap_disease_to[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_to_disease_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_to_disease_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_to_disease.n_clicks'):

        store_to_disease_data={
            'disease':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_to_disease_elements['nodes']:
            temp_node['classes']='not_selected'  
        checklist_to_disease_value=list()
        dropdown_to_disease_value=None

        return cytoscape_to_disease_elements, checklist_to_disease_value, dropdown_to_disease_value,store_to_disease_data, dropdown_to_disease_options,checklist_to_disease_options#,cytoscape_to_disease_zoom,cytoscape_to_disease_pan
