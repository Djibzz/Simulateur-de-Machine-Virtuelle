"""No comment"""

import sys
import Parser
import branchingcommand
import logiccommand
import arithcommand


class Generator:
    """No com"""

    def __init__(self, file=None):
        """ Cette fonction va prendre un fichier non vide et le parser(transformer ce code en langage)"""
        if file is not None:
            self.parser = Parser.Parser(file)
        self.branchingcommand = branchingcommand.BranchingCommand()
        self.logiccommand = logiccommand.logiccommand()
        self.arithcommand = arithcommand.arithcommand()
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
                    return self.arithcommand.asm(command)
                case 'sub':
                    return self.arithcommand.asm(command)
                case 'eq':
                    return self.arithcommand.asm(command)
                case 'gt':
                    return self.arithcommand.asm(command)
                case 'lt':
                    return self.arithcommand.asm(command)
                case 'or':
                    return self.logiccommand.asm(command)
                case 'and':
                    return self.logiccommand.asm(command)
                case 'not':
                    return self.logiccommand.asm(command)
                case'label':
                    return self.branchingcommand.asm(command)
                case 'goto':
                    return self.branchingcommand.asm(command)
                case 'if-goto':
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
