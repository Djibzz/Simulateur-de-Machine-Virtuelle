EXPlICATIONS DU CODE:
// push constant i
@{parameter}
D=A 
@SP 
A=M 
M=D
@SP 
M=M+1

// add
@SP
M=M-1 
A=M
D=M // d=3
@SP
A=M-1
M=D+M

// sub
@SP
M=M-1 
A=M
D=M // d=3
@SP
A=M-1
M=M-D

//neg
@SP
M=M-1
A=M
M=-M

//EQ
@SP
A=M-1
D=M
A=A-1
D=D-M
@IF
D;JEQ
D=0
@END
0;JMP
(IF)
D=-1
(END)
@SP
M=M-1
A=M-1
M=D