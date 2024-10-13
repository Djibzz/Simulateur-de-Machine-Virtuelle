class pushcommand:
    def asm(self, command):
        """No comment"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'constant':
                return self._commandpushconstant(command)
            case 'local':
                 return self._commandpushlocal(command)
            case 'this':
                 return self._commandpushthis(command)
            case 'that':
                 return self._commandpushthat(command)
            case 'argument':
                return self._commandpusharg(command)
            case _:
                print(f'SyntaxError: Unknown segment {segment} in command: {command}')
                exit()

    def _commandpushconstant(self, command):
            """No comment"""
            parameter = command['parameter']
            return f"""\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A 
            @SP 
            A=M 
            M=D
            @SP 
            M=M+1
            """

    def _commandpushlocal(self, command):
            parameter = command['parameter']
            return f"""
            //\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A
            @LCL
            D=D+M
            @SP
            A=M
            A=M
            M=D
            @SP
            M=M+1
            """

    def _commandpushthat(self, command):
            parameter = command['parameter']
            return f"""//\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A
            @THAT
            D=D+M
            @SP
            A=M
            A=M
            M=D
            @SP
            M=M+1
            """

    def _commandpushthis(self, command):
            parameter = command['parameter']
            return f"""//\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A
            @THIS
            D=D+M
            @SP
            A=M
            A=M
            M=D
            @SP
            M=M+1
            """

    def _commandpusharg(self, command):
            parameter = command['parameter']
            return f"""//\t//{command['type']} {command['segment']} {parameter}
            @{parameter}
            D=A
            @ARG
            D=D+M
            @SP
            A=M
            A=M
            M=D
            @SP
            M=M+1
            """