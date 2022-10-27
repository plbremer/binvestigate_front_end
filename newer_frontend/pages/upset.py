import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from . import venn_helper
import pandas as pd
from dash.dependencies import Input, Output, State
from pprint import pprint
from dash_table.Format import Format, Scheme, Group
import xlsxwriter


base_url_api = "http://127.0.0.1:4999/"

dash.register_page(__name__)

########get things from helper script########
unique_sod_combinations_dict=venn_helper.get_unique_sod_combinations()
#############################################

#df = px.data.gapminder()

#layout=dbc.Container(
layout=html.Div(
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
            #justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(width=2),
                dbc.Col(
                    children=[
                        html.H2("Metadata Combinations", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_triplet_selection',
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
                    width={'size':2}
                ),
                dbc.Col(
                    children=[
                        #html.H2("Venn Diagram", className='text-center'),
                        dbc.Row(html.H2("Upset Plot"),style={'textAlign': 'center'}),
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
                            children=[
                                #dbc.ModalHeader
                                dbc.ModalHeader(dbc.ModalTitle("Right Click + Copy Image Address for High-Res"),close_button=True),
                                dbc.ModalBody(
                                #    html.Div(className="modal-body-container",children=[
                                    html.Img(
                                        id='modal_Img_venn',
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
                            id='modal',
                            centered=True,
                            size='xl',
                            is_open=False,
                            style={"max-width": "none", "width": "90%"}
                        ),
                        html.Br(),
                    ],
                    #width={'size':3}
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
                        html.Br(),
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
                        html.Br(),
                        html.H6("Display Knowns or Unknowns", className='text-center'),
                        html.Div(className="radio-group-container add-margin-top-1", children=[
                            html.Div(className="radio-group", children=[
                                dbc.RadioItems(
                                    id='radio_items_bin_type_upset',
                                    options=[
                                        {'label': 'Knowns', 'value': 'known'},
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
                        html.Br(),
                        html.H6("What Percent Observed Constitutes Present", className='text-center'),
                        dcc.Slider(
                            id='slider_percent_present',
                            #label='Minimum Percent Present',
                            min=0,
                            max=100,
                            step=1,
                            value=50,   
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}       
                        ),
                        html.Br(),
                    ],
                    width={'size':3}
                ),
                dbc.Col(width=2),
            ],
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=3),
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
                ),
                dbc.Col(width=3),
            ],
            #justify='center'
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=2),
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
                ),
                dbc.Col(width=2),
            ],
            #justify='center'
        ),
    ]
)


@callback(
    [
        Output(component_id="table", component_property="columns"),
        Output(component_id="table", component_property="data"),
    ],
    [
        Input(component_id="button_query", component_property="n_clicks"),
    ],
    [
        State(component_id="dropdown_triplet_selection",component_property="value"),
        State(component_id="slider_percent_present", component_property="value"),
        State(component_id="toggle_average_true", component_property="value"),
        State(component_id="radio_items_filter",component_property="value"),
        State(component_id='radio_items_bin_type_upset',component_property='value')
    ],
    prevent_initial_call=True
)
def perform_query_table(
    button_query,
    dropdown_triplet_selection_value,
    slider_percent_present_value,
    toggle_average_true_value,
    radio_items_filter_value,
    radio_items_bin_type_upset_value
    ):

        ##################volcano query######################
        #prepare json for api
        venn_data_table_output={
            "dropdown_triplet_selection_value":dropdown_triplet_selection_value,
            "slider_percent_present_value":slider_percent_present_value,
            "toggle_average_true_value":toggle_average_true_value,
            "radio_items_filter_value":radio_items_filter_value,
            "radio_items_bin_type_upset_value":radio_items_bin_type_upset_value
        }

        pprint(venn_data_table_output)

        response = requests.post(base_url_api + "/venntableresource/", json=venn_data_table_output)
        total_panda = pd.read_json(response.json(), orient="records")

        total_panda=total_panda.loc[
            total_panda['bin_type']==radio_items_bin_type_upset_value,
            :
        ].copy()

        total_panda.drop(['compound','bin_type','compound_identifier'],axis='columns',inplace=True)

        # start=time.time()
        # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]
        # end=time.time()
        # print(f'the time to subset our panda is  {end-start}')

        #print(total_panda)

        #prepare columns and data for the table
        column_list = [
            {"name": "Bin", "id": "bin"},
            {"name": "English Name", "id":"english_name"},
            {"name": "InChIKey","id":"identifier"}

        ]
        sod_column_list=[
            {"name": temp_column, "id": temp_column,"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)} for temp_column in total_panda.columns 
            if (temp_column != "bin" and temp_column!="english_name" and temp_column!="identifier")
        ]

        column_list+=sod_column_list
        temp_column_names=[element['id'] for element in column_list]
        total_panda=total_panda.loc[
            :,
            temp_column_names
        ].copy()

        
        data = total_panda.to_dict(orient='records')

        return (
            column_list,
            data
        )


#generates the venn diagram
@callback(
    [
        Output(component_id="Img_venn", component_property="src"),
        Output(component_id='modal_Img_venn',component_property="src")
    ],
    [
        #Input(component_id="button_query", component_property="n_clicks"),
        Input(component_id="table",component_property="derived_virtual_data")
    ],
    # [
    #     State(component_id="dropdown_triplet_selection",component_property="value"),
    #     State(component_id="slider_percent_present", component_property="value"),
    # ],
    prevent_initial_call=True
)
def perform_query_diagram(
    table_derived_virtual_data
    ):
        """
        """
        print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['english_name','identifier','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns',inplace=True))
        #temp_img=
        temp_img=venn_helper.create_upset(pd.DataFrame.from_records(table_derived_virtual_data).drop(['english_name','identifier','bin'],axis='columns'))

        return [temp_img,temp_img]




@callback(
    [
        Output(component_id='modal', component_property='is_open'),
    ],
    [
        Input(component_id='Img_venn', component_property='n_clicks'),
    ],
    prevent_initial_call=True
)
def open_modal(Img_venn_n_clicks):
    return [True]

@callback(
    [
        Output(component_id="download_datatable", component_property="data"),
    ],
    [
        Input(component_id="button_download", component_property="n_clicks"),
    ],
    [
        State(component_id="table",component_property="data")
    ],
    prevent_initial_call=True
)
def download_datatable(
    download_click,
    table_data
    ):
        """
        """
        #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
        print(pd.DataFrame.from_records(table_data).to_excel)

        return [dcc.send_data_frame(
            pd.DataFrame.from_records(table_data).to_excel, "binvestigate_venn_datatable.xlsx", sheet_name="sheet_1"
        )]
