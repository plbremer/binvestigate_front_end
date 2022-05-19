# 1
# 20
# [{'column_id': 'continent', 'direction': 'asc'}, {'column_id': 'lifeExp', 'direction': 'asc'}]
# {continent} scontains Asia && {lifeExp} s> 50
import requests
import pathlib
import json
#import networkx as nx
from pprint import pprint
import pandas as pd
#import venn
import numpy as np
import re

import dash
#from dash import Dash
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

from plotly.tools import mpl_to_plotly
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dash_table.Format import Format, Scheme, Group

#flask app adjustment
APP_ID='sunburst_frontend'
URL_BASE='/dash/sunburst_frontend/'
MIN_HEIGHT=2000
# external_stylesheets = [dbc.themes.DARKLY]
# app = Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server

base_url_api = "http://127.0.0.1:4999/"
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


############### LOAD HIERARCHIES ##############
compound_json_address = DATA_PATH.joinpath("cyto_format_compound.json")
temp_json_file = open(compound_json_address, "r")
compound_dict = json.load(temp_json_file)
temp_json_file.close()
for temp_element in compound_dict["elements"]["nodes"]:
    #options included 'id' 'inchikey' 'name' 'value'
    #also has property "type_of_node" (is it a leaf or not)
    temp_element["data"]["label"] = temp_element["data"]["id"]
###########################################


