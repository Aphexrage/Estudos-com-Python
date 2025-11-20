class Veiculo:
    
    def descricao(self):
        return "Descricao"
        
    def mostrarDescricao(self):
        return self.descricao()
    
class Carro(Veiculo):
    
    def descricao(self):
        return "Carro"
    
class Moto(Veiculo):
    
    def descricao(self):
        return "Moto"    