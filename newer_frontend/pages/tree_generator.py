from enum import unique
from operator import index
from unittest import result
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

from itertools import combinations

from scipy.spatial.distance import cdist
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import io
import base64

#import tanglegram as tg
from . import tangle_modified


from pprint import pprint

# import pydot
# from networkx.drawing.nx_pydot import graphviz_layout
# def visualize_nodes_on_a_list(temp_nx,temp_list,temp_attribute_name):
#     '''
#     temp_attribute_name=None when you dont want to use an attribute name, rather the 
#     node names themselves
#     '''
#     '''
#     temp_attribute_name=None when you dont want to use an attribute name, rather the 
#     node names themselves
#     '''
#     if temp_attribute_name != None:
#         print('here!!!!!!!!!!!!!!!!!!')
#         color_list=list()
#         for temp_node in temp_nx.nodes:
#             if temp_nx.nodes[temp_node][temp_attribute_name] in temp_list:
#                 color_list.append('#ffa500')
#             else:
#                 color_list.append('#00ff00')
#         pos = graphviz_layout(temp_nx, prog="dot")
#         labels = nx.get_node_attributes(temp_nx, 'scientific_name') 
#         nx.draw(temp_nx, pos,with_labels=labels,node_color=color_list)
#         plt.show()    

#     elif temp_attribute_name == None:
#         print('there!!!!!!!!!!!!!!!!!!')
#         color_list=list()
#         for temp_node in temp_nx.nodes:
#             if temp_node in temp_list:
#                 color_list.append('#ffa500')
#             else:
#                 color_list.append('#00ff00')

        
#         pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')

#         labels = nx.get_node_attributes(temp_nx, 'scientific_name') 
#         print(labels)
#         nx.draw(temp_nx, pos,labels=labels)#,node_color=color_list)
#         #nx.draw(temp_nx, pos,with_labels=True,node_color=color_list)
#         plt.show()  







from pprint import pprint
dash.register_page(__name__)

base_url_api = f"http://api_alias:4999/"
#base_url_api = f"http://127.0.0.1:4999/"

########get things from helper script########
species_networkx,species_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_species()
print('+++++++++++++++++++++')
#print(species_node_dict)
print(('+++++++++++++++++++++++++++'))
organ_networkx,organ_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_organ()
disease_networkx,disease_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_disease()
index_panda=pd.read_pickle('../newer_datasets/index_panda.bin')
index_panda=index_panda.sort_index()
index_panda['species']=index_panda['species'].astype(str)
print(index_panda)
english_species_to_ncbi_id_dict=dict(zip(index_panda['species_english'].tolist(),index_panda['species'].tolist()))


#['3701', '13442', '3705', '3052', '186826', '3633', '1129', '3041', '2706', '41073', '1485', '3883', '2']
species_to_disallow_for_tanglegram={'arabidopsis', 'coffea', 'brassica', 'chlamydomonas', 'lactobacillales', 'gossypium', 'synechococcus', 'chlorophyta', 'citrus', 'carabidae', 'clostridium', 'phaseolus', 'bacteria'}
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
unique_sod_combinations_dict={
    temp_key:unique_sod_combinations_dict[temp_key] for temp_key in unique_sod_combinations_dict.keys() if (unique_sod_combinations_dict[temp_key].split(' - ')[0] not in species_to_disallow_for_tanglegram)
}

tanglegram_species_nx=nx.read_gpickle('../newer_datasets/tanglegram_species_networkx.bin')


#fix the compound names
final_curations=pd.read_pickle('../newer_datasets/compound_list_for_sun_and_bin_new.bin')
compound_bin_translator_dict=dict(zip(final_curations.loc[final_curations.bin_type=='known']['compound_identifier'].astype(int).tolist(),final_curations.loc[final_curations.bin_type=='known']['english_name'].tolist()))

#print(unique_sod_combinations_dict)
##############################################


