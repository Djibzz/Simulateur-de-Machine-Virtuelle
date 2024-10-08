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
        return f"""
        @SP
        M=M-1 
        A=M
        D=M 
        @SP
        A=M-1
        M=D+M
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
