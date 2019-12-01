import sys

from Ts import Ts
from Tag import Tag
from Token import Token
from Lexer import Lexer
from No import No

class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proximoToken()

    def sinalizaErroSintatico(self, message):
        print('\n[Erro Sintatico] na linha ' + str(self.token.getLinha()) + ' e coluna ' + str(self.token.getColuna()) + ': ')
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

    def Programa(self):
        # Programa -> Classe EOF
        self.Classe()
        if(self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico('Esperado "EOF"; encontrado ' + '"' + self.token.getLexema() + '"')

    def Classe(self):
        # Classe -> class ID : ListaFuncao Main end .
        if(self.eat(Tag.KW_CLASS)):
            # TO DO
            if (self.eat(Tag.ID)):
                self.lexer.ts.getToken(self.token.getLexema()).setTipo(Tag.TIPO_VAZIO)
            else:
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaFuncao()
            self.Main()
            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE)):
                self.sinalizaErroSintatico('Esperado ".", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "class", encontrado ' + '"' + self.token.getLexema() + '"')

    def DeclaraID(self):
        #DeclaraID -> TipoPrimitivo ID ;
        noTP = self.TipoPrimitivo()
        if (self.eat(Tag.ID)):
            self.lexer.ts.getToken(self.token.getLexema()).setTipo(Tag.TIPO_VAZIO)
        else:
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
        if (self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_DOUBLE)):
            Ts.getToken(self.token.getLexema()).setTipo(Tag.NUMERICO)
        elif (self.eat(Tag.KW_STRING)):
            Ts.getToken(self.token.getLexema()).setTipo(Tag.STRING)
        elif (self.eat(Tag.KW_VOID)):
            Ts.getToken(self.token.getLexema()).setTipo(Tag.TIPO_VAZIO)
        elif (self.eat(Tag.KW_BOOL)):
            Ts.getToken(self.token.getLexema()).setTipo(Tag.LOGICO)
        else:
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
        if (self.token.getNome() == Tag.OP_ATR):
            self.CmdAtribui()
        # CmdAtribFunc -> CmdFuncao
        elif (self.token.getNome() == Tag.KW_OPN_PARENTH):
            self.CmdFuncao()
        else:
            self.sinalizaErroSintatico('Esperado "== , (", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdIf(self):
        #CmdIF -> if ( Expressao ) : ListaCmd CmdIF’
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
        # CmdIF’ -> end ;
        if (self.eat(Tag.KW_END)):
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        # CmdIF’ -> else : ListaCmd end ;
        elif (self.eat(Tag.KW_ELSE)):
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaCmd()
            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico('Esperado "end", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "end, else", encontrado ' + '"' + self.token.getLexema() + '"')


    def CmdWhile(self):
        # CmdWhile -> while ( Expressao ) : ListaCmd end ;
        if (self.eat(Tag.KW_WHILE)):
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
        else:
            self.sinalizaErroSintatico('Esperado "while", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdWrite(self):
        # CmdWrite -> write ( Expressao ) ;
        if (self.eat(Tag.KW_WRITE)):
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            self.Expressao()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "write", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdAtribui(self):
        # CmdAtribui -> = Expressao ;
        if (self.eat(Tag.OP_ATR)):
            self.Expressao()
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "=", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdFuncao(self):
        # CmdFuncao -> ( RegexExp ) ;
        if (self.eat(Tag.KW_OPN_PARENTH)):
            self.RegexExp()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')

    def RegexExp(self):
        # RegexExp -> Expressao RegexExp’
        if (self.token.getNome() in (Tag.ID, Tag.INT, Tag.DOUBLE, Tag.STRING, Tag.KW_TRUE, Tag.KW_FALSE,
                                     Tag.OP_UNAR, Tag.OP_NOT, Tag.KW_OPN_PARENTH, Tag.EOF)):
            self.Expressao()
            self.RegexExp1()
        elif (self.token.getNome() != Tag.KW_CLS_PARENTH):
            self.sinalizaErroSintatico('Esperado "ID , ConstInteger , ConstDouble , ConstString , true , false' +
                                       ', - , ! , ( , EOF", encontrado ' + '"' + self.token.getLexema() + '"')

    def RegexExp1(self):
        # RegexExp’ -> , Expressao RegexExp’
        if (self.token.getNome() == Tag.KW_COMMA):
            self.Expressao()
            self.RegexExp1()
        elif (self.token.getNome() != Tag.KW_CLS_PARENTH):
            self.sinalizaErroSintatico('Esperado ",", encontrado ' + '"' + self.token.getLexema() + '"')

    def Expressao(self):
        # Expressao -> Exp1 Exp’
        self.Exp1()
        self.ExpLinha()

    def ExpLinha(self):
        # Exp’ -> or Exp1 Exp’ | #Exp’ -> and Exp1 Exp’
        if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
            self.Exp1()
            self.ExpLinha()
        elif(self.token.getNome() not in (Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "and, or", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp1(self):
        # Exp1 -> Exp2 Exp1’
        self.Exp2()
        self.Exp1Linha()

    def Exp1Linha(self):
        # Exp1’ -> < Exp2 Exp1’ | <= Exp2 Exp1’ | > Exp2 Exp1’ | >= Exp2 Exp1’ | == Exp2 Exp1’ | != Exp2 Exp1’
        if (self.eat(Tag.OP_LT) or self.eat(Tag.OP_LTE) or self.eat(Tag.OP_GT) or
                self.eat(Tag.OP_GTE) or self.eat(Tag.OP_EQ) or self.eat(Tag.OP_NE)):
            self.Exp2()
            self.Exp1Linha()
        elif (self.token.getNome() not in (Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "< , <= , > , >= , == , !=", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp2(self):
        # Exp2 -> Exp3 Exp2’
        self.Exp3()
        self.Exp2Linha()

    def Exp2Linha(self):
        # Exp2’ -> + Exp3 Exp2’ | - Exp3 Exp2’
        if(self.eat(Tag.OP_ADD) or self.eat(Tag.OP_SUB)):
            self.Exp3()
            self.Exp2Linha()
        elif (self.token.getNome() not in (Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ, Tag.OP_NE,
                                           Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "+ , -", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp3(self):
        # Exp3 -> Exp4 Exp3’
        self.Exp4()
        self.Exp3Linha()

    def Exp3Linha(self):
        # Exp3’ -> * Exp4 Exp3’ | / Exp4 Exp3’
        if (self.eat(Tag.OP_MULT) or self.eat(Tag.OP_DIV)):
            self.Exp4()
            self.Exp3Linha()
        elif (self.token.getNome() not in (Tag.OP_ADD, Tag.OP_SUB, Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ,
                                           Tag.OP_NE, Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "* , /", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp4(self):
        # Exp4 -> ID Exp4’
        if (self.eat(Tag.ID)):
            self.Exp4Linha()
        # Exp4 -> OpUnario Exp4
        elif (self.token.getNome() in (Tag.OP_UNAR, Tag.OP_NOT)):
            self.OpUnario()
            self.Exp4()
        # Exp4 -> ( Expressao)
        elif (self.eat(Tag.KW_OPN_PARENTH)):
            self.Expressao()
            if(not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (not self.eat(Tag.INT) and not self.eat(Tag.DOUBLE) and not self.eat(Tag.STRING)
              and not self.eat(Tag.KW_TRUE) and not self.eat(Tag.KW_FALSE)):
            self.sinalizaErroSintatico('Esperado "ID , ConstInteger , ConstDouble , ConstString , true , false' +
                                       ' , - , ! , (", encontrado ' + '"' + self.token.getLexema() + '"')

    def Exp4Linha(self):
        # Exp4’ -> ( RegexExp )
        if (self.eat(Tag.KW_OPN_PARENTH)):
            self.RegexExp()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (self.token.getNome() not in (Tag.OP_MULT, Tag.OP_DIV, Tag.OP_ADD, Tag.OP_SUB, Tag.OP_LT, Tag.OP_LTE,
                                           Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ, Tag.OP_NE, Tag.KW_OR, Tag.KW_AND,
                                           Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')

    def OpUnario(self):
        # OpUnario -> - | !
        if(not self.eat(Tag.OP_NOT) and not self.eat(Tag.OP_UNAR)):
            self.sinalizaErroSintatico('Esperado "- , !", encontrado ' + '"' + self.token.getLexema() + '"')