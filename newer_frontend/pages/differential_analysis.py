import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from . import venn_helper

dash.register_page(__name__)

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
                                id='radio_items_fold_type',
                                options=[
                                    {'label': 'Knowns', 'value': 'knowns'},
                                    {'label': 'Classes', 'value': 'classes'},
                                    {'label': 'Unknowns', 'value': 'unknowns'},
                                ],         
                                value='knowns',
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
                    html.H2("Venn Comparator", className='text-center'),
                    dcc.Graph(
                        id='leaf_volcano'
                    )
                ],
                width={'size':9}
            ),
            dbc.Col(
                children=[
                    html.H2("Venn Comparator", className='text-center'),
                    dash_table.DataTable(
                        id='table_query_summary',
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
                    dcc.Download(id="download_datatable"),
                    dash_table.DataTable(
                        id='leaf_table',
                        columns=[
                            {"name": "English Name", "id": "english_name"},
                            {"name": "Fold Average", "id": "fold_average"},
                            {"name": "Significance Welch", "id": "sig_welch"},
                            {"name": "Fold Median", "id": "fold_median"},
                            {"name": "Significance MWU", "id": "sig_mannwhit"}
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