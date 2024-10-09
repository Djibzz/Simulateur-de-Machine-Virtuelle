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

//GT
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D // ram(x)
M=-1  //on met a true de  base
@GT
D;JGT // si le reste de x-y est superieur a 0 alors x>y et on skip le code
@SP
A=M-1
M=0
(GT)

//LT
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
M=-1
@LT
D;JLT// si le reste de x-y est inferieur a 0 alors x<y et on skip le code
@SP
A=M-1
M=0
(LT)

//AND
@SP
M=M-1
A=M
D=M
A=A-1
M=M&&D

//OR
@SP
M=M-1
A=M
D=M
A=A-1
M=M||D

//NOT
@SP
A=M-1 // on décrémente pas car on change juste y en -y on ne l'enleve pas
M=!M