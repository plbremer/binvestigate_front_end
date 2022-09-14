import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

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
                            html.H2("Venn Comparator", className='text-center'),
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
                            html.H2("Venn Comparator", className='text-center'),
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
                            # html.H6("Median or Average", className='text-center'),
                            html.Div(className="radio-group-container add-margin-top-30", children=[
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
                            # daq.ToggleSwitch(
                            #     id='toggle_average_true',
                            #     value=True,
                            #     #label='Median - Average'
                            # ),
                            # html.Br(),
                            # html.H6("Bin Filters"),
                            # dcc.RadioItems(
                            #     id='radio_items_filter',
                            #     options=[
                            #         {'label': 'No Filter', 'value': 'no_filter'},
                            #         {'label': 'Common', 'value': 'common'},
                            #         #{'label': 'Unique', 'value': 'unique'},
                            #     ],         
                            #     value='no_filter'                                   
                            # ),
                            html.Br(),
                        ],
                        width={'size':4}
                    ),
                    dbc.Col(
                        children=[
                            html.H2("Venn Comparator", className='text-center'),
                            html.Br(),
                        ],
                        width={'size':4}
                    ),
                ],
            ),
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
                            html.H2("Venn Comparator", className='text-center'),
                            html.Br(),
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
            ),
        ]
    )