import sys
import Lexer


class ParserXML:
    """No comment"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.xml = open(file[0:-5] + ".xml", "w")
        self.xml.write('<?xml version="1.0" encoding="UTF-8"?>')

    def jackclass(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.xml.write(f"""<class>\n""")
        self.process('class')
        self.className()
        self.process('{')
        while self.lexer.hasNext()and self.lexer.look()['token'] in {'static','field'}:
            self.classVarDec()
        while self.check('token',{'constructor', 'function','method'}):
            self.subroutineDec()
        self.process('}')
        self.xml.write(f"""</class>\n""")

    def classVarDec(self):
        """
        classVarDec: ('static'| 'field') type varName (',' varName)* ';'
        """
        self.xml.write(f"""<classVarDec>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in {'static','field'}:
            token =self.lexer.next()['token']
            self.xml.write(f"""{token}""")
        else:
            self.error(self.lexer.next())
            print("error Vardec")
        self.type()
        self.varName()
        while self.lexer.hasNext() and self.lexer.look()['token']==",":
            self.process(',')
            self.varName()
        self.process(';')
        self.xml.write(f"""</classVarDec>\n""")

    def type(self):
        """
        type: 'int'|'char'|'boolean'|className
        """
        self.xml.write(f"""<type>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in {'int','char','boolean'}:
            token =self.lexer.next()['token']
            self.xml.write(f"""{token}""")
        elif self.check('type','identifier'):
            self.className()
        else:
            self.className()
            print("error Type")
            self.error(self.lexer.next())
        self.xml.write(f"""</type>\n""")

    def subroutineDec(self):
        """
        subroutineDec: ('constructor'| 'function'|'method') ('void'|type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        self.xml.write(f"""<subroutineDec>\n""")
        if self.check('token',{'constructor', 'function','method'}):
            token =self.lexer.next()['token']
            self.xml.write(f"""<keyword>{token}</keyword>""")
            if  token != 'constructor' and self.check('type','keyword'):
                self.xml.write(f"""<keyword>{self.lexer.next()['token']}</keyword>""")
            else:
                self.className()
            self.subroutineName()
            self.parameterList()
            self.subroutineBody()
        else:
            self.error(self.lexer.next())
        self.xml.write(f"""</subroutineDec>\n""")

    def parameterList(self):
        """
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.process('(')
        self.xml.write(f"""<parameterList>\n""")

        while not self.check('token',')'):
            if self.check('type',{'keyword','identifier'}):
                self.type()
                self.varName()
                if self.check('token',','):
                    self.process(',')
                else:
                    self.error(self.lexer.next())

        self.xml.write(f"""</parameterList>\n""")
        self.process(')')

    def subroutineBody(self):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.process('{')
        self.xml.write(f"""<subroutineBody>\n""")
        while  not self.check('token','}'):
            self.varDec()

        self.xml.write(f"""</subroutineBody>\n""")
        self.process('}')

    def varDec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.xml.write(f"""<varDec>\n""")
        if self.check('token',{'var'}):
            token =self.lexer.next()['token']
            self.xml.write(f"""<keyword>{token}</keyword>""")
            self.type()
            self.varName()
            while  self.check('token',','):
                self.process(',')
                self.varName()
            self.process(';')
        self.xml.write(f"""</varDec>\n""")

    def className(self):
        """
        className: identifier
        """
        self.xml.write(f"""<className>""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            token = self.lexer.next()
            self.xml.write(token['token'])
        else:
            print("error  Class Name")
            self.error(self.lexer.next())
        self.xml.write(f"""</className>""")

    def subroutineName(self):
        """
        subroutineName: identifier
        """
        self.xml.write(f"""<subroutineName>""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            token = self.lexer.next()
            self.xml.write(token['token'])
        else:
            print("error  subroutine Name")
            self.error(self.lexer.next())
        self.xml.write(f"""</subroutineName>""")

    def varName(self):
        """
        varName: identifier
        """

        self.xml.write(f"""<varName>\n""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            token = self.lexer.next()
            self.xml.write(token['token'])
        else:
            self.error(self.lexer.next())
        self.xml.write(f"""</varName>\n""")

    def statements(self):
        """
        statements : statements*
        """
        self.xml.write(f"""<statements>\n""")
        token = self.lexer.next()['token']
        if self.lexer.hasNext()and self.lexer.look()['token'] in {'let','if','while','do','return'}:
            self.statement()
        self.xml.write(f"""</statements>\n""")

    def statement(self):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """
        self.xml.write(f"""<statement>\n""")
        token = self.lexer.next()['token']
        match token:
            # Faire une fonction par type de commande
            case 'let':
                self.xml.write(token['token'])
                self.letStatement()
            case 'if':
                 self.xml.write(token['token'])
                 self.ifStatement()
            case 'while':
                 self.xml.write(token['token'])
                 self.whileStatement()
            case 'return':
                 self.xml.write(token['token'])
                 self.returnStatement()
            case 'do':
                 self.xml.write(token['token'])
                 self.doStatement()
        self.xml.write(f"""</statement>\n""")

    def letStatement(self):
        """
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.xml.write(f"""<letStatement>\n""")
        self.varName()
        if self.check('token','['):
            self.process('[')
            self.expression()
            self.process(']')
        self.process('=')
        self.expression()
        self.process(';')
        self.xml.write(f"""</letStatement>\n""")

    def ifStatement(self):
        """
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.xml.write(f"""<ifStatement>\n""")
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')
        if self.check('token','else'):
            self.xml.write(self.lexer.next()['token'])
            self.process('{')
            self.statements()
            self.process('}')
        self.xml.write(f"""</ifStatement>\n""")

    def whileStatement(self):
        """
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        self.xml.write(f"""<whileStatement>\n""")
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')
        self.xml.write(f"""</whileStatement>\n""")

    def doStatement(self):
        """
        doStatement : 'do' subroutineCall ';'
        """
        self.xml.write(f"""<doStatement>\n""")
        self.subroutineCall()
        self.process(';')

        self.xml.write(f"""</doStatement>\n""")

    def returnStatement(self):
        """
        returnStatement : 'return' expression? ';'
        """
        self.xml.write(f"""<returnStatement>\n""")
        if not self.check('token',';'):
            self.expression()
        self.xml.write(f"""</returnStatement>\n""")

    def expression(self):
        """
        expression : term (op term)*
        """
        self.xml.write(f"""<expression>\n""")
        """todo"""
        self.xml.write(f"""</expression>\n""")

    def term(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        self.xml.write(f"""<term>\n""")
        """todo"""
        self.xml.write(f"""</term>\n""")

    def subroutineCall(self):
        """
        subroutineCall : subroutineName '(' expressionList ')'
                | (className|varName) '.' subroutineName '(' expressionList ')'
        Attention : l'analyse syntaxique ne peut pas distingué className et varName.
            Nous utiliserons la balise <classvarName> pour (className|varName)
        """
        self.xml.write(f"""<subroutineCall>\n""")
        """todo"""
        self.xml.write(f"""</subroutineCall>\n""")

    def expressionList(self):
        """
        expressionList : (expression (',' expression)*)?
        """
        self.xml.write(f"""<expressionList>\n""")
        """todo"""
        self.xml.write(f"""</expressionList>\n""")

    def op(self):
        """
        op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        self.xml.write(f"""<op>\n""")
        """todo"""
        self.xml.write(f"""</op>\n""")

    def unaryOp(self):
        """
        unaryop : '-'|'~'
        """
        self.xml.write(f"""<unaryop>\n""")
        """todo"""
        self.xml.write(f"""</unaryop>\n""")

    def KeywordConstant(self):
        """
        KeyWordConstant : 'true'|'false'|'null'|'this'
        """
        self.xml.write(f"""<KeyWordConstant>\n""")
        """todo"""
        self.xml.write(f"""</KeyWordConstant>\n""")

    def check(self,attribute, value):
        return self.lexer.hasNext() and self.lexer.look()[f'{attribute}'] in value

    def process(self, str):
        token = self.lexer.next()
        if (token is not None and token['token'] == str):
            self.xml.write(f"""<{token['type']}>{token['token']}</{token['type']}>\n""")
        else:
            self.error(token)
            print("error process")

    def error(self, token):
        if token is None:
            print("Syntax error: end of file")
        else:
            print(f"SyntaxError (line={token['line']}, col={token['col']}): {token['token']}")
        exit()


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = ParserXML(file)
    parser.jackclass()
    print('-----fin')
