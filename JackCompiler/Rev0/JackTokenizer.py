class Tokenizer:
    #Imports an Jack file, removes whitespaces and comments

    import re
    import sys

    symbolList = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):
        
        self.filename=filename
        self.TotalTokens = -1
        self.CurrentToken = -1
        self.hasMoreTokens = True
        self.tokenType = ""
        self.keyWord = ""
        self.symbol = ""
        self.identifier =""
        self.intVal = ""
        self.stringVal = ""
        self.InputFile = []
        self.TokenFile = []
        
        self.ReadFile()
        self.ProcessFile()
               		        
    #Advance a command and deduce type of command    
    def advance(self):
        
        self.CurrentToken += 1
            
        if self.CurrentToken >= self.TotalTokens:
            self.hasMoreTokens = False
        else:
            self.hasMoreTokens = True    
 
    #Reset file for re-read (keeps existing data)        
    def reset(self):
        self.CurrentToken = -1
        self.hasMoreTokens = True

    def hasMoreTokens(self):
        return self.hasMoreTokens

    def getCurrentToken(self):
        return self.TokenFile[self.CurrentToken]

    def TotalTokens(self):
        return self.TotalTokens
    
    #Reads the input file and stores it in a list for processing
    def ReadFile(self):
        
        file = open(self.filename, 'r')
        for line in file:
            self.InputFile.append(line.strip())
        file.close()
        
    #Removes comments '//' and '/**' from a line (also removes whitespace)            
    def RemoveComments(self, line):

        line = line
        line = Tokenizer.re.split('\//', line)
        if line[0].find("/**")  == -1 and line[0].find("*")  == -1 and line[0].find("*/")  == -1:
            return line[0]
        else:
            return ''

    #Tokenises the input file    
    def ProcessFile(self):

        DelimiterList = ['(\.|\{|\}|\(|\)|\[|\]|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~)']
        Parser = [] 

        #Removes comments   
        for line in self.InputFile:
            line = self.RemoveComments(line)
            if line != '':
                Parser.append(line)

        #Tokenisation
        for line in Parser:
            line =  Tokenizer.re.split(DelimiterList[0], line) #Do initial split based on specified delimiters
            for L1 in line:
                if L1.find("\"") == -1: #If line does not contain quotes, split it further by whitespace
                    L1 =  Tokenizer.re.split('\s+', L1)
                    for L2 in L1:
                        if L2 != '' and L2 != ' ': #Remove whitespaces
                            self.TokenFile.append(L2)   
                else: #If line contains quotes, preserve the whole token
                    self.TokenFile.append(L1.strip())

        #Get total number of tokens
        for line in self.TokenFile:
            self.TotalTokens += 1

    #Deduces the tppe of token
    def TypeToken(self):

         currToken = self.getCurrentToken()

         #Check for quoted tokens  
         if currToken.find("\"") != -1:
             self.tokenType = "stringConstant" 
         #Check for a keyword
         elif currToken in Tokenizer.keywordList:
             self.tokenType = "keyword"          
         #Check for a symbol   
         elif currToken in Tokenizer.symbolList:
             self.tokenType = "symbol"
         #Check for integer constant   
         elif currToken.isdigit() == True:
             self.tokenType = "integerConstant"
         #Check for identifier
         elif currToken[0].isdigit() == False:
             self.tokenType = "identifier"
         else:
             print("Illegal Keyword Detected: " + currToken)
             Tokenizer.sys.halt()
                 
         return self.tokenType
