#from msilib.schema import Component
import re
import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio
from . import bin_browser_helper
import plotly.graph_objects as go

dash.register_page(__name__)

base_url_api = "http://127.0.0.1:4999/"

########get things from helper script########
bins_dict=bin_browser_helper.generate_bin_dropdown_options()
#############################################

#layout=dbc.Container(
layout=html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2("Select a bin", className='text-center'),
                        html.Br(),
                    ],
                    width={'size':6}
                )
            ],
            justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(width=3),
                dbc.Col(
                    children=[
                        #html.H2("From Triplet", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_bin',
                            # options=sorted([
                            #     {'label': temp.title(), 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                            # ],key=lambda x:x['label']),
                            options=[
                                {'label': x, 'value':bins_dict[x]} for x in bins_dict
                            ],
                            multi=False,
                            # style={
                            #     'color': '#212121',
                            #     'background-color': '#3EB489',
                            # }
                        ),  
                        html.Br(),
                    ],
                    width={'size':6}
                ),
                dbc.Col(width=3),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(width=4),
                dbc.Col(
                    children=[
                        #html.H2("Result Datatable", className='text-center'),
                        html.Div(
                            dbc.Button(
                                'Query and Visualize',
                                id='button_bin_visualize',
                            ),
                            className="d-grid gap-2 col-4 mx-auto",
                        ),
                    ],
                    width=3
                ),            
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(width=2),
                dbc.Col(
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            dbc.Button(
                                'Download as .xlsx',
                                id='button_download_msp',
                            ),
                            className="d-grid gap-2 col-4 mx-auto",
                        ),
                        dcc.Download(id="download_download_msp"),
                        dash_table.DataTable(
                            id='table_bin',
                            columns=[
                                {'name': 'Attribute', 'id': 'attribute'},
                                {'name': 'Value', 'id': 'value'}, 
                            ],
                            data=[],
                            # page_current=0,
                            # page_size=10,
                            # #page_action='custom',
                            # page_action='native',
                            # #sort_action='custom',
                            # sort_action='native',
                            # sort_mode='multi',
                            # #sort_by=[],
                            # #filter_action='custom',
                            # filter_action='native',
                            # row_deletable=False,
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
                                'font-family':'sans-serif',
                                'textOverflow': 'ellipsis',
                                'maxWidth':0
                            }
                        )
                    ],
                    width=3
                ),
                # dbc.Col(
                #     width=1
                # ), 
                dbc.Col(
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        
                        dcc.Graph(
                            id='figure_bin'
                        )                        
                    ],
                    width=5
                ),                
            ]
        )
    ]
)


@callback(
    [
        Output(component_id="table_bin", component_property="columns"),
        Output(component_id='table_bin', component_property='data'),
        Output(component_id='figure_bin', component_property='figure'),
    ],
    [
        Input(component_id='button_bin_visualize', component_property='n_clicks'),
        #Input(component_id='radio_items_fold_type',component_property='value')
    ],
    [
        State(component_id='dropdown_bin', component_property='value')
    ],
    prevent_initial_call=True
)
def query_figure(button_bin_visualize_n_clicks,dropdown_bin_value):

    bin_output={
        'bin_id':dropdown_bin_value
    }
    # leaf_output={
    #     "metadata_datatable":table_metadata_derived_virtual_data
    # }
    # print(table_metadata_derived_virtual_data)

    response = requests.post(base_url_api + "/binresource/", json=bin_output)
    total_panda = pd.read_json(response.json(), orient="records")
    print(total_panda)
    
    print(total_panda.T)

    print('***********************************')
    print(total_panda.at[0,'spectrum'])
    mzs=[float(x.split(':')[0]) for x in total_panda.at[0,'spectrum'].split(' ')]
    intensities=[float(x.split(':')[1]) for x in total_panda.at[0,'spectrum'].split(' ')]
    mzs=[0]+mzs
    intensities=[0]+intensities
    #mzs=[4,12]
    #intensities=[3,4]
    print(mzs)
    print(intensities)
    print('-'*50)
    spectrum_figure=go.Figure(
        go.Bar(
            x=mzs,
            y=intensities,
            marker=dict(color="rgb(220, 53, 69)")
        )
    )
    spectrum_figure.update_yaxes(title="Relative Intensity")
    spectrum_figure.update_xaxes(title="m/z")
    spectrum_figure.update_traces(width=1, hovertemplate="m/z: %{x}<br>Intensity: %{y}<br>")
    spectrum_figure.update_layout(showlegend=False,font=dict(size=18))
    # total_panda=total_panda.loc[total_panda['bin_type_dict']==radio_items_bin_type_value]

    print(total_panda.columns)
    total_panda=total_panda[['english_name','compound_identifier','retentionIndex','kovats','spectrum','quantMass','uniqueMass','splash','purity']]
    total_panda.rename(
        {
            'english_name':'Name',
            'compound_identifier':'InChIKey',
            'retentionIndex':'FAME RI',
            'kovats':'Kovats RI',
            'spectrum':'Spectrum',
            'quantMass':'Quant Mass',
            'uniqueMass':'Unique Mass',
            'splash':'SPLASH',
            'purity':'Purity'
        },
        axis='columns',
        inplace=True
    )
    total_panda=total_panda.T
    total_panda.reset_index(inplace=True)
    print(total_panda)
    total_panda.rename(
        {
            'index':'Attribute',
            0:'Value'
        },
        axis='columns',
        inplace=True
    )
    print(total_panda)

    # total_panda=pd.DataFrame.from_dict(
    #     {
    #         'Attribute':[1,2],
    #         'Value':[2,3]
    #     }
    # )
    data = total_panda.to_dict(orient='records')
    column_list=[
        {'name': temp_column, 'id':temp_column} for temp_column in total_panda.columns
    ]

    #data='nonsense'
    return [column_list,data,spectrum_figure]
    #return [spectrum_figure]




@callback(
    [
        Output(component_id="download_download_msp", component_property="data"),
    ],
    [
        Input(component_id="button_download_msp", component_property="n_clicks"),
    ],
    [
        State(component_id='table_bin', component_property='derived_virtual_data')
    ],
    prevent_initial_call=True
)
def download_sunburst_datatable(
    button_download_msp_n_clicks,
    table_bin_derived_virual_data
    ):
        """
        """
        #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
        #print(pd.DataFrame.from_records(table_data).to_excel)

        print(pd.DataFrame.from_records(table_bin_derived_virual_data).to_excel)

        return [dcc.send_data_frame(
            pd.DataFrame.from_records(table_bin_derived_virual_data).to_excel, "binvestigate_sunburst_datatable.xlsx", sheet_name="sheet_1"
        )]