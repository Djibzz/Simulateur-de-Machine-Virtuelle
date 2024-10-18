class logiccommand:
    def asm(self,command):
        match command['type']:
            case 'and':
                return self._commandAnd(command)
            case'or':
                return self._commandOr(command)
            case'not':
                return self._commandNot(command)

    def _commandAnd(self, command):
        return f"""
           //AND
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           M=D&M
           """

    def _commandOr(self, command):
        return f"""
           //OR
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           M=D|M
           """

    def _commandNot(self, command):
        return f"""
           //NOT
           @SP
           A=M-1 // on décrémente pas car on change juste y en -y on ne l'enleve pas
           M=!M
           """