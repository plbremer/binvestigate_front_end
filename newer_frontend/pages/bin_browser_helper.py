from enum import unique
import pandas as pd

def generate_bin_dropdown_options():
    temp=pd.read_pickle('../newer_datasets/compound_translation_panda.bin')
    temp=temp.loc[temp.bin_type!='class',:]
    unique_bins=dict(zip(
        temp.english_name+' | ' +temp.identifier,temp.compound_identifier
    ))
    return unique_bins