from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
# Importa o 'master_app' do workflow principal restaurado
from master_workflow import master_app

app = FastAPI(
    title="Customer Service AI Orchestrator",
    description="Roteia requisições de usuários para o agente de IA apropriado (Atendimento ou Churn).",
    version="1.0.0" # Voltando para a versão original
)

class UserRequest(BaseModel):
    session_id: str
    mensagem: str

class AgentResponse(BaseModel):
    session_id: str
    resposta: dict

@app.post("/chat", response_model=AgentResponse)
def chat_with_agent(request: UserRequest):
    """
    Endpoint principal para interagir com o sistema de agentes.
    Utiliza o workflow principal para rotear a requisição.
    """
    inputs = {"session_id": request.session_id, "mensagem": request.mensagem}
    response_state = master_app.invoke(inputs)
    return AgentResponse(session_id=request.session_id, resposta=response_state.get("resposta", {}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)