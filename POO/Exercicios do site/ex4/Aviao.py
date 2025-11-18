from Vehicle import *

class Aviao(Vehicle):
    
    # Aplicando o polimorfismo no metodo passageiros
    def passageiros(self, capacidade=200):
        return super().passageiros(capacidade=200)
    
boeing = Aviao("Boeing 737", 1000, 10000) 

print(boeing.passageiros())