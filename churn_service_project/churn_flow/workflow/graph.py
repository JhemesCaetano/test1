"""
Workflow de Churn (Liderado pelo ChurnAgent)

Este grafo orquestra a lógica de retenção. O ChurnAgent atua como o
estrategista, e o FinChurnAgent atua como o executor da estratégia.
"""
import requests
import os
from langgraph.graph import StateGraph, END
# CORREÇÃO 1: Importar a função correta para construir o agente
from churn_flow.agents.churn_agent import build_churn_agent_with_details
from churn_flow.agents.fin_churn_agent import build_fin_churn_agent
from common.session_data_tool import get_session_data

# URL do serviço de atendimento para poder devolver a chamada
SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:8002/service")


class AgentState(dict):
    """Representa o estado da conversa de churn."""
    pass

#---------------------
# --- Nós do Grafo ---
#---------------------


# CORREÇÃO 2: Manter apenas uma definição unificada e completa do strategist_node

def strategist_node(state: AgentState):
    """
    Executa o ChurnAgent. Primeiro, busca os dados da ocorrência do Redis.
    """
    print("---EXECUTANDO NÓ CHURN: ESTRATEGISTA (ChurnAgent)---")
    
    # 1. BUSCAR OS DADOS DA OCORRÊNCIA DO REDIS
    session_data = get_session_data(state["session_id"])
    customer_details = session_data.get("customer_details", {})
    print(f"ChurnFlow: Dados do cliente recuperados do Redis: {customer_details}")
    
    # 2. Continua o fluxo normal, passando os dados para o builder do agente
    agent = build_churn_agent_with_details(
        session_id=state["session_id"], 
        customer_details=customer_details
    )
    
    # CORREÇÃO 3: Lógica que estava faltando para executar o agente e salvar a resposta
    response_list = agent.run(state["mensagem"])
    agent_response = response_list[0] if isinstance(response_list, list) and response_list else {}
    
    state["agent_response"] = agent_response
    return state


def executor_node(state: AgentState):
    """
    Nó do Executor: Executa o FinChurnAgent para formular a resposta ao cliente
    com base na ação definida pelo estrategista.
    """
    print("---EXECUTANDO NÓ CHURN: EXECUTOR (FinChurnAgent)---")
    agent = build_fin_churn_agent(session_id=state["session_id"])
    
    contexto_para_fin_agent = str(state.get("agent_response", {}))
    final_response = agent.run(contexto_para_fin_agent)
    
    state["final_response"] = final_response
    return state


def return_to_service_node(state: AgentState):
    """
    Nó de Retorno: Devolve a conversa para o ServiceAgent caso o motivo não esteja claro.
    """
    print("---EXECUTANDO NÓ CHURN: DEVOLUÇÃO PARA ServiceAgent---")
    msg = state["mensagem"]
    session_id = state["session_id"]
    new_msg = f"O cliente pediu para cancelar, mas o motivo não ficou claro. Por favor, continue a conversa. Mensagem original: '{msg}'"
    
    try:
        response = requests.post(SERVICE_URL, json={"mensagem": new_msg, "session_id": session_id})
        response.raise_for_status()
        state["final_response"] = response.json()
    except requests.exceptions.RequestException as e:
        state["final_response"] = {"error": f"Erro ao devolver para o Service Flow: {e}"}
    
    return state
    

def specialist_transfer_node(state: AgentState):
    """
    Nó de Transferência: Formata uma resposta padrão para transferir para um especialista humano.
    """
    print("---EXECUTANDO NÓ CHURN: TRANSFERÊNCIA PARA ESPECIALISTA HUMANO---")
    state["final_response"] = state["agent_response"]
    return state


# --- Lógica de Roteamento ---
def route_action(state: AgentState):
    """
    Lê a ação do ChurnAgent e decide o próximo passo.
    """
    action = state.get("agent_response", {}).get("action")
    print(f"---ROTEADOR CHURN: Ação estratégica é '{action}'---")

    if action == "Esclarecer":
        return "return_to_service"
    if action == "Transferir Especialista":
        return "specialist_transfer"
        
    return "executor"


# --- Construção do Grafo ---
workflow = StateGraph(AgentState)

workflow.add_node("strategist", strategist_node)
workflow.add_node("executor", executor_node)
workflow.add_node("return_to_service", return_to_service_node)
workflow.add_node("specialist_transfer", specialist_transfer_node)

workflow.set_entry_point("strategist")

workflow.add_conditional_edges(
    "strategist",
    route_action,
    {
        "executor": "executor",
        "return_to_service": "return_to_service",
        "specialist_transfer": "specialist_transfer"
    }
)

workflow.add_edge("executor", END)
workflow.add_edge("return_to_service", END)
workflow.add_edge("specialist_transfer", END)

app = workflow.compile()