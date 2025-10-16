'''
 * Author: Ryan Son
 * Modified Date: Oct. 7, 2025
 * File: huffman.py
 * Summary: Given an input of human genomic sorted variants, it will map insertions 
            using the Huffman coding algorithm and output a huffman tree with an associated 
            encoding dictionary.
'''

import re, sys, argparse, os, vint as vint


VARIATION_FLAG = {
    'snps': 0,
    'deletions': 1,
    'insertions': 2,
}

NUC_ENCODING = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11",
}


'''
Node Class for implementing a binary tree.
'''
class Node:

    def __init__(self, symbol, frequency, leftChild=None, rightChild=None):
        self.symbol = symbol
        self.frequency = frequency
        self.leftChild = leftChild
        self.rightChild = rightChild
        

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
def read_in_file(input_file):
    with open(input_file, "r") as file_in:
        text = (file_in.read())
    return text
        

'''
Create a list of k-mers from insertion sequences.
@params: 
 * input_text - a string containing comma-separated variation data, one variation per line
 * k_mer_length - the integer length of the k-mer to be extracted from nucleotide sequences
@return:
 * processed_k_mer_array - a list of k-mer strings extracted from all insertion sequences
'''
def create_k_mer_array(input_text, k_mer_length):

    # FORMAT OF INPUT TEXT:
    # var_flag, chromosome, absolute_position, nucleotides

    k = k_mer_length
    regex_k = k * '.'
    text_array = input_text.splitlines()
    chr_insertion = {}
    processed_k_mer_array = []

    for line in text_array:

        var_flag, chromosome, absolute_position, nucleotide_seq = line.split(
            ",")
        nucleotide_seq = nucleotide_seq.split("/")[1]

        if (int(var_flag) == VARIATION_FLAG['insertions']):

            insertion_row = (var_flag, absolute_position, nucleotide_seq)

            if (chromosome not in chr_insertion):
                chr_insertion[chromosome] = [insertion_row]
            else:
                chr_insertion[chromosome].append(insertion_row)

            if (len(nucleotide_seq) >= k):

                k_mer_array = re.findall(regex_k, nucleotide_seq)

                for k_mer in k_mer_array:

                    processed_k_mer_array.append(k_mer)

    return processed_k_mer_array, chr_insertion


'''
Build the required dictionary, mapping each symbol to their frequency.
@params: 
 * input_text - string to be processed to assign each unique symbol a frequency
@return:
 * freq_dict - a dictionary containing the unique symbol with their corresponding frequency.
'''
def build_frequency_dict(input_text):
    freq_dict = {}
    for char in input_text:
        if char not in freq_dict:
            freq_dict[char] = 1
        else:
            freq_dict[char] += 1
    return freq_dict


'''
Build the huffman tree according to their frequencies.
@params: 
 * freq_dict - a dictionary containing the unique symbol with their corresponding frequency.
@return:
 * nodes - the binary Huffman Tree beginning at the root.
'''
def build_huffman_tree(freq_dict):
    nodes = []
    for symbol, freq in freq_dict.items():
        nodes.append(Node(symbol, freq))

    while len(nodes) > 1:
        # Sort nodes by frequency using key parameter and lambda function in the sorted function
        nodes = sorted(nodes, key=lambda n: n.frequency)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = Node(left.symbol + right.symbol,
                      left.frequency + right.frequency, left, right)
        nodes.append(parent)
    # Return the root node or return nothing if empty
    return nodes[0] if nodes else None


'''
Assign correct binary tree mapping to each unique symbol using recursion.
@params: 
 * root - the binary Huffman Tree beginning at the root.
 * curr - the current node of the tree
@return:
 * encoding_map - a dictionary for each unique symbol corresponding to their unique encoding
'''
def map_encodings(root, encoding_map, current):
    if root is None:
        return
    if root.leftChild is None and root.rightChild is None:
        encoding_map[root.symbol] = current
        return

    map_encodings(root.leftChild, encoding_map, current + "0")
    map_encodings(root.rightChild, encoding_map, current + "1")


'''
Encode the string according to its mapping.
@params: 
 * encoding_map - a dictionary for each unique symbol corresponding to their unique encoding
 * text - input string to be encoded
@return:
 * encoded_text - output text after it has been encoded by dict
'''
def encode_text(encoding_map, text):
    encoded_text = ""
    for char in text:
        encoded_text += str(encoding_map[char])
    return encoded_text


