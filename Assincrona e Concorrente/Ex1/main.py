# Teste para entender os conceitos

import asyncio
import time

async def funcao1():
    print("A")
    await asyncio.sleep(10)
    print("B")

def funcao2():
    print("funcao ainda esta rodando")

async def funcao3():
    inicio = time.time()

    while True:
        decorrido = int(time.time() - inicio)
        print(f"Tempo decorrido: {decorrido}s")
        await asyncio.sleep(1)

async def main():
    task1 = asyncio.create_task(funcao1())  
    task3 = asyncio.create_task(funcao3())

    await asyncio.sleep(0)
    funcao2()
    await task1

    task3.cancel()
    try:
        await task3
    except asyncio.CancelledError:
        pass

asyncio.run(main())
