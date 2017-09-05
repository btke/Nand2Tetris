class Parser:
    #Imports an ASM file, removes whitespaces and comments

    import re

    #filename = 'C:/Users/sahil.masand/OneDrive/CS/Nand2Tetris/nand2tetris/projects/06/add/Add.asm'
    
    mylist=[] #Store the initial list
    mylistL=[] #Store final list without whitespaces and comments
    TotalCommands = -1 #Gets total number of assembly lines or code
    CurrentCommand = -1 #current line number
    commandType = "" #stores type of command
    hasMoreCommands = True #Check if end is reached
    symbol="" #returns symbol or decimal if A_COMMAND or L_COMMAND
    dest="" #returns the dest mnemonic in the current C_COMMAND
    jump="" #returns the jump mnemonic in the current C_COMMAND
    comp="" #returns the comp mnemonic in the current C_COMMAND

    #Intialise the class for handling files
    def __init__(self, filename):
        self.filename=filename
        file = open(filename, 'r')
        
        for line in file:
            line = Parser.re.split('//|\s', line.strip()) #strip whitespace and split comments into mylist 
            Parser.mylist.append(line)

        #Remove blank spaces and only keep the first column containing the assembly commands into new list mylistL    
        for line in Parser.mylist:
            if line[0]!='':
                Parser.mylistL.append(line[0])
                Parser.TotalCommands += 1
                
        file.close()

    #Advance a command and deduce type of command    
    def advance(self):
        
        Parser.CurrentCommand += 1
            
        if Parser.CurrentCommand >= Parser.TotalCommands:
            Parser.hasMoreCommands = False
        else:
            Parser.hasMoreCommands = True

        #Clear previous values
        Parser.symbol=""
        Parser.dest=""
        Parser.jump=""
        Parser.commandType=""
        Parser.comp=""         

        if Parser.mylistL[Parser.CurrentCommand].find("=")!=-1 or Parser.mylistL[Parser.CurrentCommand].find(";")!=-1:
            Parser.commandType="C_COMMAND"
            #i.e. A=A+1
            if Parser.mylistL[Parser.CurrentCommand].find("=")!=-1 and Parser.mylistL[Parser.CurrentCommand].find(";")==-1:
                TypeCa=Parser.re.split('=',Parser.mylistL[Parser.CurrentCommand])
                Parser.dest=TypeCa[0]
                Parser.comp=TypeCa[1]
            #i.e. D;JMP
            elif Parser.mylistL[Parser.CurrentCommand].find(";")!=-1 and Parser.mylistL[Parser.CurrentCommand].find("=")==-1:
                TypeCb=Parser.re.split(';',Parser.mylistL[Parser.CurrentCommand])
                Parser.comp=TypeCb[0]
                Parser.jump=TypeCb[1]
            #i.e. A=A+1;JMP
            elif Parser.mylistL[Parser.CurrentCommand].find(";")!=-1 and Parser.mylistL[Parser.CurrentCommand].find("=")!=-1:
                TypeCc=Parser.re.split('=|;',Parser.mylistL[Parser.CurrentCommand])
                Parser.dest=TypeCc[0]
                Parser.comp=TypeCc[1]
                Parser.jump=TypeCc[2]                    
        elif Parser.mylistL[Parser.CurrentCommand].find("@")!=-1:
            TypeAC = Parser.re.split('@',Parser.mylistL[Parser.CurrentCommand])
            Parser.symbol=TypeAC[1]
            #if TypeAC[1].isdigit():
            Parser.commandType="A_COMMAND"
            #else:
            #    Parser.commandType="L_COMMAND"
        else:
            TypeAL = Parser.re.split(r'\((.*)\)',Parser.mylistL[Parser.CurrentCommand])
            Parser.commandType="L_COMMAND"
            Parser.symbol=TypeAL[1] 
            
    def reset(self):
        Parser.CurrentCommand = -1
        Parser.hasMoreCommands = True
        
        
    
           
    
        


              
       


 

