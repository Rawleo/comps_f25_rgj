import pandas as pd
import numpy as np
from vint import *

def encode_dels(dels_df):

    dels_df[1] = dels_df[1].astype(int).apply(writeBitVINT)
    dels_df[1] = dels_df[1].astype(int).apply(writeBitVINT)

    pos_bitstring = ''.join(dels_df[1].astype(str).tolist())
    del_bitstring = ''.join(dels_df[2].astype(str).tolist())
    dels_size = dels_df.shape[0]

    return dels_size, pos_bitstring, del_bitstring
