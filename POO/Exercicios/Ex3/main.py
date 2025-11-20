from ContaBancaria import ContaBancaria

contaGustavo = ContaBancaria(500)

acao = int(input("Voce gostaria de consultar seu 1 - saldo, 2 - depositar ou 3 - sacar?, 4 - Encerrar "))

while(acao != 4):
    if acao == 1:
        print(contaGustavo.getSaldo())
    elif acao == 2:
        deposito = float(input("Qual valor gostaria de depositar? "))
        contaGustavo.depositar(deposito)
    elif acao == 3:
        saque = float(input("Qual valor gostaria de sacar? "))
        contaGustavo.sacar(saque)
    else: 
        print("Opcao nao permitida")
        
    acao = int(input("Voce gostaria de consultar seu 1 - saldo, 2 - depositar ou 3 - sacar?, 4 - Encerrar "))
     
print("Encerrado")