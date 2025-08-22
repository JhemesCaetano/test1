"""
Workflow de atendimento geral (ServiceAgent)
"""

from langgraph.graph import StateGraph
from service_flow.agents.service_agent import build_service_agent

class AgentState(dict):
    pass


def service_node(state: AgentState):
    agent = build_service_agent(session_id=state["session_id"])
    resposta = agent.run(state["mensagem"])
    return {"resposta": resposta}


workflow = StateGraph(AgentState)
workflow.add_node("ServiceAgent", service_node)
workflow.set_entry_point("ServiceAgent")

app = workflow.compile()
