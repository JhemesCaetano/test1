from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import traceback  # Importar para logging de exceções
from master_workflow import master_app

app = FastAPI(
    title="Customer Service AI Orchestrator",
    description="Roteia requisições de usuários para o agente de IA apropriado (Atendimento ou Churn).",
    version="1.0.0"
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
    response_state = None  # Inicializa a variável
    try:
        inputs = {"session_id": request.session_id, "mensagem": request.mensagem}
        print(f"--- ORQUESTRADOR /chat: Inputs para o workflow: {inputs} ---")

        response_state = master_app.invoke(inputs)

        print(f"--- ORQUESTRADOR /chat: Estado retornado pelo workflow: {response_state} ---")

        if response_state is None:
            print("!!! ERRO CRÍTICO: O workflow retornou None.")
            # Garante que response_state seja um dicionário para o .get() funcionar
            response_state = {"resposta": {"error": "Erro crítico no workflow, retornou None."}}

    except Exception as e:
        print(f"!!! ERRO CRÍTICO: Exceção ao invocar o workflow: {e}")
        traceback.print_exc()  # Imprime o traceback completo no log do container
        response_state = {"resposta": {"error": f"Exceção no master_app.invoke: {str(e)}"}}

    # O .get() agora é seguro, pois response_state é sempre um dicionário
    return AgentResponse(session_id=request.session_id, resposta=response_state.get("resposta", {}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)