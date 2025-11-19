<a href="#">
  <img 
    width="100%" 
    src="https://capsule-render.vercel.app/api?type=waving&color=0077ff&height=120&section=header&text=&fontSize=30&fontColor=000000&animation=twinkling"
    alt="banner"
  />
</a>

<br>

<p align="center">
  <img 
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2048px-Python-logo-notext.svg.png" 
    alt="Logo Python"
    width="150px"
  />
</p>

# Estudos - Python para AI

Este repositório reúne meu plano de estudos e projetos práticos para dominar:
- Programação Orientada a Objetos (POO) em Python  
- Programação Assíncrona (`asyncio`)  
- Programação Concorrente (threads, multiprocessing, `concurrent.futures`)  
- LangChain (integração LLMs, chains, agents)  
- LangGraph (fluxos/visualização para pipelines de LLMs / agentes)  
- FastAPI (APIs modernas em Python)  
- Insomnia (testes e documentação de APIs)

## Tecnologias utilizadas
<div align="center"> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwTsKBgt67g7V83MUa-6I2Ex33DrnrxBDwMw&s" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRT9FomI3FFt6h_gVY0OQUexneOPmvEnu5f_YSABOnqgCjykwrMivAB38t8H6pyGXngSgo&usqp=CAU" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> <img src="https://miro.medium.com/1*9HFsjXjgw6oG2HwQ3Okgwg.png" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTO4H5JRdhQKQH6T8DzUgKSUeiqz-R91qHY02wn7f-gjmzKmn_uiivgTNb-hhaBY3Is9lQ&usqp=CAU" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> <img src="https://gitlab.com/uploads/-/system/project/avatar/42941426/fastapi.png" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> <img src="https://res.cloudinary.com/apideck/image/upload/v1570527747/catalog/insomnia-rest/icon128x128.jpg" style="width:50px; height:50px; border-radius:50%; margin:8px;" /> </div>

<br>

## Oq vou focar nesse estudo:

### POO (Python)
- Conceitos: classe, instância, atributos, métodos, encapsulamento, herança, composição, polimorfismo.
- Padrões comuns: factory, singleton (quando for apropriado), containers imutáveis.
- Aplicação prática: modelagem de domínios, testes unitários e refatoração orientada a objetos.

### Programação Assíncrona
- `async/await`, coroutines, event loop (`asyncio`).
- `asyncio.gather`, `asyncio.create_task`, `asyncio.run`.
- Como transformar código I/O-bound para não bloquear: websockets, HTTP async, scraping eficiente.

### Programação Concorrente
- Threads (`threading`) para I/O-bound.
- Processos (`multiprocessing`) para CPU-bound (escapar do GIL).
- `concurrent.futures` (ThreadPoolExecutor / ProcessPoolExecutor).
- Concorrência segura: locks, queues, semáforos e patterns para evitar condições de corrida.

### LangChain & LangGraph
- LangChain: arquiteturas de chains, prompts, memory, agents, ferramentas externas.
- LangGraph: modelar visualmente fluxos de LLMs / integração entre nodes (fluxos, conectores e debugging visual).
- Como orquestrar LLMs com dados locais e pipelines replicáveis.

### FastAPI & Insomnia
- FastAPI: endpoints, Pydantic models, dependências, background tasks, autenticação mínima.
- Deploy rápido: uvicorn, configuração básica para produção (gunicorn/uvicorn workers).
- Insomnia: criar collections, testar endpoints, gerar requests e documentar APIs.

---

## Materiais / Bibliografia

### POO (Python)
- **Documentação Oficial Python — Classes**  
  *O que ler*: capítulos sobre classes, métodos especiais e herança.  
  *Como estudo*: leio o capítulo + reescrevo exemplos no REPL + crio 2 mini-classes por 30 minutos (ex.: `Pessoa` / `ContaBancaria`) e escrevo 3 testes simples.
- **Real Python – OOP em Python** (artigos e tutoriais)  
  *Como estudo*: artigo teórico + implementar um pequeno projeto (ex.: gerenciador de tarefas orientado a objetos) e commitar no repo.
- **Vídeo recomendado**: aulas concisas (Corey Schafer / Tech With Tim) para ver exemplos executando.  
  *Como estudo*: assistir com o editor aberto e pausar para digitar o código.
- Achei um site interessante para eu usar com exercicios:
  https://pynative.com/python-object-oriented-programming-oop-exercise/
  https://www.w3resource.com/python-exercises/oop/index.php
  
### Programação Assíncrona
- **Documentação `asyncio` (Python docs)**  
  *Como estudo*: ler introdução e exemplos básicos; executar coroutines no REPL.
- **Real Python – Asyncio tutorial (hands-on)**  
  *Como estudo*: seguir um exemplo (ex.: downloader assíncrono) e adaptar pra 2 APIs públicas.
- **Vídeo prático** (tutorial com exemplos de `async/await`)  
  *Como estudo*: reproduzir exemplo, depois converter função sincrona → assincrona para ver diferença no tempo.

### Programação Concorrente
- **Documentação `threading` e `multiprocessing` (Python docs)**  
  *Como estudo*: entender limitações (GIL) e depois fazer benchmarks simples na minha máquina (soma, I/O fake).
- **Real Python – Concurrency vs Parallelism**  
  *Como estudo*: escolher um problema CPU-bound e resolver com `multiprocessing`, medir speedup.
- **Exemplos práticos**: `concurrent.futures` com ThreadPool/ProcessPool.

### LangChain
- **Doc oficial do LangChain (docs/langchain)**  
  *Como estudo*: seguir tutoriais "getting started", montar uma chain simples que consulta embeddings e responde perguntas a partir de documentos locais.
- **Exercícios**: criar um mini-RAG (Retriever-Augmented Generation) com PDFs ou markdowns do repo.

### LangGraph
- **Repositório/Docs oficiais do LangGraph** (ou material do autor)  
  *Como estudo*: montar visual flow simples que encadeia prompt → verificação → tool-call e rodar em modo debug.

### FastAPI
- **Documentação oficial do FastAPI**  
  *Como estudo*: criar um CRUD simples com Pydantic models, testar com Insomnia.
- **Exemplo prático**: endpoint `/process` que recebe texto, chama uma chain (simulada/local) e retorna resultado.

### Insomnia
- **Docs / GUI do Insomnia**  
  *Como estudo*: criar collection, escrever testes, salvar environment variables (chaves locais), testar endpoints do FastAPI.
  
---

## Bibliografia / Links de referência
- Python docs — Classes, asyncio, threading, multiprocessing, concurrent.futures  
- FastAPI — documentação oficial e tutoriais (Pydantic + dependencies)  
- LangChain — docs e exemplos de RAG / agents  
- LangGraph — docs / repo oficial (visual nodes para flows de LLM)  
- Real Python — artigos sobre OOP, Async e Concurrency  
- Vídeos: Corey Schafer, Tech With Tim, freeCodeCamp (playlists focadas em OOP e Async)  
- Insomnia — docs oficiais e guias de Collections

<p align="center">
  <img 
    src="https://capsule-render.vercel.app/api?type=waving&color=ffff00&height=80&section=footer"
    width="100%" 
    alt="rodapé"
  />
</p>

