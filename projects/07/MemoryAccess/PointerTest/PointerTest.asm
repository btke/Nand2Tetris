// C_PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
M=M-1
A=M
D=M
@3
M=D
// C_PUSH constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
// C_PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP this 2
@THIS
D=M
@2
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// C_PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP that 6
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// C_PUSH pointer 0
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH pointer 1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
// C_PUSH this 2
@THIS
D=M
@2
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// C_PUSH that 6
@THAT
D=M
@6
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
