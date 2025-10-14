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

        ascii_char = #FIGURE OUT THIS

        bitmap_size, bitmap = compares_dbsnp(input_file_path, dbSNP_path, chr)
        bitmap_size_VINT = writeBitVINT(bitmap_size)











        


    

    



def main(): 
    
    args    = initialize_parser()
    file_in = encode_file(args.filename)
    
    print(file_in)
    
    
    
    
    
    
    
    
    
    
    return 0 














if __name__ == "__main__":
    main()
    