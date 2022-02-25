import json
import networkx as nx
from pprint import pprint
import pandas as pd

from dash import Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


from generic_layout import *

base_url='http://127.0.0.1:5000/'
import requests



external_stylesheets = [dbc.themes.DARKLY]

app=Dash(__name__,external_stylesheets=external_stylesheets)
server=app.server














app.layout=define_layout("basic_query")














@app.callback(
    [Output(component_id='table_query_summary',component_property='columns'),
    Output(component_id='table_query_summary',component_property='data'),

    Output(component_id='table_average_welch_bins',component_property='columns'),
    Output(component_id='table_average_welch_bins',component_property='data'),
    Output(component_id='table_median_mw_bins',component_property='columns'),
    Output(component_id='table_median_mw_bins',component_property='data'),
    
    Output(component_id='table_average_welch_classyfire',component_property='columns'),
    Output(component_id='table_average_welch_classyfire',component_property='data'),
    Output(component_id='table_median_mw_classyfire',component_property='columns'),
    Output(component_id='table_median_mw_classyfire',component_property='data'),
    
    Output(component_id='volcano_average_welch_bins',component_property='figure'),
    Output(component_id='volcano_median_mw_bins',component_property='figure'),
    Output(component_id='volcano_average_welch_classyfire',component_property='figure'),
    Output(component_id='volcano_median_mw_classyfire',component_property='figure')],

    [Input(component_id='button_query',component_property='n_clicks')],
    [State(component_id='dropdown_from_species',component_property='value'),
    State(component_id='dropdown_from_organ',component_property='value'),
    State(component_id='dropdown_from_disease',component_property='value'),
    State(component_id='dropdown_to_species',component_property='value'),
    State(component_id='dropdown_to_organ',component_property='value'),
    State(component_id='dropdown_to_disease',component_property='value'),
    ]
)
def perform_volcano_query(
    query,
    from_species_value,
    from_organ_value,
    from_disease_value,
    to_species_value,
    to_organ_value,
    to_disease_value
):
    '''
    we perform the query information post as well as the
    '''


    ########metadata query########
    metadata_json_output={
        "from_species":from_species_value,
        "from_organ":from_organ_value,
        "from_disease":from_disease_value,
        "to_species":to_species_value,
        "to_organ":to_organ_value,
        "to_disease":to_disease_value
        }
    response=requests.post(base_url+'/metadataresource/',json=metadata_json_output)
    total_panda=pd.read_json(response.json(),orient='records')
    print(total_panda)

    query_summary_column_list=[
        {'name':temp_col,'id':temp_col} for temp_col in total_panda.columns
    ]
    print(query_summary_column_list)
    query_summary_data=total_panda.to_dict(orient='records')
    # query_summary_data=[
    #     {temp_key]:str(query_summary_data[temp_key]) for temp_key in query_summary_data}
    # ]
    for temp_key in query_summary_data[0]:
        query_summary_data[0][temp_key]=str(query_summary_data[0][temp_key])
    print(query_summary_data) 
    # query_summary_data=[
    #     {
    #         'triplet_count_to': 1, 
    #         'sample_count_list_to': 3160, 
    #         'min_sample_count_to': 3160, 
    #         'sum_sample_count_to': 3160, 
    #         'unique_triplet_list_real_to': 234,#[['Plasma', '10090', 'No']], 
    #         'triplet_count_from': 1, 
    #         'sample_count_list_from': 234,#[3160], 
    #         'min_sample_count_from': 3160, 
    #         'sum_sample_count_from': 3160, 
    #         'unique_triplet_list_real_from': 234# [['Plasma', '10090', 'No']]
    #     }
    # ]


    #############################
    


    #################volcano query#######3

    volcano_json_output={
        "from_species":from_species_value,
        "from_organ":from_organ_value,
        "from_disease":from_disease_value,
        "to_species":to_species_value,
        "to_organ":to_organ_value,
        "to_disease":to_disease_value,
        "include_known":"Yes",
        "include_unknown":"Yes",
        "fold_median_min":0,
        "fold_average_min":0,
        "p_welch_max":1,
        "p_mann_max":1        
    }


    response=requests.post(base_url+'/volcanoresource/',json=volcano_json_output)
    total_panda=pd.read_json(response.json(),orient='records')
    #pd.set_option('display.max_rows',200)
    print(total_panda)

    average_welch_column_list=[
        {'name':'compound','id':'compound'},{'name':'fold_average','id':'fold_average'},{'name':'sig_welch','id':'sig_welch'},
    ]
    average_welch_data_bin=total_panda.loc[
        (~total_panda['compound'].str.contains('CHEMONTID')),
        ['compound','fold_average','sig_welch']
    ].to_dict(orient='records')
    average_welch_data_classyfire=total_panda.loc[
        (total_panda['compound'].str.contains('CHEMONTID')),
        ['compound','fold_average','sig_welch']
    ].to_dict(orient='records')
    median_mw_column_list=[
        {'name':'compound','id':'compound'},{'name':'fold_median','id':'fold_median'},{'name':'sig_mannwhit','id':'sig_mannwhit'},
    ]
    median_mw_data_bin=total_panda.loc[
        (~total_panda['compound'].str.contains('CHEMONTID')),
        ['compound','fold_median','sig_mannwhit']
    ].to_dict(orient='records')
    median_mw_data_classyfire=total_panda.loc[
        (total_panda['compound'].str.contains('CHEMONTID')),
        ['compound','fold_median','sig_mannwhit']
    ].to_dict(orient='records')
    print(total_panda)
    print(total_panda.loc[(~total_panda['compound'].str.contains('CHEMONTID'))])
    print(total_panda.loc[(total_panda['compound'].str.contains('CHEMONTID'))])

    bins_panda=total_panda.loc[(~total_panda['compound'].str.contains('CHEMONTID'))].copy(deep=True)
    classyfire_panda=total_panda.loc[(total_panda['compound'].str.contains('CHEMONTID'))].copy(deep=True).reset_index()


    volcano_average_bin=dashbio.VolcanoPlot(
        dataframe=bins_panda,
        snp='compound',
        p='sig_welch',
        effect_size='fold_average',
        gene=None
    )
    volcano_average_classyfire=dashbio.VolcanoPlot(
        dataframe=classyfire_panda,
        snp='compound',
        p='sig_welch',
        effect_size='fold_average',
        gene=None
    )
    volcano_median_bin=dashbio.VolcanoPlot(
        dataframe=bins_panda,
        snp='compound',
        p='sig_mannwhit',
        effect_size='fold_median',
        gene=None
    )
    volcano_median_classyfire=dashbio.VolcanoPlot(
        dataframe=classyfire_panda,
        snp='compound',
        p='sig_mannwhit',
        effect_size='fold_median',
        gene=None
    )

    #################################################3

    return query_summary_column_list,query_summary_data,average_welch_column_list,average_welch_data_bin,median_mw_column_list,median_mw_data_bin,average_welch_column_list,average_welch_data_classyfire,median_mw_column_list,median_mw_data_classyfire,volcano_average_bin,volcano_median_bin,volcano_average_classyfire,volcano_median_classyfire

if __name__ == '__main__':

    app.run_server(debug=True)