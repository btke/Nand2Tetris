class CodeWriter:
    outputL = ["// Bootstrap code", "@256", "D=A", "@SP", "M=D"] #Store the output assembly commands (contains bootstrap code)
    
    #call sys.init() (Bootstrap Code)
    outputL.append("// Call Sys.init()") #Write a comment with current VM command
    outputL.extend(["@Sys.init$ret", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Store the return address
    outputL.extend(["@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save LCL
    outputL.extend(["@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save ARG
    outputL.extend(["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save THIS
    outputL.extend(["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save THAT
    outputL.extend(["@SP", "D=M", "@0", "D=D-A", "@5", "D=D-A", "@ARG", "M=D"]) #Reposition the ARG pointer
    outputL.extend(["@SP", "D=M", "@LCL", "M=D"]) #reposition the LCL pointed
    outputL.extend(["@Sys.init", "0;JMP"]) #jump to function
    outputL.extend(["(Sys.init$ret)"]) #return label
    outputL.extend(["@Sys.init$ret", "0;JMP"]) #Loop
    
    #outputL=[]
    MemSegDict = {'local': '@LCL', 'argument': '@ARG', 'this': '@THIS', 'that': '@THAT'} #stores the VM:ASM translation for certain memory segments
    MemSeg1 = ['local', 'argument', 'this', 'that']
    Arithmetic1 = ['add', 'sub', 'and', 'or']
    Arithmetic2 = ['eq', 'gt', 'lt']
    Arithmetic3 = ['neg', 'not']
    ArithmeticDict1 = {'add': 'M=D+M', 'sub': 'M=M-D', 'and': 'M=M&D', 'or': 'M=M|D'} #VM:ASM translation for some arithmetic commands
    ArithmeticDict2 = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}
    ArithmeticDict3 = {'neg': 'D=-M', 'not': 'D=!M'}
    IntX = 0 #used to generate unique jump labels for the eq, gt and lt commands
    IntF = 0 #used to generate a unique return label for a function
    filename = ""
    currentFunction = "foo"
    
    #Intialise the class and set filename
    def __init__(self, filename):
        self.filename = filename
        CodeWriter.filename = filename

    #Handles and writes the ASM output for push/pop commands
    def WritePushPop(self, command, segment, index):
        self.command = command
        self.segment = segment
        self.index = index
        CodeWriter.outputL.append("// " + command + " " + segment + " " + index) #Write a comment with current VM command
        
        if command == "C_PUSH":

            #Check for 'local', 'argument', 'this' or 'that' memory segment commands
            if segment in CodeWriter.MemSeg1:                
                CodeWriter.outputL.extend([CodeWriter.MemSegDict.get(segment, "ERR"), "D=M", "@" + index, "D=D+A", "A=D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
                                
            elif segment == "constant":
                CodeWriter.outputL.extend(["@"+index, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"])

            elif segment == "pointer":
                CodeWriter.outputL.extend(["@"+str(int(index)+3), "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
                
            elif segment == "temp":
                CodeWriter.outputL.extend(["@"+str(int(index)+5), "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])    

            elif segment == "static":
                CodeWriter.outputL.extend(["@"+CodeWriter.filename+"$foo."+index, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
            
        elif command == "C_POP":

            #Check for 'local', 'argument', 'this' or 'that' memory segment commands
            if segment in CodeWriter.MemSeg1:
                CodeWriter.outputL.extend([CodeWriter.MemSegDict.get(segment, "ERR"), "D=M", "@" + index, "D=D+A", "@R13", "M=D", "@SP", "M=M-1", "A=M", "D=M", "@R13", "A=M", "M=D"])

            elif segment == "pointer":
                CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@"+str(int(index)+3), "M=D"])
                
            elif segment == "temp":
                CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@"+str(int(index)+5), "M=D"])

            elif segment == "static":
                CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@"+CodeWriter.filename+"$foo."+index, "M=D"])
        
    def WriteArithmetic(self, command):
        self.command = command
        CodeWriter.outputL.append("// " + command) #Write a comment with current VM command

        #check for 'add', 'sub', 'and', 'or'
        if command in CodeWriter.Arithmetic1:
            CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", CodeWriter.ArithmeticDict1.get(command, "ERR"), "@SP", "M=M+1"])

        #check for 'eq', 'gt' or 'lt'        
        elif command in CodeWriter.Arithmetic2:
            CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D", "@TRUE"+str(CodeWriter.IntX), "D;"+CodeWriter.ArithmeticDict2.get(command, "ERR"), "@SP", "A=M", "M=0", "@END"+str(CodeWriter.IntX), "0;JMP", "(TRUE"+str(CodeWriter.IntX)+")", "@SP", "A=M", "M=-1", "@END"+str(CodeWriter.IntX), "0;JMP", "(END"+str(CodeWriter.IntX)+")", "@SP", "M=M+1"])
            CodeWriter.IntX = CodeWriter.IntX + 1

        #check for 'neg' or 'not'    
        elif command in CodeWriter.Arithmetic3:
            CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", CodeWriter.ArithmeticDict3.get(command, "ERR"), "M=D", "@SP", "M=M+1"])
    
    def writeLabel(self, label):
        self.label = label
        CodeWriter.outputL.append("// label " + label) #Write a comment with current VM command
        CodeWriter.outputL.extend(["(" + CodeWriter.currentFunction + "$" + label+")"])

    def writeGoto(self, label):
        self.label = label
        CodeWriter.outputL.append("// goto " + label) #Write a comment with current VM command
        CodeWriter.outputL.extend(["@" + CodeWriter.currentFunction + "$" + label, "0;JMP"])
        
    def writeIf(self, label):
        self.label = label
        CodeWriter.outputL.append("// if-goto " + label) #Write a comment with current VM command
        CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@" + CodeWriter.currentFunction + "$" + label, "D;JNE"])

    def writeCall(self, functionName, numArgs):
        self.functionName = functionName
        self.numArgs = numArgs
        CodeWriter.outputL.append("// Call " + functionName + " " + numArgs) #Write a comment with current VM command
        CodeWriter.outputL.extend(["@"+functionName+"$ret."+str(CodeWriter.IntF), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Store the return address
        CodeWriter.outputL.extend(["@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save LCL
        CodeWriter.outputL.extend(["@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save ARG
        CodeWriter.outputL.extend(["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save THIS
        CodeWriter.outputL.extend(["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]) #Save THAT
        CodeWriter.outputL.extend(["@SP", "D=M", "@"+numArgs, "D=D-A", "@5", "D=D-A", "@ARG", "M=D"]) #Reposition the ARG pointer
        CodeWriter.outputL.extend(["@SP", "D=M", "@LCL", "M=D"]) #reposition the LCL pointed
        CodeWriter.outputL.extend(["@"+functionName, "0;JMP"]) #jump to function
        CodeWriter.outputL.extend(["("+functionName+"$ret."+str(CodeWriter.IntF)+")"]) #return label
        CodeWriter.IntF = CodeWriter.IntF + 1

    def writeFunction(self, functionName, numLocals):
        self.functionName = functionName
        self.numLocals = numLocals
        CodeWriter.currentFunction=functionName
        CodeWriter.outputL.append("// function " + functionName + " " + numLocals) #Write a comment with current VM command
        CodeWriter.outputL.extend(["("+functionName+")"])#function label
        for i in list(range(int(numLocals))): #set local segments to zero
            CodeWriter.outputL.extend(["@SP", "A=M", "M=0", "@SP", "M=M+1"])
            
    def writeReturn(self):
        CodeWriter.outputL.append("// return")
        CodeWriter.outputL.extend(["@LCL", "D=M", "@R14", "M=D"]) #FRAME is a temporary variable, LCL=FRAME
        CodeWriter.outputL.extend(["@R14", "D=M", "@5", "D=D-A", "A=D", "D=M", "@R15", "M=D"]) #save return address in a temp. var, RET=*(FRAME-5)
        CodeWriter.outputL.extend(["@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D"]) #reposition return value for caller, *ARG=pop()
        CodeWriter.outputL.extend(["@ARG", "D=M", "D=D+1", "@SP", "M=D"]) #restore SP for caller, SP=ARG+1
        CodeWriter.outputL.extend(["@R14", "D=M", "@1", "D=D-A", "A=D", "D=M", "@THAT", "M=D"]) #restore THAT of calling function, THAT=*(FRAME-1)
        CodeWriter.outputL.extend(["@R14", "D=M", "@2", "D=D-A", "A=D", "D=M", "@THIS", "M=D"]) #restore THIS of calling function, THIS=*(FRAME-2)
        CodeWriter.outputL.extend(["@R14", "D=M", "@3", "D=D-A", "A=D", "D=M", "@ARG", "M=D"]) #restore ARG of calling function, ARG=*(FRAME-3)
        CodeWriter.outputL.extend(["@R14", "D=M", "@4", "D=D-A", "A=D", "D=M", "@LCL", "M=D"]) #restore LCL of calling function, LCL=*(FRAME-4)
        CodeWriter.outputL.extend(["@R15", "A=M", "0;JMP"]) #Goto to return address