def append_index(Z, n, i, cluster_id_list):
    # refer to the recursive progress in
    # https://github.com/scipy/scipy/blob/4cf21e753cf937d1c6c2d2a0e372fbc1dbbeea81/scipy/cluster/hierarchy.py#L3549

    # i is the idx of cluster(counting in all 2 * n - 1 clusters)
    # so i-n is the idx in the "Z"
    if i < n:
        return
    aa = int(Z[i - n, 0])
    ab = int(Z[i - n, 1])

    append_index(Z,n, aa, cluster_id_list)
    append_index(Z,n, ab, cluster_id_list)

    cluster_id_list.append(i-n)
    # Imitate the progress in hierarchy.dendrogram
    # so how `i-n` is appended , is the same as how the element in 'icoord'&'dcoord' be.
    return

def get_linkid_clusterid_relation(Z):
    Zs = Z.shape
    n = Zs[0] + 1
    i = 2 * n - 2
    cluster_id_list = []
    append_index(Z, n, i, cluster_id_list)
    # cluster_id_list[i] is the cluster idx(in Z) that the R['icoord'][i]/R['dcoord'][i] corresponds to

    dict_linkid_2_clusterid = {linkid: clusterid for linkid, clusterid in enumerate(cluster_id_list)}
    dict_clusterid_2_linkid = {clusterid: linkid for linkid, clusterid in enumerate(cluster_id_list)}
    return dict_linkid_2_clusterid, dict_clusterid_2_linkid





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
                dbc.Col(width=3),
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
                        html.H2("Step 3: Perform Cluster Analysis", className='text-center'),
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



                        dbc.Row(html.H2("Species Tanglegram"),style={'textAlign': 'center'}),
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
                            id='modal_tanglegram',
                            centered=True,
                            size='xl',
                            #fullscreen=True,
                            is_open=False,
                            style={"max-width": "none", "width": "90%"}
                        ),
                        html.H2("Clustergram", className='text-center'),
                        html.Div(
                            dbc.Button(
                                'Download Clustergram Core Matrix',
                                id='button_tree_download',
                            ),
                            className="d-grid gap-2 col-3 mx-auto",
                        ),
                        dcc.Download(id="download_tree"),
                        dcc.Store(id='store_tree'),
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
        Output(component_id='tree_clustergram_graph',component_property="figure"),
        Output(component_id='Img_tanglegram',component_property="src"),
        Output(component_id='modal_Img_tanglegram',component_property="src"),
        Output(component_id='store_tree',component_property='data')
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
    raw_data_clustergram_panda=pd.read_json(response.json(),orient='records')

    clustergram_panda=pd.read_json(response.json(),orient='records')
    clustergram_panda=clustergram_panda.loc[
        :,
        (clustergram_panda.max()-clustergram_panda.min())>200
    ]
    clustergram_panda=clustergram_panda/clustergram_panda.max()
    clustergram_panda=np.log(clustergram_panda)

    clustergram_panda.index=input_metadata.triplet_id.tolist()

    #print(compound_bin_translator_dict)
    clustergram_panda.rename(mapper=compound_bin_translator_dict, axis='columns',inplace=True)
    print(clustergram_panda)
    print([column_name for column_name in clustergram_panda.columns.tolist() if ( str(column_name).isnumeric()==True )])
    clustergram_panda.drop([column_name for column_name in clustergram_panda.columns.tolist() if ( str(column_name).isnumeric()==True )],axis='columns',inplace=True)


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
    #rows = list(clustergram_panda.index)
    rows=input_metadata.triplet_id.tolist()

    print(clustergram_panda)

    print('about to make clustergram')
    clustergram_figure = dashbio.Clustergram(
        # data=clustergram_panda.loc[rows].values,
        data=np.where(
            clustergram_panda.loc[rows].values<=-4,
            0,
            4+clustergram_panda.loc[rows].values,
        ),
        row_labels=[element[0:40] for element in rows],
        column_labels=columns,
        #height=40*len(rows),
        height=1000,
        width=2000,
        #cluster='row',
        optimal_leaf_order=False,
        standardize='none',
        center_values=False,
        # color_map= [
        #     [0.0, '#FFFFFF'],
        #     [1.0, '#008B8B']
        #     # [0.0, '#008B8B'],
        #     # [1.0, '#FFFFFF']
        # ]
        color_map=[
            [0.0,"#05061b"],
            [0.010101010101010102,"#08081e"],
            [0.020202020202020204,"#0b0920"],
            [0.030303030303030304,"#100b23"],
            [0.04040404040404041,"#130d25"],
            [0.05050505050505051,"#170f28"],
            [0.06060606060606061,"#1a102a"],
            [0.07070707070707072,"#1e122d"],
            [0.08080808080808081,"#211330"],
            [0.09090909090909091,"#251433"],
            [0.10101010101010102,"#281535"],
            [0.11111111111111112,"#2d1738"],
            [0.12121212121212122,"#30173a"],
            [0.13131313131313133,"#34193d"],
            [0.14141414141414144,"#381a40"],
            [0.15151515151515152,"#3c1a42"],
            [0.16161616161616163,"#401b44"],
            [0.17171717171717174,"#431c46"],
            [0.18181818181818182,"#481c48"],
            [0.19191919191919193,"#4b1d4a"],
            [0.20202020202020204,"#501d4c"],
            [0.21212121212121213,"#531e4d"],
            [0.22222222222222224,"#581e4f"],
            [0.23232323232323235,"#5b1e51"],
            [0.24242424242424243,"#601f52"],
            [0.25252525252525254,"#631f53"],
            [0.26262626262626265,"#681f55"],
            [0.27272727272727276,"#6b1f56"],
            [0.2828282828282829,"#701f57"],
            [0.29292929292929293,"#751f58"],
            [0.30303030303030304,"#781f59"],
            [0.31313131313131315,"#7d1f5a"],
            [0.32323232323232326,"#811e5a"],
            [0.33333333333333337,"#861e5b"],
            [0.3434343434343435,"#891e5b"],
            [0.3535353535353536,"#8e1d5b"],
            [0.36363636363636365,"#921c5b"],
            [0.37373737373737376,"#971c5b"],
            [0.38383838383838387,"#9a1b5b"],
            [0.393939393939394,"#9f1a5b"],
            [0.4040404040404041,"#a3195b"],
            [0.4141414141414142,"#a8185a"],
            [0.42424242424242425,"#ab185a"],
            [0.43434343434343436,"#b01759"],
            [0.4444444444444445,"#b51657"],
            [0.4545454545454546,"#b91657"],
            [0.4646464646464647,"#bd1655"],
            [0.4747474747474748,"#c11754"],
            [0.48484848484848486,"#c51852"],
            [0.494949494949495,"#c81951"],
            [0.5050505050505051,"#cd1c4e"],
            [0.5151515151515152,"#cf1e4d"],
            [0.5252525252525253,"#d3214b"],
            [0.5353535353535354,"#d62449"],
            [0.5454545454545455,"#d92847"],
            [0.5555555555555556,"#dc2b46"],
            [0.5656565656565657,"#df2f44"],
            [0.5757575757575758,"#e23442"],
            [0.5858585858585859,"#e43841"],
            [0.595959595959596,"#e73d3f"],
            [0.6060606060606061,"#e8403e"],
            [0.6161616161616162,"#eb463e"],
            [0.6262626262626263,"#ec4a3e"],
            [0.6363636363636365,"#ed503e"],
            [0.6464646464646465,"#ee543f"],
            [0.6565656565656566,"#ef5a41"],
            [0.6666666666666667,"#f05e42"],
            [0.6767676767676768,"#f16445"],
            [0.686868686868687,"#f26747"],
            [0.696969696969697,"#f26d4b"],
            [0.7070707070707072,"#f3714d"],
            [0.7171717171717172,"#f37651"],
            [0.7272727272727273,"#f47c55"],
            [0.7373737373737375,"#f47f58"],
            [0.7474747474747475,"#f4845d"],
            [0.7575757575757577,"#f58860"],
            [0.7676767676767677,"#f58d64"],
            [0.7777777777777778,"#f59067"],
            [0.787878787878788,"#f5966c"],
            [0.797979797979798,"#f59970"],
            [0.8080808080808082,"#f69e75"],
            [0.8181818181818182,"#f6a178"],
            [0.8282828282828284,"#f6a67e"],
            [0.8383838383838385,"#f6a981"],
            [0.8484848484848485,"#f6ae87"],
            [0.8585858585858587,"#f6b18b"],
            [0.8686868686868687,"#f6b691"],
            [0.8787878787878789,"#f6bb97"],
            [0.888888888888889,"#f6be9b"],
            [0.8989898989898991,"#f7c2a2"],
            [0.9090909090909092,"#f7c6a6"],
            [0.9191919191919192,"#f7caac"],
            [0.9292929292929294,"#f7cdb1"],
            [0.9393939393939394,"#f8d1b8"],
            [0.9494949494949496,"#f8d4bc"],
            [0.9595959595959597,"#f8d9c3"],
            [0.9696969696969697,"#f8dcc7"],
            [0.9797979797979799,"#f9e0cd"],
            [0.98989898989899,"#f9e3d2"],
            [1.0,"#fae8d8"],


        ]
    )
    print('made clustergram')
    #print(clu)
    # pprint(clustergram_figure.to_dict())
    #clustergram_figure.update_coloraxes(colorbar_dtick = 1)

    # clustergram_figure.update_layout(yaxis11=dict(coloraxis_colorbar=dict(
    #     title="Population",
    #     tickvals=[0,1,2,3,4],
    #     ticktext=["1M", "10M", "100M", "1B",'10b'],
    # )))
    heatmap_trace=clustergram_figure.data[-1]
    pprint(heatmap_trace)
    heatmap_trace.update(
        colorbar_tickvals=[0,1,2,3,4],
        colorbar_ticktext=['<=Max/10,000','Max/1,000','Max/100','Max/10','Compound Max']
    )


    # clustergram_figure.update_layout(
    #     coloraxis_colorbar=dict(
    #         title="Your Title",
    #     ),        
    # )

    #hold=input('hold')
    #dcc.Graph(id='tree_clustergram_graph',figure=clustergram_figure)

    #output_children=                  
    
    # clustergram_figure = dashbio.Clustergram(
    #     data=clustergram_panda.values,#bins_panda,
    #     row_labels=list(clustergram_panda.index),
    #     column_labels=list(clustergram_panda.columns.values),
    # )
    #volcano.update_layout(showlegend=False)\


    #convert incoming list of triplets into list of species
    incoming_species=[element.split(' - ')[0] for element in input_metadata.triplet_id.tolist()]
    #conver incoming list of species into species IDs
    incoming_species_as_ids=[english_species_to_ncbi_id_dict[element] for element in incoming_species]
    #make a copy of the species networkx
    shallow_copy_of_tanglegram_species=tanglegram_species_nx.copy()
    #delete things that arent requested or directly connecting things that are present
    nodes_to_retain=set()
    for element in incoming_species_as_ids:
        nodes_to_retain=nodes_to_retain.union(
            set(nx.shortest_path(shallow_copy_of_tanglegram_species,source='1',target=element))
        )
    nodes_to_remove=set(shallow_copy_of_tanglegram_species.nodes)-nodes_to_retain
    [shallow_copy_of_tanglegram_species.remove_node(element) for element in nodes_to_remove]
    
    
    incoming_species_as_ids_set=set(incoming_species_as_ids)
    all_remaining_nodes_set={element for element in shallow_copy_of_tanglegram_species.nodes}
    non_requested_nodes=all_remaining_nodes_set-incoming_species_as_ids_set
    incoming_species_as_ids_unique_list=list(incoming_species_as_ids_set)
    nodes_ordered_by_requested_then_necessary=incoming_species_as_ids_unique_list+list(non_requested_nodes)
    #nodes_ordered_by_requested_then_necessary=incoming_species_as_ids+list(non_requested_nodes)
    print(nodes_to_retain)
    print('!@#'*30)
    #run https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy.html#networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy
    # be sure to use the subgraph
    #  
    #so that we can subset the subgraph distance matrix
    #non_requested_nodes=
    #{element for element in shallow_copy_of_tanglegram_species.nodes}
    remaining_nodes_ordered=[element for element in shallow_copy_of_tanglegram_species.nodes]
    print(incoming_species_as_ids)
    print(remaining_nodes_ordered)
    subgraph_distance_matrix=nx.floyd_warshall_numpy(shallow_copy_of_tanglegram_species.to_undirected(),nodelist=nodes_ordered_by_requested_then_necessary)
    print(subgraph_distance_matrix)
    print(type(subgraph_distance_matrix))
    #print(subgraph_distance_matrix[[0,2],[0,2]])
    print(subgraph_distance_matrix[0:len(incoming_species_as_ids_set),0:len(incoming_species_as_ids_set)])

    core_subgraph=pd.DataFrame(
        subgraph_distance_matrix[0:len(incoming_species_as_ids_set),0:len(incoming_species_as_ids_set)],
        columns=incoming_species_as_ids_unique_list,
        index=incoming_species_as_ids_unique_list
    )
    print(core_subgraph)


    subgraph_with_multiple_instance_of_same_species=pd.DataFrame(
        data=0,
        #columns=input_metadata.triplet_id.tolist(),
        #index=input_metadata.triplet_id.tolist()
        columns=incoming_species_as_ids,
        index=incoming_species_as_ids
    )
    print(subgraph_with_multiple_instance_of_same_species)

    #yes i know this isnt fast but have you ever tried being the sole grad student developer
    for row_index in subgraph_with_multiple_instance_of_same_species.index:
        for column_index in subgraph_with_multiple_instance_of_same_species.columns:
            subgraph_with_multiple_instance_of_same_species.at[row_index,column_index]=core_subgraph.at[row_index,column_index]

    
    print(subgraph_with_multiple_instance_of_same_species)
    subgraph_with_multiple_instance_of_same_species.columns=input_metadata.triplet_id.tolist()
    subgraph_with_multiple_instance_of_same_species.index=input_metadata.triplet_id.tolist()
    print(subgraph_with_multiple_instance_of_same_species)
    #ncbi_distance_matrix_for_tanglegram=subgraph_distance_matrix[0:len(incoming_species_as_ids_set),0:len(incoming_species_as_ids_set)]
    #the below isnt necessarily true
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

    metabolomics_oriented_distance_matrix=cdist(
        XA=clustergram_panda,
        XB=clustergram_panda,
        #the clustergram default
        metric='euclidean',
    )

    metabolomics_oriented_distance_matrix_panda=pd.DataFrame(
        data=metabolomics_oriented_distance_matrix,
        columns=input_metadata.triplet_id.tolist(),
        index=input_metadata.triplet_id.tolist()
    )


    #visualize_nodes_on_a_list(shallow_copy_of_tanglegram_species,[],None)
    #nx.draw(shallow_copy_of_tanglegram_species,with_labels=True)
    #plt.show()
    #fig = plt.figure(figsize=(5, 5),dpi=200)
    #fig,ax=plt.subplots(figsize=(5,5),dpi=200)
    #metabolomics_oriented_dendrogram=dendrogram(metabolomics_oriented_linkage_matrix,ax=ax)
    start=time()
    fig,RHS_dendro_R,RHS_linkage,RHS_linkage_pre_sort,ax2=tangle_modified.plot(
        metabolomics_oriented_distance_matrix_panda, 
        subgraph_with_multiple_instance_of_same_species, 
        #sort='step2side',
        sort='random',
        figsize=(20,10),
        leaf_rotation=0,
        dend_kwargs={
            'color_threshold':0,
            'truncate_mode':None,
            'count_sort':'ascending'
            #'leaf_rotation':45
        },
        sort_kwargs={
            #'max_n_iterations':300
            'R':300
        },
        link_kwargs={
            'method':'average',
            #'optimal_ordering':True
        }       
        )



    #ax2.text(1,1,'hi there')

    pprint(RHS_dendro_R)
    for temp_key in RHS_dendro_R.keys():
        print(temp_key)
        print(len(RHS_dendro_R[temp_key]))


    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    pprint(RHS_dendro_R)
    print('=====================================================')
    pprint(RHS_linkage_pre_sort)
    pprint(RHS_linkage)
    dict_1,dict_2=get_linkid_clusterid_relation(RHS_linkage)
    pprint(dict_1)
    pprint(dict_2)


    dendro_u_to_species_dict=return_leaf_elements_for_each_dendro_u(
        dict_1,
        RHS_linkage,
        incoming_species_as_ids
    )

    dendro_u_to_parent_node_dict=return_parent_node_for_species_grouping(
        dendro_u_to_species_dict,
        shallow_copy_of_tanglegram_species
    )
    print(dendro_u_to_parent_node_dict)
    #dendro_u_to_words_we_display_dict=return_

    #we want dict 1
    #for each u element (icoord,dcoor paired lists)
    #access the proper row in the linkage matrix
    far_right_x_value=0
    for element in RHS_dendro_R['dcoord']:
        if max(element)>far_right_x_value:
            far_right_x_value=max(element)
    for i in range(len(RHS_dendro_R['dcoord'])):
        if RHS_dendro_R['dcoord'][i][1]==far_right_x_value and RHS_dendro_R['dcoord'][i][2]==far_right_x_value:
            continue
        x_value=RHS_dendro_R['dcoord'][i][1]
        y_value=(RHS_dendro_R['icoord'][i][1]+RHS_dendro_R['icoord'][i][2])/2
        ax2.text(x_value,y_value,dendro_u_to_parent_node_dict[i])
    #plt.show()

    print('=====================================================')

    end=time()
    print(f'{end-start} seconds to optimize the tangle')
    buf=io.BytesIO()
    plt.savefig(buf, format = "png")
    plt.close('all')
    #plt.clf()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    plotly_fig="data:image/png;base64,{}".format(data)
    buf.close()

    clustergram_panda.index=input_metadata.triplet_id.tolist()
    print(clustergram_panda)
    return [clustergram_figure,plotly_fig,plotly_fig,raw_data_clustergram_panda.to_dict(orient='index')]


