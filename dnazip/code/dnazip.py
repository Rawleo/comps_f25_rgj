import huffman, bitfile, dbsnp, dels, dbSNP_bit_array, snp, vint, dnazip, insr
import argparse
import pandas as pd
import numpy as np
from constants import *

    
INPUT_FILE_PATH = "../data/variants/Small_HG002.txt"
DBSNP_PATH = "../data/dbSNP/"
OUTPUT_PATH = "../data/output/Small_HG002_GRCh38_Encoded"


def encode_file(input_file_path, dbSNP_path, k_mer_size):
    
    genome_bitstring  = ""
    variants_df       = pd.read_csv(input_file_path, 
                                    names=['var_type', 'chr', 'pos', 'var_info'],
                                    header=None)

    # Create list of chromosomes to encode
    chr_list = variants_df['chr'].unique()
    
    # Testing one chromosome (smallest one by BPs)
    # chr_list = ['chr1']

    for chr in chr_list:
        
        # Begin construction of chromosomal bitstring
        chr_encoding = ""

        # Choose current chromosome
        chr_df = variants_df.where(variants_df['chr'] == chr)

        # Variation dataframes
        snps_df = chr_df.where(chr_df['var_type'] == 0).dropna()
        dels_df = chr_df.where(chr_df['var_type'] == 1).dropna()
        insr_df = chr_df.where(chr_df['var_type'] == 2).dropna()
        
        # Bitstring encoding of: chr#
        ascii_chr_bitstring = bitfile.encodeStringToBytes(chr)
        bitfile.export_as_binary(OUTPUT_PATH, ascii_chr_bitstring)
        # print(ascii_chr_bitstring)
        
        # Start of SNPs
        # chr_encoding += ascii_chr_bitstring
        
        ## Add the number 0 for SNPs
        # chr_encoding += "00"
        bitfile.export_as_binary(OUTPUT_PATH, "00")

        # Encoding of Mapped SNPs
        bitmap, bitmap_size_vint, unmapped_df = dbsnp.compares_dbsnp(snps_df, dbSNP_path, chr)
        
        ### Add above to chr_encoding
        # chr_encoding += bitmap_size_vint
        # chr_encoding += bitmap
        
        bitfile.export_as_binary(OUTPUT_PATH, bitmap_size_vint)
        bitfile.export_as_binary(OUTPUT_PATH, bitmap)

        # Encoding of Unmapped SNPs
        snp_size_vint, unmapped_pos_bitstr, unmapped_nuc_bitstr = snp.encode_SNPs(unmapped_df)

        ### Add above to chr_encoding
        chr_encoding += snp_size_vint
        chr_encoding += unmapped_pos_bitstr
        chr_encoding += unmapped_nuc_bitstr
        
        bitfile.export_as_binary(OUTPUT_PATH, snp_size_vint)
        bitfile.export_as_binary(OUTPUT_PATH, unmapped_pos_bitstr)
        bitfile.export_as_binary(OUTPUT_PATH, unmapped_nuc_bitstr)


        #bit alignemnts?!
        # bitfile.export_as_binary(OUTPUT_PATH, chr_encoding)
        # chr_encoding = "" 

        

        # Start of DELs
        # chr_encoding += ascii_chr_bitstring
        
        bitfile.export_as_binary(OUTPUT_PATH, ascii_chr_bitstring)
        # print(ascii_chr_bitstring)


        ## Add the number 1 for DELs
        # chr_encoding += "01"
        
        bitfile.export_as_binary(OUTPUT_PATH, "01")


        # Encoding of DELs
        del_size_vint, del_pos_bitstr, del_len_bitstr = dels.encode_dels(dels_df)
        
        ### Add above to chr_encoding
        # chr_encoding += del_size_vint
        # chr_encoding += del_pos_bitstr
        # chr_encoding += del_len_bitstr
        
        bitfile.export_as_binary(OUTPUT_PATH, del_size_vint)
        bitfile.export_as_binary(OUTPUT_PATH, del_pos_bitstr)
        bitfile.export_as_binary(OUTPUT_PATH, del_len_bitstr)
        
        #bit alignemnts?!
        # bitfile.export_as_binary(OUTPUT_PATH, chr_encoding)
        # chr_encoding = "" 
        
        
        # Start of INSRs 
        chr_encoding += ascii_chr_bitstring
        bitfile.export_as_binary(OUTPUT_PATH, ascii_chr_bitstring)


        ## Add the number 2 for INS
        bitfile.export_as_binary(OUTPUT_PATH, "10")
        chr_encoding += "10"
        
        # Encoding of INSRs
        ins_size_vint, ins_pos_bitstr, ins_len_bitstr, ins_bitstr_len_vint, ins_seq_bitstr = insr.encode_ins(insr_df, k_mer_size)
        
        ### Add above to chr_encoding
        chr_encoding += ins_size_vint
        chr_encoding += ins_pos_bitstr
        chr_encoding += ins_len_bitstr
        chr_encoding += ins_bitstr_len_vint
        chr_encoding += ins_seq_bitstr
        
        bitfile.export_as_binary(OUTPUT_PATH, ins_size_vint)
        bitfile.export_as_binary(OUTPUT_PATH, ins_pos_bitstr)
        bitfile.export_as_binary(OUTPUT_PATH, ins_len_bitstr)
        bitfile.export_as_binary(OUTPUT_PATH, ins_bitstr_len_vint)
        bitfile.export_as_binary(OUTPUT_PATH, ins_seq_bitstr)
        
        
        #bit alignemnts?!
        # bitfile.export_as_binary(OUTPUT_PATH, chr_encoding)
                
        genome_bitstring += chr_encoding
        
        
        
        
    return genome_bitstring
    

def export_as_txt(export_name, text):
    
    with open(export_name + ".txt", "w") as file:
        file.write(str(text))              


def main(): 
    
    # hexdump -v -C ../data/output/Small_HG002_GRCh38_Encoded.bin > ../data/output/Small_HG002_GRCh38_Hexdump.txt    
    
    k_mer_size = 4
    
    genome_bitstring = encode_file(INPUT_FILE_PATH, DBSNP_PATH, k_mer_size)
    
    export_as_txt(OUTPUT_PATH, genome_bitstring)
    
    


if __name__ == "__main__":
    main()
    