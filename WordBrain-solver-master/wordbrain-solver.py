# Copyright 2016, Howard Zeng
# All rights reserved

import sys

gDICTIONARY_FILE = None
gPLACEHOLDER = None
gDICTIONARY = None
gPREFIX_TREE_DICTIONARY = None

class cPrefixTree:

    def __init__(self):
        self.root = []
        self.isWord = False
        for i in range(26):
            self.root.append(None)
        
    def insertKey(self, iWord):
        if len(iWord) == 0:
            self.isWord = True
        else:
            # 65 is ord('A')
            letterOrd = ord(iWord[0]) - 65
            if self.root[letterOrd] == None:
                newTree = cPrefixTree()
                newTree.insertKey(iWord[1:])
                self.root[letterOrd] = newTree
            else:
                self.root[letterOrd].insertKey(iWord[1:])

    def getPrefix(self, iLetter):
        return self.root[ord(iLetter) - 65]

    def keyExists(self, iWord):
        if len(iWord) == 0:
            return True
        else:
            letterOrd = ord(iWord[0]) - 65
            if self.root[letterOrd] == None:
                return False
            else:
                return keyExists(iWord[1:])


def buildPrefixTree(iDictionaryFile):
    global gDICTIONARY_FILE
    global gPLACEHOLDER
    global gDICTIONARY
    global gPREFIX_TREE_DICTIONARY

    gDICTIONARY_FILE = iDictionaryFile
    gPLACEHOLDER = '-'
    gDICTIONARY = []
    gPREFIX_TREE_DICTIONARY = cPrefixTree()

    with open(gDICTIONARY_FILE) as f:
        lines = f.readlines()

    for line in lines:
        gDICTIONARY.append(line.strip('\n'))
        
    for word in gDICTIONARY:
        gPREFIX_TREE_DICTIONARY.insertKey(word)



# Traverses grid in all of the 8 directions on a 2d grid
def traverse(iSolutionGoesHere, iGrid, iXCoord, iYCoord, iLettersLeft, iRows, iCols, iWord, iSteps, iPrefixTree):
    global gPLACEHOLDER
    global gDICTIONARY
    
    if (iXCoord >= iCols) or (iYCoord >= iRows) or (iXCoord < 0) or (iYCoord < 0) or (iGrid[iXCoord][iYCoord] == gPLACEHOLDER):
        return False
        
    if [iXCoord, iYCoord] in iSteps:
        return False
    
    newSteps = list(iSteps)
    newSteps.append([iXCoord, iYCoord])
    iWord += iGrid[iXCoord][iYCoord]
    iLettersLeft -= 1
    letter = iWord[-1]
    iPrefixTree = iPrefixTree.getPrefix(letter)
    
    if iPrefixTree == None:
        return False
    
    if iLettersLeft == 0:
        if iPrefixTree.isWord == True:
            return [iGrid, iWord, newSteps]
        else:
            return False
        

    solution = traverse(iSolutionGoesHere, iGrid, iXCoord + 1, iYCoord, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)

    solution = traverse(iSolutionGoesHere, iGrid, iXCoord - 1, iYCoord, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord, iYCoord + 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord, iYCoord - 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord + 1, iYCoord + 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord + 1, iYCoord - 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord - 1, iYCoord + 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)
        
    solution = traverse(iSolutionGoesHere, iGrid, iXCoord - 1, iYCoord - 1, iLettersLeft, iRows, iCols, iWord, newSteps, iPrefixTree)
    if solution:
        iSolutionGoesHere.append(solution)

def pushDownGrid(iGrid, iNumRows, iNumCols):
    global gPLACEHOLDER
    
    for row in range(iNumRows-1):
        for col in range(iNumCols):
            if iGrid[row+1][col] == gPLACEHOLDER:
                for tempRow in reversed(range(row+1)):
                    iGrid[tempRow+1][col] = iGrid[tempRow][col]
                iGrid[0][col] = gPLACEHOLDER
        
        
def main(args):
    global gPLACEHOLDER
    global gPREFIX_TREE_DICTIONARY
    
    # For enumeration
    eGRID = 0
    eWORDS = 1
    eSTEPS = 2
    
    eXCOORD = 0
    eYCOORD = 1
    
    if len(args) != 1:
        print("ERROR: You should only have 1 argument which is the input file (it's probably input.txt)")
        return
    
    inputFile = args[0]
    numRows = 4
    numCols = 4
    numWords = 4
    numLetters = [5,3,3,5]
    
    with open(inputFile) as f:
        info = f.readlines()
    
    # Extract the dictionary file (first line of the input file)
    buildPrefixTree(info[0].strip('\n'))
    
    # Extract information of the number of rows, columns, and words (second line of the input file)
    rcw = info[1].strip('\n').split(" ")
    if len(rcw) != 3:
        print("ERROR: The first line of " + inputFile + " should contain only <Number of Rows> <Number of Columns> <Number of Words>")
        return
    
    numRows = int(rcw[0])
    numCols = int(rcw[1])
    numWords = int(rcw[2])
    
    # Extract the number of letters in each word (third line of the input file)
    numLetters = info[2].strip('\n').split(" ")
    for i in range(len(numLetters)):
        numLetters[i] = int(numLetters[i])
    
    if len(numLetters) != numWords:
        print("ERROR: The second line of " + inputFile + " should have the same number of numbers as the number of words")
        return
    
    
    # Extract the letter grid (the rest of the lines)
    info = info[3:]
    
    grid = []
    for row in info:
        row = row.strip('\n')
        line = row.split(" ")
        grid.append(line)
    
    possibleSolutions = [ [grid,[]] ]
    
    for passes in range(numWords):
        tempSolution2 = []
        for ps in possibleSolutions:
            tempSolutions = []
            for row in range(numRows):
                for col in range(numCols):
                    solution = traverse(tempSolutions, ps[eGRID], row, col, numLetters[passes], numRows, numCols, "", [], gPREFIX_TREE_DICTIONARY)
                    if solution:
                        tempSolutions.append(solution)

            # Create new solution list with the letters fallen down 
            # and discard the old solution list
            for tempSol in tempSolutions:
                wordList = list(ps[eWORDS])
                wordList.append(tempSol[eWORDS])
                
                # Print out position of the letters taken at each step
                #print wordList
                #print tempSol[eSTEPS]
                
                # Create new copy of the temporary intermediate solution
                newGrid = []
                for row in range(numRows):
                    tempRow = list(tempSol[eGRID][row])
                    newGrid.append(tempRow)
                
                for stepTaken in tempSol[eSTEPS]:
                    x = stepTaken[eXCOORD]
                    y = stepTaken[eYCOORD]
                    newGrid[x][y] = gPLACEHOLDER

                # Simulate the letters falling down
                pushDownGrid(newGrid, numRows, numCols)
                tempSolution2.append([newGrid, wordList])
                
                # Print out each intermediate step
                #for row in range(numRows):
                #    print newGrid[row]
                
        
        possibleSolutions = tempSolution2

    # Print out final solution
    possibleSolutions.sort()
    for ps in possibleSolutions:
        print(ps[eWORDS])



if __name__ == "__main__":
    main(sys.argv[1:])