AFIN de faire marcher le vm Translator et le parserXML on doir creer des configurations python. On creer des fichiers test.vm 
ou test.jack et les choisir comme parametres de scripts

EXPlICATIONS DU CODE ASSEMBLEUR:

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
D=M-D // x-y
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
M=D&M

//OR
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M

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
@{segment}
D=D+M
@SP
M=M-1


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
D=M// addr = ram(5+1)
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
@{parameter}
M=D

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

//return 
@LCL
@D=M  // ca récupère l'adresse indiquée dans LCL (1ere valeur locale / savedFrame+1)

@endFrame
M=D

@5
D=A
@endFrame
D=M-D           // On  cherche l'indice 5 cases au dessus de endFrame
@retAddr        // On le stocke dans une autre variable temp
M=D
""" self.popcommand({'type': 'pop', 'segment': 'argument', 'parameter': '0'})""""
//  on return la valeur de la fonction , on réplace les pointers de la frame précédente

@ARG
D=M+1
@SP
M=D

@endFrame
A=M
A=A-1           
D=M
@THAT
M=D             // THAT restored

@2
D=A
@endFrame
A=M 
A=A-D           
D=M
@THIS
M=D             // THIS restored 
        
  
@3
D=A
@endFrame
A=M
A=A-D           
D=M
@ARG            // ARG restored
M=D

@4
D=A 
@endFrame 
A=M 
A=A-D       
D=M
@LCL           // LCL restored 
M=D

@retAddr
A=M
A=M
0;JMP


//Call
@appel unique (utiliser le labelcount)
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


//Fonction
parametre = command['parameter']
function = command['function']
initia = f"// On initialise {para} variables locales\n"

for i in range(0,int(parametre)):
     initia= initia + self.pushcommand({'type': 'push', 'segment': 'constant', 'parameter': '0'})

return f""\t//{command['type']} {command['function']} {command['parameter']}"
+elf.branchingcommand.asm({'type': 'label', f'label': function}) +initia



//pour tester le code mettre 
 RAM[0] 256,
 RAM[1] 300,
 RAM[2] 400, 
RAM[3] 3000, 
RAM[4] 3010,