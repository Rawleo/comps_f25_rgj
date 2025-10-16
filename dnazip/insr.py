from vint import *
import pandas as pd

def encode_ins(insr_df):
    
    
    insr_size = insr_df.shape[0]
    insr_df["pos"] = insr_df["pos"].astype(int).apply(writeBitVINT)
    insr_df["var_info"] = insr_df["var_info"].apply(lambda x: len(x.split('/')[1])).apply(writeBitVINT)


    pos_bitstring_vint = ''.join(insr_df["pos"].astype(str).tolist())
    ins_length_vint = ''.join(insr_df["var_info"].astype(str).tolist())

    ### THEN RUN HUFFMAN ENCODING STUFF FOR THIS CHROMOSOME
    
    insertion_sequence_bitstring = ""
    
    ### Huffman encoding will be for everything within the k-mers, then the extra nucleotides will then be encoded by their bit representations.
    
    return insr_size, pos_bitstring_vint, ins_length_vint, insertion_sequence_bitstring


def main():
    
    return
    
    
if __name__ == "__main__":
    main()