'''
Decode the encoded string to retrieve the original string.
@params: 
 * encoded_text - output text after it has been encoded by dict
 * root - the binary Huffman Tree beginning at the root.
@return:
 * result - the original text after it has been decoded.
'''
def decode(encoded_text, root):
    result = ""
    curr = root
    for char in encoded_text:
        if char == "0":
            curr = curr.leftChild
        else:
            curr = curr.rightChild
        if curr.leftChild is None and curr.rightChild is None:
            result += curr.symbol
            curr = root
    return result


'''
Read in binary file from bytes to bits to string. For some reason it adds a leading zero....
@params: 
 * filename - filename of .bin file
@return:
 * bits - the original huffman encoded bits
'''
def read_bin(filename):
    with open(filename + '.bin', 'rb') as file:
        data = file.read()
        # print(data)
        bits = ''.join(format(byte, '08b') for byte in data)
        # print(bits)
    # Remove leading zero
    return bits[1:]


'''
Export as binary file consisting of the encoded string transformed into bytes.
The binary_string consists of a string of 1's and 0's, this string is then
converted into an actual binary integer. From here, it is then converted into bytes.
This transformation is accomplished by calculating the number of bytes required to 
represent the given binary integer. Adding 7 to the length of the binary integer is
done to round up to the nearest byte, so if a string is not entirely divisible by 8, 
there will still be a byte representation of the bits that are left. This is then sorted
in big-endian order.
@params: 
 * export_name - chosen filename 
 * binary_str - the encoded huffman string
@return:
 * Exports a .bin file of the encoded string now as bytes to the current directory
'''
def export_as_binary(export_name, binary_str):
    byte_value = int(binary_str, 2).to_bytes((len(binary_str) + 7) // 8,
                                             byteorder='big')
    # print(byte_value)
    with open(export_name + ".bin", "wb") as file:
        file.write(byte_value)


'''
Export input text as txt file.
@params: 
 * export_name - chosen filename 
 * text - input string to be exported
@return:
 * Exports a text file to the current directory.
'''
def export_as_txt(export_name, text):
    with open(export_name + ".txt", "w") as file:
        file.write(str(text))


# def initialize_parser():
#     parser = argparse.ArgumentParser(
#         prog="huffman",
#         description="Create Huffman encoding based on file input.")

#     parser.add_argument('filename', type=str, help="Input filename.")

#     args = parser.parse_args()

#     return args


def encode_insertions(encoding_map, chr_insertion_dict):

    k = (len(next(iter(encoding_map))))  # k_mer_length
    regex_k = k * '.'
    
    chr_bitstring_dict = {}

    for chromosome, insertion_tuple_array in chr_insertion_dict.items():
        
        insertion_chr = ""
        
        count_vint = vint.writeBitVINT(len(insertion_tuple_array))
                
        for insertion_tuple in insertion_tuple_array:
            
            flag, position, nucleotide_seq = insertion_tuple
            
            position = int(position)
            
            pos_bitstring_vint = vint.writeBitVINT(position)
            
            insertion_line = pos_bitstring_vint

            k_mer_array = re.findall(regex_k, nucleotide_seq)

            for k_mer in k_mer_array:

                encoding = encoding_map[k_mer]

                insertion_line += encoding

            num_kmers = len(nucleotide_seq) % k

            extra_nuc = nucleotide_seq[:num_kmers]

            if (num_kmers != 0):
                for char in extra_nuc:
                    encoding = NUC_ENCODING[char]

                    insertion_line += encoding
            
            insertion_chr += insertion_line
            
        chr_bitstring_dict[chromosome] = [insertion_chr]

    return chr_bitstring_dict


def print_dict(dict):
    for key, item in dict.items():
        print(f"'{key}': {item}")


'''
Run the program.
'''
def main():
    args                              = initialize_parser()

    encoding_map                      = {}
    text                              = read_in_file(args.filename)
    k_mer_array, chr_insertion_dict   = create_k_mer_array(text, 4)
    freq_dict                         = build_frequency_dict(k_mer_array)
    root                              = build_huffman_tree(freq_dict)
    map_encodings(root, encoding_map, "")
    chr_bitstring_dict                = encode_insertions(encoding_map, chr_insertion_dict) 
    
    return 0



if __name__ == "__main__":
    main()
