import networkx as nx
import re
import pandas as pd


######### HELPER FUNCTIONS ################
def create_compound_selection_labels(final_curations_address):
    # compound_dropdown_options=list()
    # compound_networkx=nx.read_gpickle(nx_address)

    # final_curations=pd.read_csv(final_curations_address,sep='\t')
    # final_curations=final_curations.loc[
    #     final_curations['english_name_curated']!='DELETE'
    # ]
    # final_curation_valid_bin_set=set(final_curations.integer_representation.unique())
    # final_curation_map=dict(zip(
    #     final_curations['integer_representation'],final_curations['english_name_curated']
    # ))
    # print(final_curation_valid_bin_set)
    # print(compound_networkx.nodes)
    
    # for temp_node in compound_networkx.nodes:

    #     if compound_networkx.nodes[temp_node]['type_of_node']=='from_binvestigate':
    #         #i believe that this is checcking for an integer name
    #         if bool(re.search('^([\s\d]+)$',compound_networkx.nodes[temp_node]['common_name'])):
    #             compound_dropdown_options.append(
    #                 {'label': 'Unknown: Bin ID '+compound_networkx.nodes[temp_node]['common_name'], 'value': temp_node}
    #             )
    #         # else:
    #         #     #print(temp_node)
    #         #     if int(temp_node) in final_curation_valid_bin_set:
    #         #         compound_dropdown_options.append(
    #         #             {
    #         #                 'label': 'Known: '+final_curation_map[temp_node],#compound_networkx.nodes[temp_node]['common_name'], 
    #         #                 'value': temp_node
    #         #             }
    #         #         )
           
    # return compound_dropdown_options
    final_curations=pd.read_pickle(final_curations_address)
    final_curations.loc[final_curations.bin_type=='known','english_name']='Known: '+final_curations.loc[final_curations.bin_type=='known']['english_name'].astype(str)
    final_curations.drop(['bin_type','identifier'],axis='columns',inplace=True)
    final_curations.rename(columns={'compound_identifier':'value','english_name':'label'},inplace=True)
    
    #compound_dropdown_options=
    return final_curations.to_dict(
        'records'
    )


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
                    #'id':df[column_list[0:i]].T.agg('/'.join).unique(),
                    'id':['/'.join(group[0][:i]) for group in df.groupby(by=column_list[0:i])],
                    'name':df.groupby(by=column_list[0:i])[column_list[i-1]].unique().map(lambda x: x[0]).values
                }
            )
        )
    tree_panda=pd.concat(pandas_list,axis='index')
    tree_panda.reset_index(inplace=True,drop=True)
    tree_panda.at[len(tree_panda.index)-1,'id']='binvestigate'
    tree_panda['average']=tree_panda['sum']/tree_panda['count']
    ###########################################################
    #there is a known bug in the way that branch totals works
    #https://community.plotly.com/t/plotly-sunburst-returning-empty-chart-with-branchvalues-total/26582/8
    #no matter what i tried, i could not get the branch total thing to work for me
    #so we use a hack workaround for now - everything except for the lowest levels is set to 0 for valeus
    #now we can use remainder and it should work as intended
    first_parent_index=len(df.index)
    tree_panda.loc[first_parent_index:,'sum']=0

    # print('*********************************')
    # print(tree_panda)

    tree_panda=tree_panda.round(decimals=0)
    tree_panda['average']=tree_panda['average'].astype(int)

    
    return tree_panda