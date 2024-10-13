class popcommand:
    def asm(self, command):
        """No comment"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'local':
                return self._commandpoplocal(command)
            case 'this':
                return self._commandpopthis(command)
            case 'that':
                return self._commandpopthat(command)
            case 'argument':
                return self._commandpoparg(command)
            case _:
                print(f'SyntaxError: Unknown segment {segment} in command: {command}')
                exit()

    def _commandpoplocal(self, command):
        parameter = command['parameter']
        return f"""
        //\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @LCL
        D=D+M
        @13
        M=D // ram(13)sert a stocker adrr
        @SP
        AM=M-1
        D=M
        @13
        A=M
        M=D // ram(adrr) =ram(sp)
        """
    def _commandpopthis(self, command):
        parameter = command['parameter']
        return f"""
        //\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @THIS
        D=D+M
        @13
        M=D // ram(13)sert a stocker adrr
        @SP
        AM=M-1
        D=M
        @13
        A=M
        M=D // ram(adrr) =ram(sp)
        """
    def _commandpopthat(self, command):
        parameter = command['parameter']
        return f"""
        //\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @THIS
        D=D+M
        @13
        M=D // ram(13)sert a stocker adrr
        @SP
        AM=M-1
        D=M
        @13
        A=M
        M=D // ram(adrr) =ram(sp)
        """
    def _commandpoparg(self, command):
        parameter = command['parameter']
        return f"""
        //\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @ARG
        D=D+M
        @13
        M=D // ram(13)sert a stocker adrr
        @SP
        AM=M-1
        D=M
        @13
        A=M
        M=D // ram(adrr) =ram(sp)
        """
