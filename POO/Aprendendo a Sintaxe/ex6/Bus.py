from Vehicle import Vehicle

class Bus(Vehicle):
    
    def calculo(self):
        tarifa = super().calculo()
        return tarifa + tarifa * 0.10 