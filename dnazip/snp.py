import pandas as pd
import numpy as np
from vint import *

def encode_SNPs(snps_df, nuc_encoding):

    # Convert positions to VINTs
    snps_df['pos'] = snps_df['pos'].astype(int).apply(writeBitVINT)

    # Convert nucleotides to two-bit representations
    snps_df['var_info'] = snps_df['var_info'].apply(lambda x: nuc_encoding[x.split('/')[-1]])

    pos_bitstring = ''.join(snps_df['pos'].astype(str).tolist())
    nuc_bitstring = ''.join(snps_df['var_info'].astype(str).tolist())
    snp_size = snps_df.shape[0]

    return snp_size, pos_bitstring, nuc_bitstring