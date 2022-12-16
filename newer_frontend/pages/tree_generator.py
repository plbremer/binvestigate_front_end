from enum import unique
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
from time import time

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

#['3701', '13442', '3705', '3052', '186826', '3633', '1129', '3041', '2706', '41073', '1485', '3883', '2']
species_to_disallow_for_tanglegram={'arabidopsis', 'coffea', 'brassica', 'chlamydomonas', 'lactobacillales', 'gossypium', 'synechococcus', 'chlorophyta', 'citrus', 'carabidae', 'clostridium', 'phaseolus', 'bacteria'}
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
unique_sod_combinations_dict={
    temp_key:unique_sod_combinations_dict[temp_key] for temp_key in unique_sod_combinations_dict.keys() if (unique_sod_combinations_dict[temp_key].split(' - ')[0] not in species_to_disallow_for_tanglegram)
}

tanglegram_species_nx=nx.read_gpickle('../newer_datasets/tanglegram_species_networkx.bin')
#print(unique_sod_combinations_dict)
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
        html.Div(
            children=[
                dbc.Spinner(
                    id='spinner_clustergram',
                    children=[



                        dbc.Row(html.H2("Tanglegram"),style={'textAlign': 'center'}),
                        dbc.Row(
                            html.Div(className="venn-thumbnail-container",
                                children=[
                                    html.Img(
                                        id='Img_tanglegram',
                                        #src=plotly_fig,
                                        height=200,
                                        width=200
                                    ),
                                ]
                            ),
                            style={'textAlign': 'center'}
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),                        
                        dbc.Modal(
                            children=[
                                #dbc.ModalHeader
                                dbc.ModalHeader(dbc.ModalTitle("Right Click + Copy Image Address for High-Res"),close_button=True),
                                dbc.ModalBody(
                                #    html.Div(className="modal-body-container",children=[
                                    html.Img(
                                        id='modal_Img_tanglegram',
                                        #src=plotly_fig,
                                        #height=400,
                                        #width=800,
                                        style={"height": "40vh"}
                                    )
                                #        ]
                                #    )
                                ),
                            ],
                            className="modal-overarching",
                            #fullscreen=True,
                            id='modal_tanglergram',
                            centered=True,
                            size='xl',
                            is_open=False,
                            style={"max-width": "none", "width": "90%"}
                        ),
                        html.H2("Clustergram", className='text-center'),
                        dcc.Graph(id='tree_clustergram_graph')




                    ],
                )
            ]
        )



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




@callback(
    [
        #Output(component_id='tree_query', component_property='n_clicks')
        #Output(component_id="leaf_table", component_property="columns"),
        #Output(component_id="leaf_table", component_property="data")
        #Output(component_id='spinner_clustergram',component_property="children")
        Output(component_id='tree_clustergram_graph',component_property="figure")
    ],
    [
        Input(component_id='tree_query', component_property='n_clicks'),
    ],
    [
        #State(component_id='dropdown_triplet_selection_from',component_property='value'),
        #State(component_id='dropdown_triplet_selection_to',component_property='value'),
        #State(component_id='radio_items_bin_type',component_property='value'),
        State(component_id='tree_table_metadata', component_property='derived_virtual_data'),
    ],
    prevent_initial_call=True
)
def query_table(
    tree_query_n_clicks,
    #radio_items_bin_type_value,
    tree_table_metadata_derived_virtual_data
):
    print('@'*50)
    pprint(tree_table_metadata_derived_virtual_data)

    input_metadata=pd.DataFrame.from_records(tree_table_metadata_derived_virtual_data)
    print(input_metadata.triplet_id.tolist())

    tree_output={
    #    "triplet_from":dropdown_triplet_selection_from_value,
    #    "triplet_to":dropdown_triplet_selection_to_value
        "metadata_triplets":input_metadata.triplet_id.tolist(),
        "bin_type":'knowns',
        "data_type":'average'
    }
    #print(table_metadata_derived_virtual_data)
    #leaf_output=table_metadata_derived_virtual_data

    start=time()
    response = requests.post(base_url_api + "/treeresource/", json=tree_output)
    end=time()
    clustergram_panda=pd.read_json(response.json(),orient='records')
    print(clustergram_panda)
    print(f'the time to get our info from the api is {end-start}')
    
    # start=time.time()
    # total_panda = pd.read_json(response.json(), orient="records")
    # print(total_panda)
    # print('&#$'*50)
    # if radio_items_bin_type_value!='class':
    #     total_panda['compound_id']=total_panda['compound_id'].map(hyperlink_translation_dict.get)
    #     total_panda['english_name']='['+total_panda['english_name']+'](/sunburst/'+total_panda['compound_id'].astype(str)+')'
    #     total_panda['identifier']='['+total_panda['identifier']+'](/bin-browser/'+total_panda['compound_id'].astype(str)+')'
    # end=time.time()
    # print(f'the time to turn our json into a panda is  {end-start}')
    # #print(total_panda)
    # #print('***********************************')

    # # start=time.time()
    # # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]
    # # end=time.time()
    # # print(f'the time to subset our panda is  {end-start}')

    # start=time.time()
    # data = total_panda.to_dict(orient='records')
    # end=time.time()
    # print(f'the time to turn our panda into json again is  {end-start}')
    # return [data]

    columns = list(clustergram_panda.columns.values)
    rows = list(clustergram_panda.index)

    print('about to make clustergram')
    clustergram_figure = dashbio.Clustergram(
        data=clustergram_panda.loc[rows].values,
        row_labels=rows,
        column_labels=columns,
        #height=40*len(rows),
        height=1000,
        width=2000
    )
    print('made clustergram')


    #dcc.Graph(id='tree_clustergram_graph',figure=clustergram_figure)

    #output_children=                  
    
    # clustergram_figure = dashbio.Clustergram(
    #     data=clustergram_panda.values,#bins_panda,
    #     row_labels=list(clustergram_panda.index),
    #     column_labels=list(clustergram_panda.columns.values),
    # )
    #volcano.update_layout(showlegend=False)\


    #convert incoming list of triplets into list of species
    #conver incoming list of species into species IDs
    #make a copy of the species networkx
    #delete things that arent present
    #run https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy.html#networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy
    # be sure to use the subgraph
    #  
    #for each species id, if present more than once, duplicate distance matrix row (of course expanding all others too )
    #if the matrix is
    #________________
    #|            |c |
    #|            |o |
    #|            |p |
    #|____________|y_|
    #|copy of abov|  |
    #|___________ |__|
    #thne the bottom right is the slice from the list of elements being copied, if possible

    #then, simply feed the distance matrices to the tanglegram

    #then, figure out exactly how to inject the genus, class, etc by looking at the locations in the R returned by "dendrogram"

    #coerce incoming data into distance matrix (in same way that clustergram does)
    #coerce mini species networkx into distance matrix
    #send both to tangleram creator






    return [clustergram_figure]









# @callback(
#     [
#         Output(component_id='modal_Img_tanglegram', component_property='is_open'),
#     ],
#     [
#         Input(component_id='Img_tanglegram', component_property='n_clicks'),
#     ],
#     prevent_initial_call=True
# )
# def open_modal(Img_tanglegram_n_clicks):
#     return [True]
