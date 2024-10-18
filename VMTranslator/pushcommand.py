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
                 return self._commandpushlocal(command)
            case 'that':
                 return self._commandpushlocal(command)
            case 'argument':
                return self._commandpushlocal(command)
            case 'temp':
                return self._commandpushtemp(command)
            case 'static':
                return self._commandpushstatic(command)
            case 'pointer':
                return self._commandpushpointer(command)
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
            A=D
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """

    def _commandpushtemp(self, command):
        par = command['parameter']
        parameter = int(command['parameter'])+5
        parameter=str(parameter)
        return f"""//\t//{command['type']} {command['segment']} {par}
            @{parameter}
            D=M // addr = ram(5+1)
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
    def _commandpushstatic(self, command):
        parameter = command['parameter']
        return f"""//\t//{command['type']} {command['segment']} {parameter}
            @Foo.{parameter} // a corriger plus 
            D=M
            @SP
            A=M // a= ram(sp)
            M=D // ram(ram(sp))=foo.i
            @SP
            M=M+1
            """
    def _commandpushpointer(self,command):
        parameter = command['parameter']
        dic = {'this': 'THIS', 'that': 'THAT'}
        if parameter == '0':
            seg = dic['this']
        else:
            seg = dic['that']
        return f"""\t//{command['type']} {command['segment']} {parameter}
                @{seg}
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """