
class Vehicle:
    def __init__(self, name, maxSpeed, mileage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage
        
    def definirCor(self, nomeCor = "Branco"):
        self.nomeCor = nomeCor = "Branco"
        return f"Cor: {nomeCor}, Nome: {self.name}, Velocidade: {self.maxSpeed}, Quilometragem: {self.mileage}"
        
class Bus(Vehicle):
    
    onibus = Vehicle("163 - Jardim POO", 70, 10000)
    print(onibus.definirCor())
        
class Car(Vehicle):
    
    honda = Vehicle("Civic", 230, 10000)
    print(honda.definirCor())