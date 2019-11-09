'''
    *****
    @Authors: Luan Hitalo & Maik moura
    *****
'''

class Token:
    def __init__(self, nome, lexema, linha, coluna):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def getNome(self):
        return self.nome

    def getLexema(self):
        return self.lexema

    def getLinha(self):
        return self.linha

    def getColuna(self):
        return self.coluna

    def setLinha(self, linha):
        self.linha = linha

    def setColuna(self, coluna):
        self.coluna = coluna

    def toString(self):
        return '<' + str(self.nome) + ', "' + str(self.lexema) + '">'