######### HELPER FUNCTIONS ################
def create_compound_selection_labels(temp_compound_dict):
    #{'label': temp_node['data']['label'], 'value': temp_node['data']['label']} for temp_node in compound_dict['elements']['nodes']
    compound_dropdown_options=list()
    for temp_node in temp_compound_dict['elements']['nodes']:
        if temp_node['data']['type_of_node']=='from_binvestigate':
            if bool(re.search('^([\s\d]+)$',temp_node['data']['common_name'])):
                compound_dropdown_options.append(
                    {'label': 'Unknown: Bin ID '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
                )
            else:
                compound_dropdown_options.append(
                    {'label': 'Known: '+temp_node['data']['common_name'], 'value': temp_node['data']['label']}
                )
        # else:
        #     compound_dropdown_options.append(
        #         {'label': 'Class: '+temp_node['data']['name'], 'value': temp_node['data']['label']}
        #     )            
    return compound_dropdown_options
compound_dropdown_options=create_compound_selection_labels(compound_dict)  


def construct_order_by(order_list):
    '''
    unlike the other order by functions, this one returns two parallel lists
    '''#[{'column_id': 'english_name', 'direction': 'asc'}, {'column_id': 'fold_average', 'direction': 'asc'}]
    # if len(order_list)==0:
    #     return ''
    # total_string='order by\n'
    column_list=[element['column_id'] for element in order_list]
    asc_list=[True if (element['direction']=='asc') else False for element in order_list]
    # for temp_dict in order_list:
    #     # total_string = total_string+temp_dict['column_id']+' '+temp_dict['direction']+',\n'
    #     column_list.append('')
    #total_string=total_string[:-2]
    return column_list,asc_list


def construct_one_clause(one_specification):
    temp_list=one_specification.split(' ')
    if (temp_list[1]=='s>') or (temp_list[1]=='s>=') or (temp_list[1]=='s<') or (temp_list[1]=='s<=') or (temp_list[1]=='s='):
        #temp_where_clause='('+temp_list[0][1:-1]+' '+temp_list[1][1:]+' '+temp_list[2]+')'
        temp_loc_clause='('+temp_list[0][1:-1]+' '+temp_list[1][1:]+' '+temp_list[2]+')'
        return temp_loc_clause#[temp_list[0][1:-1],temp_list[1][1:],temp_list[2]]#
    elif (temp_list[1]=='scontains'):
        temp_loc_clause='("'+temp_list[2]+'" in '+temp_list[0][1:-1]+')'
        return temp_loc_clause#[temp_list[0][1:-1],'contains',temp_list[2]]#

def construct_filter_where(filter_string):
    '''
    unfortunately, dash doesnt have have a parser that allows for multiple conditions build in
    so we had to write our own
    If we have a single condition (the filter description doesnt have a ")
    Then we go to the simple parsing function
    If we do have multiple conditions, then we do a lot of coercing to get our condition
    to read like multiple other conditions
    '''
    if len(filter_string)==0:
        return ''
    filter_list=filter_string.split(' && ')
    where_clauses=list()
    for filter_statement in filter_list:
        if ('"' not in filter_statement):
            where_clauses.append(construct_one_clause(filter_statement))
        elif ('\"' in filter_statement):
            filter_statement=filter_statement.replace('"','')
            filter_statement=filter_statement.replace('<','< ')
            filter_statement=filter_statement.replace('<=','<= ')
            filter_statement=filter_statement.replace('>','> ')
            filter_statement=filter_statement.replace('>=','>= ')
            filter_statement=filter_statement.replace('=','= ')
            filter_statement=filter_statement.replace('  ',' ')
            filter_statement=filter_statement.replace(' <',' s<')
            filter_statement=filter_statement.replace(' <=',' s<=')
            filter_statement=filter_statement.replace(' >',' s>')
            filter_statement=filter_statement.replace(' >=',' s>=')
            filter_statement=filter_statement.replace(' =',' s=')
            sublist=filter_statement.split(' ')
            
            if (sublist[1]=='s>') or (sublist[1]=='s>=') or (sublist[1]=='s<') or (sublist[1]=='s<=') or (sublist[1]=='s='):
                sub_sublist=list()
                connector_sublist=list()
                for i in range(1,len(sublist),3):
                    try:
                        connector_sublist.append(sublist[i+2])
                    except IndexError:
                        connector_sublist.append('')
                        
                    sub_sublist.append(sublist[0]+' '+sublist[i]+' '+sublist[i+1])
                substring='('
                #substring=list()
                for i, item in enumerate(sub_sublist):
                    substring=substring+construct_one_clause(item)+' '+connector_sublist[i]+' '#.append(construct_one_clause(item))#
                    #substring.append(connector_sublist[i])
                substring=substring+')'
            elif sublist[1]=='scontains':
                sub_sublist=list()
                connector_sublist=list()
                for i in range(2,len(sublist),2):
                    try:
                        connector_sublist.append(sublist[i+1])
                    except IndexError:
                        connector_sublist.append('')
                    sub_sublist.append(sublist[0]+' '+sublist[1]+' '+sublist[i])
                substring='('#list()
                for i, item in enumerate(sub_sublist):
                    substring=substring+construct_one_clause(item)+' '+connector_sublist[i]+' '
                    #substring.append(construct_one_clause(item))#
                    #substring.append(connector_sublist[i])
                substring=substring+')'     
            where_clauses.append(substring)
    #where_clause_string=' and '
    where_clause_string=' and '.join(where_clauses)#[element for element in where_clauses]#
    # for where_clause in where_clauses:
    #     where_clause_string=where_clause_string+where_clause+' and '
    #where_clause_string=where_clause_string.replace(' or ',' | ')
    #where_clause_string=where_clause_string.replace(' and ',' & ')
    #where_clause_string=where_clause_string[:-5]
    return where_clause_string

def coerce_full_panda(df,value_column,column_list):
    #df=df.round({value_column:6})
    pandas_list=list()
    for i in range(len(column_list),0,-1):
        pandas_list.append(
            pd.DataFrame(
                data={
                    'count':df.groupby(by=column_list[0:i]).size().to_list(),
                    'sum':df.groupby(by=column_list[0:i])[value_column].sum().to_list(),
                    'parent':['/'.join(group[0][:i-1]) for group in df.groupby(by=column_list[0:i])],
                    'id':df[column_list[0:i]].T.agg('/'.join).unique(),
                    'name':df.groupby(by=column_list[0:i])[column_list[i-1]].unique().map(lambda x: x[0]).values
                }
            )
        )
    tree_panda=pd.concat(pandas_list,axis='index')
    tree_panda.reset_index(inplace=True,drop=True)
    tree_panda['average']=tree_panda['sum']/tree_panda['count']
    ###########################################################
    #there is a known bug in the way that branch totals works
    #https://community.plotly.com/t/plotly-sunburst-returning-empty-chart-with-branchvalues-total/26582/8
    #no matter what i tried, i could not get the branch total thing to work for me
    #so we use a hack workaround for now - everything except for the lowest levels is set to 0 for valeus
    #now we can use remainder and it should work as intended
    first_parent_index=len(df.index)
    tree_panda.loc[first_parent_index:,'sum']=0
    return tree_panda
# def build_hierarchical_dataframe(df, levels, value_column):#, color_columns=None):
#     """
#     asdf
#    """
    #tree_df=pd.DataFrame(columns=['labels','ids','parents','values','averages'])

    # tree_df
    # lowest_level=pd.DataFrame(
    #     data={
    #         'labels'=df[levels[-1]],
    #         'ids':[]
    #     }
    # )

    # for i, level in enumerate(levels):
    #     df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    #     dfg = df.groupby(levels[i:]).sum()
    #     dfg = dfg.reset_index()
    #     df_tree['id'] = dfg[level].copy()
    #     if i < len(levels) - 1:
    #         df_tree['parent'] = dfg[levels[i+1]].copy()
    #     else:
    #         df_tree['parent'] = 'total'
    #     df_tree['value'] = dfg[value_column]
    #     #df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
    #     tree_df = tree_df.append(df_tree, ignore_index=True)
    # total = pd.Series(dict(id='total', parent='',
    #                           value=df[value_column].sum()))#,
    #                           #color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
    # tree_df = tree_df.append(total, ignore_index=True)
    # return tree_df
# def construct_pandas_query_string(filter_query_list):
#     my_string='('
#     for column in filter_query_list:
#         if len(column)==2:
#             if column[1]



#stolen from https://dash.plotly.com/datatable/callbacks
# operators = [['ge ', '>='],
#              ['le ', '<='],
#              ['lt ', '<'],
#              ['gt ', '>'],
#              ['ne ', '!='],
#              ['eq ', '='],
#              ['contains '],
#              ['datestartswith ']]


# def split_filter_part(filter_part):
#     '''
#     stolen from https://dash.plotly.com/datatable/callbacks
#     '''
#     for operator_type in operators:
#         for operator in operator_type:
#             if operator in filter_part:
#                 name_part, value_part = filter_part.split(operator, 1)
#                 name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

#                 value_part = value_part.strip()
#                 v0 = value_part[0]
#                 if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
#                     value = value_part[1: -1].replace('\\' + v0, v0)
#                 else:
#                     try:
#                         value = float(value_part)
#                     except ValueError:
#                         value = value_part

#                 # word operators need spaces after them in the filter string,
#                 # but we don't want these later
#                 return name, operator_type[0].strip(), value

#     return [None] * 3
########################################


#############Load pandas for data selection options ##########
# unique_sod_combinations_address = DATA_PATH.joinpath("unique_sod_combinations.bin")

# unique_sod_combinations_panda = pd.read_pickle(unique_sod_combinations_address)
# unique_sod_combinations_dict = {
#     temp:temp for temp in unique_sod_combinations_panda.keys().to_list()
# }
# pprint(unique_sod_combinations_dict)
########################################


#####Read in panda for filtering options after one is selected######

####################################################################


############Update pandas for data selection#################

#############################################

################create temp mpl fig####################
# labels = venn.get_labels([range(20), range(5, 15), range(3, 8)], fill=['number', 'logic'])
# fig, ax = venn.venn3(labels, names=['Human Plasma No', 'a;lskdjfa;lskjdfafs', 'b'])
# #plotly_fig = mpl_to_plotly(fig)
# buf = io.BytesIO() # in-memory files
# #plt.scatter(x, y)
# plt.savefig(buf, format = "png") # save to the above file object
# plt.close()
# data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
# plotly_fig="data:image/png;base64,{}".format(data)
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
    app.layout=dbc.Container(#html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H2("Sunburst Comparator", className='text-center'),
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
                                            id='compound_selection',
                                            # options=[
                                            #     #{'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict_from['elements']['nodes']
                                            #     {'label': temp, 'value':unique_sod_combinations_dict[temp]} for temp in unique_sod_combinations_dict
                                            # ],
                                            options=compound_dropdown_options,
                                            multi=False,
                                            style={
                                                'color': '#212121',
                                                'background-color': '#3EB489',
                                            }
                                        ),
                                        html.Button(
                                            'Get Results',
                                            id='button_query',
                                        )
                                    ]
                                )
                            ),
                            html.Br(),
                            dbc.Card(
                                dbc.CardBody(
                                    children=[                            
                                        # html.H6("Minimum Percent Present", className='text-center'),
                                        # dcc.Slider(
                                        #     id='slider_percent_present',
                                        #     #label='Minimum Percent Present',
                                        #     min=0,
                                        #     max=100,
                                        #     step=1,
                                        #     value=80,   
                                        #     marks=None,
                                        #     tooltip={"placement": "bottom", "always_visible": True}       
                                        # ),
                                        # html.H6("Median or Average", className='text-center'),
                                        # daq.ToggleSwitch(
                                        #     id='toggle_average_true',
                                        #     value=True,
                                        #     #label='Median - Average'
                                        # ),
                                        html.H6("Order of sunburst"),
                                        dcc.RadioItems(
                                            id='radio_items_sod_order',
                                            options=[
                                                {'label': 'Species, Organ, Disease', 'value': 'binvestigate,species,organ,disease'},
                                                {'label': 'Organ, Species, Disease', 'value': 'binvestigate,organ,species,disease'},
                                                #{'label': 'Unique', 'value': 'unique'},
                                            ],         
                                            value='binvestigate,species,organ,disease'                              
                                        ),
                                        html.H6("Type of Data"),
                                        dcc.RadioItems(
                                            id='radio_items_sunburst_value',
                                            options=[
                                                {'label': 'Average', 'value': 'intensity_average'},
                                                {'label': 'Median', 'value': 'intensity_median'},
                                                {'label': 'Percent Present', 'value':'percent_present'}
                                                #{'label': 'Unique', 'value': 'unique'},
                                            ],         
                                            value='intensity_average'                                   
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
                                    dcc.Graph(
                                        id='figure_sunburst',
                                        #figure=plotly_fig
                                    )
                                    # html.Img(
                                    #     id='Img_venn',
                                    #     #src=plotly_fig,
                                    #     height=200,
                                    #     width=200
                                    # )
                                )
                            ),
                        ],
                        width={'size':8}
                    )
                ],
                justify='around'
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Br(),
                            html.H2("Results", className='text-center'),
                            # dbc.Card(
                            #     dbc.CardBody(
                            #         children=[
                            #             # html.Button(
                            #             #     'Get Results',
                            #             #     id='button_query',
                            #             # )
                            #         ]
                            #     )
                            # )
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
                                {"name": "Species", "id": "bin_id"},
                                {"name": "Organ", "id": "compound_name"},
                                {"name": "Disease", "id": "group_1"},
                                {"name": "Metric", "id": "metric"}
                            ],
                            data=[],
                            page_current=0,
                            page_size=10,
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
            # dbc.Modal(
            #     dbc.ModalBody(
            #         html.Img(
            #             id='modal_Img_venn',
            #             #src=plotly_fig,
            #             height=700,
            #             width=700
            #         )
            #     ),
            #     id='modal',
            #     is_open=False
            # )
            # html.Div(
            #     id = 'hidden_panda',
            #     #children = [data_dict],
            #     style = {'display': 'none'}
            # )
            dcc.Store(
                id='store_data',
                #data=None
            )
        ]
    )
    #####################################################
    @app.callback(
        [
            Output(component_id='store_data', component_property='data'),
        ],
        [
            Input(component_id='button_query', component_property='n_clicks'),
        ],
        [
            State(component_id='compound_selection',component_property='value')
        ],
        prevent_initial_call=True
        #prevent_initial_call=True
    )
    def query_api(button_query_n_clicks,compound_selection_value):
        # if n % 2 == 0:
        #     return {'display': 'none'}
        # else:
        #     return {
        #         'display': 'block',
        #         'z-index': '1',
        #         'padding-top': '100',
        #         'left': '0',
        #         'top': '0',
        #         'width': '100%',
        #         'height': '100%',
        #         'overflow': 'auto'
        #         }
        print('-----------------------------------------------------')
        print(compound_selection_value)

        sunburst_output={
            "compound":compound_selection_value,
            # "page_size":page_size,
            # "sort_by":sort_by,
            # "filter_query":filter_query,
            # "dropdown_triplet_selection_value":dropdown_triplet_selection_value,
            # "slider_percent_present_value":slider_percent_present_value,
            # "toggle_average_true_value":toggle_average_true_value,
            # "radio_items_filter_value":radio_items_filter_value
        }

        #pprint(venn_data_table_output)
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
        response = requests.post(base_url_api + "/sunburstresource/", json=sunburst_output)
    #     print(response)
        total_panda = pd.read_json(response.json(), orient="records")
        print(total_panda)
        total_panda['binvestigate']='binvestigate'

    # #     #prepare columns and data for the table
    #     column_list = [
    #         {"name": "bin", "id": "bin"},
    #         {"name": "English Name", "id":"compound"}
    #     ]
    #     sod_column_list=[
    #         {"name": temp_column, "id": temp_column,"type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)} for temp_column in total_panda.columns 
    #         if (temp_column != "bin" and temp_column!="compound")
    #     ]
    #     #     {"name": "Fold Average", "id": "fold_average","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
    #     #     {"name": "Significance Welch", "id": "sig_welch","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)},
    #     #     {"name": "Fold Median", "id": "fold_median","type": "numeric","format": Format(group=Group.yes, precision=2, scheme=Scheme.exponent)},
    #     #     {"name": "Significance MWU", "id": "sig_mannwhit","type": "numeric","format": Format(group=Group.yes, precision=4, scheme=Scheme.exponent)}
    #     # ]
    #     column_list+=sod_column_list
        data = total_panda.to_dict(orient='records')


        return [data]

        #return [{'hi':'bye'}]

    @app.callback(
        [
            Output(component_id="table", component_property="columns"),
            Output(component_id="table", component_property="data"),
            Output(component_id='figure_sunburst',component_property='figure'),
            Output(component_id='table',component_property='filter_query')
        ],
        [
            Input(component_id='radio_items_sod_order',component_property='value'),
            Input(component_id='radio_items_sunburst_value',component_property='value'),
            Input(component_id="table", component_property="page_current"),
            Input(component_id="table", component_property="page_size"),
            Input(component_id="table", component_property="sort_by"),
            Input(component_id="table", component_property="filter_query"),
            Input(component_id='store_data',component_property='data'),
            Input(component_id='figure_sunburst',component_property='clickData')
        ],
        [
            State(component_id='figure_sunburst',component_property='figure')
        ]
    )
    def generate_visible_data(
        radio_items_sod_order_value,
        radio_items_sunburst_value_value,
        page_current,
        page_size,
        sort_by,
        filter_query,
        store_data_data,
        sunburst_clickdata,
        current_figure
    ):
        #print(store_data_data)
        #full_panda=pd.read_json(json.loads(store_data_data), orient="records")
        full_panda=pd.DataFrame(store_data_data)
        print('hi')
        print(dash.callback_context.triggered)
        print('#############################3')
        print(radio_items_sunburst_value_value)
        

        #if dash.callback_context.triggered=='radio_items_sunburst_value.value':


        #this didnt work. The value changed as intended btu the datatable didnt render it        
        #we need to make sure that the variable in filter is the same as the radio item sunburst value
        #we just hardcode change it every time
        if dash.callback_context.triggered[0]['prop_id']=='radio_items_sunburst_value.value':
            print(filter_query)
            filter_query_list=filter_query.split('&&')
            print(filter_query_list)
            for i,element in enumerate(filter_query_list):
                if ('intensity_average' in element) or ('intensity_median' in element) or ('percent_present' in element):
                    #filter_query_list[i]='{'+radio_items_sunburst_value_value+element[element.find('}'):]
                    del filter_query_list[i]
                else:
                    filter_query_list[i]=element.strip()
            print(filter_query_list)
            filter_query='&&'.join(filter_query_list)
            print(filter_query)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

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
        full_panda=full_panda[['binvestigate','species','organ','disease',last_column['id']]]

        print('+++++++++++++++++++++++++++++')
        print(page_current)
        print(page_size)
        print(sort_by)
        print(filter_query)
        #print(sunburst_clickdata)
        print('-----------------------------')
        
        print(construct_filter_where(filter_query))
        print('===================================')

        if len(filter_query)>0:
            filter_query_string=construct_filter_where(filter_query)
            print(filter_query_string)
            #pandas_query_string=construct_pandas_query_string(filter_query_list)
            #exec(f'full_panda=full_panda.loc[{filter_query_string}]')
            full_panda=full_panda.query(filter_query_string)
            print(full_panda)
            print('**************************************8')


        if (dash.callback_context.triggered[0]['prop_id']=='figure_sunburst.clickData'):
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(dash.callback_context.triggered[0])
            sod_order=radio_items_sod_order_value.split(',')
            print(sod_order)
            row_subset_list=sunburst_clickdata['points'][0]['id'].split('/')
            print(row_subset_list)
            sunburst_query_string_list=['("'+row_subset_list[i]+'" in '+sod_order[i]+')' for i in range(len(row_subset_list))]
            print(sunburst_query_string_list)
            sunburst_query_string=' and '.join(sunburst_query_string_list)
            print(sunburst_query_string)
            full_panda=full_panda.query(sunburst_query_string)
            print(full_panda)

        elif (dash.callback_context.triggered[0]['prop_id']!='figure_sunburst.clickData'):
            
            full_panda.to_csv('./sunburst_panda.csv',sep='@')
            print(radio_items_sunburst_value_value)
            print(radio_items_sod_order_value)
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            #tree_df=build_hierarchical_dataframe(full_panda,radio_items_sod_order_value.split(',')[::-1],radio_items_sunburst_value_value)
            tree_df=coerce_full_panda(full_panda,radio_items_sunburst_value_value,radio_items_sod_order_value.split(','))
            #count sum parent id name average
            
            # tree_df['color']=0.2
            #print(tree_df)
            # current_figure=px.sunburst(
            #     #data_frame=tree_df,
            #     parents=tree_df['parent'],
            #     names=tree_df['id'],
            #     values=tree_df['value']
            # )
            # current_figure =go.Figure(go.Sunburst(
            #     labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
            #     parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
            #     values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
            # ))
            #f#or ir range(len(tree_df.parent.values)):
            # for i,series in tree_df.iterrows():
            #     print(series['parent']+' '+series['id']+' '+str(series['value']))
            #print(tree_df.parent)
            #print(tree_df.id)
            #print(tree_df.value)
            #print(full_panda.intensity_average.sum())
            print(tree_df)
            current_figure=go.Figure(
                go.Sunburst(
                    #data_frame=tree_df,
                    parents=tree_df['parent'].to_list(),
                    labels=tree_df['name'].to_list(),
                    values=tree_df['sum'].to_list(),
                    ids=tree_df['id'].to_list(),
                    hovertext=tree_df['average'].to_list(),
                    hoverinfo='text'
                    #branchvalues='total'
                )
            )
            #print(current_figure.to_dict())
            # current_figure=px.sunburst(
            #     data_frame=tree_df,
            #     names='id',
            #     parents='parent',
            #     values='value',                
            # )       
            # current_figure=px.sunburst(
            #     data_frame=full_panda,
            #     path=radio_items_sod_order_value.split(','),
            #     values=radio_items_sunburst_value_value
            # )   
              
            # current_figure=go.Figure(
            #     go.Sunburst(
            #         # data,
            #         # names='character',
            #         # parents='parent',
            #         # values='value',
            #         #data_frame=full_panda,
            #         #path=['binvestigate','species','organ','disease'],
            #         #path=eval(radio_items_sunburst_value_value),
            #         #path=radio_items_sod_order_value.split(','),
            #         #values=np.average(radio_items_sunburst_value_value),
            #         # labels=tree_df['id'],
            #         # parents=tree_df['parent'],
            #         # values=tree_df['value'],
            #         # branchvalues='total'
            #         #labels=
            #         #hover_data=['id',last_column['id']]
            #         #hovertemplate='<b>%{label} </b>'
            #         labels=tree_df['id'],
            #         parents=tree_df['parent'],
            #         values=tree_df['value'],
            #         # branchvalues='total',
            #         # marker=dict(
            #         #     colors=tree_df['color'],
            #         #     colorscale='RdBu',
            #         #     #cmid=average_score),
            #         # )
            #     )
            # )
            # current_figure.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        # if sunburst_clickdata is not None:
        #     row_subset_list=sunburst_clickdata['points'][0]['id'].split('/')
        #     sod_order=radio_items_sod_order_value.split(',')            
        
        if len(sort_by)>0:
            sort_column_list,sort_asc_list=construct_order_by(sort_by)
            full_panda.sort_values(by=sort_column_list,ascending=sort_asc_list,inplace=True)

        full_panda=full_panda.iloc[(page_current*page_size):(page_current*page_size+page_size),:]

        data = full_panda.to_dict(orient='records')
        return [column_list,data,current_figure,filter_query]



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