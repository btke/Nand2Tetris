#Tests the Symbol Table

import glob, os
import SymbolTable #Contains the Symbol Table

#set the directory
directory = "C:/Users/sahil.masand/OneDrive/CS/Nand2Tetris/nand2tetris/projects/11/ST_Test/"
#directory = "C:/Users/Sahil/OneDrive/CS/Nand2Tetris/nand2tetris/projects/10/ArrayTest_TK/"
#directory = "C:/Users/justm/OneDrive/CS/Nand2Tetris/nand2tetris/projects/10/Pong/"

#change directory
os.chdir(directory)

ST = SymbolTable.SymbolTable() #Define a new symbol table

ST.Define('Batx', 'int', 'FIELD')
ST.Define('Baty', 'int', 'FIELD')
ST.Define('drawx', 'int', 'FIELD')
ST.Define('drawy', 'int', 'FIELD')

ST.Define('Static1', 'int', 'STATIC')
ST.Define('Static2', 'int', 'STATIC')

ST.Define('key', 'char', 'VAR')
ST.Define('exit', 'boolean', 'VAR')

ST.Define('ARG1', 'char', 'ARG')
ST.Define('ARG2', 'boolean', 'ARG')

ST.startSubroutine()

ST.Define('key1', 'char', 'VAR')
ST.Define('exit1', 'boolean', 'VAR')

ST.Define('ARGx', 'char', 'ARG')
ST.Define('ARGy', 'boolean', 'ARG')

ST.printDebug()
print(ST.VarCount('ARG'))
