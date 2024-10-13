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
            case 'static':
                return self._commandpopstatic(command)
            #case 'temp':
                #return self._commandpoptemp(command)
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
        @{parameter}
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
            @{parameter}
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
        @{parameter}
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
                @{parameter}
                D=A
                @{seg}
                A=M
                D=A-D
                @{seg}
                M=D
                """
    def _commandpoptemp(self,command):
        parameter = command['parameter'] + str(5)
        return f"""//\t//{command['type']} {command['segment']} {parameter}
                @{parameter}
                D=A
                @5
                D=D+M // addr = ram(5)+1
                @SP
                M=M-1
                A=M
                // à finir de coder
                """
    def _commandpopstatic(self,command):
        parameter = command['parameter']
        return f"""//\t//{command['type']} {command['segment']} {parameter}
                @SP
                M=M-1
                A=M // a = ram(sp) avec sp--
                D=M  // D= ram(ram(sp))
                @Foo.{parameter}
                M=D // ram(Foo.i)= ram(ram(sp))
                """