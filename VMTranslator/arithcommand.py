class arithcommand:
    def asm(self,command):
        match command['type']:
            case'add':
                return self._commandadd(command)
            case'sub':
                return self._commandsub(command)
            case'eq':
                return self._commandEQ(command)
            case'gt':
                return self._commandGT(command)
            case 'lt':
                return self._commandLT(command)
    def _commandadd(self, command):
        return f""" // add
        @SP
        M=M-1 
        A=M
        D=M 
        @SP
        A=M-1
        M=D+M
        """
    def _commandsub(self,command):
        return f""" // sub
        @SP
        M=M-1 
        A=M
        D=M // d=3
        @SP
        A=M-1
        M=M-D
        """
    def _commandEQ(self,command):
        return f"""" // EQ
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
        """
    def _commandGT(self,command):
        return f"""
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
        """
    def _commandLT(self,command):
        return f"""
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
        """