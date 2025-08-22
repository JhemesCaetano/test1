import requests
import os
import json
from langgraph.graph import StateGraph, END
from churn_flow.agents.churn_agent import build_churn_agent
from churn_flow.agents.fin_churn_agent import build_fin_churn_agent

class AgentState(dict):
    """Representa o estado da conversa de churn."""
    pass

def churn_diagnostics_node(state: AgentState):
    """
    Nó do Diagnóstico: Roda o ChurnAgent para entender o motivo.
    """
    print("--- EXECUTANDO NÓ CHURN: DIAGNÓSTICO (ChurnAgent) ---")
    agent = build_churn_agent(session_id=state["session_id"])
    response = agent.invoke({"input": state["mensagem"]})
    output_str = response.get("output", "{}")
    try:
        data = json.loads(output_str)
        state["agent_response"] = data[0] if isinstance(data, list) and data else {}
    except (json.JSONDecodeError, TypeError):
        state["agent_response"] = {}
    return state

def financial_retention_node(state: AgentState):
    """
    Nó da Retenção Financeira: Roda o FinChurnAgent para negociar.
    """
    print("--- EXECUTANDO NÓ CHURN: RETENÇÃO FINANCEIRA (FinChurnAgent) ---")
    agent = build_fin_churn_agent(session_id=state["session_id"])
    # Passa a conversa adiante para o FinChurnAgent
    response = agent.invoke({"input": state["mensagem"]})
    # A resposta final do fluxo de churn é a resposta do FinChurnAgent
    state["final_response"] = response.get("output", "{}")
    return state

def specialist_transfer_node(state: AgentState):
    """
    Nó de Transferência: Apenas repassa a mensagem do ChurnAgent.
    """
    print("--- EXECUTANDO NÓ CHURN: TRANSFERÊNCIA PARA ESPECIALISTA ---")
    # A resposta final é a mensagem de transferência gerada pelo ChurnAgent
    state["final_response"] = json.dumps([state.get("agent_response", {})])
    return state

def route_reason(state: AgentState):
    """
    Roteia a conversa com base no motivo diagnosticado pelo ChurnAgent.
    """
    reason = state.get("agent_response", {}).get("action")
    print(f"--- ROTEADOR CHURN: Motivo diagnosticado é '{reason}' ---")
    if reason == "FinancialReason":
        return "financial_retention"
    else: # TechnicalReason, OtherReason, ou qualquer outra coisa
        return "specialist_transfer"

workflow = StateGraph(AgentState)

workflow.add_node("diagnostics", churn_diagnostics_node)
workflow.add_node("financial_retention", financial_retention_node)
workflow.add_node("specialist_transfer", specialist_transfer_node)

workflow.set_entry_point("diagnostics")

workflow.add_conditional_edges(
    "diagnostics",
    route_reason,
    {
        "financial_retention": "financial_retention",
        "specialist_transfer": "specialist_transfer"
    }
)

workflow.add_edge("financial_retention", END)
workflow.add_edge("specialist_transfer", END)

app = workflow.compile()