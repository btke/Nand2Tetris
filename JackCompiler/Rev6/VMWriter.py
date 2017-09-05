class VMWriter:
    #Writes VM Commands

    import sys
    
    #Intialise the class for handling files and clear existing data
    def __init__(self, filename):
     
        self.filename=filename
        self.VMFile = []

    def writePush(self, segment, index):

        segment = segment
        index = index
       
        self.VMFile.append("push " + str(segment) + " " + str(index))   

    def writePop(self, segment, index):

        segment = segment
        index = index
        
        self.VMFile.append("pop " + str(segment) + " " + str(index))

    def WriteArithmetic(self, command):

        command = command

        if command == "+":
            self.VMFile.append("add")
        elif command == "-":
            self.VMFile.append("sub")
        elif command == "~":
            self.VMFile.append("not")
        elif command == "=":
            self.VMFile.append("eq")
        elif command == "&lt;":
            self.VMFile.append("lt")
        elif command == "&gt;":
            self.VMFile.append("gt")
        elif command == "&amp;":
            self.VMFile.append("and")
        elif command == "|":
            self.VMFile.append("or")
        elif command == "neg" :
            self.VMFile.append("neg")
        else:
            print("VMWriter: Unrecognised Symbol")
            VMWriter.sys.exit()

    def WriteLabel(self, label):

        label = label

        self.VMFile.append("label " + str(label))

    def WriteGoto(self, label):

        label = label

        self.VMFile.append("goto " + str(label))

    def WriteIf(self, label):

        label = label

        self.VMFile.append("if-goto " + str(label))

    def writeCall(self, name, nArgs):

        name = name
        nArgs = nArgs

        self.VMFile.append("call " + str(name) + " " + str(nArgs))

    def writeFunction(self, name, nLocals):

        name = name
        nLocals = nLocals

        self.VMFile.append("function " + str(name) + " " + str(nLocals))

    def writeReturn(self):

        self.VMFile.append("return")

    def writeComment(self, comment):

        self.VMFile.append("// " + comment)
        
    def printVMFile(self):
        
        OFile = self.filename.split(".")
        OFile = OFile[0] + '.vm'
        Wfile = open(OFile, 'w')

        for line in self.VMFile:
            Wfile.write(line + '\n')

        Wfile.close()
