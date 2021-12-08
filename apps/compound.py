import dash_bootstrap_components as dbc
from dash import html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from dash import callback_context
import dash_core_components as dcc

from itertools import chain
import networkx as nx
import pathlib
import json
from pprint import pprint
import fnmatch

from app import app

cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


#load the base compound network
compound_json_address=DATA_PATH.joinpath('cyto_format_compound.json')
temp_json_file=open(compound_json_address,'r')
compound_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in compound_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    try:
        temp_element['data']['label']='Bin: '+temp_element['data']['common_name']
    except KeyError:
        temp_element['data']['label']=temp_element['data']['name']
    
    temp_element['classes']='not_selected'

#defines the map between the various boxes and the node ids
checklist_hashmap={
    'both_glucoses': ['5','22'],
    'alanine':['2'],
    'all basic bins':['2', '3', '4', '5', '6', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '23']
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

# networkx_address=DATA_PATH.joinpath('compounds_networkx.bin')
# networkx=nx.readwrite.gpickle.read_gpickle(networkx_address)


layout=html.Div(
    children=[
        html.Div(
            id='div_cytoscape_compound_cyto',
            children=[
                cyto.Cytoscape(
                    id='cytoscape_compound',
                    layout={'name':'dagre'},
                    elements=compound_network_dict['elements'],
                    minZoom=0.3,
                    maxZoom=5,
                    stylesheet=basic_stylesheet,
                    style={'width': '1500px','height':'750px'}
                )
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            dcc.Checklist(
                                id='checklist_compound',
                                options=[
                                    {'label': i, 'value': i} for i in checklist_hashmap.keys()
                                ]
                            )
                        ],
                        width='auto',
                        align='center'
                    )
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            dcc.Dropdown(
                                id='dropdown_compound',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in compound_network_dict['elements']['nodes']
                                ],
                                multi=True
                            )
                        ],
                    )
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            html.Button(
                                'Reset selections',
                                id='button_compound',
                            )
                        ],
                    )
                ),
            ]
        ),

    
    ]
)


@app.callback(
    [Output(component_id='cytoscape_compound',component_property='elements'),
    Output(component_id='checklist_compound',component_property='value'),
    Output(component_id='dropdown_compound',component_property='value'),
    Output(component_id='store_compound',component_property='data')],
    
    [Input(component_id='cytoscape_compound',component_property='tapNodeData'),
    Input(component_id='checklist_compound',component_property='value'),
    Input(component_id='dropdown_compound',component_property='value'),
    Input(component_id='button_compound',component_property='n_clicks')],
    
    [State(component_id='cytoscape_compound',component_property='elements'),
    State(component_id='store_compound',component_property='data')]
)
def callback_aggregate(
    cytoscape_compound_tapnodedata,
    checklist_compound_value,
    dropdown_compound_value,
    button_compound_value,

    cytoscape_compound_elements,
    store_compound_data
):

    if (len(callback_context.triggered)>1) and (store_compound_data is None):

        store_compound_data={
            'compounds':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_compound_value=list()

        return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

    elif (len(callback_context.triggered)>1) and (store_compound_data is not None):
        cytoscape_compound_elements, 
        for temp_node in cytoscape_compound_elements['nodes']:
            if temp_node['data']['id'] in store_compound_data['compounds']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_compound_value=store_compound_data['compounds']

        checklist_compound_value=store_compound_data['checkboxes']

        #dont do anthing to store_compound_data

        return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_compound.tapNodeData'):
        
        #elements
        #try:
        #    child_nodes_and_self=nx.algorithms.dag.descendants(networkx,cytoscape_compound_tapnodedata['id'])
        #except nx.NetworkXError:
        #    child_nodes_and_self=set()
        #child_nodes_and_self.add(cytoscape_compound_tapnodedata['id'])
        child_nodes_and_self=set()
        child_nodes_and_self.add(cytoscape_compound_tapnodedata['id'])
        child_nodes_and_self=set(map(str,child_nodes_and_self))
        
        for temp_node in cytoscape_compound_elements['nodes']:
            if temp_node['data']['id'] in child_nodes_and_self:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store compounds
        new_compound_list=list()
        for temp_node in cytoscape_compound_elements['nodes']:
            if temp_node['classes']=='selected':
                new_compound_list.append(temp_node['data']['id'])        
        store_compound_data['compounds']=new_compound_list

        #dropdown
        dropdown_compound_value=store_compound_data['compounds']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap.keys():
            #if every node id is in the store
            if all([(i in store_compound_data['compounds']) for i in checklist_hashmap[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_compound_value=new_checkbox_values

        #store checkboxes        
        store_compound_data['checkboxes']=checklist_compound_value

        return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_compound.value'):

        if (len(store_compound_data['checkboxes']) < len(checklist_compound_value)):

            box_we_clicked=list(set(checklist_compound_value).difference(set(store_compound_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_compound_data['checkboxes'].append(box_we_clicked)
            store_compound_data['compounds']=list(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))

            #dropdown
            dropdown_compound_value=store_compound_data['compounds']
            
            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data
           
        elif len(store_compound_data['checkboxes']) > len(checklist_compound_value):

            box_we_unclicked=list(set(store_compound_data['checkboxes']).difference(set(checklist_compound_value)))[0]

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_compound_data['checkboxes'].remove(box_we_unclicked)
            store_compound_data['compounds']=list(set(store_compound_data['compounds']).difference(set(checklist_hashmap[box_we_unclicked])))

            #dropdown
            dropdown_compound_value=store_compound_data['compounds']

            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_compound.value'):

        if len(store_compound_data['compounds']) < len(dropdown_compound_value):

            compound_we_added=list(set(dropdown_compound_value).difference(set(store_compound_data['compounds'])))[0]

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] == compound_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_compound_data['compounds'].append(compound_we_added)

            #so the general logic is
            #we chose a compound
            #that compound belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of compounds is selected (the currently chosen compound)
            #being the "completing compound"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_compound_belongs=list()
            checkboxes_to_which_this_compound_belongs=[temp_key for temp_key in checklist_hashmap.keys() if (compound_we_added in checklist_hashmap[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_compound_belongs:
                #if the set of compounds implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of compounds is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap[temp_checkbox]).difference(set(dropdown_compound_value)))==0:
                    store_compound_data['checkboxes'].append(temp_checkbox)
                    checklist_compound_value.append(temp_checkbox)

            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

        elif len(store_compound_data['compounds']) > len(dropdown_compound_value):

            compound_we_lost=list(set(store_compound_data['compounds']).difference(set(dropdown_compound_value)))[0]

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] == compound_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_compound_data['compounds'].remove(compound_we_lost)

            #checklist
            #so the general logic is
            #we chose a compound
            #that compound belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of compounds is selected (the currently chosen compound)
            #being the "completing compound"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_compound_belongs=list()
            checkboxes_to_which_this_compound_belongs=[temp_key for temp_key in checklist_hashmap.keys() if (compound_we_lost in checklist_hashmap[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_compound_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_compound_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_compound_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_compound.n_clicks'):

        store_compound_data={
            'compounds':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_compound_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_compound_value=list()

        dropdown_compound_value=None

        return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data