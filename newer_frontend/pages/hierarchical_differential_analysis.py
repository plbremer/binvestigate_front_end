import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio
from . import hierarchical_differential_analysis_helper
import networkx as nx

dash.register_page(__name__)

base_url_api = "http://127.0.0.1:4999/"

########get things from helper script########
species_networkx,species_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_species()
organ_networkx,organ_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_organ()
disease_networkx,disease_node_dict=hierarchical_differential_analysis_helper.extract_networkx_selections_disease()
index_panda=pd.read_pickle('../newer_datasets/index_panda.bin')
index_panda=index_panda.sort_index()
index_panda['species']=index_panda['species'].astype(str)
print(index_panda)
print(index_panda.dtypes)
#############################################

#layout = html.Div(children=[
layout = dbc.Container(children=[
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
            dbc.Col(
                children=[
                    html.H2("From Triplet", className='text-center'),
                    dcc.Dropdown(
                        id='dropdown_from_species',
                        options=sorted([
                            {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ),  
                    dcc.Dropdown(
                        id='dropdown_from_organ',
                        options=sorted([
                            {'label':organ_node_dict[temp], 'value':temp.title()} for temp in organ_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ), 
                    dcc.Dropdown(
                        id='dropdown_from_disease',
                        options=sorted([
                            {'label':disease_node_dict[temp], 'value':temp.title()} for temp in disease_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ), 
                    html.Br(),
                ],
                width={'size':3}
            ),
            dbc.Col(
                children=[
                    html.Br(),
                    html.Br(),
                    html.H2("Vs.", className='text-center'),
                    html.Br(),
                ],
                width={'size':1}
            ),
            dbc.Col(
                children=[
                    html.H2("To Triplet", className='text-center'),
                    dcc.Dropdown(
                        id='dropdown_to_species',
                        options=sorted([
                            {'label':species_node_dict[temp], 'value':temp.title()} for temp in species_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ),  
                    dcc.Dropdown(
                        id='dropdown_to_organ',
                        options=sorted([
                            {'label':organ_node_dict[temp], 'value':temp.title()} for temp in organ_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ), 
                    dcc.Dropdown(
                        id='dropdown_to_disease',
                        options=sorted([
                            {'label':disease_node_dict[temp], 'value':temp.title()} for temp in disease_node_dict
                        ],key=lambda x:x['label']),
                        multi=False,
                    ), 
                    html.Br(),
                ],
                width={'size':3}
            ),
            dbc.Col(
                children=[
                    html.Br(),
                    html.Br(),
                ],
                width={'size':2}
            ),
            dbc.Col(
                children=[
                    html.H2("Options", className='text-center'),
                    html.H6("Choose Statistical Approach for Volcano", className='text-center'),
                    html.Div(className="radio-group-container add-margin-top-1", children=[
                        html.Div(className="radio-group", children=[
                            dbc.RadioItems(
                                id='radio_items_fold_type',
                                options=[
                                    {'label': 'Average/Welch', 'value': 'average_welch'},
                                    {'label': 'Median/MWU', 'value': 'median_mwu'},
                                    #{'label': 'Unique', 'value': 'unique'},
                                ],         
                                value='average_welch',
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                inputCheckedClassName="active",                                
                            ),
                        ])
                    ]),
                    html.H6("Choose Compound Result Type", className='text-center'),
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
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H2("Execute or Update Query", className='text-center'),
                    html.Div(
                        dbc.Button(
                            'Get Results',
                            id='hgda_query',
                        ),
                        className="d-grid gap-2 col-6 mx-auto",
                    ),
                ],
                width={'size':9}
            ),
            dbc.Col(
                children=[
                    html.H2("Describe Triplets", className='text-center'),
                    html.Div(
                        dbc.Button(
                            'Get Results',
                            id='hgda_metadata_query',
                        ),
                        className="d-grid gap-2 col-6 mx-auto",
                    ),
                ],
                width={'size':3}
            )
        ],
        #justify='center'
    ),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    #html.H2("Venn Comparator", className='text-center'),
                    dcc.Graph(
                        id='leaf_figure'
                    )
                ],
                width={'size':9}
            ),
            dbc.Col(
                children=[
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
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        style_cell={
                            'font-family':'sans-serif'
                        }
                    )
                ],
                width={'size':3}
            )
        ],
        #justify='center'
    ),
    html.Br(),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
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
                            {"name": "English Name", "id": "english_name"},
                            {"name": "Identifier", "id": "identifier"},
                            {"name": "Fold Average", "id": "fold_change_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                            {"name": "Significance Welch", "id": "significance_welch","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                            {"name": "Fold Median", "id": "fold_change_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
                            {"name": "Significance MWU", "id": "significance_mwu","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
                        ],
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
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        style_cell={
                            'font-family':'sans-serif'
                        }
                    )
                ],
                #width={'size':6}
            )
        ],
        #justify='center'
    ),
])


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
    print('here')
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
        {'label':organ_node_dict[temp], 'value':temp.title()} for temp in organ_node_dict if temp in all_valid_organ_options
    ],key=lambda x:x['label'])

    disease_options=sorted([
        {'label':disease_node_dict[temp], 'value':temp.title()} for temp in disease_node_dict if temp in all_valid_disease_options
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
    print('here')
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
        {'label':organ_node_dict[temp], 'value':temp.title()} for temp in organ_node_dict if temp in all_valid_organ_options
    ],key=lambda x:x['label'])

    disease_options=sorted([
        {'label':disease_node_dict[temp], 'value':temp.title()} for temp in disease_node_dict if temp in all_valid_disease_options
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

    print(total_panda)

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
        State(component_id="dropdown_from_species", component_property="value"),
        State(component_id="dropdown_from_organ", component_property="value"),
        State(component_id="dropdown_from_disease", component_property="value"),
        State(component_id="dropdown_to_species", component_property="value"),
        State(component_id="dropdown_to_organ", component_property="value"),
        State(component_id="dropdown_to_disease", component_property="value"),
        State(component_id='radio_items_bin_type',component_property='value')
    ],
    prevent_initial_call=True
)
def query_table(
    query,
    from_species_value,
    from_organ_value,
    from_disease_value,
    to_species_value,
    to_organ_value,
    to_disease_value,
    radio_items_bin_type_value
):
    json_output = {
        "from_species": from_species_value,
        "from_organ": from_organ_value,
        "from_disease": from_disease_value,
        "to_species": to_species_value,
        "to_organ": to_organ_value,
        "to_disease": to_disease_value,
    }
    #obtain results from api
    response = requests.post(base_url_api + "/hgdaresource/", json=json_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)

    total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    data = total_panda.to_dict(orient='records')

    return [data]