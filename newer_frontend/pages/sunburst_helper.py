import networkx as nx
import re



######### HELPER FUNCTIONS ################
def create_compound_selection_labels(nx_address):
    compound_dropdown_options=list()
    compound_networkx=nx.read_gpickle(nx_address)
    
    for temp_node in compound_networkx.nodes:

        if compound_networkx.nodes[temp_node]['type_of_node']=='from_binvestigate':
            if bool(re.search('^([\s\d]+)$',compound_networkx.nodes[temp_node]['common_name'])):
                compound_dropdown_options.append(
                    {'label': 'Unknown: Bin ID '+compound_networkx.nodes[temp_node]['common_name'], 'value': temp_node}
                )
            else:
                compound_dropdown_options.append(
                    {'label': 'Known: '+compound_networkx.nodes[temp_node]['common_name'], 'value': temp_node}
                )
           
    return compound_dropdown_options

