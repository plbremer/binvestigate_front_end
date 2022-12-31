#from msilib.schema import Component
import re
from typing import final
import dash
from dash import dcc, html, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.dash_table.Format import Format, Scheme, Group
import dash_bio as dashbio
from . import bin_browser_helper
import plotly.graph_objects as go
from dash import callback_context
from pprint import pprint

from dash.exceptions import PreventUpdate

dash.register_page(__name__,path_template="/bin-browser/<linked_compound>")

#base_url_api = f"http://api_alias:4999/"
base_url_api = "http://127.0.0.1:4999/"
#base_url_api = "http://172.18.0.3:4999/"

########get things from helper script########
bins_dict=bin_browser_helper.generate_bin_dropdown_options()
# compound_dropdown_options_sorted=sorted(
#     bins_dict,
#     key=lambda x:x['label']
# ),



compound_classes=bin_browser_helper.generate_compound_classes()
compound_translation_panda=pd.read_pickle('../newer_datasets/compound_list_for_differential_new.bin')
compound_translation_dict=dict(zip(compound_translation_panda.compound_identifier.tolist(),compound_translation_panda.english_name.tolist()))
del compound_translation_panda
#############################################

#to get inchikey from identifier
final_curations=pd.read_pickle('../newer_datasets/compound_list_for_sun_and_bin_new.bin')
final_curations.drop(['bin_type','english_name'],axis='columns',inplace=True)
final_curations.set_index('compound_identifier',drop=True,inplace=True)




#layout=dbc.Container(
layout=html.Div(
    children=[
        dcc.Location(id='url',refresh=False),
        dcc.Download(
            id='download_msp_known'
        ),
        dcc.Download(
            id='download_msp_unknown'
        ),
        dbc.Row(
            children=[
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        html.H2("Compound options", className='text-center'),
                        html.Br(),
                    ],
                    width={'size':5}
                ),
                dbc.Col(
                    children=[
                        html.H2("Download .msp Files", className='text-center'),
                        html.Br(),
                    ],
                    width={'size':4}
                ),
            ],
            #justify='center'
        ),
        dbc.Row(
            children=[
                dbc.Col(width=2),
                dbc.Col(
                    children=[
                        #html.H2("From Triplet", className='text-center'),
                        dcc.Dropdown(
                            id='dropdown_bin',
                            # options=sorted([
                            #     {'label': temp.title(), 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                            # ],key=lambda x:x['label']),
                            placeholder='Type compound name to search',
                            multi=False,
                            #placeholder='Known: alanine'
                            #value=2
                            # style={
                            #     'color': '#212121',
                            #     'background-color': '#3EB489',
                            # }
                        ),  
                        html.Br(),
                        html.Br(),
                        html.Div(
                            dbc.Button(
                                'Query and Visualize',
                                id='button_bin_visualize',
                            ),
                            className="d-grid gap-2 col-4 mx-auto",
                        ),
                    ],
                    width={'size':3}
                ),
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        html.Div(
                            dbc.Button(
                                'Download Identified .msp',
                                id='button_download_msp_identified',
                            ),
                            className="d-grid gap-2 col-4 mx-auto",
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            dbc.Button(
                                'Download Unknown .msp',
                                id='button_download_msp_unknown',
                            ),
                            className="d-grid gap-1 col-4 mx-auto",
                        )
                    ],
                    width=4
                ),
                #dbc.Col(width=3)
            ]
        ),
        # dbc.Row(
        #     children=[
        #         dbc.Col(width=2),
        #         dbc.Col(
        #             children=[
        #                 #html.H2("Result Datatable", className='text-center'),
        #                 html.Div(
        #                     dbc.Button(
        #                         'Query and Visualize',
        #                         id='button_bin_visualize',
        #                     ),
        #                     className="d-grid gap-2 col-4 mx-auto",
        #                 ),
        #             ],
        #             width=3
        #         ),            
        #     ]
        # ),
        dbc.Row(
            children=[
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        html.Br(),
                        html.Br(),
                        # html.Br(),
                        # html.Br(),
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
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'fontSize': 17,
                                'padding': '8px',
                                #'textAlign': 'left',
                                #'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'
                            },
                            style_header={
                                'font-family': 'arial',
                                'fontSize': 15,
                                'fontWeight': 'bold',
                                #'textAlign': 'center'
                            },
                            style_data={
                                'textAlign': 'left',
                                'fontWeight': 'bold',
                                'font-family': 'Roboto',
                                'fontSize': 15,
                            },
                        )
                    ],
                    width=3
                ),        
                dbc.Col(width=1),           
                dbc.Col(
                    dcc.Graph(
                        id='figure_bin'
                    ) 
                ),
                dbc.Col(width=1)
            ]
        ),
        # dbc.Row(
        #     children=[
        #         dbc.Col(width=2),
        #         dbc.Col(
        #             children=[
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Div(
        #                     dbc.Button(
        #                         'Download as .xlsx',
        #                         id='button_download_msp',
        #                     ),
        #                     className="d-grid gap-2 col-4 mx-auto",
        #                 ),
        #                 dcc.Download(id="download_download_msp"),
        #                 dash_table.DataTable(
        #                     id='table_bin',
        #                     columns=[
        #                         {'name': 'Attribute', 'id': 'attribute'},
        #                         {'name': 'Value', 'id': 'value'}, 
        #                     ],
        #                     data=[],
        #                     # page_current=0,
        #                     # page_size=10,
        #                     # #page_action='custom',
        #                     # page_action='native',
        #                     # #sort_action='custom',
        #                     # sort_action='native',
        #                     # sort_mode='multi',
        #                     # #sort_by=[],
        #                     # #filter_action='custom',
        #                     # filter_action='native',
        #                     # row_deletable=False,
        #                     #filter_query='',
        #                     style_cell={
        #                         'fontSize': 17,
        #                         'padding': '8px',
        #                         'textAlign': 'center'
        #                     },
        #                     style_header={
        #                         'font-family': 'arial',
        #                         'fontSize': 15,
        #                         'fontWeight': 'bold',
        #                         'textAlign': 'center'
        #                     },
        #                     style_data={
        #                         'textAlign': 'center',
        #                         'fontWeight': 'bold',
        #                         'font-family': 'Roboto',
        #                         'fontSize': 15,
        #                     },
        #                 )
        #             ],
        #             width=3
        #         ),
        #         # dbc.Col(
        #         #     width=1
        #         # ), 
        #         dbc.Col(
        #             children=[
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
                        
        #                 # dcc.Graph(
        #                 #     id='figure_bin'
        #                 # )                        
        #             ],
        #             width=5
        #         ),                
        #     ]
        # ),
        # html.Br(),
        # html.Br(),
        # dbc.Row(
        #     children=[
        #         dbc.Col(width=1),

        #         dbc.Col(width=1),

        #         dbc.Col(width=3),
        #     ]
        # )
    ]
)

