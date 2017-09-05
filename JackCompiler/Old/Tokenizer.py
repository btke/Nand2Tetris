class Tokenizer:
    #Imports an Jack file, removes whitespaces and comments

    import re
    import sys
    import nltk
    
    mylist=[] #Store the initial list
    mylistL=[] #Store final list without whitespaces and comments
    TotalCommands = -1 #Gets total number of assembly lines or code
    CurrentCommand = -1 #current line number
    commandType = "" #stores type of command
    hasMoreCommands = True #Check if end is reached
    SplitList = ['(\.|\{|\}|\(|\)|\[|\]\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~|\"|\s+)']
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):
        self.filename=filename
        Tokenizer.TotalCommands = -1
        Tokenizer.CurrentCommand = -1
        Tokenizer.hasMoreCommands = True
        Tokenizer.mylist.clear()
        Tokenizer.mylistL.clear()

        file = open(filename, 'r')
        
        for line in file:
            L1 = Tokenizer.re.split('//', line.strip()) #strip whitespace and remove comments
            if L1[0] != '' and L1[0].find("/**") == -1:
                for line in L1:
                   L2 =  Tokenizer.re.split(Tokenizer.SplitList[0], line)
                   for line in L2:
                       if line != '' and line != ' ':
                           Tokenizer.mylist.append(line)
                   #L2 = Tokenizer.nltk.wordpunct_tokenize(line)
                   
            
	 # L2 =  Tokenizer.nltk.word_tokenize(line)
        #Remove blank spaces and only keep the first column containing the vm commands into new list mylistL    
       # for line in Tokenizer.mylist:
           # line = Tokenizer.re.split("[.]|[*]|[+]|[/]|[,]|[;]", line)
        #    Tokenizer.mylistL.append(line)
        #    Tokenizer.TotalCommands += 1       
        file.close()

        for line in Tokenizer.mylist:
           print(line)
		        
    #Advance a command and deduce type of command    
    def advance(self):
        
        Tokenizer.CurrentCommand += 1
            
        if Tokenizer.CurrentCommand >= Tokenizer.TotalCommands:
            Tokenizer.hasMoreCommands = False
        else:
            Tokenizer.hasMoreCommands = True    
 

    #Reset file for re-read (keeps existing data)        
    def reset(self):
        Tokenizer.CurrentCommand = -1
        Tokenizer.hasMoreCommands = True
