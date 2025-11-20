"""
1. Circle Class for Area and Perimeter

Write a Python program to create a class representing a Circle. Include methods to calculate its area and perimeter. 
"""
import math

class Circle:
    
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        r2 = self.radius * self.radius
        return math.pi * r2
    
    def perimeter(self):
        return 2 * math.pi * self.radius