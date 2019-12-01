'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

from enum import Enum

class Tag(Enum):

    EOF = -1

    # Operadores
    OP_LT = 1
    OP_LTE = 2
    OP_GT = 3
    OP_GTE = 4
    OP_EQ = 5
    OP_NE = 6
    OP_ATR = 7
    OP_DIV = 8
    OP_MULT = 9
    OP_ADD = 10
    OP_SUB = 11
    OP_NOT = 12
    OP_UNAR = 13

    #KEYWORDS
    KW_CLASS = 14
    KW_DEF = 15
    KW_END = 16
    KW_RETURN = 17
    KW_DEFSTATIC = 18
    KW_VOID = 19
    KW_MAIN = 20
    KW_STRING = 21
    KW_BOOL = 22
    KW_INTEGER = 23
    KW_DOUBLE = 24
    KW_IF = 25
    KW_ELSE = 26
    KW_WHILE = 27
    KW_WRITE = 28
    KW_TRUE = 29
    KW_FALSE = 30
    KW_OR = 31
    KW_AND = 32
    KW_COMMENT = 33
    KW_SCORE = 34
    KW_DBL_SCORE = 35
    KW_SCORE_COMMA = 36
    KW_OPN_PARENTH = 37
    KW_CLS_PARENTH = 38
    KW_COMMA = 39
    KW_OPN_MATTR = 40
    KW_CLS_MATTR = 41

    #ID
    ID = 42

    #Numeros
    INT = 43
    DOUBLE = 44
    NUMERICO = 45
    LOGICO = 46

    #String
    STRING = 47

    #Erro
    ERROR = 48

    #VAZIO
    TIPO_VAZIO = 49