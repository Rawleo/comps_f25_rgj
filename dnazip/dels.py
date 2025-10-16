import pandas as pd
import numpy as np
from vint import *

def encode_dels(dels_df):
    
    
    ### convert respective pos and variation info into vints 

    dels_df["pos"] = dels_df["pos"].astype(int).apply(writeBitVINT)
    dels_df["var_info"] = dels_df["var_info"].apply(lambda x: len(x.split('/')[0])).apply(writeBitVINT)
    # print(dels_df["var_info"])
    
    ### merge the position and the variation info per line
    
    dels_df["pos_var_vint"] = dels_df["pos"].astype(str) + dels_df["var_info"].astype(str)
    # print(dels_df["pos_var_vint"])
    
    
    ### calc number of dels
    dels_size = dels_df.shape[0]
    
    
    ### return one whole concatenated line (pos_bitstring + del_bitstring) for the chromosome
    ### where the string is composed of pos_del_bitstring pairs. 
    
    del_bitstring_pair = ''.join(dels_df["pos_var_vint"].astype(str).tolist())
    
    return dels_size, del_bitstring_pair
