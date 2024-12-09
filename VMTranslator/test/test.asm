// Bootstrap
    @5
    // pas oublier de remettre a 256
    D=A
    @SP
    M=D 

//code de test/test.vm
	 // Function SimpleFunctiontest 2  //label SimpleFunctiontest
        (SimpleFunctiontest)
        // On initialise 2 variables locales
	//push constant 0
            @0
            D=A 
            @SP 
            A=M 
            M=D
            @SP 
            M=M+1
            	//push constant 0
            @0
            D=A 
            @SP 
            A=M 
            M=D
            @SP 
            M=M+1
            
            //	//push local 0
            @0
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
            
            //	//push local 1
            @1
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
             // add
        @SP
        M=M-1 
        A=M
        D=M 
        @SP
        A=M-1
        M=D+M
        
           //NOT
           @SP
           A=M-1 // on décrémente pas car on change juste y en -y on ne l'enleve pas
           M=!M
           
            //	//push argument 0
            @0
            D=A
            @ARG
            A=M
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
        A=M-1
        M=D+M
        
            //	//push argument 1
            @1
            D=A
            @ARG
            A=M
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
        D=M // d=3
        @SP
        A=M-1
        M=M-D
        	//return
        @LCL
        D=M  // ca recupere l'adresse indiquée dans LCL (1ere valeur locale / savedFrame+1)

@endFrame
M=D

@5
D=A
@endFrame
D=M-D           // On  cherche l'indice 5 cases au dessus de endFrame
@retAddr        // On le stocke dans une autre variable temp
M=D

        //	//pop argument 0
        @0
        D=A
        @ARG
        A=M
        D=D+A
        @ARG
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D
        @0
        D=A
        @ARG
        A=M
        D=A-D
        @ARG
        M=D
        "
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