def return_parent_node_for_species_grouping(dendro_u_to_species_dict,shallow_copy_of_tanglegram_species):
    '''
    '''
    output_dict=dict()
    # nx.draw(shallow_copy_of_tanglegram_species,with_labels=True)
    # plt.show()
    for temp_key in dendro_u_to_species_dict.keys():
        #get all common ancestor pairs
        #choose the output that is closest to the root
        #literally cant believe that LCA of {n} isnt available
        print('^'*50)
        print(dendro_u_to_species_dict[temp_key])
        pairs=list(combinations([str(element) for element in dendro_u_to_species_dict[temp_key]],2))
        print('the pairs are')
        print(pairs)
        #print(shallow_copy_of_tanglegram_species.nodes[pairs[0][0]])
        if len(pairs)==0:
            #output_dict[temp_key]='skip_single_species'
            output_dict[temp_key]=str(dendro_u_to_species_dict[temp_key].pop())
        else:
            temp_lcas=dict(
                nx.tree_all_pairs_lowest_common_ancestor(
                    shallow_copy_of_tanglegram_species,
                    pairs=pairs
                )
            )
            print(dict(temp_lcas))
            #node_id_list=[element[1] for element in list(temp_lcas)]
            node_id_list=list(temp_lcas.values())
            distance_from_root=[len(nx.shortest_path(shallow_copy_of_tanglegram_species,source='1',target=element)) for element in node_id_list]
            print('distance from root')
            print(distance_from_root)
            index_of_highest_up=distance_from_root.index(min(distance_from_root))
            print(index_of_highest_up)
            node_id_of_highest_up=node_id_list[index_of_highest_up]
            output_dict[temp_key]=node_id_of_highest_up

    print('~!@'*50)
    pprint(output_dict)
    output_dict_strings=dict()
    for temp_element in output_dict.keys():
        output_dict_strings[temp_element]=shallow_copy_of_tanglegram_species.nodes[output_dict[temp_element]]['rank']+': '+shallow_copy_of_tanglegram_species.nodes[output_dict[temp_element]]['scientific_name']

    return output_dict_strings
    #print(output_dict)


