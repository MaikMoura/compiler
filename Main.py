'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

from lexer.Tag import Tag
from lexer.Token import Token
from lexer.Lexer import Lexer
from lexer.parser1 import Parser

if __name__ == "__main__":
    lexer = Lexer('program.txt')

    parser = Parser(lexer)

    parser.Programa()

    parser.lexer.closeFile()

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