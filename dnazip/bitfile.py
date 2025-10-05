def writeBItVINT(num):

    bits = ''

    while (num >= 128):

        chrByte = ((num & 0x7F) | 0x80)
        mask = 128

        for i in range(7):

            if (chrByte & mask):
                bits += '1'
            else:
                bits += '0'

            mask = mask >> 1

        num = num >> 7
    
    chrByte = (num & 0x7F)
    mask = 128

    for i in range(7):

        if (chrByte & mask):
            bits += '1'
        else:
            bits += '0'

        mask = mask >> 1
    
    return bits

def main():

    print(writeBItVINT(111))
    print(writeBItVINT(655))
    print(writeBItVINT(3))

main()