from AGCT_tree import createTree, findFactor
from config import HEIGHT, DNA_FILE, CONTENT
from converter import baseToBinary


open(DNA_FILE + "_encoded.txt", "w").close()
outputFile = open(DNA_FILE + "_encoded.txt", "a", encoding="utf-8")

TREE = createTree(HEIGHT)

def extendedSearch(i, position, type):
    table = str.maketrans("ACTG", "TGAC")
    i=i+HEIGHT
    position=position+HEIGHT
    addLength = 0

    if(i>len(CONTENT)-1):
        return addLength

    if(type=="factor"):
        while(CONTENT[i]==CONTENT[position]):
            addLength+=1
            i+=1
            position+=1
            if(i>len(CONTENT)-1):
                return addLength

    if(type=="palindrome"):
        while(CONTENT[i].translate(table) == CONTENT[position]):
            addLength+=1
            i+=1
            position+=1
            if(i>len(CONTENT)-1):
                return addLength
    
    return addLength

def longestFactorPalindrome(i: int):
    string = CONTENT[i:i+HEIGHT]
    table = str.maketrans("ACTG", "TGAC")
    palindrome = string.translate(table)
    factorPos = findFactor(string, TREE)
    if (factorPos[1]==HEIGHT):
        addLength = 0
        positionNum = 0
        positionNumTemp = 0
        if(factorPos[0]):
            for position in factorPos[0]:
                addLengthTemp = extendedSearch(i, position, "factor")
                if (addLengthTemp > addLength): 
                    addLength = addLengthTemp
                    positionNum = positionNumTemp
                positionNumTemp +=1
                
            factorPos=(factorPos[0][positionNum], factorPos[1]+addLength)


    palindromePos = findFactor(palindrome, TREE)
    if (palindromePos[1]==HEIGHT):
        addLength = 0
        positionNum = 0
        positionNumTemp = 0
        if(palindromePos[0]):
            for position in palindromePos[0]:
                addLengthTemp = extendedSearch(i, position, "palindrome")
                if (addLengthTemp > addLength): 
                    addLength = addLengthTemp
                    positionNum = positionNumTemp
                positionNumTemp +=1
            palindromePos=(palindromePos[0][positionNum], palindromePos[1]+addLength)
    
    if(factorPos[1] and palindromePos[1]):
        if (factorPos[1]>=palindromePos[1]):
            return (factorPos + ("factor",))
        else:
            return (palindromePos + ("palindrome",))
    return None

def process(i: int):
    segment = CONTENT[i:i+HEIGHT]
    longestFactor = longestFactorPalindrome(i)
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