def return_leaf_elements_for_each_dendro_u(
    u_to_linkage_mapping_dict,
    linkage_matrix,
    singleton_elements
):
    
    
    

    top_half_of_linkage=np.array(
        [
            [int(element),int(element),-1,1] for element in singleton_elements
        ]
    )

    number_of_singletons=len(singleton_elements)
    #we need to boost the u_to_linkage_mapping_dict by number of singletons when we combine to full linkage
    u_to_linkage_mapping_dict_boosted=dict()
    for temp_key in u_to_linkage_mapping_dict:
        u_to_linkage_mapping_dict[temp_key]=number_of_singletons+u_to_linkage_mapping_dict[temp_key]
    #u_to_linkage_mapping_dict_boosted={temp_key:=(number_of_singletons+u_to_linkage_mapping_dict[temp_key] for temp_key in u_to_linkage_mapping_dict}
    print(u_to_linkage_mapping_dict_boosted)

    full_linkage_matrix=np.vstack((top_half_of_linkage,linkage_matrix))
    full_linkage_matrix=full_linkage_matrix.astype(int)
    output_dict=dict()    

    print('about to find out what the linkage elements are')
    pprint(full_linkage_matrix)
    pprint(u_to_linkage_mapping_dict)



    for temp_key in u_to_linkage_mapping_dict.keys():
        current_linkage_row=u_to_linkage_mapping_dict[temp_key]
        current_u_key_singletons=list()

        print(f'about to hop into recursion to find the children of {current_linkage_row}')
        current_u_key_singletons=set(recursively_determine_membership_for_single_cluster(full_linkage_matrix,current_u_key_singletons,current_linkage_row,number_of_singletons))
        output_dict[temp_key]=current_u_key_singletons
        result_list=list()

    pprint(output_dict)
    print('~!hi~!'*10)
    return output_dict


