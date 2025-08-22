import requests
import os
from langgraph.graph import StateGraph, END
from churn_flow.tools.context_tool import get_context_owner
from typing import TypedDict, Optional
# Importa a ferramenta para salvar dados na sessão (Redis)
from common.session_data_tool import set_session_data

# URLs base dos serviços
SERVICE_FLOW_URL = os.getenv("SERVICE_FLOW_URL", "http://localhost:8002")
CHURN_FLOW_URL = os.getenv("CHURN_URL", "http://localhost:8001")

class MasterState(TypedDict):
    session_id: str
    mensagem: str
    resposta: Optional[dict]

def trigger_service(service_name: str, base_url: str, state: MasterState):
    """Função genérica para salvar a mensagem e disparar um serviço."""
    print(f"--- NÓ DO ORQUESTRADOR: {service_name} ---")
    try:
        session_id = state["session_id"]
        mensagem = state["mensagem"]

        # 1. Salva a mensagem no Redis
        print(f"--- Salvando mensagem no Redis para session_id: {session_id} ---")
        set_session_data(session_id, {"mensagem": mensagem})

        # 2. Dispara o serviço, passando apenas o session_id na URL
        trigger_url = f"{base_url}/{service_name}/{session_id}"
        print(f"--- Disparando serviço em: {trigger_url} ---")
        response = requests.post(trigger_url)
        response.raise_for_status()
        
        return {"resposta": response.json()}
    except Exception as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" | RESPOSTA: {e.response.text}"
        print(f"!!! Erro ao disparar {service_name}: {error_message}")
        return {"resposta": {"error": error_message}}

def run_service_flow(state: MasterState):
    return trigger_service("service", SERVICE_FLOW_URL, state)

def run_churn_flow(state: MasterState):
    return trigger_service("churn", CHURN_FLOW_URL, state)

def route_message(state: MasterState):
    """Decide para qual workflow a mensagem deve ser enviada."""
    session_id = state['session_id']
    owner = get_context_owner(session_id=session_id)
    print(f"--- CONTEXTO ATUAL: {owner} ---")
    if owner and "Churn" in owner:
        return "run_churn_flow"
    return "run_service_flow"

workflow = StateGraph(MasterState)

workflow.add_node("run_service_flow", run_service_flow)
workflow.add_node("run_churn_flow", run_churn_flow)

workflow.set_conditional_entry_point(
    route_message,
    {
        "run_service_flow": "run_service_flow",
        "run_churn_flow": "run_churn_flow",
    }
)

workflow.add_edge("run_service_flow", END)
workflow.add_edge("run_churn_flow", END)
master_app = workflow.compile()