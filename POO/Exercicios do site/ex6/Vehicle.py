"""
Criar a Busclasse infantil que herda da Vehicle classe. 
A taxa padrão para qualquer veículo é a sua capacidade de assento multiplicada por 100 (capacidade de assento * 100).

Se o veículo é a Buinstância, precisamos adicionar um extra de 10% à tarifa completa como uma taxa de manutenção. 
Portanto, a tarifa total para a Businstância será o valor final, calculado como tarifa total mais 10% da tarifa total. 
(quantia final = tarifa total + 10% da tarifa total.)

Nota : A capacidade de assentos de ônibus é de 50, então o valor final da tarifa deve ser de 5500.

Use o seguinte código para seu pai Vehicle classe. Precisamos acessar a classe dos pais de dentro de um método de uma classe infantil.
"""

class Vehicle:
    
    def __init__(self, name, maxSpeed, mileage, capacidade):
        self.name = name
        self.maxSpeed = maxSpeed
        self.mileage = mileage
        self.capacidade = capacidade
        
    def calculo(self):
        return f"A tarifa total do onibus é: {self.capacidade * 100}"
