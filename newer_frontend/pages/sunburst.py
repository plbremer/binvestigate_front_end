import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from . import sunburst_helper
import pandas as pd
from dash.dependencies import Input, Output, State
from pprint import pprint
from dash_table.Format import Format, Scheme, Group
import xlsxwriter

base_url_api = "http://127.0.0.1:4999/"

dash.register_page(__name__)

compound_dropdown_options=sunburst_helper.create_compound_selection_labels("../newer_datasets/compounds_networkx.bin")

layout=dbc.Container(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            #html.H2("Venn Comparator", className='text-center'),
                            html.Br(),
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Compounds", className='text-center'),
                            dcc.Dropdown(
                                id='compound_selection',
                                options=compound_dropdown_options,
                                multi=False,
                            ),
                            html.Br(),
                        ],
                        width={'size':2}
                    ),
                    dbc.Col(
                        children=[
                            html.H2("Sunburst Diagram", className='text-center'),
                            html.Div(#className="venn-thumbnail-container",
                                children=[
                                    dcc.Graph(
                                        id='figure_sunburst',
                                        #figure=plotly_fig
                                    )
                                ]
                            ),
                            html.Br(),
                        ],
                        width={'size':6}
                    ),
                    dbc.Col(
                        children=[
                            html.H2("Options", className='text-center'),
                            html.H6("Choose Metric for Sunburst", className='text-center'),
                            html.Div(className="radio-group-container add-margin-top-1", children=[
                                html.Div(className="radio-group", children=[
                                    dbc.RadioItems(
                                        id='radio_items_sunburst_value',
                                        options=[
                                            {'label': 'Average', 'value': 'intensity_average'},
                                            {'label': 'Median', 'value': 'intensity_median'},
                                            {'label': 'Percent Present', 'value':'percent_present'}
                                            #{'label': 'Unique', 'value': 'unique'},
                                        ],         
                                        value='intensity_average',
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        inputCheckedClassName="active"                               
                                    ),
                                ])
                            ]),
                            html.Br(),
                            html.H6("Choose Order for Sunburst", className='text-center'),
                            html.Div(className="radio-group-container add-margin-top-1", children=[
                                html.Div(className="radio-group", children=[
                                    dbc.RadioItems(
                                        id='radio_items_sod_order',
                                        options=[
                                            {'label': 'Species, Organ, Disease', 'value': 'binvestigate,species,organ,disease'},
                                            {'label': 'Species, Disease, Organ', 'value': 'binvestigate,species,disease,organ'},
                                            {'label': 'Organ, Species, Disease', 'value': 'binvestigate,organ,species,disease'},
                                            {'label': 'Organ, Disease, Species', 'value': 'binvestigate,organ,disease,species'},
                                            {'label': 'Disease, Species, Organ', 'value': 'binvestigate,disease,species,organ'},
                                            {'label': 'Disease, Organ, Species', 'value': 'binvestigate,disease,organ,species'},
                                        ],         
                                        value='binvestigate,species,organ,disease',
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        inputCheckedClassName="active"                               
                                    ),
                                ])
                            ]),
                            html.Br(),
                        ],
                        width={'size':4}
                    ),
                ],
            ),
            html.Br(),
            html.Br(),
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
                                    id='button_query',
                                ),
                                className="d-grid gap-2 col-6 mx-auto",
                            ),
                            html.Br(),
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
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
                                id='table',
                                columns=[
                                    #the id were copied and pasted from the previous version...
                                    #surely an error.... but makes no difference?
                                    {"name": "Species", "id": "bin_id"},
                                    {"name": "Organ", "id": "compound_name"},
                                    {"name": "Disease", "id": "group_1"},
                                    {"name": "Metric", "id": "metric"}
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
                justify='center'
            ),
        ]
    )