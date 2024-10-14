class arithcommand:
    def __init__(self):
        self.cpt = 0
        self.classname='Foo'
    def asm(self,command):
        match command['type']:
            case'add':
                return self._commandadd(command)
            case'sub':
                return self._commandsub(command)
            case 'neg':
                return self._commandneg(command)
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
    def _commandneg(self,command):
        return f"""//neg
                @SP
                M=M-1
                A=M
                M=-M
                """
    def _commandEQ(self,command):
        self.cpt += 1
        return f""" // EQ
        @SP
        A=M-1
        D=M
        A=A-1
        D=D-M
        @{self.classname}$IF{self.cpt}
        D;JEQ
        D=0
        @END
        0;JMP
        ({self.classname}$IF{self.cpt})
        D=-1
        (END)
        @SP
        M=M-1
        A=M-1
        M=D
        """
    def _commandGT(self,command):
        self.cpt += 1
        return f"""
        //GT
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        D=M-D // ram(x)
        M=-1  //on met a true de  base
        @{self.classname}$GT{self.cpt}
        D;JGT // si le reste de x-y est superieur a 0 alors x>y et on skip le code
        @SP
        A=M-1
        M=0
        ({self.classname}$GT{self.cpt})
        """
    def _commandLT(self,command):
        self.cpt += 1
        return f"""
        //LT
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        D=M-D
        M=-1
        @{self.classname}$LT{self.cpt}
        D;JLT// si le reste de x-y est inferieur a 0 alors x<y et on skip le code
        @SP
        A=M-1
        M=0
        ({self.classname}$LT{self.cpt})
        """