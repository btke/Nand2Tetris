class CompilationEngine:
    #Compiles a Jack Program

    import sys
    import JackTokenizer #Contains the class modules for the Tokenizer
    import SymbolTable #Contains the class modules for the Symbol Table
    import VMWriter #Contains the VM writer module
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):

        self.TotalTokens = -1
        self.CurrentToken = -1
        self.hasMoreTokens = True
        
        self.filename=filename
        self.JackFile = CompilationEngine.JackTokenizer.Tokenizer(filename) #Load the .jack file into the Tokenizer
        self.SymbolTable = CompilationEngine.SymbolTable.SymbolTable(filename) #Set up a new Symbol Table
        self.VMWriter = CompilationEngine.VMWriter.VMWriter(filename) #Set up the VM Writer
        self.TokenFile = []

        self.startCompilation()
            
    def startCompilation(self):

        self.CompileClass()

        for line in self.TokenFile:
            self.TotalTokens += 1

        self.VMWriter.printVMFile()
        print("Compilation completed successfully!")
        self.SymbolTable.printDebug()

    #Compile a complete Class
    def CompileClass(self):

        #Initial if-else unique integers
        self.ElseInt = -1
        self.ExitIfInt = -1
        self.WhileInt = -1
        self.ExitWhileInt = -1
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Append <Class>
        self.TokenFile.append('<class>')
       # self.VMWriter.writeComment("<class>")
        
        #First token should be a 'class' keyword
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("CompileClass: Expected 'Class'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Second token should be a 'identifier' for className
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            self.ClassName = Token #Store the ClassName
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("CompileClass: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()
        
        #Token should be a 'symbol' {
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == "{":
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            else:
                self.printDebug()
                print("CompileClass: Expected '{'. Got: " + TokenType)
                CompilationEngine.sys.exit()
        else:
            self.printDebug()
            print("CompileClass: Expected 'symbol'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Start a loop to find any classVarDec or subroutineDec
        while self.JackFile.hasMoreTokens == True:

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()

            #If class closing tag '}' is detected, return function and end compilation
            if TokenType == "symbol":
                Token = self.JackFile.retSymbol()
                if Token == "}":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</class>') #</class>
                 #   self.VMWriter.writeComment("</class>")
                    return #End Compilation of Class
                
            #Check for classVarDec* or subroutineDec*
            elif TokenType == "keyword":
                Token = self.JackFile.retKeyWord()
                if Token == "static" or Token == "field":
                    self.CompileClassVarDec() #Compile the classVarDec
                elif Token == "constructor" or Token == "function" or Token == "method":
                    self.CompileSubroutine() #Compile the subroutineDec

        self.printDebug()
        print("CompileClass: Expected }")
        CompilationEngine.sys.exit()

    #Compile Class Variable Declarations
    def CompileClassVarDec(self):

      #  self.VMWriter.writeComment("Begin Class Variable Declarations")
        
        #<classVarDec>
        self.TokenFile.append('<classVarDec>')
      #  self.VMWriter.writeComment("<classVarDec>")
        
        TokenType = self.JackFile.retTokenType()

        #Append the keyword 'static|field'
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Static | Field
        Kind = Token.upper()
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'type' of declaration which can be a keyword (int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            
            Token = self.JackFile.retKeyWord()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
        elif TokenType == "identifier":
            
            Token = self.JackFile.retIdentifier()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
        else:
            
            self.printDebug()
            print("CompileClassVarDec: Expected 'type'")
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'varName'
        if TokenType == "identifier":
            
            Token = self.JackFile.retIdentifier()
            Name = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
        else:
            
            self.printDebug()
            print("CompileClassVarDec: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Add variable to Symbol Table
        self.SymbolTable.Define(Name, TP, Kind)
        
        #Start a loop to check for more 'VarNames'
        while self.JackFile.hasMoreTokens == True:

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()
            
            #If closing tag is detected, return function
            if TokenType == "symbol":
                
                Token = self.JackFile.retSymbol()
                if Token == ";":
                    
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</classVarDec>')
                #    self.VMWriter.writeComment("</classVarDec>")
                    return #End classVarDec
                
                elif Token == ",":
                    
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    
            elif TokenType == "identifier":
                
                Token = self.JackFile.retIdentifier()
                Name = Token
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                #Add variable to Symbol Table
                self.SymbolTable.Define(Name, TP, Kind)
                
        self.printDebug()        
        print("CompileClassVarDec: Expected ;")
        CompilationEngine.sys.exit()   

    #Compile a Subroutine
    def CompileSubroutine(self):
        
        self.TokenFile.append('<subroutineDec>')
      #  self.VMWriter.writeComment("<subroutineDec>")

        #Reset the subRoutine symbol table
        self.SymbolTable.startSubroutine()
        
        TokenType = self.JackFile.retTokenType()

        #Append the keyword 'constructor|method|function'
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        subRoutineKeyword = Token
        
        #Add 'this' as first argument of a method
        if subRoutineKeyword == "method":
            Kind = "ARG"
            Name = "this"
            TP = self.ClassName
            self.SymbolTable.Define(Name, TP, Kind)

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'type' of declaration which can be a keyword (void|int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            subRoutineType = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            subRoutineType = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("CompileSubroutine: Expected 'type'")
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'subroutineName'
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            subRoutineName = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for opening bracket (
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == "(":
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            else:
                self.printDebug()
                print("CompileSubroutine: Expected '('. Got: " + TokenType)
                CompilationEngine.sys.exit()
        else:
            self.printDebug()
            print("CompileSubroutine: Expected '('. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for closing bracket ) - if not compile the parameter list
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == ")":
                self.TokenFile.append('<parameterList>')
                self.TokenFile.append('</parameterList>')
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
            else:
                self.printDebug()
                print("CompileSubroutine: Expected ')'. Got: " + TokenType)
                CompilationEngine.sys.exit()
                
        elif TokenType == "keyword" or TokenType == "identifier":
            self.compileParameterList() #Compile the parameter list
            
            TokenType = self.JackFile.retTokenType() #Parameter list will return on ')'
            Token = self.JackFile.retSymbol()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
        else:
            self.printDebug()
            print("CompileSubroutine: Expected parameter list. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Start subroutine body
        self.TokenFile.append('<subroutineBody>')
     #   self.VMWriter.writeComment("<subroutineBody>")

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for opening bracket {
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == "{":
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            else:
                self.printDebug()
                print("CompileSubroutine: Expected '{'. Got: " + TokenType)
                CompilationEngine.sys.exit()
        else:
            self.printDebug()
            print("CompileSubroutine: Expected '{'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Start a loop to check for 'VarDec*' or 'statement*'
        while self.JackFile.hasMoreTokens == True:

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()
        
            #If closing tag is detected, return function
            if TokenType == "symbol":
                Token = self.JackFile.retSymbol()
                if Token == "}":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</subroutineBody>')
                #    self.VMWriter.writeComment("</subroutineBody>")
                    self.TokenFile.append('</subroutineDec>')
                #    self.VMWriter.writeComment("</subroutineDec>")
                    return
                
                else:
                    
                    self.printDebug()
                    print("CompileSubroutine: Expected '}'. Got: " + TokenType)
                    CompilationEngine.sys.exit()

            #Check for 'var, 'let', 'if', 'while', 'do' or 'return'        
            elif TokenType == "keyword":
                Token = self.JackFile.retKeyWord()
                
                if Token == "var":
                    self.compileVarDec() #Compile var declarations
                   
                elif Token == "let" or Token == "if" or Token == "while" or Token == "do" or Token == "return":

                    nVars = self.SymbolTable.VarCount("VAR")
                    
                    if subRoutineKeyword == "function":
                        self.VMWriter.writeFunction(self.ClassName + "." + subRoutineName, nVars)

                    #if 'method' push 'argument 0' and pop to 'this'    
                    elif subRoutineKeyword == "method":
                        self.VMWriter.writeFunction(self.ClassName + "." + subRoutineName, nVars)
                        self.VMWriter.writePush("argument", 0)
                        self.VMWriter.writePop("pointer", 0)
                    
                    elif subRoutineKeyword == "constructor":
                        self.VMWriter.writeFunction(self.ClassName + "." + subRoutineName, nVars)
                        #Get number of declared field variables and push to stack
                        nFields = self.SymbolTable.VarCount("FIELD")
                        self.VMWriter.writePush("constant", nFields)
                        #Call OS Function, memory.alloc to get a new memory/heap location
                        self.VMWriter.writeCall("Memory.alloc", 1)
                        #Save new memory location to 'this' pointer
                        self.VMWriter.writePop("pointer", 0)             
                    
                    self.compileStatements() #Compile statement - Expect return on }
                    TokenType = self.JackFile.retTokenType()
                    Token = self.JackFile.retSymbol()
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</subroutineBody>')
              #      self.VMWriter.writeComment("</subroutineBody>")
                    self.TokenFile.append('</subroutineDec>')
              #      self.VMWriter.writeComment("</subroutineDec>")
                    return
                    
                else:
                    self.printDebug()
                    print("CompileSubroutine: Unrecognised keyword in subroutine body: " + Token)
                    CompilationEngine.sys.exit()
            else:
                self.printDebug()
                print("CompileSubroutine: Unrecognised token in subroutine body")
                CompilationEngine.sys.exit()
                
        self.printDebug()
        print("CompileSubroutine: Expected }")
        CompilationEngine.sys.exit()
            
    def compileParameterList(self):

        self.TokenFile.append('<parameterList>')
     #   self.VMWriter.writeComment("<parameterList>")

        Kind = "ARG"
        
        TokenType = self.JackFile.retTokenType()
        
        #Append the keyword (void|int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileParameterList: Expected 'type'")
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'varName'
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            Name = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileParameterList: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        self.SymbolTable.Define(Name, TP, Kind)
        
        Comma = False
        
        #Start a loop to check for more parameters
        while self.JackFile.hasMoreTokens == True:

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()

            #If closing tag is detected, return function
            if TokenType == "symbol":
                
                Token = self.JackFile.retSymbol()
                if Token == ")":
                    
                    self.TokenFile.append('</parameterList>')
         #           self.VMWriter.writeComment("</parameterList>")
                    return
                
                elif Token == ",":
                    
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    Comma = True
                    
            elif TokenType == "identifier":
                Token = self.JackFile.retIdentifier()

                if Comma == True:
                    TP = Token
                    Comma = False
                else:
                    Name = Token
                    self.SymbolTable.Define(Name, TP, Kind)
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
            elif TokenType == "keyword":
                Token = self.JackFile.retKeyWord()

                if Comma == True:
                    TP = Token
                    Comma = False
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        self.printDebug() 
        print("compileParameterList: Expected )")
        CompilationEngine.sys.exit()
    
    def compileVarDec(self):

        Kind = "VAR"
        
        self.TokenFile.append('<varDec>')
     #   self.VMWriter.writeComment("<varDec>")
        TokenType = self.JackFile.retTokenType()
        
        #Append the keyword 'var'
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'type' of declaration which can be a keyword (int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            TP = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileVarDec: Expected 'type'")
            CompilationEngine.sys.exit()

        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()
         
        #Check for 'varName'
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            Name = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileVarDec: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

        self.SymbolTable.Define(Name, TP, Kind)
        
        #Start a loop to check for more 'VarNames'
        while self.JackFile.hasMoreTokens == True:

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()
            
            #If closing tag is detected, return function
            if TokenType == "symbol":
                
                Token = self.JackFile.retSymbol()
                
                if Token == ";":
                    
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</varDec>')
               #     self.VMWriter.writeComment("</varDec>")
                    return
                
                elif Token == ",":
                    
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #Else, add more VarName(s)        
            elif TokenType == "identifier":
                
                Token = self.JackFile.retIdentifier()
                Name = Token
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.SymbolTable.Define(Name, TP, Kind)
                
        self.printDebug()        
        print("compileVarDec: Expected ;")
        CompilationEngine.sys.exit()

    def compileStatements(self):
        
        self.TokenFile.append('<statements>')
    #    self.VMWriter.writeComment("<statements>")
        
        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retKeyWord()
                
        if Token == "let":
            self.compileLet()
        elif Token == "if":
            self.compileIf()
        elif Token == "while":
            self.compileWhile()
        elif Token == "do":
            self.compileDo()
        elif Token == "return":
            self.compileReturn()

        #Check for more statements
        while self.JackFile.hasMoreTokens == True:
            
            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()
            
            if TokenType == "symbol":
                Token = self.JackFile.retSymbol()
                if Token == "}":
                    self.TokenFile.append('</statements>')
           #         self.VMWriter.writeComment("</statements>")
                    return
                else:
                    self.printDebug()
                    print("compileStatements: Expected }")
                    CompilationEngine.sys.exit()

            elif TokenType == "keyword":
                
                Token = self.JackFile.retKeyWord()
                if Token == "let":
                    self.compileLet()
                elif Token == "if":
                    self.compileIf()
                elif Token == "while":
                    self.compileWhile()
                elif Token == "do":
                    self.compileDo()
                elif Token == "return":
                    self.compileReturn()
                    
        self.printDebug()
        print("compileStatements; Expected }")
        CompilationEngine.sys.exit()
        
    def compileDo(self):
        
        self.TokenFile.append('<doStatement>')
     #   self.VMWriter.writeComment("<doStatement>")

        #Append the keyword 'do'
        Token = self.JackFile.retKeyWord()
        TokenType = self.JackFile.retTokenType()
        
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()
        
        #Check for subRoutine, class or variable name and append it
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            Name = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileDo: Expected subRoutine, class or variable Name")
            CompilationEngine.sys.exit()
       
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for opening bracket ( or a '.'
        if TokenType == "symbol":
            
            Token = self.JackFile.retSymbol()

           #do someMethod()
            if Token == "(":
               
                self.ComplileSubroutineCallA(Name)

                #Discard the return value
                self.VMWriter.writePop("temp", 0)

            #do someClass.someMethod() or someClass.someFunction() or object.someMethod()                       
            elif Token == ".":
                                    
                self.ComplileSubroutineCallB(Name)    
                
                #Discard the return value
                self.VMWriter.writePop("temp", 0)
                
            else:
                self.printDebug()
                print("compileDo: Expected '(' or '.' Got: " + TokenType)
                CompilationEngine.sys.exit()
                
        else:
            self.printDebug()
            print("compileDo: Expected a symbol. Got: " + TokenType)
            CompilationEngine.sys.exit()

        #Expect return on ')'
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
             
            if Token == ";":
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.TokenFile.append('</doStatement>')
       #        self.VMWriter.writeComment("</doStatement>")
                return
            else:
                self.printDebug()
                print("compileDo: Expected ;")
                CompilationEngine.sys.exit()            
             
        else:
            self.printDebug()
            print("compileDo: Expected a symbol. Got: " + TokenType)
            CompilationEngine.sys.exit()   

    def compileLet(self):

        self.TokenFile.append('<letStatement>')
     #   self.VMWriter.writeComment("<letStatement>")

        #Append the keyword 'let'
        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for variable name and append it
        if TokenType == "identifier":
            
            Token = self.JackFile.retIdentifier()
            VarName = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
        else:
            
            self.printDebug()
            print("compileLet: Expected subRoutine, class or variable Name")
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for opening bracket [ or a '='
        if TokenType == "symbol":
            
            Token = self.JackFile.retSymbol()

            #Array i.e. VarName[expression1] = expression2
            if Token == "[":

                #Get segment of VarName
                segment = self.SymbolTable.KindOf(VarName)

                #Get index of VarName
                index = self.SymbolTable.IndexOf(VarName)
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.JackFile.advanceToken()
                self.CompileExpression() #expect return to ']' token

                #Assume token has been incremented after return from Compile Expression
                TokenType = self.JackFile.retTokenType()
                if TokenType == "symbol":
                    Token = self.JackFile.retSymbol()
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.JackFile.advanceToken()
                else:
                    self.printDebug()
                    print("compileLet: Expected closing bracket ]")
                    CompilationEngine.sys.exit()

            Token = self.JackFile.retSymbol()
            
            if Token == "=":
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.JackFile.advanceToken()
                self.CompileExpression() #Expect return to ';' token

                #Assume token has been incremented after return from Compile Expression
                TokenType = self.JackFile.retTokenType()
                if TokenType == "symbol":
                    Token = self.JackFile.retSymbol()

                    if Token == ";":
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                        self.TokenFile.append('</letStatement>')
             #           self.VMWriter.writeComment("</letStatement>")

                        #Get segment of VarName
                        segment = self.SymbolTable.KindOf(VarName)
                       
                        if segment == None:
                            print("LetStatement: Undefined variable " + VarName)

                        #Get IndexOf token i.e. 5 
                        index = self.SymbolTable.IndexOf(VarName)
                        
                        #Pop variable from stack to memory segment
                        if segment == "STATIC":
                            self.VMWriter.writePop("static", index)
                        elif segment == "FIELD":
                            self.VMWriter.writePop("this", index)
                        elif segment == "ARG":
                            self.VMWriter.writePop("argument", index)
                        elif segment == "VAR":
                            self.VMWriter.writePop("local", index)                        
                        
                        return
                    
                    else:
                        self.printDebug()
                        print("compileLet: Expected closing statement ;")
                        CompilationEngine.sys.exit()
                else:
                    self.printDebug()
                    print("compileLet: Expected symbol. Got: " + TokenType)
                    CompilationEngine.sys.exit()
                
        else:
            self.printDebug()
            print("compileLet: Expected symbol. Got: " + TokenType)
            CompilationEngine.sys.exit()   

    def compileWhile(self):

        self.WhileInt += 1
        self.ExitWhileInt += 1

        WhileInt = self.WhileInt
        ExitWhileInt = self.ExitWhileInt

        self.TokenFile.append('<whileStatement>')
    #    self.VMWriter.writeComment("<whileStatement>")

        #Append the keyword 'while'
        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        
        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Add Label for While
        self.VMWriter.WriteLabel("While" + str(WhileInt))

        if TokenType == "symbol":

            Token = self.JackFile.retSymbol()

            if Token == "(":

                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.JackFile.advanceToken()
                self.CompileExpression() #Expect return to ')' token

                #'not' the expression
                self.VMWriter.WriteArithmetic("~")

                #write if-goto
                self.VMWriter.WriteIf("ExitWhile" + str(ExitWhileInt))
                
                TokenType = self.JackFile.retTokenType()
                Token = self.JackFile.retSymbol()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                if TokenType == "symbol":

                    Token = self.JackFile.retSymbol()

                    if Token == "{":

                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                        self.JackFile.advanceToken()
                        self.compileStatements() #Compile statement - Expect return on }

                        #Write goto
                        self.VMWriter.WriteGoto("While" + str(WhileInt))

                        #Write label
                        self.VMWriter.WriteLabel("ExitWhile" + str(ExitWhileInt))
                        
                        TokenType = self.JackFile.retTokenType()
                        Token = self.JackFile.retSymbol()
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                        self.TokenFile.append('</whileStatement>')
            #            self.VMWriter.writeComment("</whileStatement>")

                        return

                    else:
                        self.printDebug()
                        print("compileIf: Expected '{' ")
                        CompilationEngine.sys.exit()

                else:
                    self.printDebug()
                    print("compileIf: Expected a symbol. Got: " + TokenType)
                    CompilationEngine.sys.exit()

            else:
                self.printDebug()
                print("compileIf: Expected '(' ")
                CompilationEngine.sys.exit()

        else:
            self.printDebug()
            print("compileIf: Expected a symbol. Got: " + TokenType)
            CompilationEngine.sys.exit()
            
    def compileReturn(self):

        self.TokenFile.append('<returnStatement>')
    #    self.VMWriter.writeComment("<returnStatement>")
        
        #Append the keyword 'return'
        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()

            if Token == ";":
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.TokenFile.append('</returnStatement>')
        #       self.VMWriter.writeComment("</returnStatement>")

                #No expression - return constant 0
                self.VMWriter.writePush("constant", 0)
                self.VMWriter.writeReturn()
                
                return
            
            else:
                self.printDebug()
                print("compileReturn: Expected ;")
                CompilationEngine.sys.exit()
            
        else:
            self.CompileExpression() #Expect return to ';' token
            TokenType = self.JackFile.retTokenType()
            Token = self.JackFile.retSymbol()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            self.TokenFile.append('</returnStatement>')
       #     self.VMWriter.writeComment("</returnStatement>")

            self.VMWriter.writeReturn()
            
            return

        self.printDebug()
        print("compileReturn: Expected ;")
        CompilationEngine.sys.exit() 

    def compileIf(self):

        self.ElseInt += 1 
        self.ExitIfInt += 1

        ElseInt = self.ElseInt
        ExitIfInt = self.ExitIfInt
        
        self.TokenFile.append('<ifStatement>')
    #    self.VMWriter.writeComment("<ifStatement>")

        #Append the keyword 'if'
        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        if TokenType == "symbol":
            
            Token = self.JackFile.retSymbol()

            if Token == "(":
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                self.JackFile.advanceToken()
                self.CompileExpression() #Expect return to ')' token

                #Neg the expression
                self.VMWriter.WriteArithmetic("~")

                #Write if-goto
                self.VMWriter.WriteIf("Else" + str(ElseInt))
                
                TokenType = self.JackFile.retTokenType()
                Token = self.JackFile.retSymbol()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                if TokenType == "symbol":
                    
                    Token = self.JackFile.retSymbol()

                    if Token == "{":
                        
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                        self.JackFile.advanceToken()
                        self.compileStatements() #Compile statement - Expect return on }
                        
                        TokenType = self.JackFile.retTokenType()
                        Token = self.JackFile.retSymbol()
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                        LookAheadTokenType = self.JackFile.retTokenTypeLookAhead()
                        LookAheadToken = self.JackFile.retTokenLookAhead()

                        if LookAheadTokenType == "keyword":
                        
                            if LookAheadToken == "else":

                                #Advance Token and append 'Else' keyword
                                self.JackFile.advanceToken()
                                TokenType = self.JackFile.retTokenType()
                                Token = self.JackFile.retKeyWord()
                                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                                #Advance Token
                                self.JackFile.advanceToken()
                                TokenType = self.JackFile.retTokenType()

                                if TokenType == "symbol":
                                    Token = self.JackFile.retSymbol()

                                    if Token == "{":
                                        
                                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                                        self.JackFile.advanceToken()

                                        #Write goto
                                        self.VMWriter.WriteGoto("ExitIf" + str(ExitIfInt))
                                            
                                        #Write Else label
                                        self.VMWriter.WriteLabel("Else" + str(ElseInt))
                                        
                                        self.compileStatements() #Compile statement - Expect return on }
                                        
                                        TokenType = self.JackFile.retTokenType()
                                        Token = self.JackFile.retSymbol()
                                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                                        self.TokenFile.append('</ifStatement>')
                                     #   self.VMWriter.writeComment("</ifStatement>")

                                        #Write ExitIf label
                                        self.VMWriter.WriteLabel("ExitIf" + str(ExitIfInt))
                                        
                                        return
                
                                    else:
                                        self.printDebug()
                                        print("compileIf: Expected '{' ")
                                        CompilationEngine.sys.exit()

                                else:
                                    self.printDebug()
                                    print("compileIf: Expected a symbol. Got: " + TokenType)
                                    CompilationEngine.sys.exit()

                            else:
                                
                                #Write Else label
                                self.VMWriter.WriteLabel("Else" + str(ElseInt))
                                
                                self.TokenFile.append('</ifStatement>')
                           #     self.VMWriter.writeComment("</ifStatement>")
                                return

                        else:
                            #Write Else label
                            self.VMWriter.WriteLabel("Else" + str(ElseInt))
                            self.TokenFile.append('</ifStatement>')
                           #self.VMWriter.writeComment("</ifStatement>")
                            return
                        
                    else:
                        self.printDebug()
                        print("compileIf: Expected '{' ")
                        CompilationEngine.sys.exit()
                    
                else:
                    self.printDebug()
                    print("compileIf: Expected a symbol. Got: " + TokenType)
                    CompilationEngine.sys.exit()
                   
            else:
                self.printDebug()
                print("compileIf: Expected '(' ")
                CompilationEngine.sys.exit()
                    
        else:
            self.printDebug()
            print("compileIf: Expected a symbol. Got: " + TokenType)
            CompilationEngine.sys.exit()
        
    def CompileExpression(self):

        self.TokenFile.append('<expression>')
     #   self.VMWriter.writeComment("<expression>")

        self.CompileTerm()
        
        #Check for more statements (op term)*
        while self.JackFile.hasMoreTokens == True:

       #     LookAheadTokenType = self.JackFile.retTokenTypeLookAhead()
       #    LookAheadToken = self.JackFile.retTokenLookAhead()
                
            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()
            
            if TokenType == "symbol":
                Token = self.JackFile.retSymbol()
                
                #Return if "," is detected
                if Token == ",":
                    self.TokenFile.append('</expression>')
           #         self.VMWriter.writeComment("</expression>")
                    return
                
                #Check for closing statements and return function
                elif Token == ";" or Token == "]" or Token == ")":
                    self.TokenFile.append('</expression>')
              #      self.VMWriter.writeComment("</expression>")
                    return
                
                else:
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    operator = Token
            else:
                self.printDebug()
                print("CompileExpression: Expected Operator. Got: " + TokenType)
                CompilationEngine.sys.exit()

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()

            self.CompileTerm()

            #Push operator to the stack
            if operator == "*":
                self.VMWriter.writeCall("Math.multiply", 2)
            elif operator == "/":
                self.VMWriter.writeCall("Math.divide", 2)
            else:
                self.VMWriter.WriteArithmetic(operator)
            
    def CompileTerm(self):
        
        self.TokenFile.append('<term>')
      #  self.VMWriter.writeComment("<term>")
        
        TokenType = self.JackFile.retTokenType()
        LookAheadTokenType = self.JackFile.retTokenTypeLookAhead()
        LookAheadToken = self.JackFile.retTokenLookAhead()

        #integerConstant i.e. '5'       
        if TokenType == "integerConstant":
            
            Token = self.JackFile.retIntVal()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #Push integer constant to the stack
            self.VMWriter.writePush("constant", Token)

        #stringConstant i.e. can be a character array 'chc'
        elif TokenType == "stringConstant":
            
            Token = self.JackFile.retStringVal()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #Get total number of characters
            nChars = 0
            for chc in Token:
                nChars += 1

            #Push number of characters to stack and call string.new
            self.VMWriter.writePush("constant", nChars)
            self.VMWriter.writeCall("String.new", 1)

            #Push ASCII code to stack and call string.append
            for chc in Token:
                self.VMWriter.writePush("constant", ord(chc))
                self.VMWriter.writeCall("String.appendChar", 2)

        #keyword i.e. 'True', 'False', 'null' and 'this'
        elif TokenType == "keyword":
            
            Token = self.JackFile.retKeyWord()

            #If false or null, push constant 0 to the stack
            if Token == "false" or Token == "null":
                self.VMWriter.writePush("constant", 0)
                
            #Push 'this' pointer to stack
            elif Token == "this":
                self.VMWriter.writePush("pointer", 0)

            #push constant 1 and 'neg' it
            elif Token == "true":
                self.VMWriter.writePush("constant", 0)
                self.VMWriter.WriteArithmetic("~")

            else:
                print("CompileTerm: Unexpected keyword " + Token)
                CompilationEngine.sys.exit()
                
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #varName 'x'
        elif TokenType == "identifier" and LookAheadTokenType != "symbol":
            
            Token = self.JackFile.retIdentifier()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #Get KindOf token i.e. static, field, arg or var
            segment = self.SymbolTable.KindOf(Token)

            if segment == None:
                print("CompileTerm: Undeclared variable: " + Token)
                CompilationEngine.sys.exit()
            
            #Get IndexOf token i.e. 5 
            index = self.SymbolTable.IndexOf(Token)

            #Push variable to stack
            if segment == "STATIC":
                self.VMWriter.writePush("static", index)
            elif segment == "FIELD":
                self.VMWriter.writePush("this", index)
            elif segment == "ARG":
                self.VMWriter.writePush("argument", index)
            elif segment == "VAR":
                self.VMWriter.writePush("local", index)
            
        #varName[] (array) or someMethod() or someClass.someMethod() or 'x (symbol)'
        elif TokenType == "identifier" and LookAheadTokenType == "symbol":

            #varName[] i.e. array
            if LookAheadToken == '[':
                
                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                Token = self.JackFile.retSymbol()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()
                
                self.CompileExpression()

                Token = self.JackFile.retSymbol()
                TokenType = self.JackFile.retTokenType()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #subroutineName() i.e. someMethod()
            elif LookAheadToken == '(':

                Token = self.JackFile.retIdentifier()
                Name = Token
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                self.ComplileSubroutineCallA(Name)

            #className|varName.subRoutineName
            elif LookAheadToken == '.':
                
                Token = self.JackFile.retIdentifier()
                Name = Token
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                self.ComplileSubroutineCallB(Name)

            #Other possible identifier + symbol variations
            elif LookAheadToken == '+' or LookAheadToken == '-' or LookAheadToken == '*' or LookAheadToken == '/' or LookAheadToken == '&amp;' or LookAheadToken == '|' or LookAheadToken == '&lt;' or LookAheadToken == '&gt;' or LookAheadToken == '=':

                Token = self.JackFile.retIdentifier()
                TokenType = self.JackFile.retTokenType()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Get KindOf token i.e. static, field, arg or var
                segment = self.SymbolTable.KindOf(Token)

                if segment == None:
                    print("CompileTerm: Undeclared variable: " + Token)
                    CompilationEngine.sys.exit()
                
                #Get IndexOf token i.e. 5 
                index = self.SymbolTable.IndexOf(Token)

                #Push variable to stack
                if segment == "STATIC":
                    self.VMWriter.writePush("static", index)
                elif segment == "FIELD":
                    self.VMWriter.writePush("this", index)
                elif segment == "ARG":
                    self.VMWriter.writePush("argument", index)
                elif segment == "VAR":
                    self.VMWriter.writePush("local", index)

            #other possible identifier + symbol variations
            elif LookAheadToken == ')' or LookAheadToken == ";" or LookAheadToken == "," or LookAheadToken == "]":
                
                Token = self.JackFile.retIdentifier()
                TokenType = self.JackFile.retTokenType()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Get KindOf token i.e. static, field, arg or var
                segment = self.SymbolTable.KindOf(Token)

                if segment == None:
                    print("CompileTerm: Undeclared variable: " + Token)
                    CompilationEngine.sys.exit()
                
                #Get IndexOf token i.e. 5 
                index = self.SymbolTable.IndexOf(Token)

                #Push variable to stack
                if segment == "STATIC":
                    self.VMWriter.writePush("static", index)
                elif segment == "FIELD":
                    self.VMWriter.writePush("this", index)
                elif segment == "ARG":
                    self.VMWriter.writePush("argument", index)
                elif segment == "VAR":
                    self.VMWriter.writePush("local", index)

            else:
                
                self.printDebug()
                print("CompileTerm: Expected '[', '(' or '.'. Got: " + TokenType)
                CompilationEngine.sys.exit()

        #expression or unaryOp        
        elif TokenType == "symbol":
                        
            Token = self.JackFile.retSymbol()

            #'(' expression ')' 
            if Token == '(':
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()
                
                self.CompileExpression() #Returns on ')'
                
                TokenType = self.JackFile.retTokenType()
                Token = self.JackFile.retSymbol()
                
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #UnaryOp ('-' or '~')
            elif Token == '-' or Token == '~':
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                operator = Token
                #Advance Token and compileTerm
                self.JackFile.advanceToken()
                self.CompileTerm()

                #Push operator to the stack
                if operator == "-":
                    operator = "neg"
                    
                self.VMWriter.WriteArithmetic(operator)

            else:
                self.printDebug()
                print("CompileTerm: Expected '-', '~' or '('")
                CompilationEngine.sys.exit()
        
        else:
            self.printDebug()
            print("CompileTerm: Expected integerconstant, stringconstant, keyword or identifier. Got: " + TokenType)
            CompilationEngine.sys.exit()
        
        self.TokenFile.append('</term>')
   #     self.VMWriter.writeComment("</term>")
        return 

    def CompileExpressionList(self):

        nArgs = 0
        
        self.TokenFile.append('<expressionList>')
     #   self.VMWriter.writeComment("<expressionList>")
        
        self.CompileExpression()

        nArgs += 1
                        
        TokenType = self.JackFile.retTokenType()
       
        if TokenType == "symbol":
            
            Token = self.JackFile.retSymbol()
            
            if Token == ")":
                
                self.TokenFile.append('</expressionList>')
      #          self.VMWriter.writeComment("</expressionList>")
                return nArgs
       
        #Start a loop to check for more expressions
        while self.JackFile.hasMoreTokens == True:

           # self.JackFile.advanceToken()
           # TokenType = self.JackFile.retTokenType()
                
            #If closing tag is detected, return function
            if TokenType == "symbol":
                
                Token = self.JackFile.retSymbol()
                
                if Token == ")":
                    
                    self.TokenFile.append('</expressionList>')
        #            self.VMWriter.writeComment("</expressionList>")
                    return nArgs
                
                elif Token == ",":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.JackFile.advanceToken()
                    self.CompileExpression() #Will return on ',' or ')'
                    nArgs += 1
            else:
                
                self.JackFile.advanceToken()
              #  print("CompileExpressionList: Expected symbol ',' or ')' ")
              #  CompilationEngine.sys.exit()

        self.printDebug()        
        print("CompileExpressionList: Expected )")
        CompilationEngine.sys.exit()
     
    def ComplileSubroutineCallA(self, methodName):

        #Push 'this' to the stack as the first argument
        self.VMWriter.writePush("pointer", 0)
        
        methodName = methodName
        
        #Handles calls when '(' is detected

        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retSymbol()
        
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #check for closing bracket ) - if not compile the expressionList
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == ")":
                self.TokenFile.append('<expressionList>')
                self.TokenFile.append('</expressionList>')
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
                #Call the subRoutine
                self.VMWriter.writeCall(self.ClassName + "." + methodName, 1)
                
            else:
                self.printDebug()
                print("ComplileSubroutineCallA: Expected brackets )")
                CompilationEngine.sys.exit()
                
        else:
            
            nArgs = self.CompileExpressionList() #Return will be on ')'
            TokenType = self.JackFile.retTokenType()
            Token = self.JackFile.retSymbol()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #Call the subRoutine
            self.VMWriter.writeCall(self.ClassName + "." + methodName, nArgs + 1)
        
        return

    def ComplileSubroutineCallB(self, Name):

        #Handles calls when '.' is detected
        
        Name = Name
        
        #if x.someRoutine(expression)
        if self.SymbolTable.KindOf(Name) != None:
           
            #Get kindOf variable 'field, static, arg or var':
            segment = self.SymbolTable.KindOf(Name)
           
            #Get IndexOf token i.e. 5 
            index = self.SymbolTable.IndexOf(Name)

            #Get class asscociated with object i.e. 'Ball'
            className = self.SymbolTable.TypeOf(Name)
                    
            #Push 'varName' to the stack as the first argument
            if segment == "STATIC":
                self.VMWriter.writePush("static", index)
            elif segment == "FIELD":
                self.VMWriter.writePush("this", index)
            elif segment == "ARG":
                self.VMWriter.writePush("argument", index)
            elif segment == "VAR":
                self.VMWriter.writePush("local", index)
                    
            intArg = 1
             
        #if someClass.constructor(expression) or someClass.someFunction(expression)    
        else:
            
            className = Name
            intArg = 0
               
        #Handles calls when '.' is detected

        TokenType = self.JackFile.retTokenType()
        Token = self.JackFile.retSymbol()
        
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()
        
        #Get subroutine Name and append it
        if TokenType == "identifier":
            
            Token = self.JackFile.retIdentifier()
            subroutineName = Token
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            
            self.JackFile.advanceToken()
            
            TokenType = self.JackFile.retTokenType()
            Token = self.JackFile.retSymbol()
            
            #Get the opening brackets (
            if Token == "(":
                                      
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()
                
                #check for closing bracket ) - if not compile the expressionList
                if TokenType == "symbol":
                    
                    Token = self.JackFile.retSymbol()
                    
                    if Token == ")":
                        
                        self.TokenFile.append('<expressionList>')
                        self.TokenFile.append('</expressionList>')
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                        #Call the subRoutine
                        self.VMWriter.writeCall(className + "." + subroutineName, intArg)
                        
                    else:
                        
                        nArgs = self.CompileExpressionList() #Return will be on ')'
                        TokenType = self.JackFile.retTokenType()
                        Token = self.JackFile.retSymbol()
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                        #Call the subRoutine
                        self.VMWriter.writeCall(className + "." + subroutineName, nArgs + intArg)
                        
                        #self.printDebug()
                        #print("ComplileSubroutineCallB: Expected brackets )")
                        #CompilationEngine.sys.exit()
                        
                else:
                    nArgs = self.CompileExpressionList() #Return will be on ')'
                    TokenType = self.JackFile.retTokenType()
                    Token = self.JackFile.retSymbol()
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                    #Call the subRoutine
                    self.VMWriter.writeCall(className + "." + subroutineName, nArgs + intArg)
                    
            else:
                self.printDebug()
                print("ComplileSubroutineCallB: Expected '('. Got: " + TokenType)
                CompilationEngine.sys.exit()
                
        else:
            self.printDebug()
            print("ComplileSubroutineCallB: Expected subRoutine Name")
            CompilationEngine.sys.exit() 

        return
    
    def retCurrentToken(self):
        return self.TokenFile[self.CurrentToken]    

    def advanceToken(self):
        self.CurrentToken += 1
        if self.CurrentToken >= self.TotalTokens:
            self.hasMoreTokens = False
        else:
            self.hasMoreTokens = True

    def printDebug(self):

        OFile = self.filename + 'DebugCmp.xml'
        Wfile = open(OFile, 'w')

        for line in self.TokenFile:
            Wfile.write(line + '\n')

        Wfile.close()
