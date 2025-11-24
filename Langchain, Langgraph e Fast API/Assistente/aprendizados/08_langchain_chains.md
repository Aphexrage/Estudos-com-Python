# LangChain - Chains e Operador Pipe

## O que são Chains?

Chains conectam múltiplos componentes do LangChain em sequência. O operador pipe (`|`) é a forma moderna de criar chains.

## Operador Pipe

O operador `|` permite criar chains de forma intuitiva:
```python
chain = prompt | llm | output_parser
```

## Exercício 1: Chain Básica

### Objetivo
Criar sua primeira chain usando o operador pipe.

### Código Base

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("human", "{pergunta}")
])

llm = ChatOpenAI()

chain = prompt | llm

response = chain.invoke({"pergunta": "Olá!"})
print(response.content)
```

### Exercício Prático

1. Crie uma chain que traduz texto
2. Crie uma chain que resume texto
3. Crie uma chain que responde perguntas

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# Chain de tradução
prompt_traducao = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional."),
    ("human", "Traduza para {idioma}: {texto}")
])

chain_traducao = prompt_traducao | llm

traducao = chain_traducao.invoke({
    "idioma": "inglês",
    "texto": "Bom dia!"
})
print(traducao.content)

# Chain de resumo
prompt_resumo = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em resumos."),
    ("human", "Resuma em 3 frases: {texto}")
])

chain_resumo = prompt_resumo | llm

resumo = chain_resumo.invoke({
    "texto": "Aqui vai um texto muito longo..."
})
print(resumo.content)
```

## Exercício 2: Chain com Múltiplos Passos

### Objetivo
Criar chains que processam informações em múltiplas etapas.

### Exercício Prático

Crie uma chain que:
1. Recebe um tópico
2. Gera um esboço
3. Expande cada ponto do esboço

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI()

# Passo 1: Gerar esboço
prompt_esboco = ChatPromptTemplate.from_messages([
    ("system", "Você é um escritor profissional."),
    ("human", "Crie um esboço com 5 pontos principais sobre: {topico}")
])

# Passo 2: Expandir cada ponto
prompt_expandir = ChatPromptTemplate.from_messages([
    ("system", "Você é um escritor profissional."),
    ("human", "Expanda o seguinte ponto do esboço em 2-3 parágrafos:\n\n{ponto}")
])

def criar_esboco(inputs):
    chain_esboco = prompt_esboco | llm
    esboco = chain_esboco.invoke(inputs)
    return {"esboco": esboco.content, "topico": inputs["topico"]}

def expandir_pontos(inputs):
    pontos = inputs["esboco"].split("\n")
    pontos = [p.strip() for p in pontos if p.strip() and p.strip()[0].isdigit()]
    
    chain_expandir = prompt_expandir | llm
    expandido = []
    
    for ponto in pontos[:3]:  # Primeiros 3 pontos
        resultado = chain_expandir.invoke({"ponto": ponto})
        expandido.append(f"{ponto}\n\n{resultado.content}\n")
    
    return {"conteudo_final": "\n".join(expandido)}

chain_completa = (
    RunnablePassthrough() 
    | criar_esboco 
    | expandir_pontos
)

resultado = chain_completa.invoke({"topico": "inteligência artificial"})
print(resultado["conteudo_final"])
```

## Exercício 3: Chain com Memória

### Objetivo
Criar chains que mantêm contexto entre chamadas.

### Exercício Prático

Crie um assistente conversacional que lembra do que foi dito anteriormente.

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI()

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente amigável. Mantenha o contexto da conversa."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

def criar_chain_com_memoria():
    def chain_func(inputs):
        # Adiciona mensagem do usuário à memória
        memory.chat_memory.add_user_message(inputs["input"])
        
        # Busca histórico
        history = memory.chat_memory.messages
        
        # Invoca chain
        chain = prompt | llm
        response = chain.invoke({
            "input": inputs["input"],
            "history": history
        })
        
        # Adiciona resposta à memória
        memory.chat_memory.add_ai_message(response.content)
        
        return response.content
    
    return chain_func

chain = criar_chain_com_memoria()

print(chain({"input": "Meu nome é João"}))
print(chain({"input": "Qual é o meu nome?"}))
print(chain({"input": "O que eu te falei antes?"}))
```

