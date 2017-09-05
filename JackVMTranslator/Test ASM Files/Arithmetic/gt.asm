// gt

@SP
M=M-1
A=M
D=M //select y

@SP
M=M-1
A=M
D=M-D //x-y

@TRUE
D;JGT //if D>0 then eq condition is satisfied

@SP
A=M
M=0 //if jump fails, set FALSE flag
@END
0;JMP

(TRUE)
@SP
A=M
M=-1
@END
0;JMP

(END)
@SP
M=M+1
