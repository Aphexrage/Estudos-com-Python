import asyncio
import time

async def uploadFoto():
    inicio = time.time()
    print("Descompactando arquivo")
    await asyncio.sleep(1)
    print("Subindo arquivo")
    await asyncio.sleep(3)
    print("Upload feito - Foto")
    
    decorrido = int(time.time() - inicio)
    print(f"Tempo decorrido: {decorrido}s - Foto")
    
async def uploadVideo():
    inicio = time.time()
    print("Descompactando arquivo")
    await asyncio.sleep(1)
    print("Subindo arquivo")
    await asyncio.sleep(5)
    print("Upload feito - Video")
    decorrido = int(time.time() - inicio)
    print(f"Tempo decorrido: {decorrido}s - Video")
    
async def uploadTxt():
    inicio = time.time()
    print("Descompactando arquivo")
    await asyncio.sleep(1)
    print("Subindo arquivo")
    await asyncio.sleep(1)
    print("Upload feito - Arquivo.txt")
    decorrido = int(time.time() - inicio)
    print(f"Tempo decorrido: {decorrido}s - Arquivo.txt")
    
async def main():
    await asyncio.gather(uploadFoto(), uploadVideo(), uploadTxt())
    
asyncio.run(main())