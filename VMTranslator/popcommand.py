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
        segment = command['segment']
        dic ={'this':'THIS','local':'LCL','argument':'ARG','that':'THAT'}
        seg=dic[segment]
        return f"""
        //\t//{command['type']} {command['segment']} {parameter}
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
        @1
        D=A
        @{seg}
        A=M
        D=A-D
        @{seg}
        M=D
        """
    def _commandpopthis(self, command):
        parameter = command['parameter']
        segment = command['segment']
        dic = {'this': 'THIS', 'local': 'LCL', 'argument': 'ARG', 'that': 'THAT'}
        seg = dic[segment]
        return f"""
                //\t//{command['type']} {command['segment']} {parameter}
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
                @1
                D=A
                @{seg}
                A=M
                D=A-D
                @{seg}
                M=D
                """
    def _commandpopthat(self, command):
        parameter = command['parameter']
        segment = command['segment']
        dic = {'this': 'THIS', 'local': 'LCL', 'argument': 'ARG', 'that': 'THAT'}
        seg = dic[segment]
        return f"""
                //\t//{command['type']} {command['segment']} {parameter}
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
                @1
                D=A
                @{seg}
                A=M
                D=A-D
                @{seg}
                M=D
                """
    def _commandpoparg(self, command):
        parameter = command['parameter']
        segment = command['segment']
        dic = {'this': 'THIS', 'local': 'LCL', 'argument': 'ARG', 'that': 'THAT'}
        seg = dic[segment]
        return f"""
                //\t//{command['type']} {command['segment']} {parameter}
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
                @1
                D=A
                @{seg}
                A=M
                D=A-D
                @{seg}
                M=D
                """
