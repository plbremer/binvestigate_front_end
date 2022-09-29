import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from . import venn_helper
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio

dash.register_page(__name__)

base_url_api = "http://127.0.0.1:4999/"

########get things from helper script########
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
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
                        id='dropdown_triplet_selection_from',
                        options=sorted([
                            {'label': temp.title(), 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                        ],key=lambda x:x['label']),
                        multi=True,
                        # style={
                        #     'color': '#212121',
                        #     'background-color': '#3EB489',
                        # }
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
                        id='dropdown_triplet_selection_to',
                        options=sorted([
                            {'label': temp.title(), 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                        ],key=lambda x:x['label']),
                        multi=True,
                        # style={
                        #     'color': '#212121',
                        #     'background-color': '#3EB489',
                        # }
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
                            id='leaf_query',
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
                            id='metadata_query',
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
                        id='table_metadata',
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
                    dcc.Download(id="download_leaf_datatable"),
                    dash_table.DataTable(
                        id='leaf_table',
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
        Output(component_id='leaf_figure', component_property='figure'),
    ],
    [
        Input(component_id='leaf_table', component_property='derived_virtual_data'),
        Input(component_id='radio_items_fold_type',component_property='value')
    ],
    prevent_initial_call=True
)
def query_figure(leaf_table_derived_virtual_data,radio_items_fold_type_value):

    #get dataframe from derived data
    temp=pd.DataFrame.from_records(leaf_table_derived_virtual_data)
    print(temp)
    print(temp.columns[-1])

    if radio_items_fold_type_value=='average_welch':
        p='significance_welch'
        effect_size='fold_change_average'
    elif radio_items_fold_type_value=='median_mwu':
        p='significance_mwu'
        effect_size='fold_change_median'
        

    volcano = dashbio.VolcanoPlot(
        dataframe=temp,#bins_panda,
        snp="english_name",
        p=p,
        effect_size=effect_size,
        gene=None,
        xlabel='log2 Fold Change',
        genomewideline_value=1e-2,
    )



    return [volcano]



@callback(
    [
        #Output(component_id="leaf_table", component_property="columns"),
        Output(component_id="leaf_table", component_property="data")
    ],
    [
        Input(component_id='leaf_query', component_property='n_clicks'),
    ],
    [
        State(component_id='dropdown_triplet_selection_from',component_property='value'),
        State(component_id='dropdown_triplet_selection_to',component_property='value'),
        State(component_id='radio_items_bin_type',component_property='value')
    ],
    prevent_initial_call=True
)
def query_table(leaf_query_n_clicks,dropdown_triplet_selection_from_value,dropdown_triplet_selection_to_value,radio_items_bin_type_value):

    leaf_output={
        "triplet_from":dropdown_triplet_selection_from_value,
        "triplet_to":dropdown_triplet_selection_to_value
    }

    response = requests.post(base_url_api + "/leafresource/", json=leaf_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)


    total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    data = total_panda.to_dict(orient='records')

    return [data]












@callback(
    [
        Output(component_id="download_leaf_datatable", component_property="data"),
    ],
    [
        Input(component_id="button_download", component_property="n_clicks"),
    ],
    [
        State(component_id="leaf_table",component_property="data")
    ],
    prevent_initial_call=True
)
def download_leaf_datatable(
    download_click,
    table_data
    ):
        """
        """
        #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
        print(pd.DataFrame.from_records(table_data).to_excel)

        return [dcc.send_data_frame(
            pd.DataFrame.from_records(table_data).to_excel, "binvestigate_differential_datatable.xlsx", sheet_name="sheet_1"
        )]





@callback(
    [
        #Output(component_id="leaf_table", component_property="columns"),
        Output(component_id="table_metadata", component_property="data")
    ],
    [
        Input(component_id='metadata_query', component_property='n_clicks'),
    ],
    [
        State(component_id='dropdown_triplet_selection_from',component_property='value'),
        State(component_id='dropdown_triplet_selection_to',component_property='value'),
    ],
    prevent_initial_call=True
)
def query_table(metadata_query_n_clicks,dropdown_triplet_selection_from_value,dropdown_triplet_selection_to_value):

    leaf_output={
        "triplet_from":dropdown_triplet_selection_from_value,
        "triplet_to":dropdown_triplet_selection_to_value
    }

    response = requests.post(base_url_api + "/leafmetadataresource/", json=leaf_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)


    # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    data = total_panda.to_dict(orient='records')

    return [data]