'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

from Tag import Tag
from Token import Token
from Lexer import Lexer
from parser1 import Parser

if __name__ == "__main__":
    lexer = Lexer('HelloWorld.txt')

    parser = Parser(lexer)

    parser.Programa()

    print('\n=>Lista de Tokens:')
    token = lexer.proximoToken()
    while (token is not None and token.getNome() != Tag.EOF):
        if (token.getNome() != Tag.ERROR):
            print('{} , Linha: {} Coluna: {}'.format(token.toString(), str(token.getLinha()), str(token.getColuna())))
        token = lexer.proximoToken()


    print('\n=>Tabela de Simbolos:')
    lexer.imprimirTs()
    lexer.fecharArquivo()

    print('\n=> Erros: (Modo Panico)')
    lexer.imprimirErros()

    print('\n=> Fim da Compilacao')