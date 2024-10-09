"""No comment"""

import sys
import Parser


class Generator:
    """No com"""

    def __init__(self, file=None):
        """ Cette fonction va prendre un fichier non vide et le parser(transformer ce code en langage)"""
        if file is not None:
            self.parser = Parser.Parser(file)

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
            case _:
                print(f'SyntaxError : {command}')
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
