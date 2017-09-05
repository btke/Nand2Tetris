class Parser:
    #Imports an ASM file, removes whitespaces and comments

    import re
    import sys

    #filename = 'C:/Users/sahil.masand/OneDrive/CS/Nand2Tetris/nand2tetris/projects/06/add/Add.asm'
    
    mylist=[] #Store the initial list
    mylistL=[] #Store final list without whitespaces and comments
    TotalCommands = -1 #Gets total number of assembly lines or code
    CurrentCommand = -1 #current line number
    commandType = "" #stores type of command
    hasMoreCommands = True #Check if end is reached
    ArithmeticList= ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"] #Stores a list of arithmetic commands
    arg1 = "" #stores argument 1
    arg2 = "" #stores argument 2
    Comment = "" #stores the vm line as a comment

    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):
        self.filename=filename
        Parser.TotalCommands = -1
        Parser.CurrentCommand = -1
        Parser.hasMoreCommands = True
        Parser.mylist.clear()
        Parser.mylistL.clear()

        file = open(filename, 'r')
        
        for line in file:
            line = Parser.re.split('//', line.strip()) #strip whitespace and split comments into mylist 
            Parser.mylist.append(line)

        #Remove blank spaces and only keep the first column containing the vm commands into new list mylistL    
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

        Parser.commandType=""
        Parser.arg1=""
        Parser.arg2=""
        Parser.Comment = "// " + Parser.mylistL[Parser.CurrentCommand] #stores the current VM command as a comment
        line=Parser.re.split('\s',Parser.mylistL[Parser.CurrentCommand]) #split command
        
        if line[0].find("push")!=-1: #Check for push command
            Parser.commandType="C_PUSH"
            Parser.arg1 = line[1]
            Parser.arg2 = line[2]
        elif line[0].find("pop")!=-1: #check for pop command
            Parser.commandType="C_POP"
            Parser.arg1 = line[1]
            Parser.arg2 = line[2]
        elif any(substring in line[0] for substring in Parser.ArithmeticList) == True: #check for arithmetic command
            Parser.commandType="C_ARITHMETIC"
            Parser.arg1 = line[0]
        elif line[0].find("if")!=-1: #check for branching commands
            Parser.commandType="C_IF"
            Parser.arg1 = line[1]
        elif line[0].find("goto")!=-1:
            Parser.commandType="C_GOTO"
            Parser.arg1 = line[1]
        elif line[0].find("label")!=-1:
            Parser.commandType="C_LABEL"
            Parser.arg1 = line[1]
        elif line[0].find("function")!=-1: #check for function commands
            Parser.commandType="C_FUNCTION"
            Parser.arg1 = line[1]
            Parser.arg2 = line[2]
        elif line[0].find("call")!=-1:
            Parser.commandType="C_CALL"
            Parser.arg1 = line[1]
            Parser.arg2 = line[2]
        elif line[0].find("return")!=-1:
            Parser.commandType="C_RETURN"
        else:
            print("Unrecognised Syntax: " + line[0] +". Program will now quit.")
            Parser.sys.exit()
            

    #Reset file for re-read (keeps existing data)        
    def reset(self):
        Parser.CurrentCommand = -1
        Parser.hasMoreCommands = True
        
        
    
           
    
        


              
       


 

