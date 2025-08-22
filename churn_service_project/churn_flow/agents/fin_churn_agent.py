from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from common.memory import build_memory
from common.prompt_loader import load_prompt
from churn_flow.tools.context_tool import set_context_owner
from churn_flow.tools.offers_tool import obter_ofertas_rotatividade
from churn_flow.config import OPENAI_API_KEY

def build_fin_churn_agent(session_id: str, verbose: bool = True):
    tools = [
        Tool(
            name="ObterOfertasRotatividade",
            # A função original não precisa de customer_details, mantemos assim
            func=lambda: obter_ofertas_rotatividade(session_id=session_id, customer_details={}),
            description="Obtém ofertas de retenção financeiras para o cliente. Use apenas se precisar buscar ofertas novamente."
        ),
        Tool(
            name="SetContextOwner",
            func=lambda owner_string: set_context_owner(owner=owner_string, session_id=session_id),
            description="Define o proprietário do contexto para FinChurnAgent."
        )
    ]
    base_prompt = load_prompt("churn_flow/prompts/base_agent_fin_churn.md")
    fin_prompt = load_prompt("churn_flow/prompts/fin_churn_agent.md")
    system_message = base_prompt + "\n\n" + fin_prompt
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
    memory = build_memory(f"{session_id}:fin_churn")
    agent = initialize_agent(
        tools=tools, llm=llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory, verbose=verbose,
        agent_kwargs={"system_message": system_message},
        handle_parsing_errors=True
    )
    return agent