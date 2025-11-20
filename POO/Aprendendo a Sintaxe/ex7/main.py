class Vehicle:
    
    def __init__(self, name, maxSpeed, mileage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage
        
class Bus(Vehicle):
    pass

    onibus = Vehicle("Onibus", 70, 100000)
    print(type(onibus))