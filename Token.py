'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''
from Tag import Tag

class Token:
    def __init__(self, nome, lexema, linha, coluna):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        self.tipo = Tag.TIPO_VAZIO

    def getNome(self):
        return self.nome

    def getLexema(self):
        return self.lexema

    def getTipo(self):
        return self.tipo

    def getLinha(self):
        return self.linha

    def getColuna(self):
        return self.coluna

    def setLinha(self, linha):
        self.linha = linha

    def setTipo(self, tipo):
        self.tipo = tipo

    def setColuna(self, coluna):
        self.coluna = coluna

    def toString(self):
        return '<' + str(self.nome) + ', "' + str(self.lexema) + '">'