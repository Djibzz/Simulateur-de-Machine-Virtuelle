// Bootstrap
    @5
    // pas oublier de remettre a 256
    D=A
    @SP
    M=D
	//Call Sys.init 0
    Code assembleur de {'type': 'Call', 'function': 'Sys.init', 'parameter': '0'}


//code de test/test.vm
	//push constant 7
        @7
        D=A 
        @SP 
        A=M 
        M=D
        @SP 
        M=M+1
        	//push constant 2
        @2
        D=A 
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
        	//push constant 27
        @27
        D=A 
        @SP 
        A=M 
        M=D
        @SP 
        M=M+1
        	//push constant 8
        @8
        D=A 
        @SP 
        A=M 
        M=D
        @SP 
        M=M+1
        