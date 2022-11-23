from logging import PlaceHolder
import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from . import venn_helper
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio
import time

dash.register_page(__name__)

#import os
#my_api_env_variable=os.getenv('API_ADDRESS')
#print('*'*50)
#print(my_api_env_variable)
base_url_api = f"http://api_alias:4999/"
#base_url_api = "http://127.0.0.1:4999/"
#base_url_api = "http://172.18.0.3:4999/"
########get things from helper script########
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
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
                            id='dropdown_triplet_selection_from',
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
                            id='dropdown_triplet_selection_to',
                            options=sorted([
                                {'label': temp, 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                            ],key=lambda x:x['label']),
                            multi=True,
                            placeholder='Select Triplet'
                            # style={
                            #     'color': '#212121',
                            #     'background-color': '#3EB489',
                            # }
                        ),  
                        html.Br(),
                    ],
                    width={'size':4}
                ),
                # dbc.Col(
                #     children=[
                #         html.Br(),
                #         html.Br(),
                #     ],
                #     width={'size':0}
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
                                id='metadata_query',
                            ),
                            className="d-grid gap-2 col-3 mx-auto",
                        ),
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
                            row_deletable=True,
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
                            },
                            filter_options={
                                'case':'insensitive',
                                'placeholder_text':'Type here to filter'
                            }
                        )
                    ],
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
                                id='leaf_query',
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
                dbc.Col(width=2),
                dbc.Col(
                    dbc.Spinner(
                        children=[
                            #html.H2("Venn Comparator", className='text-center'),
                            dcc.Graph(
                                id='leaf_figure'
                            ),
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
                                filter_options={
                                    'case':'insensitive',
                                    'placeholder_text':'Type here to filter'
                                },
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
                                },

                            )
                        ],
                    ),
                    width={'size':8}
                ),
                dbc.Col(width=2),
            ],
            #justify='center'
        ),
        html.Br(),
        html.Br(),
        # dbc.Row(
        #     children=[
        #         dbc.Col(width=2),
        #         dbc.Col(
        #             children=[
        #                 #html.H2("Result Datatable", className='text-center'),
        #                 html.Div(
        #                     dbc.Button(
        #                         'Download Datatable as .xlsx',
        #                         id='button_download',
        #                     ),
        #                     className="d-grid gap-2 col-3 mx-auto",
        #                 ),
        #                 dcc.Download(id="download_leaf_datatable"),
        #                 dash_table.DataTable(
        #                     id='leaf_table',
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
        #             width={'size':8}
        #         ),
        #         dbc.Col(width=2),
        #     ],
        #     #justify='center'
        # ),
    ]
)

@callback(
    [
        Output(component_id='leaf_figure', component_property='figure'),
    ],
    [
        Input(component_id='leaf_table', component_property='derived_virtual_data'),
        # Input(component_id='radio_items_fold_type',component_property='value')
    ],
    [
        State(component_id='dropdown_triplet_selection_from',component_property='value'),
        State(component_id='dropdown_triplet_selection_to',component_property='value'),
    ],
    prevent_initial_call=True
)
def query_figure(leaf_table_derived_virtual_data,dropdown_triplet_selection_from_value,dropdown_triplet_selection_to_value):

    #get dataframe from derived data
    temp=pd.DataFrame.from_records(leaf_table_derived_virtual_data)
    print(temp)
    print(temp.columns[-1])

    # if radio_items_fold_type_value=='average_welch':
    p='significance_welch'
    effect_size='fold_change_average'
    # elif radio_items_fold_type_value=='median_mwu':
        # p='significance_mwu'
        # effect_size='fold_change_median'
        

    volcano = dashbio.VolcanoPlot(
        dataframe=temp,#bins_panda,
        snp="english_name",
        p=p,
        effect_size=effect_size,
        gene=None,
        xlabel='log2 Fold Change',
        genomewideline_value=2,
        title=dropdown_triplet_selection_from_value[0].title()+'             vs.               '+dropdown_triplet_selection_to_value[0].title(),
        title_x=0.5
    )
    volcano.update_layout(showlegend=False)


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
        #State(component_id='dropdown_triplet_selection_from',component_property='value'),
        #State(component_id='dropdown_triplet_selection_to',component_property='value'),
        State(component_id='radio_items_bin_type',component_property='value'),
        State(component_id='table_metadata', component_property='derived_virtual_data'),
    ],
    prevent_initial_call=True
)
def query_table(leaf_query_n_clicks,radio_items_bin_type_value,table_metadata_derived_virtual_data):

    leaf_output={
    #    "triplet_from":dropdown_triplet_selection_from_value,
    #    "triplet_to":dropdown_triplet_selection_to_value
        "metadata_datatable":table_metadata_derived_virtual_data,
        "bin_type":radio_items_bin_type_value
    }
    #print(table_metadata_derived_virtual_data)
    #leaf_output=table_metadata_derived_virtual_data

    start=time.time()
    response = requests.post(base_url_api + "/leafresource/", json=leaf_output)
    end=time.time()
    print(f'the time to get our info from the api is {end-start}')
    
    start=time.time()
    total_panda = pd.read_json(response.json(), orient="records")
    end=time.time()
    print(f'the time to turn our json into a panda is  {end-start}')
    #print(total_panda)
    #print('***********************************')

    # start=time.time()
    # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]
    # end=time.time()
    # print(f'the time to subset our panda is  {end-start}')

    start=time.time()
    data = total_panda.to_dict(orient='records')
    end=time.time()
    print(f'the time to turn our panda into json again is  {end-start}')
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
def query_md_table(metadata_query_n_clicks,dropdown_triplet_selection_from_value,dropdown_triplet_selection_to_value):
    #print(dropdown_triplet_selection_from_value)
    leaf_output={
        "triplet_from":dropdown_triplet_selection_from_value,
        "triplet_to":dropdown_triplet_selection_to_value
    }

    response = requests.post(base_url_api + "/leafmetadataresource/", json=leaf_output)
    total_panda = pd.read_json(response.json(), orient="records")
    #print(total_panda)


    # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    data = total_panda.to_dict(orient='records')

    return [data]