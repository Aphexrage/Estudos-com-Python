# FastAPI - Rotas e Métodos HTTP

## Métodos HTTP Comuns

- **GET**: Buscar dados (leitura)
- **POST**: Criar novos dados
- **PUT**: Atualizar dados completos
- **PATCH**: Atualizar dados parciais
- **DELETE**: Deletar dados

## Exercício 1: Criando um CRUD Completo

### Objetivo
Implementar todas as operações CRUD (Create, Read, Update, Delete) usando FastAPI.

### Código Base

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    nome: str
    preco: float

items_db: List[Item] = []

@app.get("/items")
def listar_items():
    return items_db
```

### Exercício Prático

Implemente as seguintes rotas:

1. **POST** `/items` - Criar um novo item
2. **GET** `/items/{item_id}` - Buscar um item específico
3. **PUT** `/items/{item_id}` - Atualizar um item completo
4. **PATCH** `/items/{item_id}` - Atualizar parcialmente um item
5. **DELETE** `/items/{item_id}` - Deletar um item

### Solução Esperada

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float

class ItemUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None

items_db: List[Item] = []
next_id = 1

@app.post("/items", status_code=201)
def criar_item(item: Item):
    global next_id
    item.id = next_id
    next_id += 1
    items_db.append(item)
    return item

@app.get("/items")
def listar_items():
    return items_db

@app.get("/items/{item_id}")
def buscar_item(item_id: int):
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@app.put("/items/{item_id}")
def atualizar_item(item_id: int, item: Item):
    index = next((i for i, it in enumerate(items_db) if it.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item.id = item_id
    items_db[index] = item
    return item

@app.patch("/items/{item_id}")
def atualizar_item_parcial(item_id: int, item_update: ItemUpdate):
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    if item_update.nome is not None:
        item.nome = item_update.nome
    if item_update.preco is not None:
        item.preco = item_update.preco
    
    return item

@app.delete("/items/{item_id}", status_code=204)
def deletar_item(item_id: int):
    global items_db
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    items_db = [i for i in items_db if i.id != item_id]
    return None
```

## Exercício 2: Rotas com Múltiplos Métodos

### Objetivo
Aprender a usar o mesmo path com diferentes métodos HTTP.

### Exercício Prático

Crie um sistema de usuários onde:
- `GET /usuarios` - Lista todos
- `POST /usuarios` - Cria novo
- `GET /usuarios/{id}` - Busca um
- `PUT /usuarios/{id}` - Atualiza
- `DELETE /usuarios/{id}` - Deleta

### Solução Esperada

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    idade: int

usuarios_db: List[Usuario] = []
next_id = 1

@app.get("/usuarios")
def listar_usuarios():
    return usuarios_db

@app.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuario):
    global next_id
    usuario.id = next_id
    next_id += 1
    usuarios_db.append(usuario)
    return usuario

@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    usuario = next((u for u in usuarios_db if u.id == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    index = next((i for i, u in enumerate(usuarios_db) if u.id == usuario_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.id = usuario_id
    usuarios_db[index] = usuario
    return usuario

@app.delete("/usuarios/{usuario_id}", status_code=204)
def deletar_usuario(usuario_id: int):
    global usuarios_db
    usuario = next((u for u in usuarios_db if u.id == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuarios_db = [u for u in usuarios_db if u.id != usuario_id]
    return None
```

## Exercício 3: Status Codes e Respostas Customizadas

### Objetivo
Aprender a controlar status codes HTTP e criar respostas customizadas.

### Código Base

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/items")
def criar_item():
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Item criado com sucesso"}
    )
```

### Exercício Prático

1. Crie uma rota que retorna 201 quando cria com sucesso
2. Retorne 404 quando não encontra
3. Retorne 400 quando há erro de validação
4. Retorne 200 quando atualiza com sucesso

### Solução Esperada

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Produto(BaseModel):
    nome: str
    preco: float

produtos = []

@app.post("/produtos", status_code=status.HTTP_201_CREATED)
def criar_produto(produto: Produto):
    if produto.preco < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preço não pode ser negativo"
        )
    produtos.append(produto)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Produto criado com sucesso",
            "produto": produto.dict()
        }
    )

@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    if produto_id < 0 or produto_id >= len(produtos):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return produtos[produto_id]
```

## Exercício 4: Rotas Aninhadas e Prefixos

### Objetivo
Organizar rotas usando prefixos e routers.

### Código Base

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter(prefix="/api/v1")

@router.get("/items")
def list_items():
    return {"items": []}

app.include_router(router)
```

### Exercício Prático

Crie uma estrutura de rotas organizada:
- `/api/v1/usuarios` - Operações de usuários
- `/api/v1/produtos` - Operações de produtos
- `/api/v1/pedidos` - Operações de pedidos

### Solução Esperada

```python
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List

app = FastAPI()

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])
produtos_router = APIRouter(prefix="/produtos", tags=["produtos"])
pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

class Usuario(BaseModel):
    id: int
    nome: str

class Produto(BaseModel):
    id: int
    nome: str
    preco: float

class Pedido(BaseModel):
    id: int
    usuario_id: int
    produto_id: int

@usuarios_router.get("")
def listar_usuarios():
    return [{"id": 1, "nome": "João"}]

@produtos_router.get("")
def listar_produtos():
    return [{"id": 1, "nome": "Produto A", "preco": 99.99}]

@pedidos_router.get("")
def listar_pedidos():
    return [{"id": 1, "usuario_id": 1, "produto_id": 1}]

app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(produtos_router, prefix="/api/v1")
app.include_router(pedidos_router, prefix="/api/v1")
```

## Desafio Final

Crie uma API completa de blog com:
- Posts (título, conteúdo, autor, data)
- Comentários (post_id, autor, conteúdo)
- Categorias

Use routers para organizar e implemente todas as operações CRUD.

## Próximo Passo

Avançar para **03_fastapi_schemas.md** para dominar validação de dados com Pydantic.

