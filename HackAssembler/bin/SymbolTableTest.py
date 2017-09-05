import SymbolTableModule

ST = SymbolTableModule.SymbolTable()

print(ST.contains('KBD'))
print(ST.GetAddress('R1'))

print(ST.contains('LOOP'))
ST.addEntry('LOOP' , '56')
print(ST.GetAddress('LOOP'))
