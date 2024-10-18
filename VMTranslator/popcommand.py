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
                return self._commandpoplocal(command)
            case 'that':
                return self._commandpoplocal(command)
            case 'argument':
                return self._commandpoplocal(command)
            case 'static':
                return self._commandpopstatic(command)
            case 'pointer':
                return self._commandpoppointer(command)
            case 'temp':
                return self._commandpoptemp(command)
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
    def _commandpoptemp(self,command):
        par= command['parameter']
        parameter = int(command['parameter']) + 5
        parameter = str(parameter)
        return f"""//\t//{command['type']} {command['segment']} {par}
                @SP
                M=M-1
                A=M
                D=M
                @{parameter}
                M=D
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
    def _commandpoppointer(self,command):
        parameter = command['parameter']
        dic = {'this': 'THIS', 'that': 'THAT'}
        if parameter =='0':
            seg=dic['this']
        else:
            seg=dic['that']
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        A=M
        D=M
        @{seg}
        M=D
        """