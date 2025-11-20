class ContaBancaria:
    def __init__(self, saldo):
        self._saldo = saldo
        
        
    def depositar(self, valor):
        if valor >= 0:
            self._saldo += valor
        else:
            raise ValueError("O valor precisa ser maior que 0")
            
    def sacar(self, valor):
        if valor >= 0:
            if self._saldo >= valor:
                self._saldo -= valor
            else:
                raise ValueError(f"Saldo insuficiente para realizar a transação. Saldo atual: {self._saldo}")
        else:
            raise ValueError("O valor precisa ser maior que 0")
    
    def getSaldo(self):
        return self._saldo
