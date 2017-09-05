// call f n

//Store the return address
@f$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1

//Save LCL
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1

//Save ARG
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1

//Save THIS
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1

//Save THAT
@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1

//Reposition ARG
@SP
D=A
@n //number of arguments
D=D-A
@5
D=D-A
@ARG
M=D

//reposition LCL
@SP
D=A
@LCL
M=D

//Jump to function
@f
0;JMP

(f$ret.1) //return here