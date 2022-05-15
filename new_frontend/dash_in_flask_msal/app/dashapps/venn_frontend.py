# 1
# 20
# [{'column_id': 'continent', 'direction': 'asc'}, {'column_id': 'lifeExp', 'direction': 'asc'}]
# {continent} scontains Asia && {lifeExp} s> 50
import requests
import pathlib
import json
import networkx as nx
from pprint import pprint
import pandas as pd
import venn

import dash
from dash import Dash
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bio as dashbio
import dash_daq as daq

#from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt
import io
import base64

from dash_table.Format import Format, Scheme, Group

#flask app adjustment
APP_ID='venn_frontend'
URL_BASE='/dash/venn_frontend/'
MIN_HEIGHT=2000
# external_stylesheets = [dbc.themes.DARKLY]
# app = Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server

base_url_api = "http://127.0.0.1:4999/"
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


############### LOAD HIERARCHIES ##############

###########################################


######### HELPER FUNCTIONS ################

########################################


#############Load pandas for data selection options ##########
unique_sod_combinations_address = DATA_PATH.joinpath("unique_sod_combinations.bin")

unique_sod_combinations_panda = pd.read_pickle(unique_sod_combinations_address)
unique_sod_combinations_dict = {
    temp:temp for temp in unique_sod_combinations_panda.keys().to_list()
}
pprint(unique_sod_combinations_dict)
########################################


#####Read in panda for filtering options after one is selected######

####################################################################


############Update pandas for data selection#################

#############################################

################create temp mpl fig####################
from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt
labels = venn.get_labels([range(10), range(5, 15), range(3, 8), range(8, 17)], fill=['number', 'logic'])
fig, ax = venn.venn4(labels, names=['list 1', 'list 2', 'list 3', 'list 4'])
#plotly_fig = mpl_to_plotly(fig)
buf = io.BytesIO() # in-memory files
#plt.scatter(x, y)
plt.savefig(buf, format = "png") # save to the above file object
plt.close()
data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
plotly_fig="data:image/png;base64,{}".format(data)
######################################################

