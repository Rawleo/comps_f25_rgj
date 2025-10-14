import pandas as pd
import numpy as np
import sys

def compares_dbsnp(variants_path, dbsnp_path, chr):

    variants_df = pd.read_csv(variants_path, header=None)
    snps_df = variants_df.where(variants_df[0] == 0).dropna()

    chr_df = snps_df.where(snps_df[1] == chr)[[1, 2, 3]]
    dbsnp_df = pd.read_csv(dbsnp_path + chr + ".txt", header=None)
    dbsnp_df['bit_array'] = 0
    chr_df['mapped'] = 0

    # Set bit_array to 1 where dbsnp_df row matches chr_df row (columns 1, 2, 3)
    match_mask = dbsnp_df.set_index([0, 1, 2]).index.isin(chr_df.set_index([1, 2, 3]).index)
    dbsnp_df.loc[match_mask, 'bit_array'] = 1

    map_mask = chr_df.set_index([1, 2, 3]).index.isin(dbsnp_df.set_index([0, 1, 2]).index)
    chr_df.loc[map_mask, 'mapped'] = 1
    unmapped_snps_df = chr_df.where(chr_df['mapped'] == 0).dropna()
    unmapped_snps_df[[1, 2, 3]].to_csv(dbsnp_path + "unmapped_" + chr + ".csv", header=None, index=False)


    # Return bit_array column as a single string
    return dbsnp_df.shape[0], ''.join(dbsnp_df['bit_array'].astype(str).tolist())

def main():

    variants_path = sys.argv[1]
    dbsnp_path = sys.argv[2]
    chr = sys.argv[3]

    dbsnp_size, bit_map = compares_dbsnp(variants_path, dbsnp_path, chr)
