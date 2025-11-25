# FastAPI - Middlewares e CORS

## O que são Middlewares?

Middlewares são funções que processam requisições antes que cheguem às rotas e processam respostas antes de serem enviadas. Eles são úteis para:
- Logging
- Autenticação
- CORS
- Rate limiting
- Processamento de erros

## CORS (Cross-Origin Resource Sharing)

CORS permite que um frontend em um domínio faça requisições para uma API em outro domínio. Sem CORS, o navegador bloqueia essas requisições por segurança.

## Exercício 1: Configurando CORS

### Objetivo
Configurar CORS corretamente no FastAPI.

### Código Base

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Exercício Prático

1. Configure CORS para permitir apenas `http://localhost:3000`
2. Permita apenas métodos GET e POST
3. Permita apenas headers Content-Type e Authorization

### Solução Esperada

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

## Exercício 2: Criando Middleware Customizado

### Objetivo
Criar um middleware para logging de requisições.

### Código Base

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {process_time:.3f}s")
    return response
```

### Exercício Prático

Crie um middleware que:
1. Registra todas as requisições com timestamp
2. Adiciona um header `X-Process-Time` na resposta
3. Bloqueia requisições sem User-Agent

### Solução Esperada

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import time
from datetime import datetime

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    if not request.headers.get("user-agent"):
        raise HTTPException(status_code=400, detail="User-Agent obrigatório")
    
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/")
def root():
    return {"message": "Hello"}
```

## Exercício 3: Middleware de Autenticação

### Objetivo
Criar um middleware que valida tokens de autenticação.

### Exercício Prático

Crie um middleware que:
1. Verifica se a rota requer autenticação
2. Valida o token no header Authorization
3. Adiciona informações do usuário ao request.state

### Solução Esperada

```python
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

app = FastAPI()
security = HTTPBearer()

ROTAS_PUBLICAS = ["/", "/docs", "/openapi.json", "/login"]

def verificar_token(token: str) -> dict:
    tokens_validos = {
        "abc123": {"user_id": 1, "nome": "João"},
        "def456": {"user_id": 2, "nome": "Maria"}
    }
    return tokens_validos.get(token)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ROTAS_PUBLICAS:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação necessário"
        )
    
    token = auth_header.split("Bearer ")[1]
    usuario = verificar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    request.state.usuario = usuario
    return await call_next(request)

@app.get("/")
def root():
    return {"message": "Público"}

@app.get("/protegido")
def rota_protegida(request: Request):
    usuario = request.state.usuario
    return {"message": f"Olá {usuario['nome']}", "user_id": usuario["user_id"]}
```

## Exercício 4: Rate Limiting

### Objetivo
Criar um middleware que limita requisições por IP.

### Exercício Prático

Crie um middleware que:
1. Limita a 10 requisições por minuto por IP
2. Retorna 429 (Too Many Requests) quando exceder
3. Adiciona headers informando o limite

### Solução Esperada

```python
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from collections import defaultdict
from datetime import datetime, timedelta
import time

app = FastAPI()

rate_limits = defaultdict(list)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = datetime.now()
    
    rate_limits[client_ip] = [
        req_time for req_time in rate_limits[client_ip]
        if now - req_time < timedelta(minutes=1)
    ]
    
    if len(rate_limits[client_ip]) >= 10:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Muitas requisições. Tente novamente em 1 minuto."},
            headers={
                "X-RateLimit-Limit": "10",
                "X-RateLimit-Remaining": "0",
                "Retry-After": "60"
            }
        )
    
    rate_limits[client_ip].append(now)
    remaining = 10 - len(rate_limits[client_ip])
    
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = "10"
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    
    return response

@app.get("/")
def root():
    return {"message": "Hello"}
```

## Exercício 5: Error Handling Middleware

### Objetivo
Criar um middleware que trata erros globalmente.

### Exercício Prático

Crie um middleware que:
1. Captura todas as exceções
2. Registra erros em um log
3. Retorna respostas de erro padronizadas

### Solução Esperada

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_id = f"ERR-{int(time.time())}"
    
    print(f"[ERROR {error_id}] {exc.__class__.__name__}: {str(exc)}")
    print(traceback.format_exc())
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_id": error_id,
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error_id": error_id,
            "detail": "Erro interno do servidor",
            "type": exc.__class__.__name__
        }
    )

@app.get("/erro")
def causar_erro():
    raise ValueError("Este é um erro de teste")

@app.get("/http-erro")
def causar_http_erro():
    raise HTTPException(status_code=404, detail="Recurso não encontrado")
```

## Desafio Final

Crie um sistema completo de middlewares que:
1. Faz logging estruturado de todas as requisições
2. Implementa autenticação JWT
3. Rate limiting por usuário (não apenas IP)
4. Tratamento global de erros
5. Adiciona headers de segurança (X-Content-Type-Options, etc.)

## Próximo Passo

Avançar para **05_fastapi_arquivos_estaticos.md** para aprender a servir arquivos estáticos.

