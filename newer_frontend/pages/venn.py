import dash
from dash import dcc, html, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
#import dash_table as dt
#from dash import dash_table as dt
#from dash import dash_table

from . import venn_helper

dash.register_page(__name__)

########get things from helper script########
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
#############################################



#df = px.data.gapminder()

layout=dbc.Container(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Venn Comparator", className='text-center'),
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
                            html.H2("Metadata Combinations", className='text-center'),
                            dcc.Dropdown(
                                id='dropdown_triplet_selection',
                                options=sorted([
                                    {'label': temp.title(), 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                                ],key=lambda x:x['label']),
                                multi=True,
                                style={
                                    'color': '#212121',
                                    'background-color': '#3EB489',
                                }
                            ),  
                            html.Br(),
                        ],
                        width={'size':4}
                    ),
                    dbc.Col(
                        children=[
                            html.H2("Venn Diagram", className='text-center'),
                            html.Div(className="venn-thumbnail-container",
                                children=[
                                    html.Img(
                                        id='Img_venn',
                                        #src=plotly_fig,
                                        height=200,
                                        width=200
                                    ),
                                ]
                            ),
                            dbc.Modal(
                                dbc.ModalBody(
                                    html.Img(
                                        id='modal_Img_venn',
                                        #src=plotly_fig,
                                        height=700,
                                        width=700
                                    )
                                ),
                                id='modal',
                                is_open=False
                            ),
                            html.Br(),
                        ],
                        width={'size':4}
                    ),
                    dbc.Col(
                        children=[
                            html.H2("Options", className='text-center'),
                            html.H6("Display Average or Median in Datatable", className='text-center'),
                            html.Div(className="radio-group-container add-margin-top-1", children=[
                                html.Div(className="radio-group", children=[
                                    dbc.RadioItems(
                                        id='toggle_average_true',
                                        options=[
                                            {'label':'Average','value':True},
                                            {'label':'Median','value':False}
                                        ],
                                        value=True,
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        inputCheckedClassName="active",                                
                                    ),
                                ])
                            ]),
                            html.H6("Display All Compounds or Only Compounds In-common", className='text-center'),
                            html.Div(className="radio-group-container add-margin-top-1", children=[
                                html.Div(className="radio-group", children=[
                                    dbc.RadioItems(
                                        id='radio_items_filter',
                                        options=[
                                            {'label': 'No Filter', 'value': 'no_filter'},
                                            {'label': 'Common', 'value': 'common'},
                                            #{'label': 'Unique', 'value': 'unique'},
                                        ],         
                                        value='no_filter',
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        inputCheckedClassName="active",                                
                                    ),
                                ])
                            ]),
                            html.H6("What Percent Observed Constitutes Present", className='text-center'),
                            dcc.Slider(
                                id='slider_percent_present',
                                #label='Minimum Percent Present',
                                min=0,
                                max=100,
                                step=1,
                                value=80,   
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}       
                            ),
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
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Result Datatable", className='text-center'),
                            html.Br(),
                            dash_table.DataTable(
                                id='table',
                                columns=[
                                    {"name": "Bin ID", "id": "bin_id"},
                                    {"name": "Compound Name", "id": "compound_name"},
                                    {"name": "Group 1", "id": "group_1"},
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
                                #filter_query=''
                                

                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white'
                                },
                                style_data={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                },

                            )
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
            ),
        ]
    )