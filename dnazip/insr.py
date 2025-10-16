from vint import *
from huffman import *
import pandas as pd

def encode_ins(insr_df, NUC_ENCODING):
    
    insr_size_vint = writeBitVINT(insr_df.shape[0])
    insr_df["pos"] = insr_df["pos"].astype(int).apply(writeBitVINT)
    insr_df["var_info"] = insr_df["var_info"].apply(lambda x: x.split('/')[1])
    insr_df["var_length"] = insr_df["var_info"].apply(lambda x: len(x)).apply(writeBitVINT)

    # print(insr_df["var_info"])
    # print(insr_df["var_length"])

    ins_seq = ''.join(insr_df["var_info"].astype(str).tolist())
    
    # print(insertion_sequence)

    pos_bitstr = ''.join(insr_df["pos"].astype(str).tolist())
    len_bitstr = ''.join(insr_df["var_length"].astype(str).tolist())

    ### THEN RUN HUFFMAN ENCODING STUFF FOR THIS CHROMOSOME
    
    encoding_len_vint, insr_seq_bitstring = run_huffman(ins_seq, NUC_ENCODING)
    
    ins_seq_bitstr = ""
    
    ### Huffman encoding will be for everything within the k-mers, then the extra nucleotides will then be encoded by their bit representations.
    
    return insr_size_vint, pos_bitstr, len_bitstr, ins_seq_bitstr


def main():
    
    return
    
    
if __name__ == "__main__":
    main()