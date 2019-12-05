import sys

from Tag import Tag
from Token import Token
from Lexer import Lexer
from No import No

class Parser():

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proximoToken()
        self.ts = self.lexer.getTs()

    def sinalizaErroSintatico(self, message):
        print('\n[Erro Sintatico] na linha ' + str(self.token.getLinha()) + ' e coluna ' + str(self.token.getColuna()) + ': ')
        print(message, '\n')

    def sinalizaErroSemantico(self, message):
        print('\n[Erro Semantico] na linha ' + str(self.token.getLinha()) + ' e coluna ' + str(self.token.getColuna()) + ": ")
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
            tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                self.ts.setTipo(tempToken.getLexema(), Tag.TIPO_VAZIO)
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
        tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.ts.setTipo(tempToken.getLexema(), noTP.getTipo())
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
            noTP = self.TipoPrimitivo()
            tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                self.ts.setTipo(tempToken.getLexema(), noTP.getTipo())
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            self.ListaArg()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_DBL_SCORE)):
                self.sinalizaErroSintatico('Esperado ":", encontrado ' + '"' + self.token.getLexema() + '"')
            self.RegexDeclaraId()
            self.ListaCmd()

            noReturn = self.Retorno()
            if(noReturn.getTipo() != noTP.getTipo()):
                self.sinalizaErroSemantico('Tipo de retorno incompativel')
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
        noTP = self.TipoPrimitivo()
        tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico('Esperado "ID", encontrado ' + '"' + self.token.getLexema() + '"')
        else:
            self.ts.setTipo(tempToken.getLexema(), noTP.getTipo())

    def Retorno(self):
        noReturn = No()
        # Retorno -> return Expressao ;
        if (self.eat(Tag.KW_RETURN)):
            noExp = self.Expressao()
            if (self.eat(Tag.KW_SCORE_COMMA)):
                noReturn.setTipo(noExp.getTipo())
                return noReturn
            else:
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
        elif (self.token.getNome() == Tag.KW_END):
            noReturn.setTipo(Tag.TIPO_VAZIO)
            return noReturn
        else:
            self.sinalizaErroSintatico('Esperado "return", encontrado ' + '"' + self.token.getLexema() + '"')
            noReturn.setTipo(Tag.ERROR)
            return noReturn


    def Main(self):
        tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())
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
            else:
                self.ts.setTipo(tempToken.getLexema(), Tag.STRING)
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
        noTP = No()
        # TipoPrimitivo -> integer | double
        if (self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_DOUBLE)):
            noTP.setTipo(Tag.NUMERICO)
            return noTP
        # TipoPrimitivo -> String
        elif (self.eat(Tag.KW_STRING)):
            noTP.setTipo(Tag.STRING)
            return noTP
        # TipoPrimitivo -> void
        elif (self.eat(Tag.KW_VOID)):
            noTP.setTipo(Tag.TIPO_VAZIO)
            return noTP
        # TipoPrimitivo -> bool
        elif (self.eat(Tag.KW_BOOL)):
            noTP.setTipo(Tag.LOGICO)
            return noTP
        else:
            self.sinalizaErroSintatico('Esperado "bool, integer, String, double, void", encontrado ' + '"' + self.token.getLexema() + '"')
            noTP.setTipo(Tag.ERROR)
            return noTP

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
        noCmd = No()
        tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())
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
            if (self.ts.getTipo(tempToken.getLexema()) == None):
                self.sinalizaErroSemantico('ID não declarado')
            noCmdAtribuiFunc = self.CmdAtribFunc()
            if (noCmdAtribuiFunc.getTipo() != Tag.TIPO_VAZIO and self.ts.getTipo(tempToken.getLexema()) != noCmdAtribuiFunc.getTipo()):
                self.sinalizaErroSemantico('Atribuição incompatível')
        else:
            self.sinalizaErroSintatico('Esperado "if , while , write , id", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdAtribFunc(self):
        noCmdAtribFunc = No()
        # CmdAtribFunc -> CmdAtribui
        if (self.token.getNome() == Tag.OP_ATR):
            noCmdAtribui = self.CmdAtribui()
            noCmdAtribFunc.setTipo(noCmdAtribui.getTipo())
            return noCmdAtribFunc
        # CmdAtribFunc -> CmdFuncao
        elif (self.token.getNome() == Tag.KW_OPN_PARENTH):
            self.CmdFuncao()
            noCmdAtribFunc.setTipo(Tag.TIPO_VAZIO)
            return noCmdAtribFunc
        else:
            self.sinalizaErroSintatico('Esperado "== , (", encontrado ' + '"' + self.token.getLexema() + '"')
            noCmdAtribFunc.setTipo(Tag.ERROR)
            return noCmdAtribFunc

    def CmdIf(self):
        noCmdIf = No()
        #CmdIF -> if ( Expressao ) : ListaCmd CmdIF’
        if(self.eat(Tag.KW_IF)):
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp = self.Expressao()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                if (noExp.getTipo() != Tag.LOGICO):
                    self.sinalizaErroSemantico('Esperado "logico", encontrado' + '"' + self.token.getLexema() + '"')
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
        noCmdWhile = No()
        # CmdWhile -> while ( Expressao ) : ListaCmd end ;
        if (self.eat(Tag.KW_WHILE)):
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp = self.Expressao()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                if (noExp.getTipo() != Tag.LOGICO):
                    self.sinalizaErroSemantico('Esperado "logico", encontrado' + '"' + self.token.getLexema() + '"')
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
        noCmdWrite = No()
        # CmdWrite -> write ( Expressao ) ;
        if (self.eat(Tag.KW_WRITE)):
            if (not self.eat(Tag.KW_OPN_PARENTH)):
                self.sinalizaErroSintatico('Esperado "(", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp = self.Expressao()
            if (not self.eat(Tag.KW_CLS_PARENTH)):
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                if (noExp.getTipo() != Tag.STRING):
                    self.sinalizaErroSemantico('Esperado "string", encontrado' + '"' + self.token.getLexema() + '"')
        else:
            self.sinalizaErroSintatico('Esperado "write", encontrado ' + '"' + self.token.getLexema() + '"')

    def CmdAtribui(self):
        noCmdAtribui = No()
        # CmdAtribui -> = Expressao ;
        if (self.eat(Tag.OP_ATR)):
            noExp = self.Expressao()
            if (not self.eat(Tag.KW_SCORE_COMMA)):
                self.sinalizaErroSintatico('Esperado ";", encontrado ' + '"' + self.token.getLexema() + '"')
            else:
                noCmdAtribui.setTipo(noExp.getTipo())
                return noCmdAtribui
        else:
            self.sinalizaErroSintatico('Esperado "=", encontrado ' + '"' + self.token.getLexema() + '"')
        noCmdAtribui.setTipo(Tag.ERROR)
        return noCmdAtribui

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
        noExp = No()
        # Expressao -> Exp1 Exp’
        noExp1 = self.Exp1()
        noExpLinha = self.ExpLinha()
        if (noExpLinha.getTipo() == Tag.TIPO_VAZIO):
            noExp.setTipo(noExp1.getTipo())
        elif (noExpLinha.getTipo() == noExp1.getTipo() and noExpLinha.getTipo() == Tag.LOGICO):
            noExp.setTipo(Tag.LOGICO)
        else:
            noExp.setTipo(Tag.ERROR)
        return noExp

    def ExpLinha(self):
        noExpLinha = No()
        # Exp’ -> or Exp1 Exp’ | #Exp’ -> and Exp1 Exp’
        if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
            noExp1 = self.Exp1()
            noExpLinhaFilho = self.ExpLinha()
            if (noExpLinhaFilho.getTipo() in (Tag.TIPO_VAZIO, noExp1.getTipo()) and noExp1.getTipo() == Tag.LOGICO):
                noExpLinha.setTipo(Tag.LOGICO)
            else:
                noExpLinha.setTipo(Tag.ERROR)
            return noExpLinha
        elif (self.token.getNome() in (Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            noExpLinha.setTipo(Tag.TIPO_VAZIO)
            return noExpLinha
        else:
            self.sinalizaErroSintatico('Esperado "and, or", encontrado ' + '"' + self.token.getLexema() + '"')
            noExpLinha.setTipo(Tag.ERROR)
            return noExpLinha

    def Exp1(self):
        noExp1 = No()
        # Exp1 -> Exp2 Exp1’
        noExp2 = self.Exp2()
        noExp1Linha = self.Exp1Linha()
        if (noExp1Linha.getTipo() == Tag.TIPO_VAZIO):
            noExp1.setTipo(noExp2.getTipo())
        elif (noExp1Linha.getTipo() == noExp2.getTipo() and noExp1Linha.getTipo() == Tag.NUMERICO):
            noExp1.setTipo(Tag.LOGICO)
        else:
            noExp1.setTipo(Tag.ERROR)
        return noExp1


    def Exp1Linha(self):
        noExp1Linha = No()
        # Exp1’ -> < Exp2 Exp1’ | <= Exp2 Exp1’ | > Exp2 Exp1’ | >= Exp2 Exp1’ | == Exp2 Exp1’ | != Exp2 Exp1’
        if (self.eat(Tag.OP_LT) or self.eat(Tag.OP_LTE) or self.eat(Tag.OP_GT) or
                self.eat(Tag.OP_GTE) or self.eat(Tag.OP_EQ) or self.eat(Tag.OP_NE)):
            noExp2 = self.Exp2()
            noExp1LinhaFilho = self.Exp1Linha()
            if (noExp1LinhaFilho.getTipo() in (Tag.TIPO_VAZIO, noExp2.getTipo()) and noExp2.getTipo() == Tag.NUMERICO):
                noExp1Linha.setTipo(Tag.NUMERICO)
            else:
                noExp1Linha.setTipo(Tag.ERROR)
            return noExp1Linha
        elif (self.token.getNome() in (Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            noExp1Linha.setTipo(Tag.TIPO_VAZIO)
            return noExp1Linha
        else:
            self.sinalizaErroSintatico('Esperado "< , <= , > , >= , == , !=", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp1Linha.setTipo(Tag.ERROR)
            return noExp1Linha

    def Exp2(self):
        noExp2 = No()
        # Exp2 -> Exp3 Exp2’
        noExp3 = self.Exp3()
        noExp2Linha = self.Exp2Linha()
        if (noExp2Linha.getTipo() == Tag.TIPO_VAZIO):
            noExp2.setTipo(noExp3.getTipo())
        elif (noExp2Linha.getTipo() == noExp3.getTipo() and noExp2Linha.getTipo() == Tag.NUMERICO):
            noExp2.setTipo(Tag.NUMERICO)
        else:
            noExp2.setTipo(Tag.ERROR)
        return noExp2

    def Exp2Linha(self):
        noExp2Linha = No()
        # Exp2’ -> + Exp3 Exp2’ | - Exp3 Exp2’
        if(self.eat(Tag.OP_ADD) or self.eat(Tag.OP_SUB)):
            noExp3 = self.Exp3()
            noExp2LinhaFilho = self.Exp2Linha()
            if (noExp2LinhaFilho.getTipo() in (Tag.TIPO_VAZIO, noExp3.getTipo()) and noExp3.getTipo() == Tag.NUMERICO):
                noExp2Linha.setTipo(Tag.NUMERICO)
                return noExp2Linha
            else:####
                noExp2Linha.setTipo(Tag.ERROR)
                return noExp2Linha
        elif (self.token.getNome() in (Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ, Tag.OP_NE,
                                           Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            noExp2Linha.setTipo(Tag.TIPO_VAZIO)
            return noExp2Linha
        else:
            self.sinalizaErroSintatico('Esperado "+ , -", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp2Linha.setTipo(Tag.ERROR)
            return noExp2Linha

    def Exp3(self):
        noExp3 = No()
        # Exp3 -> Exp4 Exp3’
        noExp4 = self.Exp4()
        noExp3Linha = self.Exp3Linha()
        if (noExp3Linha.getTipo() == Tag.TIPO_VAZIO):
            noExp3.setTipo(noExp4.getTipo())
        elif (noExp3Linha.getTipo() == noExp4.getTipo() and noExp3Linha.getTipo() == Tag.NUMERICO):
            noExp3.setTipo(Tag.NUMERICO)
        else:
            noExp3.setTipo(Tag.ERROR)

        return noExp3

    def Exp3Linha(self):
        noExp3Linha = No()
        # Exp3’ -> * Exp4 Exp3’ | / Exp4 Exp3’
        if (self.eat(Tag.OP_MULT) or self.eat(Tag.OP_DIV)):
            noExp4 = self.Exp4()
            noExp3LinhaFilho = self.Exp3Linha()
            if (noExp3LinhaFilho.getTipo() in (Tag.TIPO_VAZIO, noExp4.getTipo()) and noExp4.getTipo() == Tag.NUMERICO):
                noExp3Linha.setTipo(Tag.NUMERICO)
            else:
                noExp3Linha.setTipo(Tag.ERROR)
            return noExp3Linha
        elif (self.token.getNome() in (Tag.OP_ADD, Tag.OP_SUB, Tag.OP_LT, Tag.OP_LTE, Tag.OP_GT, Tag.OP_GTE, Tag.OP_EQ,
                                        Tag.OP_NE, Tag.KW_OR, Tag.KW_AND, Tag.KW_CLS_PARENTH, Tag.KW_SCORE_COMMA, Tag.KW_COMMA)):
            noExp3Linha.setTipo(Tag.TIPO_VAZIO)
            return noExp3Linha
        else:
            self.sinalizaErroSintatico('Esperado "* , /", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp3Linha.setTipo(Tag.ERROR)
            return noExp3Linha

    def Exp4(self):
        noExp4 = No()
        tempToken = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

        # Exp4 -> ID Exp4’
        if (self.eat(Tag.ID)):
            self.Exp4Linha()
            noExp4.setTipo(tempToken.getTipo())
            if (noExp4.getTipo() == Tag.TIPO_VAZIO):
                noExp4.setTipo(Tag.ERROR)
                self.sinalizaErroSemantico('ID não declarado')
                return noExp4
        # Exp4 -> ConstInteger | ConstDouble
        elif (self.eat(Tag.INT) or self.eat(Tag.DOUBLE)):
            noExp4.setTipo(Tag.NUMERICO)
            return noExp4
        # Exp4 -> ConstString
        elif (self.eat(Tag.STRING)):
            noExp4.setTipo(Tag.STRING)
            return noExp4
        # Exp4 -> ConstString
        elif (self.eat(Tag.KW_TRUE) or self.eat(Tag.KW_FALSE)):
            noExp4.setTipo(Tag.LOGICO)
            return noExp4
        # Exp4 -> OpUnario Exp4
        elif (self.token.getNome() in (Tag.OP_UNAR, Tag.OP_NOT)):
            noUnario = self.OpUnario()
            noExp4Filho = self.Exp4()
            if (noExp4Filho.getTipo() == noUnario.getTipo() and noUnario.getTipo() == Tag.NUMERICO):
                noExp4.setTipo(Tag.NUMERICO)
            elif (noExp4Filho.getTipo() == noUnario.getTipo() and noUnario.getTipo() == Tag.LOGICO):
                noExp4.setTipo(Tag.LOGICO)
            else:
                noExp4.setTipo(Tag.ERROR)
            return noExp4
        # Exp4 -> ( Expressao )
        elif (self.eat(Tag.KW_OPN_PARENTH)):
            noExp = self.Expressao()
            if(self.eat(Tag.KW_CLS_PARENTH)):
                noExp4.setTipo(noExp.getTipo())
                return noExp4
            else:
                self.sinalizaErroSintatico('Esperado ")", encontrado ' + '"' + self.token.getLexema() + '"')
                noExp4.setTipo(Tag.ERROR)
                return noExp4
        else:
            self.sinalizaErroSintatico('Esperado "ID , ConstInteger , ConstDouble , ConstString , true , false' +
                                       ' , - , ! , (", encontrado ' + '"' + self.token.getLexema() + '"')
            noExp4.setTipo(Tag.ERROR)
            return noExp4

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
        noUnario = No()
        # OpUnario -> - | !
        if (self.eat(Tag.OP_UNAR)):
            noUnario.setTipo(Tag.NUMERICO)
            return noUnario
        elif(self.eat(Tag.OP_NOT)):
            noUnario.setTipo(Tag.LOGICO)
            return noUnario
        else:
            self.sinalizaErroSintatico('Esperado "- , !", encontrado ' + '"' + self.token.getLexema() + '"')
            noUnario.setTipo(Tag.ERROR)
            return noUnario