class Vehicle:
    def __init__(self, name, maxSpeed, mileage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage
    
    def passageiros(self, capacidade):
        return f"A capacidade do {self.name} é de {capacidade} passageiros"