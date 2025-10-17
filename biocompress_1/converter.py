from config import CONTENT

def encodeFibonacci(num):
    fibNumbers = [1,2]
    while(fibNumbers[len(fibNumbers)-1]<=num):
        fibNumbers.append(fibNumbers[len(fibNumbers)-1]+fibNumbers[len(fibNumbers)-2])
    del fibNumbers[len(fibNumbers)-1]

    
    code = []
    for val in reversed(fibNumbers):
        if(num>=val):
            code.insert(0,"1")
            num -= val
        else:
            code.insert(0,"0")
    code.append("1")
    binaryCode = "".join(code)

    return binaryCode

def decodeFibonacci(num):
    decoded = 0
    num = num[:-1]
    fibNumbers = [1,2]
    while(len(fibNumbers)<len(num)):
        fibNumbers.append(fibNumbers[-1]+fibNumbers[-2])
    for i in range(len(num)):
        if(num[i]=="1"):
            decoded+=fibNumbers[i]
    return decoded


def encodeBinary(num):
    return bin(num)[2:]
    


def baseToBinary(base: str):
    mapping = {
            "A": "11",
            "C": "10",
            "T": "01",
            "G": "00",
        }
    return mapping.get(base, "11")

def binaryToBase(base):
    mapping = {
            "11": "A",
            "10": "C",
            "01": "T",
            "00": "G",
        }
    return mapping.get(base, "A")

def encodeFactor(factor):
    length = factor[1]
    type = factor[2]
    position = factor[0][0]+1
    if(type=="factor"):
        type="0"
    else:
        type="1"
    posFib=encodeFibonacci(position)
    position = posFib #figure out binary later
    length=encodeFibonacci(length)

    if((factor[1]*2)<=len(length+type+position)):
        string = CONTENT[factor[0][0]:factor[0][0]+factor[1]]
        binary = ""
        for base in string:
            binary+=baseToBinary(base)
        return binary
    else:
        return length+type+position

def main():
    print(encodeFibonacci(3))

if __name__ == "__main__":
    main()