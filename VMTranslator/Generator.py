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
        self.cpt = 0
        self.classname = 'Foo'
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
            #        Function|Call|

            match type:
                # Faire une fonction par type de commande
                case 'push':
                    return self.pushcommand.asm(command)
                case 'pop':
                    return self.popcommand.asm(command)
                case 'Call':
                    return self._commandcall(command)
                case 'return':
                    return self._commandreturn(command)
                case 'Function':
                    return self._commandfunction(command)
                case 'add'|'sub'|'eq'|'neg'|'gt'|'lt':
                    return self.arithcommand.asm(command)
                case 'or'|'and'|'not':
                    return self.logiccommand.asm(command)
                case'label'|'goto'|'if-goto':
                    return self.branchingcommand.asm(command)
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandcall(self, command):
        """No comment"""
        self.cpt += 1
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    @{command['function']}$RETADRR{self.cpt}
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

    def _commandreturn(self,command):
        return f"""\t//{command['type']}
        @LCL
        D=M  // ca recupere l'adresse indiquée dans LCL (1ere valeur locale / savedFrame+1)

@endFrame
M=D

@5
D=A
@endFrame
D=M-D           // On  cherche l'indice 5 cases au dessus de endFrame
@retAddr        // On le stocke dans une autre variable temp
M=D
""" + self.popcommand.asm({'type': 'pop', 'segment': 'argument', 'parameter': '0'})+ """"
 //  on return la valeur de la fonction , on réplace les pointers de la frame précédente

@ARG
D=M+1
@SP
M=D

@endFrame
A=M
A=A-1           
D=M
@THAT
M=D             // THAT restored

@2
D=A
@endFrame
A=M 
A=A-D           
D=M
@THIS
M=D             // THIS restored 
        
  
@3
D=A
@endFrame
A=M
A=A-D           
D=M
@ARG            // ARG restored
M=D

@4
D=A 
@endFrame 
A=M 
A=A-D       
D=M
@LCL           // LCL restored 
M=D

@retAddr
A=M
A=M
0;JMP
"""


    def _commandfunction(self,command):
        """Ne marche avec les noms qui comprennent des caractères spéciaux"""
        parametre = command['parameter']
        function = command['function']
        initia = f"// On initialise {parametre} variables locales\n"

        for i in range(0, int(parametre)):
            initia = initia + self.pushcommand.asm({'type': 'push', 'segment': 'constant', 'parameter': '0'})

        return (f"""\t // {command['type']} {command['function']} {command['parameter']} """+
                self.branchingcommand.asm({'type': 'label', 'label': function}) + initia)


if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')
