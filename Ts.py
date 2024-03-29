'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

from Tag import Tag
from Token import Token


class Ts:

    def __init__(self):
        self.ts = {}

        self.ts['class'] = Token(Tag.KW_CLASS, 'class', 1, 1)
        self.ts['end'] = Token(Tag.KW_END, 'end', 1, 1)
        self.ts['def'] = Token(Tag.KW_DEF, 'def', 1, 1)
        self.ts['return'] = Token(Tag.KW_RETURN, 'return', 1, 1)
        self.ts['defstatic'] = Token(Tag.KW_DEFSTATIC, 'defstatic', 1, 1)
        self.ts['void'] = Token(Tag.KW_VOID, 'void', 1, 1)
        self.ts['main'] = Token(Tag.KW_MAIN, 'main', 1, 1)
        self.ts['String'] = Token(Tag.KW_STRING, 'String', 1, 1)
        self.ts['bool'] = Token(Tag.KW_BOOL, 'bool', 1, 1)
        self.ts['integer'] = Token(Tag.KW_INTEGER, 'integer', 1, 1)
        self.ts['double'] = Token(Tag.KW_DOUBLE, 'double', 1, 1)
        self.ts['if'] = Token(Tag.KW_IF, 'if', 1, 1)
        self.ts['else'] = Token(Tag.KW_ELSE, 'else', 1, 1)
        self.ts['while'] = Token(Tag.KW_WHILE, 'while', 1, 1)
        self.ts['write'] = Token(Tag.KW_WRITE, 'write', 1, 1)
        self.ts['true'] = Token(Tag.KW_TRUE, 'true', 1, 1)
        self.ts['false'] = Token(Tag.KW_FALSE, 'false', 1, 1)
        self.ts['or'] = Token(Tag.KW_OR, 'or', 1, 1)
        self.ts['and'] = Token(Tag.KW_AND, 'and', 1, 1)

    def getToken(self, lexema):
        token = self.ts.get(lexema)
        return token

    def addToken(self, lexema, token):
        self.ts[lexema] = token

    def removeToken(self, lexema):
        self.ts.pop(lexema)

    def printTs(self):
        for k, t in (self.ts.items()):
            print('{}: {}'.format(k, t.toString()))

    def setTipo(self, lexema, tipo):
        self.getToken(lexema).setTipo(tipo)

    def getTipo(self, lexema):
        return self.getToken(lexema).getTipo()