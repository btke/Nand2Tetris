//push local 5

//Get location of local memory segment
@LCL
D=M //D=RAM[LCL]

@5
D=D+A //local + 5
A=D 
D=M //D=RAM[LCL+5]

@SP
A=M //RAM[SP]
M=D //RAM[SP] = D

@SP
M=M+1 //SP++
