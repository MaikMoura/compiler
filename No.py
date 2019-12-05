from Tag import Tag

class No():
   def __init__(self):
      self.tipo = Tag.TIPO_VAZIO

   def getTipo(self):
      return self.tipo

   def setTipo(self, tipo):
      self.tipo = tipo