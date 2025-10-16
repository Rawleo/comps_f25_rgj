import huffman, bitfile, dbsnp, dels, dbSNP_bit_array, snp, vint, dnazip, insr
import argparse
import pandas as pd
import numpy as np
from constants import *

    
INPUT_FILE_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/files/HG003_GRCh38_sorted_variants.txt"
DBSNP_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/dbSNP/"


def encode_file(input_file_path, dbSNP_path, k_mer_size):
    
    variants_df = pd.read_csv(input_file_path, 
                              names=['var_type', 'chr', 'pos', 'var_info'],
                              header=None)

    # Create list of chromosomes to encode
    # chr_list = variants_df['char'].unique()
    
    # Testing one chromosome (smallest one by BPs)
    chr_list = ['chr21']

    for chr in chr_list:
        
        # Begin construction of chromosomal bitstring
        chr_encoding = ""

        # Choose chromosome to work with 
        chr_df = variants_df.where(variants_df['chr'] == chr)

        # Variation dataframes
        snps_df = chr_df.where(chr_df['var_type'] == 0).dropna()
        dels_df = chr_df.where(chr_df['var_type'] == 1).dropna()
        insr_df = chr_df.where(chr_df['var_type'] == 2).dropna()
        
        # Bitstring encoding of: chr#
        ascii_chr_bitstring = ''.join(format(ord(x), 'b') for x in chr)
        
        # Start of SNPs
        chr_encoding += ascii_chr_bitstring

        # Encoding of Mapped SNPs
        bitmap, bitmap_size_vint, unmapped_df = dbsnp.compares_dbsnp(snps_df, dbSNP_path, chr)
        
        ### Add above to chr_encoding

        # Encoding of Unmapped SNPs
        snp_size_vint, unmapped_pos_bitstr, unmapped_nuc_bitstr = snp.encode_SNPs(unmapped_df)

        #bit alignemnts?!

        # Start of DELs
        chr_encoding += ascii_chr_bitstring

        # Encoding of DELs
        del_size_vint, del_pos_bitstr, del_len_bitstr = dels.encode_dels(dels_df)
        
        ### Add above to chr_encoding

        #bit alignemnts?!
        
        # Start of INSRs 
        chr_encoding += ascii_chr_bitstring
        
        # Encoding of INSRs
        ins_size_vint, ins_pos_bitstr, ins_len_bitstr, ins_bitstr_len_vint, ins_seq_bitstr = insr.encode_ins(insr_df, k_mer_size)
        
        ### Add above to chr_encoding
        
        #bit alignemnts?!        


def main(): 
    k_mer_size = 4
    
    encode_file(INPUT_FILE_PATH, DBSNP_PATH, k_mer_size)

if __name__ == "__main__":
    main()
    