def recursively_determine_membership_for_single_cluster(full_linkage,result_list,row_to_check,number_of_singletons):
    '''
    
    '''
    #if we reach a core singleton
    if full_linkage[row_to_check][3]==1:
        #print(result_list)
        #print(full_linkage[row_to_check][0])
        #result_list+=[full_linkage[row_to_check][0]]
        print(result_list)
        #return [full_linkage[row_to_check][0]]
        result_list+=[full_linkage[row_to_check][0]]
        return result_list

    else:
        print('doing recursion')
        print(f'we are checking row {row_to_check}')
        # result_list+=recursively_determine_membership_for_single_cluster(full_linkage,result_list,full_linkage[row_to_check][0],number_of_singletons)
        # result_list+=recursively_determine_membership_for_single_cluster(full_linkage,result_list,full_linkage[row_to_check][1],number_of_singletons)
        # return result_list
        result_list=recursively_determine_membership_for_single_cluster(full_linkage,result_list,full_linkage[row_to_check][0],number_of_singletons)
        result_list=recursively_determine_membership_for_single_cluster(full_linkage,result_list,full_linkage[row_to_check][1],number_of_singletons)
        return result_list


@callback(
    [
        Output(component_id="download_tree", component_property="data"),
    ],
    [
        Input(component_id="button_tree_download", component_property="n_clicks"),
    ],
    [
        #State(component_id="leaf_table",component_property="data"),
        State(component_id='store_tree',component_property='data')
    ],
    prevent_initial_call=True
)
def download_leaf_datatable(
    button_tree_download_n_clicks,
    store_tree_data
    ):
