import huffman, bitfile, dbsnp, dels, dbSNP_bit_array, snp, vint, dnazip, insr
import argparse
import pandas as pd
import numpy as np

NUC_ENCODING = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11",
}

def encode_file(input_file_path, dbSNP_path):
    
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
        bitmap, bitmap_size, unmapped_df = dbsnp.compares_dbsnp(snps_df, dbSNP_path, chr)
        bitmap_size_VINT = vint.writeBitVINT(bitmap_size)
        
        ### Add above to chr_encoding

        # Encoding of Unmapped SNPs
        snp_size, pos_bitstring, nuc_bitstring = snp.encode_SNPs(unmapped_df, NUC_ENCODING)
        snp_size_VINT = vint.writeBitVINT(snp_size)

        #bit alignemnts?!

        # Start of DELs
        chr_encoding += ascii_chr_bitstring

        # Encoding of DELs
        del_size, pos_bitstring_vint, del_length_vint = dels.encode_dels(dels_df)
        del_size_VINT = vint.writeBitVINT(del_size)
        
        ### Add above to chr_encoding

        #bit alignemnts?!
        
        # Start of INSRs 
        chr_encoding += ascii_chr_bitstring
        
        # Encoding of INSRs
        ins_size, pos_bitstring_vint, ins_length_vint, insertion_sequence_bitstring = insr.encode_ins(insr_df)
        ins_size_VINT = vint.writeBitVINT(ins_size)
        
        ### Add above to chr_encoding
        
        #bit alignemnts?!        


# def encode_insertions(variation_filepath): 
    
#     encoding_map                      = {}
#     variation_file_text               = huffman.read_in_file(variation_filepath)
#     k_mer_array, chr_insertion_dict   = huffman.create_k_mer_array(variation_file_text, 4)
#     freq_dict                         = huffman.build_frequency_dict(k_mer_array)
#     root                              = huffman.build_huffman_tree(freq_dict)
    
#     huffman.map_encodings(root, encoding_map, "")
    
#     chr_insertion_bitstring_dict      = huffman.encode_insertions(encoding_map, chr_insertion_dict)
    
#     return chr_insertion_bitstring_dict


def main(): 
    
    # args              = initialize_parser()
    # filepath          = args.filepath
    
    INPUT_FILE_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/files/HG003_GRCh38_sorted_variants.txt"
    DBSNP_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/dbSNP/"
    
    # chr_insertion_bitstring_dict = encode_insertions(INPUT_FILE_PATH)
    
    # huffman.print_dict(chr_insertion_bitstring_dict)
    
    encode_file(INPUT_FILE_PATH, DBSNP_PATH)    
      
    
    return 0 



if __name__ == "__main__":
    main()
    