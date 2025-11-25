# LangChain - Introdução e Conceitos Básicos

## O que é LangChain?

LangChain é um framework para construir aplicações com Large Language Models (LLMs). Ele fornece abstrações e ferramentas para:
- Conectar LLMs a fontes de dados
- Criar chains (cadeias) de processamento
- Gerenciar memória e contexto
- Integrar com ferramentas externas

## Por que LangChain?

- 🔗 **Modularidade**: Componentes reutilizáveis
- 🔄 **Chains**: Conectar múltiplas operações
- 💾 **Memória**: Manter contexto entre interações
- 🛠️ **Ferramentas**: Integrar com APIs, bancos de dados, etc.

## Exercício 1: Primeira Conexão com LLM

### Objetivo
Conectar-se a um modelo LLM usando LangChain.

### Pré-requisitos

```bash
pip install langchain langchain-openai python-dotenv
```

Crie um arquivo `.env`:
```
OPENAI_API_KEY=sua-chave-aqui
```

### Código Base

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

response = llm.invoke("Qual é a capital do Brasil?")
print(response.content)
```

### Exercício Prático

1. Crie uma função que recebe uma pergunta e retorna a resposta
2. Teste com diferentes perguntas
3. Experimente diferentes valores de temperature (0.0, 0.7, 1.0)

### Solução Esperada

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def perguntar_llm(pergunta: str, temperatura: float = 0.7) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperatura)
    response = llm.invoke(pergunta)
    return response.content

# Testes
print(perguntar_llm("Qual é a capital do Brasil?", temperatura=0.0))
print(perguntar_llm("Conte uma piada", temperatura=1.0))
print(perguntar_llm("Explique quantum computing", temperatura=0.7))
```

## Exercício 2: Trabalhando com Mensagens

### Objetivo
Entender como LangChain estrutura mensagens (System, Human, AI).

### Código Base

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI()

messages = [
    SystemMessage(content="Você é um assistente útil."),
    HumanMessage(content="Olá!")
]

response = llm.invoke(messages)
print(response.content)
```

### Exercício Prático

1. Crie um assistente especializado em culinária
2. Faça uma conversa com múltiplas mensagens
3. Mantenha o contexto da conversa

### Solução Esperada

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatOpenAI()

messages = [
    SystemMessage(content="Você é um chef de cozinha experiente. Ajude com receitas e dicas culinárias."),
    HumanMessage(content="Como faço um bolo de chocolate?"),
]

response = llm.invoke(messages)
print("Chef:", response.content)

# Continuar a conversa
messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="E se eu quiser fazer sem açúcar?"))

response2 = llm.invoke(messages)
print("Chef:", response2.content)
```

## Exercício 3: Extraindo Informações Estruturadas

### Objetivo
Fazer o LLM retornar dados estruturados.

### Exercício Prático

Crie uma função que extrai informações de um texto:
- Nome
- Email
- Telefone
- Endereço

### Solução Esperada

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOpenAI(model="gpt-3.5-turbo")

def extrair_informacoes(texto: str) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um extrator de informações. Retorne apenas JSON válido."),
        ("human", """Extraia as seguintes informações do texto abaixo e retorne em formato JSON:
        - nome
        - email
        - telefone
        - endereco
        
        Texto: {texto}""")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"texto": texto})
    
    try:
        return json.loads(response.content)
    except:
        return {"erro": "Não foi possível extrair informações"}

texto = """
Meu nome é João Silva, meu email é joao@email.com,
telefone: (11) 99999-8888, e moro na Rua das Flores, 123, São Paulo.
"""

info = extrair_informacoes(texto)
print(json.dumps(info, indent=2, ensure_ascii=False))
```

## Exercício 4: Stream de Respostas

### Objetivo
Aprender a receber respostas em tempo real (streaming).

### Código Base

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(streaming=True)

for chunk in llm.stream("Conte uma história curta"):
    print(chunk.content, end="", flush=True)
```

### Exercício Prático

Crie uma função que:
1. Faz streaming da resposta
2. Processa cada chunk
3. Retorna a resposta completa

### Solução Esperada

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def perguntar_com_stream(pergunta: str):
    llm = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages([
        ("human", "{pergunta}")
    ])
    
    chain = prompt | llm
    
    resposta_completa = ""
    print("Assistente: ", end="", flush=True)
    
    for chunk in chain.stream({"pergunta": pergunta}):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            resposta_completa += chunk.content
    
    print()  # Nova linha
    return resposta_completa

resposta = perguntar_com_stream("Explique o que é inteligência artificial em 3 parágrafos")
```

## Exercício 5: Tratamento de Erros

### Objetivo
Implementar tratamento robusto de erros com LangChain.

### Exercício Prático

Crie uma função que:
1. Tenta fazer uma requisição ao LLM
2. Trata erros de API
3. Retorna uma mensagem amigável em caso de erro
4. Implementa retry automático

### Solução Esperada

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import time
from openai import APIError

def perguntar_com_retry(pergunta: str, max_tentativas: int = 3) -> str:
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("human", "{pergunta}")
    ])
    
    chain = prompt | llm
    
    for tentativa in range(max_tentativas):
        try:
            response = chain.invoke({"pergunta": pergunta})
            return response.content
        except APIError as e:
            if tentativa == max_tentativas - 1:
                return f"Erro ao processar sua pergunta. Detalhes: {str(e)}"
            print(f"Tentativa {tentativa + 1} falhou. Tentando novamente...")
            time.sleep(2 ** tentativa)  # Backoff exponencial
        except Exception as e:
            return f"Erro inesperado: {str(e)}"
    
    return "Não foi possível obter resposta após várias tentativas."

print(perguntar_com_retry("Qual é a capital da França?"))
```

## Desafio Final

Crie um assistente de linha de comando que:
- Mantém histórico de conversa
- Permite diferentes "personas" (cientista, poeta, etc.)
- Faz streaming das respostas
- Trata erros graciosamente
- Salva o histórico em arquivo

## Próximo Passo

Avançar para **07_langchain_prompts.md** para dominar a criação de prompts eficazes.

