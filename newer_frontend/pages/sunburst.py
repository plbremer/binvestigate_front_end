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
import plotly.express as px
import plotly.graph_objects as go

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
                        width={'size':6}
                    ),
                ],
            ),
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
                #dbc.Col(
                    #children=[
                    #html.H2("Sunburst Diagram", className='text-center'),
                    html.Div(className="sunburst-container",
                        children=[
                            dcc.Graph(
                                id='sunburst_figure'
                            )
                        ]
                    ),
                    html.Br(),
                    #],
                    #width={'size':12}
                #),
                ],
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
                                id='sunburst_table',
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

@callback(
    [
        Output(component_id="sunburst_table", component_property="columns"),
        Output(component_id="sunburst_table", component_property="data")
    ],
    [
        Input(component_id='button_query', component_property='n_clicks'),
    ],
    [
        State(component_id='compound_selection',component_property='value'),
        State(component_id='radio_items_sunburst_value',component_property='value')
    ],
    prevent_initial_call=True
)
def query_table(button_query_n_clicks,compound_selection_value,radio_items_sunburst_value_value):

    sunburst_output={
        "compound":compound_selection_value
    }

    response = requests.post(base_url_api + "/sunburstresource/", json=sunburst_output)
    total_panda = pd.read_json(response.json(), orient="records")
    total_panda['binvestigate']='binvestigate'

    if radio_items_sunburst_value_value=='intensity_average':
        last_column={'name': 'Average Intensity','id':'intensity_average',"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
    elif radio_items_sunburst_value_value=='intensity_median':
        last_column={'name': 'Median Intensity','id':'intensity_median',"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
    elif radio_items_sunburst_value_value=='percent_present':
        last_column={'name': 'Percent Present','id':'percent_present',"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)}
    column_list=[
        {'name':'Species','id':'species'},
        {'name':'Organ','id':'organ'},
        {'name':'Disease','id':'disease'},
        #{'name':'Species','id':'species'},
        last_column
    ]
    total_panda=total_panda[['binvestigate','species','organ','disease',last_column['id']]]

    data = total_panda.to_dict(orient='records')

    return [column_list,data]

@callback(
    [
        Output(component_id='sunburst_figure', component_property='figure'),
    ],
    [
        Input(component_id='sunburst_table', component_property='derived_virtual_data'),
        Input(component_id='radio_items_sod_order',component_property='value')
    ],
    [
        State(component_id='radio_items_sunburst_value',component_property='value')
    ],
    prevent_initial_call=True
)
def query_table(sunburst_table_derived_virtual_data,radio_items_sod_order_value,radio_items_sunburst_value_value):

    #get dataframe from derived data
    temp=pd.DataFrame.from_records(sunburst_table_derived_virtual_data)
    print(temp)
    print(temp.columns[-1])
    #coerce it into sunburst form with helper function
    temp_in_sunburst_form=sunburst_helper.coerce_full_panda(temp,radio_items_sunburst_value_value,radio_items_sod_order_value.split(','))
    print('----------------------')
    print(temp_in_sunburst_form)

    #my_hovertext_values=(temp_in_sunburst_form['id'].str.split('/').str[1])+' - '+(temp_in_sunburst_form['id'].str.split('/').str[2])+' - '+(temp_in_sunburst_form['id'].str.split('/').str[3])+': '+(temp_in_sunburst_form['sum'].astype(str))
    #my_hovertext_values=' - '.join((temp_in_sunburst_form['id'].str.split('/'))[1:])
    my_hovertext_values=(temp_in_sunburst_form['id'].str.split('/').str[1:].str.join(' - '))+': '+(temp_in_sunburst_form['average'].astype(str))
    current_figure=go.Figure(
        go.Sunburst(
            #data_frame=temp_in_sunburst_form,
            parents=temp_in_sunburst_form['parent'].to_list(),
            labels=temp_in_sunburst_form['name'].to_list(),
            values=temp_in_sunburst_form['sum'].to_list(),
            ids=temp_in_sunburst_form['id'].to_list(),
            hovertext=my_hovertext_values,#temp_in_sunburst_form['id'].to_list(),
            hoverinfo='text',
            #branchvalues='total',
            
        ),
        layout=go.Layout(height=1000,width=1000)
    )
    current_figure.update_layout(
        margin = dict(t=0, l=0, r=0, b=0),
        hoverlabel=dict(font_size=24)
    )
    return [current_figure]