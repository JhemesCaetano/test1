from langchain.agents import AgentExecutor, Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from common.memory import build_memory
from common.prompt_loader import load_prompt
from churn_flow.tools.context_tool import set_context_owner
from churn_flow.tools.offers_tool import get_churn_offers
from churn_flow.config import OPENAI_API_KEY

def build_fin_churn_agent(session_id: str, verbose: bool = True):
    print("--- Construindo FinChurnAgent ---")
    tools = [
        Tool(
            name="getChurnOffers",
            # --- CORREÇÃO AQUI ---
            func=lambda *args, **kwargs: get_churn_offers(session_id=session_id),
            description="Use esta ferramenta se precisar obter novamente as ofertas de retenção para o cliente."
        ),
        Tool(
            name="setContextOwnerFin", 
            func=lambda owner_string: set_context_owner(owner=owner_string, session_id=session_id),
            description="Use esta ferramenta ao final do seu atendimento para definir o proprietário do contexto como 'FinChurnAgent'."
        )
    ]
    
    base_prompt = load_prompt("churn_flow/prompts/base_agent_fin_churn.md")
    fin_prompt = load_prompt("churn_flow/prompts/fin_churn_agent.md")
    system_message = base_prompt + "\n\n" + fin_prompt

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ])

    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)

    agent_chain = ({
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
    } | prompt | llm_with_tools | OpenAIToolsAgentOutputParser())

    memory = build_memory(f"{session_id}:fin_churn")
    agent_executor = AgentExecutor(
        agent=agent_chain, 
        tools=tools, 
        verbose=verbose, 
        memory=memory,
        handle_parsing_errors=True
    )

    return agent_executor