#         """
#         """
#         #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

#         #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
#         print(pd.DataFrame.from_records(table_data).to_excel)

        downloaded_panda=pd.DataFrame.from_dict(store_tree_data,orient='index')
        # print(store_tree_data)
        # print(downloaded_panda)

#         if radio_items_bin_type_value!='class':
#             downloaded_panda['english_name']=downloaded_panda['english_name'].str.extract('\[(.*)\]')
#             downloaded_panda['identifier']=downloaded_panda['identifier'].str.extract('\[(.*)\]')
#             # total_panda['english_name']='['+total_panda['english_name']+'](/sunburst/'+total_panda['compound_id'].astype(str)+')'
#             # total_panda['identifier']='['+total_panda['identifier']+'](/bin-browser/'+total_panda['compound_id'].astype(str)+')'

    
#         # temp['english_name']=temp['english_name'].str.extract('\[(.*)\]')

        return [dcc.send_data_frame(
            downloaded_panda.to_excel, "binvestigate_phylo_metabolomic_datatable.xlsx", sheet_name="sheet_1"
        )]





@callback(
    [
        Output(component_id='modal_tanglegram', component_property='is_open'),
    ],
    [
        Input(component_id='Img_tanglegram', component_property='n_clicks'),
    ],
    prevent_initial_call=True
)
def open_modal(Img_tanglegram_n_clicks):
    return [True]
