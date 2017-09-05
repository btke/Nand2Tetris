//return

//FRAME is a temporary variable, LCL=FRAME
@LCL
D=M
@FRAME
M=D

//save return address in a temp. var, RET=*(FRAME-5)
@FRAME
D=M
@5
D=D-A //FRAME-5
A=D //Goto [FRAME-5]
D=M
@RET
M=D

//reposition return value for caller, *ARG=pop()
//Pop last value in stack
@SP
M=M-1
A=M
D=M
//Overwrite the value in *ARG
@ARG
A=M
M=D

//restore SP for caller, SP=ARG+1
@ARG
D=M
D=D+1
@SP
M=D


//restore THAT of calling function, THAT=*(FRAME-1)
@FRAME
D=M
@1
D=D-A //FRAME-1
A=D //Goto [FRAME-1]
D=M
@THAT
M=D

//restore THIS of calling function, THIS=*(FRAME-2)
@FRAME
D=M
@2
D=D-A //FRAME-2
A=D //Goto [FRAME-2]
D=M
@THIS
M=D

//restore ARG of calling function, ARG = *(FRAME-3)
@FRAME
D=M
@3
D=D-A //FRAME-3
A=D //Goto [FRAME-3]
D=M
@ARG
M=D

//restore LCL of calling function, LCL = *(FRAME-4)
@FRAME
D=M
@4
D=D-A //FRAME-4
A=D //Goto [FRAME-4]
D=M
@LCL
M=D

// GOTO the return-address
@RET
A=M
0;JMP