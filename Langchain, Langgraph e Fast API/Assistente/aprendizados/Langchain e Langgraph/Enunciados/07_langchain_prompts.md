# LangChain - Prompts e Templates

## O que são Prompts?

Prompts são instruções dadas ao LLM para guiar seu comportamento. Um bom prompt é essencial para obter resultados úteis.

## ChatPromptTemplate

O `ChatPromptTemplate` permite criar prompts estruturados com diferentes tipos de mensagens (System, Human, AI).

## Exercício 1: Criando Prompts Básicos

### Objetivo
Aprender a criar e usar templates de prompts.

### Código Base

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente útil."),
    ("human", "{pergunta}")
])

llm = ChatOpenAI()
chain = prompt | llm

response = chain.invoke({"pergunta": "Olá!"})
print(response.content)
```

### Exercício Prático

1. Crie um prompt para um tradutor
2. Crie um prompt para um resumidor de textos
3. Crie um prompt para um gerador de código

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# Tradutor
prompt_tradutor = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional. Traduza o texto mantendo o tom e estilo original."),
    ("human", "Traduza para {idioma}: {texto}")
])

chain_tradutor = prompt_tradutor | llm
traducao = chain_tradutor.invoke({
    "idioma": "inglês",
    "texto": "Olá, como você está?"
})
print("Tradução:", traducao.content)

# Resumidor
prompt_resumidor = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em resumir textos. Crie resumos concisos e informativos."),
    ("human", "Resuma o seguinte texto em {numero_palavras} palavras:\n\n{texto}")
])

chain_resumidor = prompt_resumidor | llm
resumo = chain_resumidor.invoke({
    "numero_palavras": 50,
    "texto": "Aqui vai um texto muito longo que precisa ser resumido..."
})
print("Resumo:", resumo.content)

# Gerador de código
prompt_codigo = ChatPromptTemplate.from_messages([
    ("system", "Você é um programador experiente. Gere código limpo e bem documentado."),
    ("human", "Crie uma função em {linguagem} que {descricao}")
])

chain_codigo = prompt_codigo | llm
codigo = chain_codigo.invoke({
    "linguagem": "Python",
    "descricao": "calcula o fatorial de um número"
})
print("Código:", codigo.content)
```

## Exercício 2: Prompts com Múltiplas Variáveis

### Objetivo
Criar prompts complexos com várias variáveis.

### Exercício Prático

Crie um gerador de emails profissionais que aceita:
- Nome do destinatário
- Assunto
- Tipo de email (formal, casual, etc.)
- Informações adicionais

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

prompt_email = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente especializado em escrever emails profissionais.
    Adapte o tom conforme o tipo solicitado (formal, casual, amigável)."""),
    ("human", """Escreva um email {tipo} com as seguintes informações:
    
    Destinatário: {destinatario}
    Assunto: {assunto}
    Informações: {informacoes}
    
    Retorne apenas o corpo do email, sem cabeçalhos.""")
])

chain_email = prompt_email | llm

email = chain_email.invoke({
    "tipo": "formal",
    "destinatario": "Dr. Silva",
    "assunto": "Solicitação de reunião",
    "informacoes": "Gostaria de agendar uma reunião para discutir o projeto X na próxima semana."
})

print(email.content)
```

## Exercício 3: Few-Shot Learning

### Objetivo
Usar exemplos no prompt para ensinar o modelo o padrão desejado.

### Exercício Prático

Crie um classificador de sentimentos usando few-shot learning.

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

examples = [
    {"input": "Adorei o filme!", "output": "positivo"},
    {"input": "Que filme terrível.", "output": "negativo"},
    {"input": "O filme estava ok.", "output": "neutro"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um classificador de sentimentos. Classifique como: positivo, negativo ou neutro."),
    few_shot_prompt,
    ("human", "{input}")
])

chain = final_prompt | llm

testes = [
    "Estou muito feliz hoje!",
    "Que dia horrível.",
    "Tudo normal por aqui."
]

for teste in testes:
    response = chain.invoke({"input": teste})
    print(f"'{teste}' -> {response.content}")
```

## Exercício 4: Prompts com Condicionais

### Objetivo
Criar prompts que se adaptam baseado em condições.

### Exercício Prático

Crie um sistema que gera diferentes tipos de conteúdo baseado em parâmetros.

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

def gerar_conteudo(tipo: str, topico: str, estilo: str = "neutro"):
    estilos = {
        "formal": "Use linguagem formal e técnica",
        "casual": "Use linguagem casual e acessível",
        "criativo": "Use linguagem criativa e envolvente"
    }
    
    instrucoes_estilo = estilos.get(estilo, estilos["neutro"])
    
    if tipo == "artigo":
        system_msg = f"Você é um escritor profissional. {instrucoes_estilo}. Escreva artigos informativos."
        human_msg = "Escreva um artigo sobre: {topico}"
    elif tipo == "resumo":
        system_msg = f"Você é um especialista em resumos. {instrucoes_estilo}."
        human_msg = "Crie um resumo sobre: {topico}"
    else:
        system_msg = f"Você é um assistente. {instrucoes_estilo}."
        human_msg = "Fale sobre: {topico}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", human_msg)
    ])
    
    chain = prompt | llm
    return chain.invoke({"topico": topico})

# Testes
print(gerar_conteudo("artigo", "inteligência artificial", "formal").content)
print(gerar_conteudo("resumo", "inteligência artificial", "casual").content)
```

## Exercício 5: Prompts com Output Parsers

### Objetivo
Estruturar a saída do LLM em formatos específicos.

### Exercício Prático

Crie um sistema que extrai informações estruturadas usando output parsers.

### Solução Esperada

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

class Receita(BaseModel):
    nome: str = Field(description="Nome da receita")
    ingredientes: List[str] = Field(description="Lista de ingredientes")
    passos: List[str] = Field(description="Passos de preparo")
    tempo_preparo: int = Field(description="Tempo em minutos")

llm = ChatOpenAI()
parser = PydanticOutputParser(pydantic_object=Receita)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um chef de cozinha. 
    {format_instructions}"""),
    ("human", "Crie uma receita de {prato}")
])

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

receita = chain.invoke({"prato": "lasanha"})
print(f"Nome: {receita.nome}")
print(f"Ingredientes: {', '.join(receita.ingredientes)}")
print(f"Tempo: {receita.tempo_preparo} minutos")
```

## Desafio Final

Crie um sistema de geração de conteúdo que:
- Aceita tipo de conteúdo (artigo, post, email)
- Aceita público-alvo (técnico, geral, crianças)
- Aceita tom (formal, casual, humorístico)
- Gera conteúdo personalizado
- Retorna em formato estruturado

## Próximo Passo

Avançar para **08_langchain_chains.md** para aprender sobre chains e o operador pipe.

