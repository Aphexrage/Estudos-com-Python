from Item import Item

class Carrinho:
    
    def __init__(self):
        self.itens = []
        
    def adicionarItem(self, item):
        self.itens.append(item)
        
    def removerItem(self, item):
        if item in self.itens:
            self.itens.remove(item)
            
    def calcularTotal(self):
        return sum(i.preco for i in self.itens)