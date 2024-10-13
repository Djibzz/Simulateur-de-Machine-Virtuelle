"""No comment"""

import sys
import Parser
import branchingcommand
import logiccommand
import arithcommand
import pushcommand
import popcommand


class Generator:
    """No com"""

    def __init__(self, file=None):
        """ Cette fonction va prendre un fichier non vide et le parser(transformer ce code en langage)"""
        if file is not None:
            self.parser = Parser.Parser(file)
        self.branchingcommand = branchingcommand.BranchingCommand()
        self.logiccommand = logiccommand.logiccommand()
        self.arithcommand = arithcommand.arithcommand()
        self.pushcommand = pushcommand.pushcommand()
        self.popcommand = popcommand.popcommand()
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
                    return self.pushcommand.asm(command)
                case 'pop':
                    return self.popcommand.asm(command)
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
