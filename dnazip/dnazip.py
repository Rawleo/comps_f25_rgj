import huffman, bitfile, dbsnp, dels, dbSNP_bit_array, snp, vint
import argparse
import pandas as pd
import numpy as np

NUC_ENCODING = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11",
}

# def initialize_parser():
#     parser = argparse.ArgumentParser(
#         prog="huffman",
#         description="Create Huffman encoding based on sorted variant file input.")

#     parser.add_argument('filepath', type=str, help="Input filepath.")

#     args = parser.parse_args()

#     return args


def encode_file(input_file_path, dbSNP_path, chr_insertion_bitstring_dict):
    
    variants_df = pd.read_csv(input_file_path, 
                              names=['var_type', 'chr', 'pos', 'var_info'],
                              header=None)

    # chr_list = variants_df['char'].unique()
    chr_list = ['chr1']

    for chr in chr_list:
        
        chr_encoding = ""

        chr_df = variants_df.where(variants_df['chr'] == chr)

        snps_df = chr_df.where(chr_df['var_type'] == 0).dropna()
        dels_df = chr_df.where(chr_df['var_type'] == 1).dropna()

        ascii_char_bitstring = ' '.join(format(ord(x), 'b') for x in chr)
        
        chr_encoding += ascii_char_bitstring

        bitmap, bitmap_size, unmapped_df = dbSNP_bit_array.compares_dbsnp(snps_df, dbSNP_path, chr)
        bitmap_size_VINT = vint.writeBitVINT(bitmap_size)
        # print(bitmap_size_VINT)


        snp_size, pos_bitstring, nuc_bitstring = snp.encode_SNPs(unmapped_df, NUC_ENCODING)
        snp_size_VINT = vint.writeBitVINT(snp_size)
        # print(snp_size_VINT)


        #bit alignemnts?!

        chr_encoding += ascii_char_bitstring


        del_size, pos_bitstring, del_bitstring = dels.encode_dels(dels_df)
        del_size_VINT = vint.writeBitVINT(del_size)
        print(del_size_VINT)

        #bit alignemnts?!
        
        chr_encoding += ascii_char_bitstring

        insertions = chr_insertion_bitstring_dict[chr]


#LINE 2982 in HG002, need to clean vars
        



def encode_insertions(variation_filepath): 
    
    encoding_map                      = {}
    variation_file_text               = huffman.read_in_file(variation_filepath)
    k_mer_array, chr_insertion_dict   = huffman.create_k_mer_array(variation_file_text, 4)
    freq_dict                         = huffman.build_frequency_dict(k_mer_array)
    root                              = huffman.build_huffman_tree(freq_dict)
    
    huffman.map_encodings(root, encoding_map, "")
    
    chr_insertion_bitstring_dict      = huffman.encode_insertions(encoding_map, chr_insertion_dict)
    
    return chr_insertion_bitstring_dict


def main(): 
    
    # args              = initialize_parser()
    # filepath          = args.filepath
    
    INPUT_FILE_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/files/HG003_GRCh38_sorted_variants.txt"
    DBSNP_PATH = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/dbSNP/"
    
    chr_insertion_bitstring_dict = encode_insertions(INPUT_FILE_PATH)
    
    # huffman.print_dict(chr_insertion_bitstring_dict)
    
    encode_file(INPUT_FILE_PATH, DBSNP_PATH, chr_insertion_bitstring_dict)    
    
    # print(file_in)
    
    
    
    
    
    
    
    
    
    return 0 














if __name__ == "__main__":
    main()
    