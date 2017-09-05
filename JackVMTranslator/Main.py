#Main code

import glob, os
import ParserModule #Contains the class modules for the Parser
import CodeWriterModule #Contains the codewriter module

#set the directory
directory = "C:/Users/Sahil/OneDrive/CS/Nand2Tetris/nand2tetris/projects/08/FunctionCalls/NestedCall/"
filenames = [] #.vm files are stored in this list
#OutFile = "temp.vm"

#change directory
os.chdir(directory)

#get .vm files in director and add to the list
for file in glob.glob("*.vm"):
    filenames.append(file)

#with open(OutFile, 'w') as outfile:
#    for fname in filenames:
#        with open(fname) as infile:
#            outfile.write(infile.read())
#outfile.close()

#loop through each file
for file in filenames:
    
    NFile = ParserModule.Parser(file) #Load the .VM file  
    ASMCode = CodeWriterModule.CodeWriter(file) #initialise the code writer and set the filename

    #Loop through the parsed file
    while NFile.hasMoreCommands == True:

        #advance the parser and deduce .vm command
        NFile.advance()

        #check command type
        if NFile.commandType == "C_PUSH" or NFile.commandType == "C_POP":
            ASMCode.WritePushPop(NFile.commandType, NFile.arg1, NFile.arg2)
        elif NFile.commandType == "C_ARITHMETIC":
            ASMCode.WriteArithmetic(NFile.arg1)
        elif NFile.commandType == "C_IF":
            ASMCode.writeIf(NFile.arg1)
        elif NFile.commandType == "C_GOTO":
            ASMCode.writeGoto(NFile.arg1)
        elif NFile.commandType == "C_LABEL":
            ASMCode.writeLabel(NFile.arg1)
        elif NFile.commandType == "C_CALL":
            ASMCode.writeCall(NFile.arg1, NFile.arg2)
        elif NFile.commandType == "C_FUNCTION":
            ASMCode.writeFunction(NFile.arg1, NFile.arg2)
        elif NFile.commandType == "C_RETURN":
            ASMCode.writeReturn()
        
#Set Outfile name
OFile = 'NestedCall.asm'

#Write .asm file
file = open(OFile, 'w')

for line in ASMCode.outputL:
    file.write(line + '\n')

file.close()

#os.remove('temp.vm') 
