# Vou realizar um teste sem usar polimorfismo:

from Vehicle import Vehicle

class Teste:
    
    HondaCivic = Vehicle("Honda Civic", 240, 100000)
    FiatUno = Vehicle("Fiat Uno", 100, 100000)
    Fusca = Vehicle("Fusca", 230, 100000)
    
    print(HondaCivic.passageiros(capacidade=4))
    print(FiatUno.passageiros(capacidade=4))
    print(Fusca.passageiros(capacidade=16))
    
    
    