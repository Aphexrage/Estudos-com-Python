from pydantic import BaseModel

class PerguntaRequest(BaseModel):
    question: str

class PerguntaResponse(BaseModel):
    answer: str
