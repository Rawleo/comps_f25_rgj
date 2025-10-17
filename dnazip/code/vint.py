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
