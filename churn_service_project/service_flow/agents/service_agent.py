"""
ServiceAgent - responsável pelo atendimento geral (suporte, dúvidas, consultas)
"""
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI

# CORREÇÃO: Imports absolutos a partir da raiz do projeto (/app)
from common.memory import build_memory
from common.prompt_loader import load_prompt
from service_flow.tools.context_tool import set_context_owner
from service_flow.tools.customer_tool import get_customer_details
from service_flow.config import OPENAI_API_KEY

def build_service_agent(session_id: str, verbose: bool = True):
    tools = [
        Tool(
            name="SetContextOwner",
            func=lambda owner_string: set_context_owner(owner=owner_string, session_id=session_id),
            description="Define o proprietário do contexto para ServiceAgent"
        ),
        Tool(
            name="GetCustomerDetails",
            func=lambda: get_customer_details(session_id),
            description="Use para obter os detalhes do cliente, como nome e plano atual, no início da conversa."
        )
    ]
    base_prompt = load_prompt("service_flow/prompts/base_service_agent.md")
    service_prompt = load_prompt("service_flow/prompts/service_agent.md")
    system_message = base_prompt + "\n\n" + service_prompt
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
    memory = build_memory(f"{session_id}:service")
    agent = initialize_agent(
        tools=tools, llm=llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory, verbose=verbose,
        agent_kwargs={"system_message": system_message},
        handle_parsing_errors=True
    )
    return agent