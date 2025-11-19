"""
1. Circle Class for Area and Perimeter
Write a Python program to create a class representing a Circle. Include methods to calculate its area and perimeter. 
"""

from Circle import Circle


radius = int(input("Informe o radius: "))
# Descobri que um input sempre sera um str
# Preciso sempre colocar qual o tipo de var recebida:
calculo = Circle(radius)
print(f"A area é {calculo.area()}")
print(f"O perimetro é {calculo.perimeter()}")
    
    