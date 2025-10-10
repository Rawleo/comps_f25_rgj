from AGCT_tree import createTree, findFactor
from config import HEIGHT, DNA_FILE, CONTENT
from converter import baseToBinary


open(DNA_FILE + "_encoded.txt", "w").close()
outputFile = open(DNA_FILE + "_encoded.txt", "a", encoding="utf-8")

TREE = createTree(HEIGHT)

def longestFactorPalindrome(string: str):
    table = str.maketrans("ACTG", "CTGA")
    palindrome = string.translate(table)
    factorPos = findFactor(string, TREE)
    palindromePos = findFactor(palindrome, TREE)
    if(factorPos[1] and palindromePos[1]):
        if (factorPos[1]>=palindromePos[1]):
            return (factorPos + ("factor",))
        else:
            return (palindromePos + ("palindrome",))
    return None

def process(i: int):
    segment = CONTENT[i:i+HEIGHT]
    longestFactor = longestFactorPalindrome(CONTENT[i:i+HEIGHT])
    print(longestFactor)
    TREE.createPositions(segment, i)

    outputFile.write(baseToBinary(CONTENT[i]))
    

def main():
    position = 0
    for base in CONTENT:
        process(position)
        position+=1

    #print(TREE)
    outputFile.close()

if __name__ == "__main__":
    main()