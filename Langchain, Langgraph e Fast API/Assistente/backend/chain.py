import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Problema no .env e na chave API - Verifique se OPENAI_API_KEY está definida")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
)

prompt = ChatPromptTemplate([
    ("system", "Voce se chama Prototipo e seu papel é apenas conversar com o usuario"),
    ("human", "{question}")
])

chain = prompt | model

def perguntaLLM(question: str) -> str:
    resultado = chain.invoke({"question": question})
    
    if hasattr(resultado, 'content'):
        return resultado.content
    
    if isinstance(resultado, str):
        return resultado
    
    if isinstance(resultado, dict):
        return resultado.get("text", resultado.get("content", str(resultado)))
    
    return str(resultado)
