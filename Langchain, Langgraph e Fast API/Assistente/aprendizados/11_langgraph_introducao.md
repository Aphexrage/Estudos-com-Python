# LangGraph - Introdução

## O que é LangGraph?

LangGraph é uma biblioteca para construir aplicações stateful com LLMs usando grafos. Permite criar fluxos complexos onde o estado é mantido entre nodes.

## Conceitos Fundamentais

- **Nodes**: Funções que processam o estado
- **Edges**: Conexões que definem o fluxo entre nodes
- **State**: Dados compartilhados entre nodes
- **Graph**: Estrutura completa do fluxo

## Instalação

```bash
pip install langgraph
```

## Exercício 1: Primeiro Grafo

### Objetivo
Criar um grafo simples com 3 nodes.

### Solução

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    mensagem: str
    resultado: str

def entrada(state: State) -> State:
    return {"mensagem": state.get("mensagem", "Olá")}

def processamento(state: State) -> State:
    mensagem = state["mensagem"]
    return {"resultado": f"Processado: {mensagem.upper()}"}

def saida(state: State) -> State:
    print(state["resultado"])
    return state

workflow = StateGraph(State)
workflow.add_node("entrada", entrada)
workflow.add_node("processamento", processamento)
workflow.add_node("saida", saida)

workflow.set_entry_point("entrada")
workflow.add_edge("entrada", "processamento")
workflow.add_edge("processamento", "saida")
workflow.add_edge("saida", END)

app = workflow.compile()

resultado = app.invoke({"mensagem": "Teste"})
```

## Exercício 2: Grafo com Condicionais

### Objetivo
Criar um grafo que toma decisões.

### Solução

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class State(TypedDict):
    pergunta: str
    tipo: Literal["simples", "complexa"]
    resposta: str

def classificar(state: State) -> State:
    pergunta = state["pergunta"]
    tipo = "complexa" if len(pergunta.split()) > 5 else "simples"
    return {"tipo": tipo}

def responder_simples(state: State) -> State:
    return {"resposta": f"Resposta simples para: {state['pergunta']}"}

def responder_complexa(state: State) -> State:
    return {"resposta": f"Resposta detalhada para: {state['pergunta']}"}

def rotear(state: State) -> Literal["simples", "complexa"]:
    return state["tipo"]

workflow = StateGraph(State)
workflow.add_node("classificar", classificar)
workflow.add_node("simples", responder_simples)
workflow.add_node("complexa", responder_complexa)

workflow.set_entry_point("classificar")
workflow.add_conditional_edges("classificar", rotear)
workflow.add_edge("simples", END)
workflow.add_edge("complexa", END)

app = workflow.compile()
resultado = app.invoke({"pergunta": "Como funciona?"})
```

## Exercício 3: Loops e Ciclos

### Objetivo
Implementar iterações no grafo.

### Solução

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    numero: int
    iteracoes: int
    resultado: int

def processar(state: State) -> State:
    numero = state["numero"]
    iteracoes = state.get("iteracoes", 0) + 1
    resultado = numero * 2
    
    return {
        "numero": resultado,
        "iteracoes": iteracoes,
        "resultado": resultado
    }

def verificar_parada(state: State) -> Literal["continuar", "parar"]:
    if state["iteracoes"] >= 3 or state["resultado"] > 100:
        return "parar"
    return "continuar"

workflow = StateGraph(State)
workflow.add_node("processar", processar)
workflow.set_entry_point("processar")
workflow.add_conditional_edges("processar", verificar_parada, {
    "continuar": "processar",
    "parar": END
})

app = workflow.compile()
resultado = app.invoke({"numero": 5, "iteracoes": 0})
```

## Exercício 4: State Management

### Objetivo
Gerenciar estado complexo.

### Solução

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class State(TypedDict):
    historico: List[str]
    contexto: dict
    etapa_atual: str

def coletar_info(state: State) -> State:
    historico = state.get("historico", [])
    historico.append("Informações coletadas")
    return {
        "historico": historico,
        "contexto": {"info": "dados coletados"},
        "etapa_atual": "processamento"
    }

def processar(state: State) -> State:
    historico = state["historico"]
    historico.append("Processamento concluído")
    return {
        "historico": historico,
        "etapa_atual": "finalizado"
    }

workflow = StateGraph(State)
workflow.add_node("coletar", coletar_info)
workflow.add_node("processar", processar)

workflow.set_entry_point("coletar")
workflow.add_edge("coletar", "processar")
workflow.add_edge("processar", END)

app = workflow.compile()
resultado = app.invoke({"historico": [], "contexto": {}, "etapa_atual": ""})
```

## Exercício 5: Human-in-the-Loop

### Objetivo
Pausar para entrada do usuário.

### Solução

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    pergunta: str
    resposta_usuario: str
    finalizado: bool

def fazer_pergunta(state: State) -> State:
    print(f"Pergunta: {state['pergunta']}")
    return {"finalizado": False}

def aguardar_resposta(state: State) -> State:
    resposta = input("Sua resposta: ")
    return {"resposta_usuario": resposta, "finalizado": True}

workflow = StateGraph(State)
workflow.add_node("perguntar", fazer_pergunta)
workflow.add_node("aguardar", aguardar_resposta)

workflow.set_entry_point("perguntar")
workflow.add_edge("perguntar", "aguardar")
workflow.add_edge("aguardar", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
resultado = app.invoke(
    {"pergunta": "Qual é seu nome?", "finalizado": False},
    config=config
)
```

## Desafio

Construa um assistente de vendas completo com todas as etapas mencionadas.

## Próximo Passo

Avançar para **12_langgraph_grafos.md** para aprender a construir grafos mais complexos.

