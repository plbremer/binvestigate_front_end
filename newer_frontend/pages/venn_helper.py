#the purpose of this is to keep all of the things that assist in the venn diagram creation
#separate in order to make the code less confusing

import pandas as pd


#############Load pandas for data selection options ##########
def get_unique_sod_combinations():
    unique_sod_combinations_address = "../newer_datasets/unique_sod_combinations.bin"
    unique_sod_combinations_panda = pd.read_pickle(unique_sod_combinations_address)
    unique_sod_combinations_dict = {
        temp:temp for temp in unique_sod_combinations_panda.keys().to_list()
    }
    return unique_sod_combinations_dict
##############################################################