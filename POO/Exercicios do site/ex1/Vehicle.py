#Escreva um programa em Python para criar uma classe `Vehicle` com max_speedatributos mileagede instância.

class Vehicle:
    
    def __init__(self, maxSpeed, meliage):
        self.maxSpeed = maxSpeed
        self.meliage = meliage
        return print(f"A velocidade maxima é {maxSpeed} e a quilometragem é {meliage}")
        
carro1 = Vehicle(200, 20)

# Testando agora cada atributo:
print(f"Maxspeed: {carro1.maxSpeed}")
print(f"Meliage: {carro1.meliage}")