def add_dash(server):

    external_stylesheets = [dbc.themes.DARKLY]
    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )

    #####################Structure of app#################
    app.layout=html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Metadata Group Comparator", className='text-center'),
                            html.Br(),
                        ],
                        width={'size':6}
                    )
                ],
                justify='center'
            ),
            html.Br(),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        dcc.Dropdown(
                                            id='dropdown_triplet_selection',
                                            options=[
                                                #{'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                                {'label': temp, 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                                            ],
                                            multi=True,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        ),                                        
                                        html.H6("Minimum Percent Present", className='text-center'),
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
                                        html.H6("Median or Average", className='text-center'),
                                        daq.ToggleSwitch(
                                            id='toggle_average_true',
                                            value=True,
                                            #label='Median - Average'
                                        ),
                                        html.H6("Bin Filters"),
                                        dcc.RadioItems(
                                            id='radio_items_filter',
                                            options=[
                                                {'label': 'No Filter', 'value': 'no_filter'},
                                                {'label': 'Common', 'value': 'common'},
                                                #{'label': 'Unique', 'value': 'unique'},
                                            ],                                            
                                        )
                                    ]
                                )
                            ),
                        ],
                        width={'size':4}
                    ),
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    # children=[
                                    #     html.H6("Minimum Percent Present", className='text-center'),
                                    #     dcc.Slider(
                                    #         id='slider_percent_present',
                                    #         #label='Minimum Percent Present',
                                    #         min=0,
                                    #         max=100,
                                    #         step=1,
                                    #         value=80,   
                                    #         marks=None,
                                    #         tooltip={"placement": "bottom", "always_visible": True}       
                                    #     ),
                                    #     html.H6("Median or Average", className='text-center'),
                                    #     daq.ToggleSwitch(
                                    #         id='toggle_average_true',
                                    #         value=True,
                                    #         #label='Median - Average'
                                    #     )
                                    # ]
                                    # dcc.Graph(
                                    #     id='figure_venn',
                                    #     figure=plotly_fig
                                    # )
                                    html.Img(
                                        id='figure_venn',
                                        #src=plotly_fig,
                                        height=500,
                                        width=500
                                    )
                                )
                            ),
                        ],
                        width={'size':4}
                    )
                ],
                justify='around'
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Br(),
                            html.H2("Results - Individual Compounds", className='text-center'),
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.Button(
                                            'Get Results',
                                            id='button_query',
                                        )
                                    ]
                                )
                            )
                        ],
                        width={'size':3}
                    )
                ],
                justify='center'
            ),
            dbc.Row(
                children=[
                    dbc.Card(
                        dt.DataTable(
                            id='table',
                            columns=[
                                {"name": "Bin ID", "id": "bin_id"},
                                {"name": "Compound Name", "id": "compound_name"},
                                {"name": "Group 1", "id": "group_1"},
                            ],
                            data=[],
                            page_current=0,
                            page_size=50,
                            page_action='custom',
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_data={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            },

                            sort_action='custom',
                            sort_mode='multi',
                            sort_by=[],

                            filter_action='custom',
                            filter_query=''
                        )
                    ),
                ],
                justify='center'
            ),
        ]
    )
    ######################################################

    @app.callback(
        [
            Output(component_id="table", component_property="columns"),
            Output(component_id="table", component_property="data"),
            #Output(component_id="volcano_average_welch", component_property="figure"),
            #Output(component_id="volcano_median_mw", component_property="figure"),
        ],
        [
            Input(component_id="button_query", component_property="n_clicks"),
            Input(component_id="table", component_property="page_current"),
            Input(component_id="table", component_property="page_size"),
            Input(component_id="table", component_property="sort_by"),
            Input(component_id="table", component_property="filter_query"),
        ],
        [
            State(component_id="dropdown_triplet_selection",component_property="value"),
            State(component_id="slider_percent_present", component_property="value"),
            State(component_id="toggle_average_true", component_property="value"),
            State(component_id="radio_items_filter",component_property="value")
            # State(component_id="dropdown_from_disease", component_property="value"),
            # State(component_id="dropdown_to_species", component_property="value"),
            # State(component_id="dropdown_to_organ", component_property="value"),
            # State(component_id="dropdown_to_disease", component_property="value"),
        ],
    )
    def perform_volcano_query(
        query,
        page_current,
        page_size,
        sort_by,
        filter_query,
        dropdown_triplet_selection_value,
        slider_percent_present_value,
        toggle_average_true_value,
        radio_items_filter_value
    #     checklist_query,
    #     from_species_value,
    #     from_organ_value,
    #     from_disease_value,
    #     to_species_value,
    #     to_organ_value,
    #     to_disease_value,
        ):
            """
            """
            # print(page_current)
            # print(page_size)
            # print(sort_by)
            # print(filter_query)


        #     print('before json')

        #     if "Classes" in checklist_query:
        #         include_classes='Yes'
        #     else:
        #         include_classes='No'
        #     if "Knowns" in checklist_query:
        #         include_knowns='Yes'
        #     else:
        #         include_knowns='No'
        #     if "Unknowns" in checklist_query:
        #         include_unknowns='Yes'
        #     else:
        #         include_unknowns='No'

        #     ##################volcano query######################
            #prepare json for api
            venn_data_table_output={
                "page_current":page_current,
                "page_size":page_size,
                "sort_by":sort_by,
                "filter_query":filter_query,
                "dropdown_triplet_selection_value":dropdown_triplet_selection_value,
                "slider_percent_present_value":slider_percent_present_value,
                "toggle_average_true_value":toggle_average_true_value,
                "radio_items_filter_value":radio_items_filter_value
            }

            pprint(venn_data_table_output)
        #     volcano_json_output = {
        #         "from_species": from_species_value,
        #         "from_organ": from_organ_value,
        #         "from_disease": from_disease_value,
        #         "to_species": to_species_value,
        #         "to_organ": to_organ_value,
        #         "to_disease": to_disease_value,
        #         "include_classes": include_classes,
        #         "include_knowns": include_knowns,
        #         "include_unknowns": include_unknowns,
        #         "page_current":page_current,
        #         "page_size":page_size,
        #         "sort_by":sort_by,
        #         "filter_query":filter_query,
        #     }

        #     print('after json before api')
        #     #call api
            response = requests.post(base_url_api + "/venntableresource/", json=venn_data_table_output)
            print(response)
            total_panda = pd.read_json(response.json(), orient="records")
            print(total_panda)

        #     #prepare columns and data for the table
            column_list = [
                {"name": "bin", "id": "bin"},
                {"name": "English Name", "id":"compound"}
            ]
            sod_column_list=[
                {"name": temp_column, "id": temp_column,"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)} for temp_column in total_panda.columns 
                if (temp_column != "bin" and temp_column!="compound")
            ]
            #     {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
            #     {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
            #     {"name": "Significance MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
            # ]
            column_list+=sod_column_list
            data = total_panda.to_dict(orient='records')

        #     #prepare figures for volcano plots
        #     volcano_average = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_welch",
        #         effect_size="fold_average",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     volcano_median = dashbio.VolcanoPlot(
        #         dataframe=total_panda,#bins_panda,
        #         snp="english_name",
        #         p="sig_mannwhit",
        #         effect_size="fold_median",
        #         gene=None,
        #         xlabel='log2 Fold Change',
        #         genomewideline_value=1e-2,
        #     )
        #     #################################################3

            return (
                column_list,
                data
        #         volcano_average,
        #         volcano_median,
            )



    return server

# if __name__ == "__main__":
#     app.run_server(debug=True)
if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap

    bootstrap = Bootstrap()
    app = Flask(__name__)
    bootstrap.init_app(app)

    # inject Dash
    app = add_dash(app) #, login_req=False)

    @app.route(URL_BASE)
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 8050
    print(f'http://localhost:{app_port}{URL_BASE}')
    app.run(debug=True, port=app_port)