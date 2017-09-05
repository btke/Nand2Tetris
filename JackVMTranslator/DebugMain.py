#Main code

import ParserModule #Contains the class modules for the Parser
import CodeWriterModule

#NFile = ParserModule.Parser('C:/Users/Sahil/OneDrive/CS/Nand2Tetris/nand2tetris/projects/07/MemoryAccess/BasicTest/BasicTest.vm') #Load the .VM file

NFile = ParserModule.Parser('test.vm') #Load the .VM file
ASMCode = CodeWriterModule.CodeWriter("test.vm") #initialise the code writer

while NFile.hasMoreCommands == True:
    NFile.advance()
    print(NFile.commandType, NFile.arg1, NFile.arg2)
    print(" ")

#print(NFile.mylistL)


