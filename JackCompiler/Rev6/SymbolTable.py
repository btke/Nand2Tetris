class SymbolTable:
    #Manages the symbol table for a Jack Program

    import sys

    #Initialise the symbol table
    def __init__(self, filename):

        self.filename = filename
        self.ClassScope = []
        self.SubRoutineScope = []
        self.StaticIndex = -1
        self.FieldIndex = -1
        self.ArgIndex = -1
        self.VarIndex = -1

    #Starts a new subroutine scope (and resets the subroutine symbol table)
    def startSubroutine(self):

        self.SubRoutineScope.clear()
        self.ArgIndex = -1
        self.VarIndex = -1

    #Defines it a new identifier of a given name, kind and type
    def Define(self, Name, TP, Kind):

        Name = Name
        TP = TP #Type
        Kind = Kind

        if Kind == "STATIC":
            
            self.StaticIndex += 1
            self.ClassScope.append([Name, TP, Kind, self.StaticIndex])

        elif Kind == "FIELD":

            self.FieldIndex += 1
            self.ClassScope.append([Name, TP, Kind, self.FieldIndex])

        elif Kind == "ARG":

            self.ArgIndex += 1
            self.SubRoutineScope.append([Name, TP, Kind, self.ArgIndex])

        elif Kind == "VAR":

            self.VarIndex += 1
            self.SubRoutineScope.append([Name, TP, Kind, self.VarIndex])

        else:
            
            print("SymbolTable: Unexpected kind in Define")
            SymbolTable.sys.exit()

    #Returns the number of variables of the given kind
    def VarCount(self, Kind):

        Kind = Kind

        if Kind == "STATIC":
            
            return (self.StaticIndex + 1)

        elif Kind == "FIELD":

            return (self.FieldIndex + 1)

        elif Kind == "ARG":

            return (self.ArgIndex + 1)

        elif Kind == "VAR":

            return (self.VarIndex + 1)

        else:
            
            print("SymbolTable: Unexpected kind in VarCount")
            SymbolTable.sys.exit()

    #Returns kind of the named identifier in the current scope. Return None if no identifier is found        
    def KindOf(self, Name):

        Name = Name

        #Search the Subroutine table
        for Line in self.SubRoutineScope:
            if Name == Line[0]:
                return Line[2]

        #Search the class level table
        for Line in self.ClassScope:
            if Name == Line[0]:
                return Line[2]

        #If not found, return None
        return None

    def TypeOf(self, Name):

        Name = Name

        #Search the Subroutine table
        for Line in self.SubRoutineScope:
            if Name == Line[0]:
                return Line[1]

        #Search the class level table
        for Line in self.ClassScope:
            if Name == Line[0]:
                return Line[1]

        print("SymbolTable: Name not found in TypeOf")
        SymbolTable.sys.exit()
        
    def IndexOf(self, Name):

        Name = Name

        #Search the Subroutine table
        for Line in self.SubRoutineScope:
            if Name == Line[0]:
                return Line[3]

        #Search the class level table
        for Line in self.ClassScope:
            if Name == Line[0]:
                return Line[3]

        print("SymbolTable: Name not found in IndexOf")
        SymbolTable.sys.exit()
        
    def printDebug(self):

        filename = self.filename
        
        OFile = filename + '_SymbolTable.txt'
        Wfile = open(OFile, 'w')
        
        Wfile.write("ClassScope" +' \n')
            
        for Line in self.ClassScope:
            Wfile.write(str(Line[0]) + '|' + str(Line[1]) + '|' + str(Line[2]) + '|' + str(Line[3]) + '\n')

        Wfile.write("SubRoutineScope" +' \n')

        for Line in self.SubRoutineScope:
            Wfile.write(str(Line[0]) + '|' + str(Line[1]) + '|' + str(Line[2]) + '|' + str(Line[3]) + '\n')
        
        Wfile.close()
