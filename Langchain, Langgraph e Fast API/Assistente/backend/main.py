from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemas import PerguntaRequest, PerguntaResponse
from chain import perguntaLLM
import os

app = FastAPI(
    title="Assistente Virtual API",
    description="API para um assistente virtual usando LangChain e OpenAI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/pergunta", response_model=PerguntaResponse)
def pergunta(request: PerguntaRequest):
    resposta = perguntaLLM(request.question)
    return PerguntaResponse(answer=resposta)
