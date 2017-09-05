#Main code

import glob, os
import CompilationEngine #Contains the class modules for the Parser

#set the directory
#directory = "C:/Users/sahil.masand/OneDrive/CS/Nand2Tetris/nand2tetris/projects/11/ConvertToBin/"
#directory = "C:/Users/Sahil/OneDrive/CS/Nand2Tetris/nand2tetris/projects/11/ST_Test/"
directory = "C:/Users/justm/OneDrive/CS/Nand2Tetris/nand2tetris/projects/11/Pong/"

filenames = [] #.jack files are stored in this list

#change directory
os.chdir(directory)

#get .vm files in director and add to the list
for file in glob.glob("*.jack"):
    filenames.append(file)

#loop through each file
for file in filenames:
    
    NFile = CompilationEngine.CompilationEngine(file) #Load the .jack file
    
    #Set Outfile name
    OFile = file.split(".")
    OFile = OFile[0] + 'Cmp.xml'
    #Write .token file
    Wfile = open(OFile, 'w')
    
    #Loop through the parsed file
    while NFile.hasMoreTokens == True:
        #advance the parser and deduce .vm command
        NFile.advanceToken()
        Wfile.write(NFile.retCurrentToken() + '\n')

    Wfile.close()
    
