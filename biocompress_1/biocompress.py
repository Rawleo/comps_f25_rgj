from AGCT_tree import createTree, findFactor
from config import HEIGHT, DNA_FILE, DNA_FILE_TXT
from converter import baseToBinary


with open(DNA_FILE_TXT, "r") as file:
       CONTENT = file.read()

open(DNA_FILE + "_encoded.txt", "w").close()
outputFile = open(DNA_FILE + "_encoded.txt", "a", encoding="utf-8")

TREE = createTree(HEIGHT)

def process(i: int):
    segment = CONTENT[i:i+HEIGHT]
    print(findFactor(CONTENT[i:i+HEIGHT], TREE))
    TREE.createPositions(segment, i)
    print(TREE)

    outputFile.write(baseToBinary(CONTENT[i]))
    

def main():
    position = 0
    for base in CONTENT:
        process(position)
        position+=1

    print(TREE)
    outputFile.close()

if __name__ == "__main__":
    main()