@callback(
    Output("dropdown_bin", "options"),
    Input("dropdown_bin", "search_value")
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in bins_dict if search_value in o["label"]]



@callback(
    [
        Output(component_id="table_bin", component_property="columns"),
        Output(component_id='table_bin', component_property='data'),
        Output(component_id='figure_bin', component_property='figure'),
        Output(component_id='url', component_property='pathname'),
        Output(component_id='dropdown_bin', component_property='value')
    ],
    [
        
        Input(component_id='button_bin_visualize', component_property='n_clicks'),
        #Input(component_id='url', component_property='pathname'),
        #Input(component_id='radio_items_fold_type',component_property='value')
    ],
    [
        State(component_id='url', component_property='pathname'),
        State(component_id='dropdown_bin', component_property='value')
    ],
    #prevent_initial_call=True
)
def query_figure(button_bin_visualize_n_clicks,url_pathname,dropdown_bin_value):

    print(callback_context.triggered[0]['prop_id'])
    print(dropdown_bin_value)
    print(url_pathname)
    print('+='*50)
    if callback_context.triggered[0]['prop_id']=='.':
        bin_output={
            'bin_id':url_pathname.split('/')[-1]
        }
        output_url=url_pathname.split('/')[-1]
    else:
        bin_output={
            'bin_id':dropdown_bin_value
        }
        output_url=dropdown_bin_value

    # leaf_output={
    #     "metadata_datatable":table_metadata_derived_virtual_data
    # }
    # print(table_metadata_derived_virtual_data)
    pprint(bin_output)
    response = requests.post(base_url_api + "/binresource/", json=bin_output)
    print(response.json())
    print('!@#'*20)
    total_panda = pd.read_json(response.json(), orient="records")
    #print(total_panda)
    


    #print(total_panda.T)

    #print('***********************************')
    #print(total_panda.at[0,'spectrum'])
    mzs=[float(x.split(':')[0]) for x in total_panda.at[0,'spectrum'].split(' ')]
    intensities=[float(x.split(':')[1]) for x in total_panda.at[0,'spectrum'].split(' ')]
    mzs=[0]+mzs
    intensities=[0]+intensities
    #mzs=[4,12]
    #intensities=[3,4]
    #print(mzs)
    #print(intensities)
    #print('-'*50)
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

    #print(total_panda.columns)
    #total_panda=total_panda[['english_name','compound_identifier','retentionIndex','kovats','spectrum','quantMass','uniqueMass','splash','purity']]
    total_panda=total_panda[['english_name','compound_identifier','retentionIndex','kovats','spectrum','quantMass','uniqueMass','splash']]
    
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
            #'purity':'Purity'
        },
        axis='columns',
        inplace=True
    )
    total_panda=total_panda.T
    print('+'*50)
    print(total_panda)
    print(final_curations)
    total_panda.at['InChIKey',0]=final_curations.at[
        str(total_panda.at['InChIKey',0]),'identifier'
    ]
    try:
        total_panda.at['Superclass',0]=compound_classes.at[
            total_panda.at['InChIKey',0],'Superclass'
        ]
        total_panda.at['Class',0]=compound_classes.at[
            total_panda.at['InChIKey',0],'Class'
        ]
        total_panda.at['Subclass',0]=compound_classes.at[
            total_panda.at['InChIKey',0],'Subclass'
        ]
    except KeyError:
        total_panda.at['Superclass',0]=''
        total_panda.at['Class',0]=''      
        total_panda.at['Subclass',0]=''       



    total_panda.reset_index(inplace=True)
    #print(total_panda)
    total_panda.rename(
        {
            'index':'Attribute',
            0:'Value'
        },
        axis='columns',
        inplace=True
    )
    #print(total_panda)

    #the names that we stashed into the DB are sometimes old. eg have things like 'NIST' in them. translate here
    print(compound_translation_dict)
    print(compound_translation_dict[str(bin_output['bin_id'])])
    print(total_panda)
    total_panda.at[0,'Value']=compound_translation_dict[
        str(bin_output['bin_id'])
    ]

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
    print(url_pathname.split('/'))
    return [column_list,data,spectrum_figure,'/'+url_pathname.split('/')[1]+'/'+str(output_url),bin_output['bin_id']]
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
def download_bin_datatable(
    button_download_msp_n_clicks,
    table_bin_derived_virual_data
    ):
        """
        """
        #print(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))

        #temp_img=venn_helper.make_venn_figure_from_panda(pd.DataFrame.from_records(table_derived_virtual_data).drop(['compound','bin'],axis='columns'))
        #print(pd.DataFrame.from_records(table_data).to_excel)

        #print(pd.DataFrame.from_records(table_bin_derived_virual_data).to_excel)

        return [dcc.send_data_frame(
            pd.DataFrame.from_records(table_bin_derived_virual_data).to_excel, "binvestigate_sunburst_datatable.xlsx", sheet_name="sheet_1"
        )]


@callback(
    [
        Output(component_id="download_msp_known", component_property="data"),
    ],
    [
        Input(component_id="button_download_msp_identified", component_property="n_clicks"),
    ],
    prevent_initial_call=True
)
def download_msp_known(    button_download_msp_identified_n_clicks    ):
    return [dcc.send_file(
        '../newer_datasets/GCBinbase_knowns_curated.msp'
    )]

@callback(
    [
        Output(component_id="download_msp_unknown", component_property="data"),
    ],
    [
        Input(component_id="button_download_msp_unknown", component_property="n_clicks"),
    ],
    prevent_initial_call=True
)
def download_msp_unknown(    button_download_msp_unknown_n_clicks    ):
    return [dcc.send_file(
        '../newer_datasets/GCBinbase_unknowns.msp'
    )]