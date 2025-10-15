import huffman
import bitfile
import argparse
import dbSNP_bit_array
import pandas as pd
import numpy as np

def initialize_parser():
    parser = argparse.ArgumentParser(
        prog="huffman",
        description="Create Huffman encoding based on sorted variant file input.")

    parser.add_argument('filename', type=str, help="Input filename.")

    args = parser.parse_args()

    return args

'''
Read in an input file.
@params: 
 * input_file - text file to be read
@return:
 * text - the contents of the file as a string
'''
def encode_file(input_file_path, dbSNP_path):
    
    variants_df = pd.read_csv(input_file_path, 
                              names=['var_type', 'chr', 'pos', 'var_info'],
                              header=None)
    
    chr_list = variants_df['char'].unique()

    del_count = variants_df.where(variants_df['var_type'] == 1).dropna().shape[0]
    insert_count = variants_df.where(variants_df['var_type'] == 1).dropna().shape[0]

    for chr in chr_list:

        ascii_char = str(ord("c")) + str(ord("h")) + str(ord("r")) + str(chr)

        bitmap_size, bitmap = dbSNP_bit_array.compares_dbsnp(input_file_path, dbSNP_path, chr)
        bitmap_size_VINT = bitfile.writeBitVINT(bitmap_size)




def run_huffman(variation_file_text): 
    
    encoding_map = {}
    
    # In our paper, cite or create an appendix that discusses how we got to this.
    k_mer_array, chr_insertion_dict = huffman.create_k_mer_array(
        variation_file_text, 4)  # Cite insertion k-mer in DNAZip.
    # print(k_mer_array)
    freq_dict = huffman.build_frequency_dict(
        k_mer_array)  # Cite huffman paper, by Huffman himself.
    # print(freq_dict)
    root = huffman.build_huffman_tree(freq_dict)
    huffman.map_encodings(
        root, encoding_map, ""
    )  # frequency table 4-mer, cite DNAZip paper and huffman table (paper).
    chr_insertion_bitstring_dict = huffman.encode_insertions(encoding_map, chr_insertion_dict) # This will contain the per chromosome insertions with the VINTs preceding the sequences. 
    
    return chr_insertion_bitstring_dict
  



def main(): 
    
    args              = initialize_parser()
    filepath          = args.filename
    insertion_text    = huffman.read_in_file(filepath)
    
    dbSNP_path = "/Users/ryanson/Documents/Comps/comps_repo_venvs/comps_f25_rgj/dnazip/dbSNP"
    
    chr_insertion_bitstring_dict = run_huffman(insertion_text)
    
    # huffman.print_dict(chr_insertion_bitstring_dict)
    
    file_in = encode_file(filepath, dbSNP_path)    
    
    print(file_in)
    
    
    
    
    
    
    
    
    
    return 0 














if __name__ == "__main__":
    main()
    