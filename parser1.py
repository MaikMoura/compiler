import sys

from Ts import Ts
from Tag import Tag
from Token import Token
from Lexer import Lexer

class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proximoToken()

    def sinalizaErroSintatico(self, message):
        print('[Erro Sintatico] na linha ' + str(self.token.getLinha()) + ' e coluna ' + str(self.token.getColuna()) + ': ')
        print(message, '\n')

    def advance(self):
        print('[DEBUG] token: ', self.token.toString())
        self.token = self.lexer.proximoToken()

    def skip(self, message):
        self.sinalizaErroSintatico(message)
        self.advance()

    # verifica token esperado t
    def eat(self, t):
        if(self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False

    """
    LEMBRETE:
    Todas as decisoes do Parser, sao guiadas pela Tabela Preditiva (TP)
    """
    # Programa -> CMD EOF
    def Programa(self):
        self.Classe()
        if(self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico('Esperado "EOF"; encontrado ' + '"' + self.token.getLexema() + '"')

    def Classe(self):
        # Classe -> class ID : ListaFuncao Main end .
        if(self.eat(Tag.KW_CLASS)):
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            if(not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaFuncao()
            self.Main()
            if(not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if(not self.eat(Tag.KW_SCORE)):
                self.sinalizaErroSintatico('Esperado ".", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "class", encontrado ' + '"' + self.token.getLexema() + '"')

    def DeclaraID(self):
        #DeclaraID -> TipoPrimitivo ID ;
        self.TipoPrimitivo()
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_SCORE_COMMA)):
            self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def ListaFuncao(self):
        #ListaFuncao -> ListaFuncao1
        self.ListaFuncao1()

    def ListaFuncao1(self):
        #ListaFuncao’ -> Funcao ListaFuncao’
        if(self.token.getNome() == Tag.KW_DEF):
            self.Funcao()
            self.ListaFuncao1()
        elif(self.token.getNome() != Tag.KW_DEFSTATIC):
            self.sinalizaErroSintatico('Esperado "def", encontrado ' + '"' + self.token.getLexema() + '"')

    def Funcao(self):
        #Funcao -> def TipoPrimitivo ID ( ListaArg ) : RegexDeclaraId ListaCmd Retorno end ;
        if (self.eat(Tag.KW_DEF)):
            self.TipoPrimitivo()
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaArg()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.RegexDeclaraId()
            self.ListaCmd()
            self.Retorno()
            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "def", encontrado ' + '"' + self.token.getLexema() + '"')

    def RegexDeclaraId(self):
        #RegexDeclaraId -> DeclaraID RegexDeclaraId
        if(self.token.getNome() in (Tag.KW_BOOL, Tag.KW_INTEGER, Tag.KW_STRING, Tag.KW_VOID, Tag.KW_DOUBLE)):
            self.DeclaraID()
            self.RegexDeclaraId()
        elif (self.token.getNome() not in (Tag.KW_IF, Tag.KW_WHILE, Tag.ID, Tag.KW_WRITE, Tag.KW_END, Tag.KW_RETURN)):
            self.sinalizaErroSintatico('Esperado "bool, integer, String, double, void", Encontrado ' + '"' + self.token.getLexema() + '"')

    def ListaArg(self):
        # ListaArg -> Arg ListaArg’
        self.Arg()
        self.ListaArg1()

    def ListaArg1(self):
        # ListaArg’ -> , ListaArg
        if (self.token.getNome() == Tag.KW_COMMA):
            self.ListaArg()
        elif(self.token.getNome() != Tag.KW_CLS_PARENTH):
            self.sinalizaErroSintatico('Esperado ",", encontrado ' + '"' + self.token.getLexema() + '"')

    def Arg(self):
        self.TipoPrimitivo()
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')

    def Retorno(self):
        # Retorno -> return Expressao ;
        if (self.eat(Tag.KW_RETURN)):
            self.Expressao()
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (self.token.getNome() != Tag.KW_END):
            self.sinalizaErroSintatico('Esperado "return", encontrado ' + '"' + self.token.getLexema() + '"')

    def Main(self):
        # Main -> defstatic void main ( String [ ] ID ) : RegexDeclaraId ListaCmd end ;
        if (self.eat(Tag.KW_DEFSTATIC)):
            if (not self.eat(Tag.KW_VOID)):
                self.sinalizaErroSintatico('Esperado "void", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_MAIN)):
                self.sinalizaErroSintatico('Esperado "main", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_STRING)):
                self.sinalizaErroSintatico('Esperado "String", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_OPN_MATTR)):
                self.sinalizaErroSintatico('Esperado "[", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_CLS_MATTR)):
                self.sinalizaErroSintatico('Esperado "]", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.RegexDeclaraId()
            self.ListaCmd()
            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "defstatic", encontrado ' + '"' + self.token.getLexema() + '"')

    def TipoPrimitivo(self):
        # TipoPrimitivo -> bool | integer | String | double | void
        if (not self.eat(Tag.KW_BOOL) and not self.eat(Tag.KW_INTEGER) and not self.eat(Tag.KW_STRING) and
                not self.eat(Tag.KW_DOUBLE) and not self.eat(Tag.KW_VOID)):
            self.sinalizaErroSintatico('Esperado "bool, integer, String, double, void", encontrado ' + '"' + self.token.getLexema() + '"')

    def ListaCmd(self):
        # ListaCmd -> ListaCmd’
        self.ListaCmd1()

    def ListaCmd1(self):
        # ListaCmd’ -> Cmd ListaCmd’
        if (self.token.getNome() in (Tag.KW_IF, Tag.KW_WRITE, Tag.KW_WHILE, Tag.ID)):
            self.Cmd()
            self.ListaCmd1()
        elif(self.token.getNome() not in (Tag.KW_RETURN, Tag.KW_END, Tag.KW_ELSE)):
            self.sinalizaErroSintatico('Esperado "if , write , while , id ", encontrado ' + '"' + self.token.getLexema() + '"')

    def Cmd(self):
        # Cmd -> CmdIF
        if (self.token.getNome() == Tag.KW_IF):
            self.CmdIf()
        # Cmd -> CmdWhile
        elif (self.token.getNome() == Tag.KW_WHILE):
            self.CmdWhile()
        # Cmd -> CmdWrite
        elif (self.token.getNome() == Tag.KW_WRITE):
            self.CmdWrite()
        # Cmd -> ID CmdAtribFunc
        elif (self.eat(Tag.ID)):
            self.CmdAtribFunc()
        else:
            self.sinalizaErroSintatico('Esperado "if , while , write , id", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdAtribFunc(self):
        # CmdAtribFunc -> CmdAtribui
        if (self.token.getNome() == Tag.OP_EQ):
            self.CmdAtribui()
        # CmdAtribFunc -> CmdFuncao
        elif (self.token.getNome() == Tag.KW_OPN_PARENTH):
            self.CmdFuncao()
        else:
            self.sinalizaErroSintatico('Esperado "== , (", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdIf(self):
        if(self.eat(Tag.KW_IF)):
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            self.Expressao()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaCmd()
            self.CmdIf1()
        else:
            self.sinalizaErroSintatico('Esperado "if", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdIf1(self):
        if (self.eat(Tag.KW_END)):
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (self.eat(Tag.KW_ELSE)):
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaCmd()
            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdWhile(self):
        if (not self.eat(Tag.KW_WHILE)):
            self.sinalizaErroSintatico('Esperado "while", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_OPN_PARENTH)):
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
        self.Expressao()
        if (not self.eat(Tag.KW_CLS_PARENTH)):
            self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_DBL_SCORE)):
            self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
        self.ListaCmd()
        if (not self.eat(Tag.KW_END)):
            self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_SCORE_COMMA)):
            self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdWrite(self):
        if (not self.eat(Tag.KW_WRITE)):
            self.sinalizaErroSintatico('Esperado "write", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_OPN_PARENTH)):
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
        self.Expressao()
        if (not self.eat(Tag.KW_CLS_PARENTH)):
            self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_SCORE_COMMA)):
            self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdAtribui(self):
        if (not self.eat(Tag.OP_ATR)):
            self.sinalizaErroSintatico('Esperado "=", encontrado ' + '"' + self.token.getLexema() + '"')
        self.Expressao()
        if (not self.eat(Tag.KW_SCORE_COMMA)):
            self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdFuncao(self):
        if (not self.eat(Tag.KW_OPN_PARENTH)):
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
        self.RegexExp()
        if (not self.eat(Tag.KW_CLS_PARENTH)):
            self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        if (not self.eat(Tag.KW_SCORE_COMMA)):
            self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')

    def RegexExp(self):
        if (self.token.getNome() in (Tag.ID, Tag.KW_INTEGER, Tag.KW_FALSE, Tag.KW_DOUBLE, Tag.KW_STRING,
                                     Tag.KW_TRUE, Tag.OP_UNAR, Tag.OP_NOT, Tag.KW_OPN_PARENTH)):
            self.Expressao()
            self.RegexExp1()
        elif (self.token.getNome() != Tag.KW_CLS_PARENTH):
            self.sinalizaErroSintatico('Esperado "ID , integer , double , String , true , false , - , !", encontrado ' + '"' + self.token.getLexema() + '"')


    def RegexExp1(self):
        if (self.token.getNome() == Tag.KW_COMMA):
            self.Expressao()
            self.RegexExp1()
        elif (self.token.getNome() != Tag.KW_CLS_PARENTH):
            self.sinalizaErroSintatico('Esperado ",", encontrado ' + '"' + self.token.getLexema() + '"')

    def Expressao(self):
        self.Exp1()
        self.ExpLinha()

    def ExpLinha(self):
        if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
            self.Exp1()
            self.ExpLinha()
        elif(self.token.getNome() not in (Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "and, or", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp1(self):
        self.Exp2()
        self.Exp1Linha()


    def Exp1Linha(self):
        if (self.eat(Tag.OP_LT) or self.eat(Tag.OP_LTE) or self.eat(Tag.OP_GT) or
                self.eat(Tag.OP_GTE) or self.eat(Tag.OP_EQ) or self.eat(Tag.OP_DIFERENTE)):
            self.Exp2()
            self.Exp1Linha()
        elif (self.token.getNome() not in (Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "< , <= , > , >= , == , !=", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp2(self):
        self.Exp3()
        self.Exp2Linha()

    def Exp2Linha(self):
        if(self.eat(Tag.OP_ADD) or self.eat(Tag.OP_SUB)):
            self.Exp3()
            self.Exp2Linha()
        elif (self.token.getNome() not in (Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ, Tag.OP_NE,
                                           Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "+ , -", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp3(self):
        self.Exp4()
        self.Exp3Linha()

    def Exp3Linha(self):
        if (self.eat(Tag.OP_MULT) or self.eat(Tag.OP_DIV)):
            self.Exp4()
            self.Exp3Linha()
        elif (self.token.getNome() not in (Tag.OP_ADD, Tag.OP_SUB, Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ,
                                           Tag.OP_NE, Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "* , /", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp4(self):
        if(self.eat(Tag.ID)):
            self.Exp4Linha()
        elif(self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_FALSE) or self.eat(Tag.KW_DOUBLE) or
           self.eat(Tag.KW_STRING) or self.eat(Tag.KW_TRUE)):
            print('oi')
        elif (self.eat(Tag.OP_UNAR)):
            self.Exp4()
        elif (self.eat(Tag.KW_OPN_PARENTH)):
            self.Expressao()
            if(not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "( , integer , double , String , true , false , - , ! ", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp4Linha(self):
        if (self.eat(Tag.KW_OPN_PARENTH)):
            self.RegexExp()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (self.token.getNome() not in (Tag.OP_MULT, Tag.OP_DIV, Tag.OP_ADD, Tag.OP_SUB, Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE,
                                           Tag.OP_EQ, Tag.OP_NE, Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')

    def OpUnario(self):
        if(not self.eat(Tag.OP_NOT) and not self.eat(Tag.OP_UNAR)):
            self.sinalizaErroSintatico('Esperado "- , !", encontrado ' + '"' + self.token.getLexema() + '"')