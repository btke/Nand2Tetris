//pop local 5

//Calculate location of local memory segment and store it in a temp. register
@LCL
D=M //D=LCL
@5
D=D+A //local + 5
@R13
M=D

@SP
M=M-1 //SP--
A=M //RAM[SP]
D=M //D=RAM[SP]

@R13
A=M
M=D





