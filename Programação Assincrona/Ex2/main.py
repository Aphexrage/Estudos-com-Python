import asyncio

async def trocandoPneu():
    print("Tirando o pneu do carro")
    await asyncio.sleep(1)
    print("Colocando e parafusando o pneu")
    await asyncio.sleep(1)
    print("Pneus trocados")

async def colocandoCombustivel():
    print("Colocando combustivel")
    await asyncio.sleep(3)
    print("Carro abastecido")
    
async def main():
    await asyncio.gather(trocandoPneu(), colocandoCombustivel())
    
asyncio.run(main())