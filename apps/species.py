import pathlib

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import json
from dash import html
from dash import callback_context


from app import app

cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#load the base species network
species_json_address=DATA_PATH.joinpath('cyto_format_species.json')
temp_json_file=open(species_json_address,'r')
species_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict_from['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name species
    #try:
    temp_element['data']['label']=temp_element['data']['scientific_name']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'



#load the base species network
species_json_address=DATA_PATH.joinpath('cyto_format_species.json')
temp_json_file=open(species_json_address,'r')
species_network_dict_to=json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict_to['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name species
    #try:
    temp_element['data']['label']=temp_element['data']['scientific_name']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'


#defines the map between the various boxes and the node ids
checklist_hashmap_species_from={
    'some random plants': ['4081','29760','3760','3656','4081','3694'],
    'some random bacteria':['45133','33196','3705','5007','5476','9397','3052','47906','3055','3081','3075','3076','554065','3077','3041','535','1485','1502','13442','5207','3046','3038','853'],
    'monkeyish things':['9606','9544','9598','9557']
}
checklist_hashmap_species_to={
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

# #might want to put this in index?
# networkx_address_species=DATA_PATH.joinpath('species_networkx.bin')
# networkx_species=nx.readwrite.gpickle.read_gpickle(networkx_address_species)

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
                            align='center'
                        ),
                        dbc.Col(
                            children=[
                                html.H5('Pre-selected common groups of individuals')
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
                                dcc.Checklist(
                                    id='checklist_from_species',
                                    options=[
                                        {'label': i, 'value': i} for i in checklist_hashmap_species_from.keys()
                                    ]
                                )
                            ],
                            width={'size':4,'offset':0},
                            align='center'
                        ),
                        dbc.Col(
                            children=[
                                dcc.Checklist(
                                    id='checklist_to_species',
                                    options=[
                                        {'label': i, 'value': i} for i in checklist_hashmap_species_from.keys()
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
                                    id='dropdown_from_species',
                                    options=[
                                        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                    ],
                                    multi=True
                                )
                            ],
                            width={'size':4,'offset':0},
                        ),
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    id='dropdown_to_species',
                                    options=[
                                        {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
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
                                    id='button_from_species',
                                )
                            ],
                            width={'size':4,'offset':0},
                        ),
                        dbc.Col(
                            children=[
                                html.Button(
                                    'Reset selections',
                                    id='button_to_species',
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
                        cyto.Cytoscape(
                            id='cytoscape_from_species',
                            layout={'name':'klay'},
                            elements=species_network_dict_from['elements'],
                            minZoom=0.15,
                            maxZoom=5,
                            stylesheet=basic_stylesheet,
                            style={'width': '700px','height':'1000px'}
                        )
                    ),
                    dbc.Col(
                        html.H1('VS'),
                        width={'size':2,'offset':0}
                    ),
                    dbc.Col(
                        cyto.Cytoscape(
                            id='cytoscape_to_species',
                            layout={'name':'klay'},
                            elements=species_network_dict_from['elements'],
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


@app.callback(
    [Output(component_id='cytoscape_from_species',component_property='elements'),
    Output(component_id='checklist_from_species',component_property='value'),
    Output(component_id='dropdown_from_species',component_property='value'),
    Output(component_id='store_from_species',component_property='data')],
    
    [Input(component_id='cytoscape_from_species',component_property='tapNodeData'),
    Input(component_id='checklist_from_species',component_property='value'),
    Input(component_id='dropdown_from_species',component_property='value'),
    Input(component_id='button_from_species',component_property='n_clicks')],
    
    [State(component_id='cytoscape_from_species',component_property='elements'),
    State(component_id='store_from_species',component_property='data')]
)
def callback_aggregate(
    cytoscape_from_species_tapnodedata,
    checklist_from_species_value,
    dropdown_from_species_value,
    button_from_species_value,

    cytoscape_from_species_elements,
    store_from_species_data
):

    
    if (len(callback_context.triggered)>1) and (store_from_species_data is None):

        store_from_species_data={
            'species':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_from_species_value=list()

        return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

    elif (len(callback_context.triggered)>1) and (store_from_species_data is not None):
        cytoscape_from_species_elements, 
        for temp_node in cytoscape_from_species_elements['nodes']:
            if temp_node['data']['id'] in store_from_species_data['species']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_from_species_value=store_from_species_data['species']

        checklist_from_species_value=store_from_species_data['checkboxes']

        #dont do anthing to store_from_species_data

        return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_from_species.tapNodeData'):
        
        #elements
        # try:
        #     child_nodes_and_self=nx.algorithms.dag.descendants(networkx_species,cytoscape_from_species_tapnodedata['id'])
        # except nx.NetworkXError:
        #     child_nodes_and_self=set()
        # child_nodes_and_self.add(cytoscape_from_species_tapnodedata['id'])
        # child_nodes_and_self=set(map(str,child_nodes_and_self))
        this_click=set()
        this_click.add(cytoscape_from_species_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_from_species_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store species
        new_species_list=list()
        for temp_node in cytoscape_from_species_elements['nodes']:
            if temp_node['classes']=='selected':
                new_species_list.append(temp_node['data']['id'])        
        store_from_species_data['species']=new_species_list

        #dropdown
        dropdown_from_species_value=store_from_species_data['species']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_species_from.keys():
            #if every node id is in the store
            if all([(i in store_from_species_data['species']) for i in checklist_hashmap_species_from[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_from_species_value=new_checkbox_values

        #store checkboxes        
        store_from_species_data['checkboxes']=checklist_from_species_value

        return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_from_species.value'):

        if (len(store_from_species_data['checkboxes']) < len(checklist_from_species_value)):

            box_we_clicked=list(set(checklist_from_species_value).difference(set(store_from_species_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_from_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species_from[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_species_data['checkboxes'].append(box_we_clicked)
            store_from_species_data['species']=list(set(store_from_species_data['species']).union(set(checklist_hashmap_species_from[box_we_clicked])))

            #dropdown
            dropdown_from_species_value=store_from_species_data['species']
            
            return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data
           
        elif len(store_from_species_data['checkboxes']) > len(checklist_from_species_value):

            box_we_unclicked=list(set(store_from_species_data['checkboxes']).difference(set(checklist_from_species_value)))[0]

            #elements
            for temp_node in cytoscape_from_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species_from[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_species_data['checkboxes'].remove(box_we_unclicked)
            store_from_species_data['species']=list(set(store_from_species_data['species']).difference(set(checklist_hashmap_species_from[box_we_unclicked])))

            #dropdown
            dropdown_from_species_value=store_from_species_data['species']

            return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_from_species.value'):

        if len(store_from_species_data['species']) < len(dropdown_from_species_value):

            species_we_added=list(set(dropdown_from_species_value).difference(set(store_from_species_data['species'])))[0]

            #elements
            for temp_node in cytoscape_from_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_species_data['species'].append(species_we_added)

            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species_from.keys() if (species_we_added in checklist_hashmap_species_from[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #if the set of species implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of species is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_species_from[temp_checkbox]).difference(set(dropdown_from_species_value)))==0:
                    store_from_species_data['checkboxes'].append(temp_checkbox)
                    checklist_from_species_value.append(temp_checkbox)

            return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

        elif len(store_from_species_data['species']) > len(dropdown_from_species_value):

            species_we_lost=list(set(store_from_species_data['species']).difference(set(dropdown_from_species_value)))[0]

            #elements
            for temp_node in cytoscape_from_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_species_data['species'].remove(species_we_lost)

            #checklist
            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species_from.keys() if (species_we_lost in checklist_hashmap_species_from[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_species_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_from_species_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_from_species.n_clicks'):

        store_from_species_data={
            'species':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_from_species_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_from_species_value=list()

        dropdown_from_species_value=None

        return cytoscape_from_species_elements, checklist_from_species_value, dropdown_from_species_value,store_from_species_data


@app.callback(
    [Output(component_id='cytoscape_to_species',component_property='elements'),
    Output(component_id='checklist_to_species',component_property='value'),
    Output(component_id='dropdown_to_species',component_property='value'),
    Output(component_id='store_to_species',component_property='data')],
    
    [Input(component_id='cytoscape_to_species',component_property='tapNodeData'),
    Input(component_id='checklist_to_species',component_property='value'),
    Input(component_id='dropdown_to_species',component_property='value'),
    Input(component_id='button_to_species',component_property='n_clicks')],
    
    [State(component_id='cytoscape_to_species',component_property='elements'),
    State(component_id='store_to_species',component_property='data')]
)
def callback_aggregate(
    cytoscape_to_species_tapnodedata,
    checklist_to_species_value,
    dropdown_to_species_value,
    button_to_species_value,

    cytoscape_to_species_elements,
    store_to_species_data
):

    
    if (len(callback_context.triggered)>1) and (store_to_species_data is None):

        store_to_species_data={
            'species':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_to_species_value=list()

        return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

    elif (len(callback_context.triggered)>1) and (store_to_species_data is not None):
        cytoscape_to_species_elements, 
        for temp_node in cytoscape_to_species_elements['nodes']:
            if temp_node['data']['id'] in store_to_species_data['species']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_to_species_value=store_to_species_data['species']

        checklist_to_species_value=store_to_species_data['checkboxes']

        #dont do anthing to store_to_species_data

        return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_to_species.tapNodeData'):
        
        #elements
        # try:
        #     child_nodes_and_self=nx.algorithms.dag.descendants(networkx_species,cytoscape_to_species_tapnodedata['id'])
        # except nx.NetworkXError:
        #     child_nodes_and_self=set()
        # child_nodes_and_self.add(cytoscape_to_species_tapnodedata['id'])
        # child_nodes_and_self=set(map(str,child_nodes_and_self))
        this_click=set()
        this_click.add(cytoscape_to_species_tapnodedata['id'])
        this_click=set(map(str,this_click))
        
        for temp_node in cytoscape_to_species_elements['nodes']:
            if temp_node['data']['id'] in this_click:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store species
        new_species_list=list()
        for temp_node in cytoscape_to_species_elements['nodes']:
            if temp_node['classes']=='selected':
                new_species_list.append(temp_node['data']['id'])        
        store_to_species_data['species']=new_species_list

        #dropdown
        dropdown_to_species_value=store_to_species_data['species']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_species_to.keys():
            #if every node id is in the store
            if all([(i in store_to_species_data['species']) for i in checklist_hashmap_species_to[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_to_species_value=new_checkbox_values

        #store checkboxes        
        store_to_species_data['checkboxes']=checklist_to_species_value

        return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_to_species.value'):

        if (len(store_to_species_data['checkboxes']) < len(checklist_to_species_value)):

            box_we_clicked=list(set(checklist_to_species_value).difference(set(store_to_species_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_to_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species_to[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_to_species_data['checkboxes'].append(box_we_clicked)
            store_to_species_data['species']=list(set(store_to_species_data['species']).union(set(checklist_hashmap_species_to[box_we_clicked])))

            #dropdown
            dropdown_to_species_value=store_to_species_data['species']
            
            return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data
           
        elif len(store_to_species_data['checkboxes']) > len(checklist_to_species_value):

            box_we_unclicked=list(set(store_to_species_data['checkboxes']).difference(set(checklist_to_species_value)))[0]

            #elements
            for temp_node in cytoscape_to_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species_to[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_to_species_data['checkboxes'].remove(box_we_unclicked)
            store_to_species_data['species']=list(set(store_to_species_data['species']).difference(set(checklist_hashmap_species_to[box_we_unclicked])))

            #dropdown
            dropdown_to_species_value=store_to_species_data['species']

            return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_to_species.value'):

        if len(store_to_species_data['species']) < len(dropdown_to_species_value):

            species_we_added=list(set(dropdown_to_species_value).difference(set(store_to_species_data['species'])))[0]

            #elements
            for temp_node in cytoscape_to_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_to_species_data['species'].append(species_we_added)

            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species_to.keys() if (species_we_added in checklist_hashmap_species_to[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #if the set of species implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of species is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_species_to[temp_checkbox]).difference(set(dropdown_to_species_value)))==0:
                    store_to_species_data['checkboxes'].append(temp_checkbox)
                    checklist_to_species_value.append(temp_checkbox)

            return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

        elif len(store_to_species_data['species']) > len(dropdown_to_species_value):

            species_we_lost=list(set(store_to_species_data['species']).difference(set(dropdown_to_species_value)))[0]

            #elements
            for temp_node in cytoscape_to_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_to_species_data['species'].remove(species_we_lost)

            #checklist
            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species_to.keys() if (species_we_lost in checklist_hashmap_species_to[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_to_species_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_to_species_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_to_species.n_clicks'):

        store_to_species_data={
            'species':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_to_species_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_to_species_value=list()

        dropdown_to_species_value=None

        return cytoscape_to_species_elements, checklist_to_species_value, dropdown_to_species_value,store_to_species_data
