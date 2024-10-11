"""No comment"""

import sys
import Parser
import branchingcommand


class Generator:
    """No com"""

    def __init__(self, file=None):
        """ Cette fonction va prendre un fichier non vide et le parser(transformer ce code en langage)"""
        if file is not None:
            self.parser = Parser.Parser(file)
        self.branchingcommand = branchingcommand.BranchingCommand()
    def __iter__(self):
        return self

    def __next__(self):
        if self.parser is not None and self.parser.hasNext():
            return self._next()
        else:
            raise StopIteration

    def _next(self):
        # No comment
        command = self.parser.next()
        if command is None:
            return None
        else:
            type = command['type']
            # type = push|pop|
            #        add|sub|neg|eq|gt|lt|and|or|not) |
            #        label|goto|if-goto|
            #        Function|Call|return

            match type:
                # Faire une fonction par type de commande
                case 'push':
                    return self._commandpush(command)
                case 'pop':
                    return self._commandpop(command)
                case 'Call':
                    return self.commandcall(command)
                case 'add':
                    return self._commandadd(command)
                case 'sub':
                    return self._commandsub(command)
                case 'eq':
                    return self._commandEQ(command)
                case 'gt':
                    return self._commandGT(command)
                case 'lt':
                    return self._commandLT(command)
                case'label':
                    return self.branchingcommand.asm(command)
                case 'goto':
                    return self.branchingcommand.asm(command)
                case 'ifgoto':
                    return self.branchingcommand.asm(command)
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandpush(self, command):
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
    def _commandpop(self, command):
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
        return f"""" 
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
    def _commandAnd(self,command):
        return f"""
        //AND
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M&&D
        """
    def _commandOr(self,command):
        return f"""
        //OR
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M||D
        """
    def _commandNot(self,command):
        return f"""
        //NOT
        @SP
        A=M-1 // on décrémente pas car on change juste y en -y on ne l'enleve pas
        M=!M
        """
    def _commandlabel(self,command):
        return f""" //label {command['label']}
        ({command['label']})
        """
    def _commandgoto(self,command):
        return f""" //goto {command['label']}
        @{command['label']}
        0;JMP
        """
    def _commandifgoto(self,command):
        return f""" //if goto {command['label']}
        @SP
        AM=M-1
        D=M
        @{command['label']}
        D;JNE
        """

    def _commandcall(self, command):
        """No comment"""
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n"""


if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')
