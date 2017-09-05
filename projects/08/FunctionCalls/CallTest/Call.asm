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
@Call.Call.fn$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Call.Call.fn
0;JMP
(Call.Call.fn$ret.0)
// label loop
(Call.foo$loop)
// goto loop
@Call.foo$loop
0;JMP
// function Call.fn 0
(Call.Call.fn)
// label halt
(Call.Call.fn$halt)
// goto halt
@Call.Call.fn$halt
0;JMP
