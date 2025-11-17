# OOP Exercise 2: Create a Vehicle class without any variables and methods

class Vehicle:
    def __init__(self, name, maxSpeed, miliage):
        self.name = name
        self.maxSpeed = maxSpeed
        self.miliage = miliage
        return print(f"O nome do veiculo é {name}, velocidade max é {maxSpeed} e a quilometragem é {miliage}")
        