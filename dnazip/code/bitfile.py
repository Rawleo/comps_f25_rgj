def writeBitVINT(num):

    bit_string = ''

    while (num >= 128):

        # Get last 7 bits and set first bit to 1
        chrByte = ((num & 0x7F) | 0x80)
        mask = 128

        for i in range(8):

            if (chrByte & mask):
                bit_string += '1'
            else:
                bit_string += '0'

            mask = mask >> 1

        # num by 7 bits
        num = num >> 7

    chrByte = num
    mask = 128

    for i in range(8):

        if (chrByte & mask):
            bit_string += '1'
        else:
            bit_string += '0'

        mask = mask >> 1
    
    return bit_string

def BitStringToBytes(bit_string):

    return int(bit_string, 2).to_bytes(len(bit_string) // 8, 'big')

def BytesToBitString(bytes_obj):

    return ''.join(format(byte, '08b') for byte in bytes_obj)

def encodeStringToBytes(str):
    
    byte_representation = str.encode('utf-8')
    
    return "".join(format(byte, '08b') for byte in byte_representation)


def readBitVINT(bytes_obj):

    bit_string = BytesToBitString(bytes_obj)
    
    num = 0
    shift = 0

    for i in range(0, len(bit_string), 8):

        byte = bit_string[i:i+8]
        bits = byte[1:]
        bit_val = int(bits, 2)

        num |= (bit_val << shift)

        shift += 7

        if byte[0] == '0':
            break

    return num


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
def export_as_binary(export_name, bitstr):
    
    byte_value = int(bitstr, 2).to_bytes((len(bitstr) + 7) // 8, byteorder='big')
    
    with open(export_name + ".bin", "ab") as file:
        file.write(byte_value)


def main():

    VINT_string = writeBitVINT(300)
    byte_obj = BitStringToBytes(VINT_string)
    byte_decode = BytesToBitString(byte_obj)

    print('Testing Position to VINT: \n')
    print('Original Number: 300')
    print(f'VINT Representation: {VINT_string}')
    print(f'Binary Representation: {byte_obj}')
    print(f'Binary Back to String: {byte_decode}')

    readBitVINT(byte_obj)


if __name__ == "__main__":
    main()
