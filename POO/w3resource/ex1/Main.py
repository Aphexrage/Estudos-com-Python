from Circle import Circle

class Main(Circle):
    
    radius = input("Informe o radius: ")
    calculo = Circle(radius)
    print(f"A area é {calculo.area()}")
    print(f"O perimetro é {calculo.perimeter()}")
    
    