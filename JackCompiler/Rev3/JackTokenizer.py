class Tokenizer:
    #Imports an Jack file, removes whitespaces and comments

    import re
    import sys

    symbolList = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbolConvert = {'<': '&lt;', '>': '&gt;', '"': '@quot;', '&': '&amp;'}
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):
        
        self.filename=filename
        
        self.TotalTokens = -1
        self.CurrentToken = -1
        self.hasMoreTokens = True
        
        self.TotalLines = -1
        self.CurrentLine = -1
        self.hasMoreLines = True

        self.TotalChc = -1
        self.CurrentChc = -1
        self.hasMoreChc = True
        
        self.tokenType = ""
        self.keyWord = ""
        self.symbol = ""
        self.identifier =""
        self.intVal = ""
        self.stringVal = ""
        self.InputFile = []
        self.TokenFile = []
        
        self.ReadFile()
        self.TokenizeFile()

    #Advance the line in the Input File List
    def advanceLine(self):
        
        self.CurrentLine += 1

        if self.CurrentLine >=self.TotalLines:
            self.hasMoreLines = False
        else:
            self.hasMoreLines = True

        #Reset character parameters of the line
        self.TotalChc = -1
        self.CurrentChc = -1
        self.hasMoreChc = True

        #Get total number of characters in current line
        for NChc in self.InputFile[self.CurrentLine]:
            self.TotalChc += 1

    def advanceChc(self):

        self.CurrentChc += 1

        if self.CurrentChc >= self.TotalChc:
            self.hasMoreChc = False
        else:
            self.hasMoreChc = True

    #Get the next character in the current line
    def getChc(self):

        #Get current line    
        line = self.InputFile[self.CurrentLine]
        return line[self.CurrentChc]

    #Used to look ahead to the next character
    def LookAheadChc(self):

        if self.hasMoreChc == True:
            line = self.InputFile[self.CurrentLine]
            return line[self.CurrentChc + 1]
        else:
            return False

    #Tokenize the current Input File
    def TokenizeFile(self):

        StateInComment = False
        
        while self.hasMoreLines == True:
            self.advanceLine()
            Token = ""
            c = ""
            cNext = ""
            StateInQuote = False
                        
            while self.hasMoreChc == True:
                self.advanceChc()
                
                c = self.getChc()
                cNext = self.LookAheadChc()

                #The following if-elseif-else statements implement a basic finite state machine to catch and generate tokens
                    
                #Check if in comment
                if c == "/" and cNext == "*":
                    StateInComment = True
                    
                elif c == "*" and cNext == "/" and StateInComment == True:
                    StateInComment = False
                    c = ' '
                    cNext = ' '
                    self.advanceLine()
                    
                #If quotes are detected (outside a comment), set QuoteState to True
                elif c == '"' and StateInComment == False:
                    if StateInQuote == False:
                        StateInQuote = True
                    elif StateInQuote == True: #If quoteState has turned from True to False, the quote has ended so output token
                        StateInQuote = False
                        self.TokenFile.append([Token, "stringConstant"])
                        Token = ""
                
                #If QuoteState is True, append characters to Token
                elif StateInQuote == True and StateInComment == False and c != '"':
                    Token = Token + str(c)
                    
                #Check for in-line comment    
                elif c == "/" and cNext == "/" and StateInQuote == False and StateInComment == False:
                    if self.hasMoreLines == True:
                        self.advanceLine()
                    else:
                        print("Error detected. Expected end of file.")
                        Tokenizer.sys.exit()
                                                
                #Check if current character is a symbol - if so output current Token and character
                elif c in Tokenizer.symbolList and StateInQuote == False and StateInComment == False:
                    if Token != "":
                        self.TokenFile.append([Token, self.getTokenType(Token)])
                        Token = ""
                    if c == '<' or c == '>' or c =='"' or c == '&':
                        self.TokenFile.append([Tokenizer.symbolConvert.get(c, "ERR"), "symbol"])
                    else:
                        self.TokenFile.append([c, "symbol"])
                            
                #Check if current character is a whitespace - if so output current Token
                elif c.isspace() == True and StateInQuote == False and StateInComment == False:
                    if Token != "":
                        self.TokenFile.append([Token, self.getTokenType(Token)])
                        Token = ""
                            
                #If none of the above - append character to Token
                elif StateInQuote == False and StateInComment == False and c != '"':
                    Token = Token + str(c)
                
        for line in self.TokenFile:
            self.TotalTokens += 1     
               		        
    #Advance a command and deduce type of command    
    def advanceToken(self):
        
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

    def retCurrentToken(self):
        line = self.TokenFile[self.CurrentToken]
        return line[0]

    def retTokenType(self):
        line = self.TokenFile[self.CurrentToken]
        return line[1]
        
    def retKeyWord(self):
        line = self.TokenFile[self.CurrentToken]

        if line[1] == "keyword":
            return line[0]
        else:
            print("Expected keyword. Got " + line[1])
            Tokenizer.sys.exit()

    def retSymbol(self):
        line = self.TokenFile[self.CurrentToken]

        if line[1] == "symbol":
            return line[0]
        else:
            print("Expected symbol. Got " + line[1])
            Tokenizer.sys.exit()

    def retSymbolLookAhead(self):

        if self.hasMoreTokens == True:
            line = self.TokenFile[self.CurrentToken + 1]
            if line[1] == "symbol":
                return line[0]
            else:
                print("Expected symbol. Got " + line[1])
                Tokenizer.sys.exit()
        else:
            return False
        
    def retIdentifier(self):
        line = self.TokenFile[self.CurrentToken]

        if line[1] == "identifier":
            return line[0]
        else:
            print("Expected identifier. Got " + line[1])
            Tokenizer.sys.exit()

    def retIntVal(self):
        line = self.TokenFile[self.CurrentToken]

        if line[1] == "integerConstant":
            return line[0]
        else:
            print("Expected integerConstant. Got " + line[1])
            Tokenizer.sys.exit()

    def retStringVal(self):
        line = self.TokenFile[self.CurrentToken]

        if line[1] == "stringConstant":
            return line[0]
        else:
            print("Expected stringConstant. Got " + line[1])
            Tokenizer.sys.exit()
    
    def TotalTokens(self):
        return self.TotalTokens
    
    #Reads the input file and stores it in a list for processing
    def ReadFile(self):
        
        file = open(self.filename, 'r')
        for line in file:
            if line.isspace() == False:
                self.InputFile.append(line.strip())
                self.TotalLines += 1
        file.close()

    #Deduces the type of token
    def getTokenType(self, Token):

         currToken = Token   
         
         if currToken in Tokenizer.keywordList:
             return "keyword"          
         #Check for integer constant   
         elif currToken.isdigit() == True:
             return "integerConstant"
         #Check for identifier
         elif currToken[0].isdigit() == False:
             return "identifier"
         else:
             print("Illegal Keyword Detected: " + currToken)
             Tokenizer.sys.exit()
            