## Exercício 4: Chain com Condicionais

### Objetivo
Criar chains que tomam decisões baseadas em condições.

### Exercício Prático

Crie um sistema que decide qual especialista usar baseado no tipo de pergunta.

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableBranch

llm = ChatOpenAI()

def classificar_pergunta(pergunta: str) -> str:
    prompt_classificar = ChatPromptTemplate.from_messages([
        ("system", "Classifique a pergunta como: programacao, ciencia, ou geral"),
        ("human", "Pergunta: {pergunta}\n\nResponda apenas com uma palavra: programacao, ciencia ou geral")
    ])
    
    chain = prompt_classificar | llm
    resultado = chain.invoke({"pergunta": pergunta})
    return resultado.content.lower().strip()

prompt_programacao = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em programação."),
    ("human", "{pergunta}")
])

prompt_ciencia = ChatPromptTemplate.from_messages([
    ("system", "Você é um cientista."),
    ("human", "{pergunta}")
])

prompt_geral = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente geral."),
    ("human", "{pergunta}")
])

chain_programacao = prompt_programacao | llm
chain_ciencia = prompt_ciencia | llm
chain_geral = prompt_geral | llm

def rotear_pergunta(inputs):
    pergunta = inputs["pergunta"]
    tipo = classificar_pergunta(pergunta)
    
    if "programacao" in tipo:
        return chain_programacao.invoke({"pergunta": pergunta})
    elif "ciencia" in tipo:
        return chain_ciencia.invoke({"pergunta": pergunta})
    else:
        return chain_geral.invoke({"pergunta": pergunta})

perguntas = [
    "Como funciona o Python?",
    "O que é a teoria da relatividade?",
    "Qual é a capital do Brasil?"
]

for pergunta in perguntas:
    resposta = rotear_pergunta({"pergunta": pergunta})
    print(f"P: {pergunta}")
    print(f"R: {resposta.content}\n")
```

## Exercício 5: Chain Paralela

### Objetivo
Processar múltiplas tarefas em paralelo.

### Exercício Prático

Crie um sistema que analisa um texto de múltiplas formas simultaneamente:
- Sentimento
- Tópicos principais
- Resumo

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI()

prompt_sentimento = ChatPromptTemplate.from_messages([
    ("system", "Analise o sentimento do texto: positivo, negativo ou neutro."),
    ("human", "{texto}")
])

prompt_topicos = ChatPromptTemplate.from_messages([
    ("system", "Identifique os 3 tópicos principais do texto."),
    ("human", "{texto}")
])

prompt_resumo = ChatPromptTemplate.from_messages([
    ("system", "Crie um resumo conciso do texto."),
    ("human", "{texto}")
])

chain_sentimento = prompt_sentimento | llm
chain_topicos = prompt_topicos | llm
chain_resumo = prompt_resumo | llm

chain_paralela = RunnableParallel({
    "sentimento": chain_sentimento,
    "topicos": chain_topicos,
    "resumo": chain_resumo
})

texto = """
A inteligência artificial está revolucionando diversos setores.
Empresas estão adotando IA para melhorar eficiência e inovação.
No entanto, há preocupações sobre privacidade e emprego.
"""

resultado = chain_paralela.invoke({"texto": texto})

print("Sentimento:", resultado["sentimento"].content)
print("Tópicos:", resultado["topicos"].content)
print("Resumo:", resultado["resumo"].content)
```

## Desafio Final

Crie um sistema de análise de documentos que:
1. Recebe um documento
2. Extrai informações (entidades, datas, pessoas)
3. Gera resumo executivo
4. Identifica tópicos principais
5. Sugere ações
6. Tudo em uma única chain

## Próximo Passo

Avançar para **09_langchain_modelos.md** para aprender sobre diferentes modelos LLM.

