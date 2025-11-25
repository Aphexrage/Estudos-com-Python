# FastAPI - Schemas e Validação com Pydantic

## O que é Pydantic?

Pydantic é uma biblioteca que usa type hints do Python para validação de dados. FastAPI usa Pydantic para validar automaticamente os dados de entrada e saída.

## Por que Schemas são Importantes?

- ✅ Validação automática de tipos
- 📝 Documentação automática
- 🔒 Segurança (validação antes de processar)
- 🎯 Type safety

## Exercício 1: Schemas Básicos

### Objetivo
Criar e usar schemas simples para validação.

### Código Base

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    nome: str
    preco: float

@app.post("/items")
def criar_item(item: Item):
    return item
```

### Exercício Prático

1. Crie um schema `Usuario` com: nome, email, idade
2. Adicione validação: idade deve ser entre 18 e 100
3. Email deve ser válido
4. Nome deve ter pelo menos 3 caracteres

### Solução Esperada

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, validator

app = FastAPI()

class Usuario(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    idade: int = Field(..., ge=18, le=100)
    
    @validator('nome')
    def nome_deve_ter_espaco(cls, v):
        if ' ' not in v:
            raise ValueError('Nome deve conter sobrenome')
        return v.title()

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    return usuario
```

## Exercício 2: Schemas com Relacionamentos

### Objetivo
Criar schemas que se relacionam entre si.

### Exercício Prático

Crie um sistema de blog onde:
- `Post` tem: título, conteúdo, autor_id
- `Autor` tem: nome, email
- `Comentario` tem: post_id, autor, conteúdo

### Solução Esperada

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

class Autor(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr

class Post(BaseModel):
    id: Optional[int] = None
    titulo: str
    conteudo: str
    autor_id: int

class Comentario(BaseModel):
    id: Optional[int] = None
    post_id: int
    autor: str
    conteudo: str

class PostComComentarios(Post):
    comentarios: List[Comentario] = []

@app.post("/posts")
def criar_post(post: Post):
    return post

@app.get("/posts/{post_id}")
def buscar_post_com_comentarios(post_id: int):
    return PostComComentarios(
        id=post_id,
        titulo="Título do Post",
        conteudo="Conteúdo...",
        autor_id=1,
        comentarios=[
            Comentario(id=1, post_id=post_id, autor="João", conteudo="Ótimo post!")
        ]
    )
```

## Exercício 3: Schemas de Request e Response

### Objetivo
Separar schemas de entrada (request) e saída (response).

### Código Base

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    nome: str
    preco: float

class ItemResponse(BaseModel):
    id: int
    nome: str
    preco: float

@app.post("/items", response_model=ItemResponse)
def criar_item(item: ItemCreate):
    return ItemResponse(id=1, **item.dict())
```

### Exercício Prático

Crie schemas separados para:
- `UsuarioCreate` - dados para criar (sem ID)
- `UsuarioUpdate` - dados para atualizar (todos opcionais)
- `UsuarioResponse` - dados retornados (com ID e data_criacao)

### Solução Esperada

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI()

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

class UsuarioResponse(UsuarioBase):
    id: int
    data_criacao: datetime
    
    class Config:
        orm_mode = True

@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate):
    return UsuarioResponse(
        id=1,
        nome=usuario.nome,
        email=usuario.email,
        data_criacao=datetime.now()
    )

@app.patch("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    dados_atualizados = usuario.dict(exclude_unset=True)
    return UsuarioResponse(
        id=usuario_id,
        nome=dados_atualizados.get("nome", "Nome Padrão"),
        email=dados_atualizados.get("email", "email@exemplo.com"),
        data_criacao=datetime.now()
    )
```

## Exercício 4: Validação Customizada

### Objetivo
Criar validadores customizados para regras de negócio.

### Exercício Prático

Crie um schema `Produto` com:
- Nome (obrigatório, 3-50 caracteres)
- Preço (deve ser positivo)
- Categoria (deve ser uma das: eletrônicos, roupas, livros)
- SKU (deve ter formato: ABC-1234)

### Solução Esperada

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Literal
import re

app = FastAPI()

CATEGORIAS_VALIDAS = ["eletronicos", "roupas", "livros"]

class Produto(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    preco: float = Field(..., gt=0)
    categoria: str
    sku: str
    
    @validator('categoria')
    def categoria_valida(cls, v):
        if v.lower() not in CATEGORIAS_VALIDAS:
            raise ValueError(f'Categoria deve ser uma de: {", ".join(CATEGORIAS_VALIDAS)}')
        return v.lower()
    
    @validator('sku')
    def sku_formato_valido(cls, v):
        pattern = r'^[A-Z]{3}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError('SKU deve ter formato ABC-1234')
        return v.upper()
    
    @validator('preco')
    def preco_deve_ser_razoavel(cls, v):
        if v > 10000:
            raise ValueError('Preço muito alto!')
        return round(v, 2)

@app.post("/produtos")
def criar_produto(produto: Produto):
    return produto
```

## Exercício 5: Schemas Aninhados e Listas

### Objetivo
Trabalhar com estruturas de dados complexas.

### Exercício Prático

Crie um schema `Pedido` que contém:
- Lista de itens (cada item tem produto_id e quantidade)
- Endereço de entrega (rua, cidade, CEP)
- Informações do cliente

### Solução Esperada

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

app = FastAPI()

class Endereco(BaseModel):
    rua: str
    numero: str
    cidade: str
    cep: str
    complemento: str = ""

class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: float

class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str

class Pedido(BaseModel):
    cliente: Cliente
    itens: List[ItemPedido] = Field(..., min_items=1)
    endereco_entrega: Endereco
    observacoes: str = ""
    
    @property
    def total(self):
        return sum(item.preco_unitario * item.quantidade for item in self.itens)

class PedidoResponse(Pedido):
    id: int
    data_criacao: datetime
    status: str = "pendente"
    total: float

@app.post("/pedidos", response_model=PedidoResponse)
def criar_pedido(pedido: Pedido):
    return PedidoResponse(
        id=1,
        cliente=pedido.cliente,
        itens=pedido.itens,
        endereco_entrega=pedido.endereco_entrega,
        observacoes=pedido.observacoes,
        data_criacao=datetime.now(),
        total=pedido.total
    )
```

## Desafio Final

Crie um sistema completo de e-commerce com schemas para:
- Produtos (com variações: cor, tamanho)
- Carrinho de compras
- Checkout
- Histórico de pedidos

Implemente todas as validações necessárias.

## Próximo Passo

Avançar para **04_fastapi_middlewares.md** para aprender sobre middlewares e CORS.

