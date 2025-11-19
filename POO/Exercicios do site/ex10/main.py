"""
You have given a Shape class and subclasses Circle and Square. 
The parent class (Shape) has a area() method.

Now, Write a OOP code to calculate the area of each shapes 
(each subclass must write its own implementation of area() method to calculates its area).
"""
import math

class Shape:
    def area(self):
        raise NotImplementedError("O metodo da area deve ser implementado na subclass")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        r2 = self.radius * self.radius
        calculo = math.pi * r2
        return calculo
        
class Square(Shape):
    def __init__(self, side):
        self.side = side
        
    def area(self):
        calculo = self.side * self.side
        return calculo
        
shapes = [Circle(5), Square(7), Circle(3)]

for shape in shapes:
    print(shape.area())