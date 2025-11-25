# FastAPI - Arquivos Estáticos e Frontend

## Servindo Arquivos Estáticos

FastAPI pode servir arquivos estáticos (HTML, CSS, JS, imagens) diretamente, permitindo criar aplicações full-stack.

## Exercício 1: Servindo Arquivos Estáticos Básicos

### Objetivo
Configurar FastAPI para servir arquivos HTML, CSS e JavaScript.

### Código Base

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
```

### Exercício Prático

1. Crie uma pasta `static/` com:
   - `index.html` - página principal
   - `style.css` - estilos
   - `app.js` - JavaScript
2. Configure FastAPI para servir esses arquivos
3. Crie uma página que faz uma requisição à API

### Solução Esperada

**main.py:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/mensagem")
def get_mensagem():
    return {"mensagem": "Olá do backend!"}
```

**static/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Minha App</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Minha Aplicação FastAPI</h1>
    <button id="btnCarregar">Carregar Mensagem</button>
    <div id="resultado"></div>
    <script src="/static/app.js"></script>
</body>
</html>
```

**static/app.js:**
```javascript
document.getElementById('btnCarregar').addEventListener('click', async () => {
    const response = await fetch('/api/mensagem');
    const data = await response.json();
    document.getElementById('resultado').textContent = data.mensagem;
});
```

## Exercício 2: SPA (Single Page Application)

### Objetivo
Criar uma aplicação de página única que se comunica com a API.

### Exercício Prático

Crie uma aplicação de lista de tarefas (TODO) onde:
- Frontend em HTML/CSS/JS
- Backend em FastAPI
- CRUD completo via API

### Solução Esperada

**main.py:**
```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Tarefa(BaseModel):
    id: int
    titulo: str
    concluida: bool = False

tarefas_db: List[Tarefa] = []
next_id = 1

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/tarefas")
def listar_tarefas():
    return tarefas_db

@app.post("/api/tarefas")
def criar_tarefa(tarefa: Tarefa):
    global next_id
    tarefa.id = next_id
    next_id += 1
    tarefas_db.append(tarefa)
    return tarefa

@app.put("/api/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa):
    index = next((i for i, t in enumerate(tarefas_db) if t.id == tarefa_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.id = tarefa_id
    tarefas_db[index] = tarefa
    return tarefa

@app.delete("/api/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    global tarefas_db
    tarefa = next((t for t in tarefas_db if t.id == tarefa_id), None)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefas_db = [t for t in tarefas_db if t.id != tarefa_id]
    return {"message": "Tarefa deletada"}
```

**static/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Tarefas</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Minhas Tarefas</h1>
        <form id="formTarefa">
            <input type="text" id="titulo" placeholder="Nova tarefa..." required>
            <button type="submit">Adicionar</button>
        </form>
        <ul id="listaTarefas"></ul>
    </div>
    <script src="/static/app.js"></script>
</body>
</html>
```

**static/app.js:**
```javascript
let tarefas = [];

async function carregarTarefas() {
    const response = await fetch('/api/tarefas');
    tarefas = await response.json();
    renderizarTarefas();
}

async function criarTarefa(titulo) {
    const response = await fetch('/api/tarefas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: 0, titulo, concluida: false})
    });
    await carregarTarefas();
}

async function atualizarTarefa(tarefa) {
    await fetch(`/api/tarefas/${tarefa.id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(tarefa)
    });
    await carregarTarefas();
}

async function deletarTarefa(id) {
    await fetch(`/api/tarefas/${id}`, {method: 'DELETE'});
    await carregarTarefas();
}

function renderizarTarefas() {
    const lista = document.getElementById('listaTarefas');
    lista.innerHTML = tarefas.map(tarefa => `
        <li class="${tarefa.concluida ? 'concluida' : ''}">
            <input type="checkbox" ${tarefa.concluida ? 'checked' : ''} 
                   onchange="atualizarTarefa({...tarefas.find(t => t.id === ${tarefa.id}), concluida: this.checked})">
            <span>${tarefa.titulo}</span>
            <button onclick="deletarTarefa(${tarefa.id})">Deletar</button>
        </li>
    `).join('');
}

document.getElementById('formTarefa').addEventListener('submit', async (e) => {
    e.preventDefault();
    const titulo = document.getElementById('titulo').value;
    await criarTarefa(titulo);
    document.getElementById('titulo').value = '';
});

window.atualizarTarefa = atualizarTarefa;
window.deletarTarefa = deletarTarefa;

carregarTarefas();
```

## Exercício 3: Upload de Arquivos

### Objetivo
Permitir upload de arquivos através da API.

### Exercício Prático

Crie um sistema de upload onde:
1. Frontend permite selecionar e enviar arquivos
2. Backend salva os arquivos
3. Lista de arquivos enviados é exibida

### Solução Esperada

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": f"/uploads/{file.filename}"}

@app.get("/api/arquivos")
def listar_arquivos():
    arquivos = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    return {"arquivos": arquivos}
```

## Desafio Final

Crie uma aplicação completa de galeria de imagens:
- Upload de imagens
- Listagem de imagens
- Visualização em miniatura
- Deletar imagens
- Interface moderna e responsiva

## Próximo Passo

Avançar para **06_langchain_basico.md** para começar a aprender LangChain.

