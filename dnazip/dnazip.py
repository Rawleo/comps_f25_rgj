import huffman, bitfile, argparse

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



def main(): 
    
    args    = initialize_parser()
    file_in = read_in_file(args.filename)
    
    print(file_in)
    
    
    
    
    
    
    
    
    
    
    return 0 














if __name__ == "__main__":
    main()
    