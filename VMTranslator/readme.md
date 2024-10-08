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
M=D-M

//