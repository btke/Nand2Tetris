// C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 456
@456
D=A
@SP
A=M
M=D
@SP
M=M+1
// Call Call.fn 2
@Call.fn$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=A
@2
D=D+A
@5
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@Call.fn
0;JMP
(Call.fn$ret.0)
// label loop
(loop)
// goto loop
@loop
0;JMP
// function Call.fn 0
(Call.fn)
// label halt
(halt)
// goto halt
@halt
0;JMP
