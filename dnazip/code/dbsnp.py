import pandas as pd
import numpy as np
import sys
from vint import *

def compares_dbsnp(snps_df, dbsnp_path, chr):

    dbsnp_df = pd.read_csv(dbsnp_path + chr + ".txt", header=None)
    dbsnp_df['bit_array'] = 0
    snps_df['mapped'] = 0

    # Set bit_array to 1 where dbsnp_df row matches snps_df row (columns 'chr', 'pos', 'var_info')
    match_mask = dbsnp_df.set_index([0, 1, 2]).index.isin(snps_df.set_index(['chr', 'pos', 'var_info']).index)
    dbsnp_df.loc[match_mask, 'bit_array'] = 1

    map_mask = snps_df.set_index(['chr', 'pos', 'var_info']).index.isin(dbsnp_df.set_index([0, 1, 2]).index)
    snps_df.loc[map_mask, 'mapped'] = 1
    unmapped_snps_df = snps_df.where(snps_df['mapped'] == 0).dropna()[['chr', 'pos', 'var_info']]

    bitmap_size_vint = writeBitVINT(dbsnp_df.shape[0])
    bitmap = ''.join(dbsnp_df['bit_array'].astype(str).tolist())

    # Return bit_array column as a single string
    return bitmap, bitmap_size_vint, unmapped_snps_df
