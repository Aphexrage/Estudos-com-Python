class Vehicle:
    def __init__(self, name, maxSpeed, mileage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage
        return print(f"O nome do veiculo é {name}, velocidade max é {maxSpeed} e a quilometragem é de {mileage}")
    
    def passageiros(self, capacidade):
        self.capacidade = capacidade
        return print(f"A capacidade do veiculo é de {capacidade}")