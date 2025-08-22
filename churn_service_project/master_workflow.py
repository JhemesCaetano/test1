"""
Orquestrador Principal (Master Workflow)
"""
import requests
import os
from langgraph.graph import StateGraph, END
from churn_flow.tools.context_tool import get_context_owner

SERVICE_FLOW_URL = os.getenv("SERVICE_FLOW_URL", "http://localhost:8002/service")
CHURN_FLOW_URL = os.getenv("CHURN_FLOW_URL", "http://localhost:8001/churn")

class MasterState(dict):
    """Representa o estado do grafo principal."""
    pass

def run_service_flow(state: MasterState):
    """Executa o workflow de atendimento geral fazendo uma chamada de API."""
    print("---ROTEADO PARA: Service Flow---")
    try:
        # --- CORREÇÃO: Construir o payload JSON explicitamente ---
        payload = {
            "session_id": state.get("session_id"),
            "mensagem": state.get("mensagem")
        }
        response = requests.post(SERVICE_FLOW_URL, json=payload)
        response.raise_for_status()
        state["resposta"] = response.json()
    except requests.exceptions.RequestException as e:
        state["resposta"] = {"error": f"Erro ao comunicar com Service Flow: {e}"}
    return state

def run_churn_flow(state: MasterState):
    """Executa o workflow de churn fazendo uma chamada de API."""
    print("---ROTEADO PARA: Churn Flow---")
    try:
        # --- CORREÇÃO: Construir o payload JSON explicitamente ---
        payload = {
            "session_id": state.get("session_id"),
            "mensagem": state.get("mensagem")
        }
        response = requests.post(CHURN_FLOW_URL, json=payload)
        response.raise_for_status()
        state["resposta"] = response.json()
    except requests.exceptions.RequestException as e:
        state["resposta"] = {"error": f"Erro ao comunicar com Churn Flow: {e}"}
    return state

def route_message(state: MasterState):
    """Verifica o proprietário do contexto para decidir para qual agente rotear."""
    session_id = state.get("session_id", "default_session")
    owner = get_context_owner(session_id=session_id)
    print(f"---CONTEXTO ATUAL: {owner}---")
    if owner and "Churn" in owner:
        return "run_churn_flow"
    return "run_service_flow"

workflow = StateGraph(MasterState)
workflow.add_node("run_service_flow", run_service_flow)
workflow.add_node("run_churn_flow", run_churn_flow)
workflow.set_conditional_entry_point(route_message)
workflow.add_edge("run_service_flow", END)
workflow.add_edge("run_churn_flow", END)
master_app = workflow.compile()