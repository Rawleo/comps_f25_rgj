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


def baseToBinary(base: str):
    mapping = {
            "A": "11",
            "C": "10",
            "T": "01",
            "G": "00",
        }
    return mapping.get(base, "11")


def main():
    print(encodeFibonacci(19))

if __name__ == "__main__":
    main()