class Vehicle:
    def __init__(self, name, maxSpeed, meliage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.meliage = meliage
        
class Teste:
    def __init__(self, teste):
        self.teste = teste
        
class Bus(Vehicle, Teste):
    
    onibus = Vehicle("Onibus", 100, 100000)
    print(isinstance(onibus, Vehicle))
    print(isinstance(onibus, Teste))
    