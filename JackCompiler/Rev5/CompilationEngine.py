class CompilationEngine:
    #Compiles a Jack Program

    import sys
    import JackTokenizer #Contains the class modules for the Tokenizer
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):

        self.TotalTokens = -1
        self.CurrentToken = -1
        self.hasMoreTokens = True
        
        self.filename=filename
        self.JackFile = CompilationEngine.JackTokenizer.Tokenizer(filename) #Load the .jack file into the Tokenizer
        self.TokenFile = []

        self.startCompilation()
            
    def startCompilation(self):

        self.CompileClass()

        for line in self.TokenFile:
            self.TotalTokens += 1
            
        print("Compilation completed successfully!")

    #Compile a complete Class
    def CompileClass(self):

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Append <Class>
        self.TokenFile.append('<class>')
        
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

        #<classVarDec>
        self.TokenFile.append('<classVarDec>')
        
        TokenType = self.JackFile.retTokenType()

        #Append the keyword 'static|field'
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'type' of declaration which can be a keyword (int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("CompileClassVarDec: Expected 'type'")
            CompilationEngine.sys.exit()

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for class 'varName'
        if TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("CompileClassVarDec: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

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
                    return #End classVarDec
                elif Token == ",":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            elif TokenType == "identifier":
                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        self.printDebug()        
        print("CompileClassVarDec: Expected ;")
        CompilationEngine.sys.exit()   

    #Compile a Subroutine
    def CompileSubroutine(self):
        
        self.TokenFile.append('<subroutineDec>')
        
        TokenType = self.JackFile.retTokenType()

        #Append the keyword 'constructor|method|function'
        Token = self.JackFile.retKeyWord()
        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #Advance Token
        self.JackFile.advanceToken()
        TokenType = self.JackFile.retTokenType()

        #Check for 'type' of declaration which can be a keyword (void|int|char|boolean) or an identifier (className)
        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
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
                    self.TokenFile.append('</subroutineDec>')
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
                    self.compileStatements() #Compile statement - Expect return on }
                    TokenType = self.JackFile.retTokenType()
                    Token = self.JackFile.retSymbol()
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.TokenFile.append('</subroutineBody>')
                    self.TokenFile.append('</subroutineDec>')
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
        TokenType = self.JackFile.retTokenType()

        #Append the keyword (void|int|char|boolean) or an identifier (className)

        if TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
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
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileParameterList: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()

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
                    return
                elif Token == ",":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            elif TokenType == "identifier":
                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            elif TokenType == "keyword":
                Token = self.JackFile.retKeyWord()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        self.printDebug() 
        print("compileParameterList: Expected )")
        CompilationEngine.sys.exit()
    
    def compileVarDec(self):
        
        self.TokenFile.append('<varDec>')
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
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        elif TokenType == "identifier":
            Token = self.JackFile.retIdentifier()
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
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        else:
            self.printDebug()
            print("compileVarDec: Expected 'Identifier'. Got: " + TokenType)
            CompilationEngine.sys.exit()
        
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
                    return
                elif Token == ",":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            elif TokenType == "identifier":
                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                
        self.printDebug()        
        print("compileVarDec: Expected ;")
        CompilationEngine.sys.exit()

    def compileStatements(self):
        
        self.TokenFile.append('<statements>')
        
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
           
            if Token == "(":
                self.ComplileSubroutineCallA()
                                       
            elif Token == ".":
                self.ComplileSubroutineCallB()
                
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

            if Token == "[":
            
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

        self.TokenFile.append('<whileStatement>')

        #Append the keyword 'while'
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

                        self.TokenFile.append('</whileStatement>')
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
            return

        self.printDebug()
        print("compileReturn: Expected ;")
        CompilationEngine.sys.exit() 

    def compileIf(self):

        self.TokenFile.append('<ifStatement>')

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
                                        
                                        self.compileStatements() #Compile statement - Expect return on }
                                        
                                        TokenType = self.JackFile.retTokenType()
                                        Token = self.JackFile.retSymbol()
                                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                                        self.TokenFile.append('</ifStatement>')
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
                                self.TokenFile.append('</ifStatement>')
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

        self.CompileTerm()
        
        #Check for more statements
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
                    return
                
                #Check for closing statements and return function
                elif Token == ";" or Token == "]" or Token == ")":
                    self.TokenFile.append('</expression>')
                    return
                
                else:
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
            else:
                self.printDebug()
                print("CompileExpression: Expected Operator. Got: " + TokenType)
                CompilationEngine.sys.exit()

            #Advance Token
            self.JackFile.advanceToken()
            TokenType = self.JackFile.retTokenType()

            self.CompileTerm()

    def CompileTerm(self):
        
        self.TokenFile.append('<term>')
        
        TokenType = self.JackFile.retTokenType()
        LookAheadTokenType = self.JackFile.retTokenTypeLookAhead()
        LookAheadToken = self.JackFile.retTokenLookAhead()

        #integerConstant        
        if TokenType == "integerConstant":
            Token = self.JackFile.retIntVal()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #stringConstant    
        elif TokenType == "stringConstant":
            Token = self.JackFile.retStringVal()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #keyword
        elif TokenType == "keyword":
            Token = self.JackFile.retKeyWord()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #varName    
        elif TokenType == "identifier" and LookAheadTokenType != "symbol":
            
            Token = self.JackFile.retIdentifier()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

        #varName[] or subRoutineCall
        elif TokenType == "identifier" and LookAheadTokenType == "symbol":

            #varName[]
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

            #subroutineName()
            elif LookAheadToken == '(':

                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                self.ComplileSubroutineCallA()

            #className|varName.subRoutineName
            elif LookAheadToken == '.':
                
                Token = self.JackFile.retIdentifier()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

                #Advance Token
                self.JackFile.advanceToken()
                TokenType = self.JackFile.retTokenType()

                self.ComplileSubroutineCallB()

            #Other possible identifier + symbol variations
            elif LookAheadToken == '+' or LookAheadToken == '-' or LookAheadToken == '*' or LookAheadToken == '/' or LookAheadToken == '&amp;' or LookAheadToken == '|' or LookAheadToken == '&lt;' or LookAheadToken == '&gt;' or LookAheadToken == '=':

                Token = self.JackFile.retIdentifier()
                TokenType = self.JackFile.retTokenType()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

            #other possible identifier + symbol variations
            elif LookAheadToken == ')' or LookAheadToken == ";" or LookAheadToken == "," or LookAheadToken == "]":
                
                Token = self.JackFile.retIdentifier()
                TokenType = self.JackFile.retTokenType()
                self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')

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
                #Advance Token
                self.JackFile.advanceToken()
                self.CompileTerm()

            else:
                self.printDebug()
                print("CompileTerm: Expected '-', '~' or '('")
                CompilationEngine.sys.exit()
        
        else:
            self.printDebug()
            print("CompileTerm: Expected integerconstant, stringconstant, keyword or identifier. Got: " + TokenType)
            CompilationEngine.sys.exit()
        
        self.TokenFile.append('</term>')
        return 

    def CompileExpressionList(self):
      
        self.TokenFile.append('<expressionList>')

        self.CompileExpression()
                
        TokenType = self.JackFile.retTokenType()
       
        if TokenType == "symbol":
            Token = self.JackFile.retSymbol()
            if Token == ")":
                self.TokenFile.append('</expressionList>')
                return
       
        #Start a loop to check for more expressions
        while self.JackFile.hasMoreTokens == True:

           # self.JackFile.advanceToken()
           # TokenType = self.JackFile.retTokenType()
                
            #If closing tag is detected, return function
            if TokenType == "symbol":
                Token = self.JackFile.retSymbol()
                if Token == ")":
                    self.TokenFile.append('</expressionList>')
                    return
                elif Token == ",":
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    self.JackFile.advanceToken()
                    self.CompileExpression() #Will return on ',' or ')'
            else:
                self.JackFile.advanceToken()
              #  print("CompileExpressionList: Expected symbol ',' or ')' ")
              #  CompilationEngine.sys.exit()

        self.printDebug()        
        print("CompileExpressionList: Expected )")
        CompilationEngine.sys.exit()
     
    def ComplileSubroutineCallA(self):
        
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
            else:
                self.printDebug()
                print("ComplileSubroutineCallA: Expected brackets )")
                CompilationEngine.sys.exit()
                
        else:
            self.CompileExpressionList() #Return will be on ')'
            TokenType = self.JackFile.retTokenType()
            Token = self.JackFile.retSymbol()
            self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
        
        return

    def ComplileSubroutineCallB(self):

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
                    else:
                        self.CompileExpressionList() #Return will be on ')'
                        TokenType = self.JackFile.retTokenType()
                        Token = self.JackFile.retSymbol()
                        self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                        #self.printDebug()
                        #print("ComplileSubroutineCallB: Expected brackets )")
                        #CompilationEngine.sys.exit()
                        
                else:
                    self.CompileExpressionList() #Return will be on ')'
                    TokenType = self.JackFile.retTokenType()
                    Token = self.JackFile.retSymbol()
                    self.TokenFile.append('<' + TokenType + '> ' + Token + ' </' + TokenType + '>')
                    
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
        
