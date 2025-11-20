class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        
    def calcularTotal(self, quantidade):
        if quantidade <= self.estoque:        
            total = self.preco * quantidade
            self.estoque -= quantidade
            return total
        else:
            raise ValueError(f"Não há quantidade disponivel no estoque do produto: {self.nome}")
    