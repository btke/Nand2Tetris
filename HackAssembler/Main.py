#Main code

import ParserModule #Contains the class modules for the Parser 
import CodeModule #Contains the class module to convert C Instructions to binary
import SymbolTableModule #Contains the symbol table class

OutputL= [] #List to store the output binary values

print("Processing...")

NFile = ParserModule.Parser('C:/Users/justm/OneDrive/CS/Nand2Tetris/nand2tetris/projects/06/rect/Rect.asm') #Load the .ASM file
#print(NFile.TotalCommands) #debug

ST = SymbolTableModule.SymbolTable() #Setup the base symbol table
VarAdr = 16 #Base variable address
NLabels = 0 #Number of labels

#First Pass to generate all the lables
while NFile.hasMoreCommands == True: #check if end of file
    NFile.advance() #advance file
    if NFile.commandType == "L_COMMAND": #check for label
        if ST.contains(NFile.symbol) == False: #check if lable exists, if not add it to the symbol table
            NLabels += 1 #increment the number of labels by 1
            ST.addEntry(NFile.symbol, NFile.CurrentCommand + 1 - NLabels) #store the label in address current line + 1 - NLabels

print(NLabels)
NFile.reset() #Go back to the start of the file
            
#2nd pass to generate the binary code        
while NFile.hasMoreCommands == True:
    NFile.advance()
    if NFile.commandType == 'C_COMMAND':
        Cint=CodeModule.Code(NFile.dest, NFile.comp, NFile.jump) #Convert the C-Instruction to binary
        OutputL.append(Cint.c_instruction) #add to the output list
        #print(Cint.c_instruction) #debug
    elif NFile.commandType == 'A_COMMAND':
        if NFile.symbol.isdigit(): #Check if the A-Instruction contains a number
            Aint=bin(int(NFile.symbol))[2:].zfill(15) #convert to 15 bit binary number
            OutputL.append('0' + Aint) #convert to 16 bit A-Instruction
           # print('0' + Aint) #debug
        else: #contains a variable or label
            if ST.contains(NFile.symbol) == True:
                Aint=bin(int(ST.GetAddress(NFile.symbol)))[2:].zfill(15) #get address, convert to binary
                OutputL.append('0' + Aint)
               # print('0' + Aint) #debug
            else:
                ST.addEntry(NFile.symbol, VarAdr)
                Aint=bin(int(ST.GetAddress(NFile.symbol)))[2:].zfill(15) #get address, convert to binary
                OutputL.append('0' + Aint)
                VarAdr += 1 #increment base address
            #    print('0' + Aint) #debug
        
    #print(' ')
    
OFile = 'C:/Users/justm/OneDrive/CS/Nand2Tetris/nand2tetris/projects/06/rect/Rect.hack'

file = open(OFile, 'w')

for line in OutputL:
    file.write(line + '\n')

file.close()

#print(ST.Table) #debug

print("All done!")
