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

//label {command['label']}
({command['label']})


//goto {command['label']}
@{command['label']}
0;JMP

//if goto
@SP
AM=M-1
D=M
@{command['label']}
D;JNE


//pop segment i
@{parameter}
D=A 
@{seg}
        A=M
        D=D+A
        @{seg}
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @{seg}
        A=M
        M=D
        @{parameter}
        D=A
        @{seg}
        A=M
        D=A-D
        @{seg}
        M=D

//push segment i
@{parameter}
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1


//push static i
@Foo.{parameter}
D=M
@SP
A=M // a= ram(sp)
M=D // ram(ram(sp))=foo.i
@SP
M=M+1

// pop static i
@SP
M=M-1
A=M // a = ram(sp) avec sp--
D=M  // D= ram(ram(sp))
@Foo.{parameter}
M=D // ram(Foo.i)= ram(ram(sp))



//push temp i
@{parameter}
D=A
@5
D=D+M // addr = ram(5)+1
@SP
A=M
A=M
M=D
@SP
M=M+1

//pop temp i
@SP
M=M-1
A=M
D=M

push pointer i
@THIS/THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

//pop pointer i
@SP
M=M-1
A=M
D=M
@THIS/THAT
M=D
