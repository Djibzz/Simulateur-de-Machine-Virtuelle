class BranchingCommand:
    def asm(self,command):
        match command['type']:
            case 'label':
                return self._commandlabel(command)
            case 'goto':
                return self._commandgoto(command)
            case 'if-goto':
                return self._commandifgoto(command)


    def _commandlabel(self, command):
        return f""" //label {command['label']}
        ({command['label']})
        """


    def _commandgoto(self, command):
        return f""" //goto {command['label']}
        @{command['label']}
        0;JMP
        """


    def _commandifgoto(self, command):
        return f""" //if goto {command['label']}
        @SP
        AM=M-1
        D=M
        @{command['label']}
        D;JNE
        """