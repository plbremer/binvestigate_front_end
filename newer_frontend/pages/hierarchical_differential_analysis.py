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

dash.register_page(__name__)

#base_url_api = f"http://api_alias:4999/"
base_url_api = "http://127.0.0.1:4999/"
#base_url_api = "http://172.18.0.3:4999/"

########get things from helper script########
species_networkx,species_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_species()
organ_networkx,organ_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_organ()
disease_networkx,disease_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_disease()
index_panda=pd.read_pickle('../newer_datasets/index_panda.bin')
index_panda=index_panda.sort_index()
index_panda['species']=index_panda['species'].astype(str)
#print(index_panda)
#print(index_panda.dtypes)
compound_translation_panda=pd.read_pickle('../newer_datasets/compound_translation_panda.bin')
hyperlink_translation_dict=dict(zip(compound_translation_panda.integer_representation.tolist(),compound_translation_panda.compound_identifier.tolist()))
del compound_translation_panda
#############################################

#layout=dbc.Container(
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
                            id='dropdown_from_species',
                            options=sorted([
                                {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select species ontology node'
                        ),  
                        dcc.Dropdown(
                            id='dropdown_from_organ',
                            options=sorted([
                                {'label':organ_node_dict[temp], 'value':temp} for temp in organ_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select organ ontology node'
                        ), 
                        dcc.Dropdown(
                            id='dropdown_from_disease',
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
                # dbc.Col(
                #     children=[
                #         html.Br(),
                #         html.Br(),
                #         html.H2("Vs.", className='text-center'),
                #         html.Br(),
                #     ],
                #     width={'size':1}
                # ),
                dbc.Col(
                    children=[
                        #html.H2("To Triplet", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_to_species',
                            options=sorted([
                                {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select species ontology node'
                        ),  
                        dcc.Dropdown(
                            id='dropdown_to_organ',
                            options=sorted([
                                {'label':organ_node_dict[temp], 'value':temp} for temp in organ_node_dict
                            ],key=lambda x:x['label']),
                            multi=False,
                            placeholder='Select organ ontology node'
                        ), 
                        dcc.Dropdown(
                            id='dropdown_to_disease',
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
                # dbc.Col(
                #     children=[
                #         html.Br(),
                #         html.Br(),
                #     ],
                #     width={'size':2}
                # ),
                dbc.Col(
                    children=[
                        #html.H2("Options", className='text-center'),
                        # html.H6("Choose Statistical Approach for Volcano", className='text-center'),
                        # html.Div(className="radio-group-container add-margin-top-1", children=[
                        #     html.Div(className="radio-group", children=[
                        #         dbc.RadioItems(
                        #             id='radio_items_fold_type',
                        #             options=[
                        #                 {'label': 'Average/Welch', 'value': 'average_welch'},
                        #                 {'label': 'Median/MWU', 'value': 'median_mwu'},
                        #                 #{'label': 'Unique', 'value': 'unique'},
                        #             ],         
                        #             value='average_welch',
                        #             className="btn-group",
                        #             inputClassName="btn-check",
                        #             labelClassName="btn btn-outline-primary",
                        #             inputCheckedClassName="active",                                
                        #         ),
                        #     ])
                        # ]),
                        # html.Br(),
                        # html.H6("Choose Compound Result Type", className='text-center'),
                        html.Div(className="radio-group-container add-margin-top-1", children=[
                            html.Div(className="radio-group", children=[
                                dbc.RadioItems(
                                    id='radio_items_bin_type',
                                    options=[
                                        {'label': 'Knowns', 'value': 'known'},
                                        {'label': 'Classes', 'value': 'class'},
                                        {'label': 'Unknowns', 'value': 'unknown'},
                                    ],         
                                    value='known',
                                    className="btn-group",
                                    inputClassName="btn-check",
                                    labelClassName="btn btn-outline-primary",
                                    inputCheckedClassName="active",                                
                                ),
                            ])
                        ]),
                    ],
                    width={'size':3}
                ),
            ],
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
                                id='hgda_metadata_query',
                            ),
                            className="d-grid gap-2 col-3 mx-auto",
                        ),
                        #html.H2("Venn Comparator", className='text-center'),
                        dash_table.DataTable(
                            id='hgda_table_metadata',
                            columns=[
                                {'name': 'From or To', 'id': 'from_or_to'},
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
                                id='hgda_query',
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
        dbc.Row(
            children=[
                dbc.Col(width={'size':2}),
                dbc.Col(
                    dbc.Spinner(
                        children=[
                            #html.H2("Venn Comparator", className='text-center'),
                            dcc.Graph(
                                id='hgda_figure'
                            ),
                            html.H2("Result Datatable", className='text-center'),
                            html.Div(
                                dbc.Button(
                                    'Download Datatable as .xlsx',
                                    id='button_download',
                                ),
                                className="d-grid gap-2 col-3 mx-auto",
                            ),
                            dcc.Download(id="download_hgda_datatable"),
                            dash_table.DataTable(
                                id='hgda_table',
                                columns=[
                                    {"name": "English Name", "id": "english_name",'presentation':'markdown'},
                                    {"name": "Identifier", "id": "identifier",'presentation':'markdown'},
                                    {"name": "Fold Average", "id": "fold_change_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                                    {"name": "Significance Welch", "id": "significance_welch","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                                #    {"name": "Fold Median", "id": "fold_change_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                                #    {"name": "Significance MWU", "id": "significance_mwu","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
                                ],
                                markdown_options={"link_target": "_blank"},
                                data=[],
                                page_current=0,
                                page_size=50,
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
                            )
                        ],
                    ),

                    width={'size':8}
                ),
                dbc.Col(width={'size':2}),
                
            ],
            #justify='center'
        ),
        html.Br(),
        html.Br(),
        # dbc.Row(
        #     children=[
        #         dbc.Col(width={'size':2}),
        #         dbc.Col(
        #             children=[
        #                 html.H2("Result Datatable", className='text-center'),
        #                 html.Div(
        #                     dbc.Button(
        #                         'Download Datatable as .xlsx',
        #                         id='button_download',
        #                     ),
        #                     className="d-grid gap-2 col-3 mx-auto",
        #                 ),
        #                 dcc.Download(id="download_hgda_datatable"),
        #                 dash_table.DataTable(
        #                     id='hgda_table',
        #                     columns=[
        #                         {"name": "English Name", "id": "english_name"},
        #                         {"name": "Identifier", "id": "identifier"},
        #                         {"name": "Fold Average", "id": "fold_change_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        #                         {"name": "Significance Welch", "id": "significance_welch","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        #                         {"name": "Fold Median", "id": "fold_change_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
        #                         {"name": "Significance MWU", "id": "significance_mwu","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
        #                     ],
        #                     data=[],
        #                     page_current=0,
        #                     page_size=50,
        #                     #page_action='custom',
        #                     page_action='native',
        #                     #sort_action='custom',
        #                     sort_action='native',
        #                     sort_mode='multi',
        #                     #sort_by=[],
        #                     #filter_action='custom',
        #                     filter_action='native',
        #                     #filter_query='',
        #                     style_header={
        #                         'backgroundColor': 'rgb(30, 30, 30)',
        #                         'color': 'white'
        #                     },
        #                     style_data={
        #                         'backgroundColor': 'rgb(50, 50, 50)',
        #                         'color': 'white'
        #                     },
        #                     style_cell={
        #                         'font-family':'sans-serif'
        #                     }
        #                 )
        #             ],
        #             #width={'size':6}
        #         ),
        #         dbc.Col(width={'size':2}),
        #     ],
        # #justify='center'
        # ),
    ]
)


@callback(
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
    prevent_initial_call=True
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
    # print('here')
    #determine valid species options
    temp_view=index_panda.copy()
    if from_species_value_input!=None:
        temp_set=nx.algorithms.dag.descendants(species_networkx,from_species_value_input)
        temp_set.add(from_species_value_input)
        temp_view=temp_view.loc[
            temp_view.species.isin(temp_set)
        ]

    if from_organ_value_input!=None:
        temp_set=nx.algorithms.dag.descendants(organ_networkx,from_organ_value_input)
        temp_set.add(from_organ_value_input)
        temp_view=temp_view.loc[
            temp_view.organ.isin(temp_set)
        ]

    if from_disease_value_input!=None:
        temp_set=nx.algorithms.dag.descendants(disease_networkx,from_disease_value_input)
        temp_set.add(from_disease_value_input)
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
        Output(component_id="dropdown_to_species", component_property="options"),
        Output(component_id="dropdown_to_organ", component_property="options"),
        Output(component_id="dropdown_to_disease", component_property="options"),
    ],
    [
        Input(component_id="dropdown_to_species", component_property="value"),
        Input(component_id="dropdown_to_organ", component_property="value"),
        Input(component_id="dropdown_to_disease", component_property="value"),
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
        Output(component_id="hgda_table_metadata", component_property="data")
    ],
    [
        Input(component_id="hgda_metadata_query", component_property="n_clicks"),
    ],
    [
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),
    ],
    prevent_initial_call=True
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
    response = requests.post(base_url_api + "/hgdametadataresource/", json=metadata_json_output)
    total_panda = pd.read_json(response.json(), orient="records")

    #print(total_panda)

    data = total_panda.to_dict(orient='records')

    return [data]

@callback(
    [
        #Output(component_id="leaf_table", component_property="columns"),
        Output(component_id="hgda_table", component_property="data")
    ],
    [
        Input(component_id='hgda_query', component_property='n_clicks'),
    ],
    [
        # State(component_id="dropdown_from_species", component_property="value"),
        # State(component_id="dropdown_from_organ", component_property="value"),
        # State(component_id="dropdown_from_disease", component_property="value"),
        # State(component_id="dropdown_to_species", component_property="value"),
        # State(component_id="dropdown_to_organ", component_property="value"),
        # State(component_id="dropdown_to_disease", component_property="value"),
        State(component_id='radio_items_bin_type',component_property='value'),
        State(component_id='hgda_table_metadata', component_property='derived_virtual_data')
    ],
    prevent_initial_call=True
)
def query_table(
    query,
    # from_species_value,
    # from_organ_value,
    # from_disease_value,
    # to_species_value,
    # to_organ_value,
    # to_disease_value,
    radio_items_bin_type_value,
    hgda_table_metadata_derived_virtual_data
):
    json_output = {
        # "from_species": from_species_value,
        # "from_organ": from_organ_value,
        # "from_disease": from_disease_value,
        # "to_species": to_species_value,
        # "to_organ": to_organ_value,
        # "to_disease": to_disease_value,
        'metadata_datatable':hgda_table_metadata_derived_virtual_data,
        "bin_type":radio_items_bin_type_value
    }
    #obtain results from api
    response = requests.post(base_url_api + "/hgdaresource/", json=json_output)
    total_panda = pd.read_json(response.json(), orient="records")
    #print(total_panda)
    if radio_items_bin_type_value!='class':
        total_panda['compound_id']=total_panda['compound_id'].map(hyperlink_translation_dict.get)
        total_panda['english_name']='['+total_panda['english_name']+'](/sunburst/'+total_panda['compound_id'].astype(str)+')'
        total_panda['identifier']='['+total_panda['identifier']+'](/bin-browser/'+total_panda['compound_id'].astype(str)+')'
    # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    data = total_panda.to_dict(orient='records')

    return [data]












@callback(
    [
        Output(component_id='hgda_figure', component_property='figure'),
    ],
    [
        Input(component_id='hgda_table', component_property='derived_virtual_data'),
        #Input(component_id='radio_items_fold_type',component_property='value')
    ],
    [
        State(component_id='dropdown_from_species',component_property='value'),
        State(component_id='dropdown_from_organ',component_property='value'),
        State(component_id='dropdown_from_disease',component_property='value'),
        State(component_id='dropdown_to_species',component_property='value'),
        State(component_id='dropdown_to_organ',component_property='value'),
        State(component_id='dropdown_to_disease',component_property='value'),
        State(component_id='radio_items_bin_type',component_property='value'),

    ],
    prevent_initial_call=True
)
def query_figure(hgda_table_derived_virtual_data,#radio_items_fold_type_value,
    dropdown_from_species_value,
    dropdown_from_organ_value,
    dropdown_from_disease_value,
    dropdown_to_species_value,
    dropdown_to_organ_value,
    dropdown_to_disease_value,
    radio_items_bin_type_value
):

    #get dataframe from derived data
    temp=pd.DataFrame.from_records(hgda_table_derived_virtual_data)
    #print(temp)
    #print(temp.columns[-1])

    if radio_items_bin_type_value!='class':
        temp['english_name']=temp['english_name'].str.extract('\[(.*)\]')


    #if radio_items_fold_type_value=='average_welch':
    p='significance_welch'
    effect_size='fold_change_average'
    #elif radio_items_fold_type_value=='median_mwu':
    #    p='significance_mwu'
    #    effect_size='fold_change_median'
        
    title_string_from=' - '.join([species_node_dict[dropdown_from_species_value],organ_node_dict[dropdown_from_organ_value].split(' - ')[0],disease_node_dict[dropdown_from_disease_value].split(' - ')[0]])
    title_string_to=' - '.join([species_node_dict[dropdown_to_species_value],organ_node_dict[dropdown_to_organ_value].split(' - ')[0],disease_node_dict[dropdown_to_disease_value].split(' - ')[0]])

    volcano = dashbio.VolcanoPlot(
        dataframe=temp,#bins_panda,
        snp="english_name",
        p=p,
        effect_size=effect_size,
        gene=None,
        xlabel='log2 Fold Change - negative values are decreases from \"'+title_string_from+'\" to \"'+title_string_to+'\"',
        genomewideline_value=2,
        title=title_string_from+'        vs.       '+title_string_to,
        title_x=0.5
    )
    volcano.update_layout(showlegend=False)

    return [volcano]


@callback(
    [
        Output(component_id="download_hgda_datatable", component_property="data"),
    ],
    [
        Input(component_id="button_download", component_property="n_clicks"),
    ],
    [
        State(component_id="hgda_table",component_property="data"),
        State(component_id='radio_items_bin_type',component_property='value')
    ],
    prevent_initial_call=True
)
def download_hgda_datatable(
    download_click,
    table_data,
    radio_items_bin_type_value
    ):
        """
        """
        #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
        #print(pd.DataFrame.from_records(table_data).to_excel)

        downloaded_panda=pd.DataFrame.from_records(table_data)

        if radio_items_bin_type_value!='class':
            downloaded_panda['english_name']=downloaded_panda['english_name'].str.extract('\[(.*)\]')
            downloaded_panda['identifier']=downloaded_panda['identifier'].str.extract('\[(.*)\]')
            # total_panda['english_name']='['+total_panda['english_name']+'](/sunburst/'+total_panda['compound_id'].astype(str)+')'
            # total_panda['identifier']='['+total_panda['identifier']+'](/bin-browser/'+total_panda['compound_id'].astype(str)+')'

    
        # temp['english_name']=temp['english_name'].str.extract('\[(.*)\]')

        return [dcc.send_data_frame(
            downloaded_panda.to_excel, "binvestigate_differential_datatable.xlsx", sheet_name="sheet_1"
        )]
