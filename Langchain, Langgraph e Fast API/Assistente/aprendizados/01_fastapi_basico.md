# FastAPI - Primeiros Passos

## O que é FastAPI?

FastAPI é um framework web moderno e rápido para construir APIs REST em Python. Ele é baseado em padrões Python modernos e oferece validação automática de dados, documentação interativa e alta performance.

## Por que FastAPI?

- ⚡ **Rápido**: Uma das frameworks mais rápidas disponíveis
- 📝 **Documentação automática**: Swagger UI e ReDoc incluídos
- ✅ **Validação automática**: Usa Pydantic para validar dados
- 🔒 **Type hints**: Suporte completo a type hints do Python
- 🚀 **ASGI**: Suporte nativo a async/await

## Exercício 1: Criando sua primeira API

### Objetivo
Criar um servidor FastAPI básico com uma rota simples.

### Código Base

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Olá, FastAPI!"}
```

### Como executar

```bash
uvicorn main:app --reload
```

Acesse: `http://localhost:8000`

### Exercício Prático

1. Crie um arquivo `exercicio_01.py`
2. Adicione uma rota `/saudacao` que retorna uma saudação personalizada
3. Adicione uma rota `/info` que retorna informações sobre você
4. Teste no navegador ou usando `curl`

### Solução Esperada

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Olá, FastAPI!"}

@app.get("/saudacao")
def saudacao():
    return {"mensagem": "Bem-vindo à minha API!"}

@app.get("/info")
def info():
    return {
        "nome": "Seu Nome",
        "tecnologia": "FastAPI",
        "versao": "1.0"
    }
```

## Exercício 2: Rotas com Parâmetros

### Objetivo
Aprender a passar parâmetros nas rotas.

### Código Base

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/usuario/{user_id}")
def get_usuario(user_id: int):
    return {"user_id": user_id, "nome": f"Usuário {user_id}"}
```

### Exercício Prático

1. Crie uma rota `/produto/{produto_id}` que retorna informações do produto
2. Crie uma rota `/categoria/{categoria}/produtos` que lista produtos de uma categoria
3. Adicione validação: produto_id deve ser maior que 0

### Solução Esperada

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/produto/{produto_id}")
def get_produto(produto_id: int):
    if produto_id <= 0:
        raise HTTPException(status_code=400, detail="ID deve ser maior que 0")
    return {
        "produto_id": produto_id,
        "nome": f"Produto {produto_id}",
        "preco": 99.99
    }

@app.get("/categoria/{categoria}/produtos")
def get_produtos_categoria(categoria: str):
    return {
        "categoria": categoria,
        "produtos": [
            {"id": 1, "nome": "Produto A"},
            {"id": 2, "nome": "Produto B"}
        ]
    }
```

## Exercício 3: Query Parameters

### Objetivo
Aprender a usar query parameters (parâmetros de consulta).

### Código Base

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### Exercício Prático

1. Crie uma rota `/buscar` que aceita `q` (query) e `tipo` como parâmetros
2. Faça `q` obrigatório e `tipo` opcional com valor padrão "todos"
3. Retorne resultados filtrados baseados nos parâmetros

### Solução Esperada

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/buscar")
def buscar(q: str, tipo: Optional[str] = "todos"):
    resultados = {
        "query": q,
        "tipo": tipo,
        "resultados": [
            {"id": 1, "titulo": f"Resultado para {q}"},
            {"id": 2, "titulo": f"Outro resultado para {q}"}
        ]
    }
    return resultados
```

## Desafio Final

Crie uma API de lista de tarefas (TODO) com:
- GET `/tarefas` - Lista todas as tarefas
- GET `/tarefas/{id}` - Busca uma tarefa específica
- GET `/tarefas?status=pendente` - Filtra por status

Use uma lista em memória para armazenar as tarefas.

### Solução do Desafio

```python
from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str

tarefas_db = [
    Tarefa(id=1, titulo="Aprender FastAPI", descricao="Estudar documentação", status="pendente"),
    Tarefa(id=2, titulo="Criar API", descricao="Implementar endpoints", status="concluida")
]

@app.get("/tarefas")
def listar_tarefas(status: Optional[str] = None):
    if status:
        return [t for t in tarefas_db if t.status == status]
    return tarefas_db

@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int):
    tarefa = next((t for t in tarefas_db if t.id == tarefa_id), None)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa
```

## Próximo Passo

Avançar para **02_fastapi_rotas.md** para aprender sobre métodos HTTP e rotas mais complexas.

