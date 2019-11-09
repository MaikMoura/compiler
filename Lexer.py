'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

import sys

from lexer.Ts import Ts
from lexer.Tag import Tag
from lexer.Token import Token


class Lexer():

    def __init__(self, file):
        try:
            self.file = open(file,'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 0
            self.ts = Ts()
            self.erros = [] #Modo Pânico
        except IOError:
            print('Erro ao abrir o arquivo.')
            sys.exit(0)

    def fecharArquivo(self):
        try:
            self.file.close()
        except IOError:
            print('Erro ao fechar o arquivo')
            sys.exit(0)

    def sinalizarErroLexico(self, message):
        self.erros.append('[Erro Lexico]: {}'.format(message))

    def imprimirErros(self):
        for e in self.erros:
            print(e)

    def retornarPonteiro(self):
        if (self.lookahead.decode('ascii') != ''):
            self.file.seek(self.file.tell() - 1)
            self.n_column -= 1

    def imprimirTs(self):
        self.ts.printTs()

    def proximoToken(self):
        estado = 1
        lexema = ''
        c = '\u0000'

        while (True):
            self.lookahead = self.file.read(1)
            self.n_column += 1
            c = self.lookahead.decode('ascii')

            # Modo Pânico
            if (len(self.erros) == 5):
                return None

            if (estado == 1):
                if (c == ''):
                    return Token(Tag.EOF,'EOF', self.n_line, self.n_column)
                elif (c in ('\n')):
                    self.n_line += 1
                    self.n_column = 0
                    estado = 1
                elif (c in (' ', '\t', '\r')):
                    estado = 1
                elif (c == '-'):
                    lexema += c
                    estado = 2
                elif (c == '+'):
                    #Estado 3
                    return Token(Tag.OP_ADD, '+', self.n_line, self.n_column)
                elif (c == '*'):
                    #Estado 4
                    return Token(Tag.OP_MULT, '*', self.n_line, self.n_column)
                elif (c == '('):
                    #Estado 5
                    return Token(Tag.KW_OPN_PARENTH,'(', self.n_line, self.n_column)
                elif (c == ')'):
                    #Estado 6
                    return Token(Tag.KW_CLS_PARENTH, ')', self.n_line, self.n_column)
                elif (c == ';'):
                    # Estado 7
                    return Token(Tag.KW_SCORE_COMMA, ';', self.n_line, self.n_column)
                elif (c == ':'):
                    #Estado 8
                    return Token(Tag.KW_DBL_SCORE, ':', self.n_line, self.n_column)
                elif (c == ','):
                    #Estado 9
                    return Token(Tag.KW_COMMA, ',', self.n_line, self.n_column)
                elif (c == '='):
                    estado = 10
                elif (c == '!'):
                    estado = 13
                elif (c == '<'):
                    estado = 16
                elif (c == '>'):
                    estado = 19
                elif (c == '['):
                    return Token(Tag.KW_OPN_MATTR, '[', self.n_line, self.n_column)
                elif (c == ']'):
                    return Token(Tag.KW_CLS_MATTR, ']', self.n_line, self.n_column)
                elif (c == '.'):
                    return Token(Tag.KW_SCORE, '.', self.n_line, self.n_column)
                elif (c.isalpha()):
                    lexema += c
                    estado = 25
                elif (c == '"'):
                    lexema += c
                    estado = 27
                elif (c.isdigit()):
                    lexema += c
                    estado = 30
                elif (c == '#'):
                    estado = 35
                elif (c == '/'):
                    return Token(Tag.OP_DIV, '/', self.n_line, self.n_column)
                else:
                    self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                                            str(self.n_line) + ' e coluna ' + str(self.n_column))
                    return Token(Tag.ERROR, 'Erro', 0, 0)
            elif (estado == 2):
                if (c == '-'):
                    return Token(Tag.OP_UNAR, '--', self.n_line, self.n_column)
                else:
                    self.retornarPonteiro()
                    return Token(Tag.OP_SUB, '-', self.n_line, self.n_column)
            elif (estado == 10):
                if (c == '='):
                    #Estado 11
                    return Token(Tag.OP_EQ, '==', self.n_line, self.n_column)
                else:
                    #Estado 12
                    self.retornarPonteiro()
                    return Token(Tag.OP_ATR, '=', self.n_line, self.n_column)
            elif (estado == 13):
                if (c == '='):
                    #Estado 14
                    return Token(Tag.OP_NE, '!=', self.n_line, self.n_column)
                else:
                    #Estado 15
                    self.retornarPonteiro()
                    return Token(Tag.OP_NOT, '!', self.n_line, self.n_column)
            elif (estado == 16):
                if (c == '='):
                    #Estado 17
                    return Token(Tag.OP_LTE, '<=', self.n_line, self.n_column)
                else:
                    #Estado 18
                    self.retornarPonteiro()
                    return Token(Tag.OP_LT, '<', self.n_line, self.n_column)
            elif (estado == 19):
                if (c == '='):
                    #Estado 20
                    return Token(Tag.OP_GTE, '>=', self.n_line, self.n_column)
                else:
                    #Estado 21
                    self.retornarPonteiro()
                    return Token(Tag.OP_GT, '>', self.n_line, self.n_column)
            elif (estado == 25):
                if (c.isalnum() or c == '_'):
                    lexema += c
                else:
                    #Estado 26
                    self.retornarPonteiro()
                    token = self.ts.getToken(lexema)
                    if (token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    else:
                        self.ts.getToken(lexema).linha = self.n_line
                        self.ts.getToken(lexema).coluna = self.n_column
                    return token
            elif (estado == 27):
                if (len(lexema) == 1 and c == '"'):
                    self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                                             str(self.n_line) + ' e coluna ' + str(self.n_column) +
                                             ' String vazia nao permitido')
                    lexema = ''
                elif (len(lexema) > 1 and c == '"'):
                    # Estado 29
                    lexema += c
                    return Token(Tag.STRING, lexema, self.n_line, self.n_column)
                elif (c == '\n'):
                    self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                                             str(self.n_line) + ' e coluna ' + str(self.n_column) +
                                             ' Nao eh possivel quebrar linha ou finalizar arquivo antes de fechar a String')
                    self.n_line += 1
                    self.n_column = 0
                elif (c == ''):
                    self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                                            str(self.n_line) + ' e coluna ' + str(self.n_column)
                                            + ' EOF encontrado antes de fechar String')
                else:
                    lexema += c
            elif (estado == 30):
                if (c.isdigit()):
                    lexema += c
                elif (c == '.'):
                    lexema += c
                    estado = 32
                else:
                    #Estado 31
                    self.retornarPonteiro()
                    return Token(Tag.INT, lexema, self.n_line, self.n_column)
            elif (estado == 32):
                if (c.isdigit()):
                    lexema += c
                    estado = 33
                else:
                    self.retornarPonteiro()
                    self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                                str(self.n_line) + ' e coluna ' + str(self.n_column))
            elif (estado == 33):
                if (c.isdigit() == False):
                    #Estado 34
                    self.retornarPonteiro()
                    return Token(Tag.DOUBLE, lexema, self.n_line, self.n_column)
                else:
                    lexema += c
            elif (estado == 35):
                if (c == '\n'):
                    estado = 1
                    self.n_line += 1
                    self.n_column = 0
            else:
                self.sinalizarErroLexico('Caractere invalido [' + c + '] na linha ' +
                            str(self.n_line) + ' e coluna ' + str(self.n_column))