"""
ServiceAgent - responsável pelo atendimento geral (suporte, dúvidas, consultas)
"""
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import Tool
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
            # --- CORREÇÃO AQUI ---
            # Aceita quaisquer argumentos (*args, **kwargs) e os ignora,
            # garantindo que a chamada sempre funcione.
            func=lambda *args, **kwargs: get_customer_details(session_id),
            description="Use para obter os detalhes do cliente, como nome e plano atual, no início da conversa."
        )
    ]

    base_prompt_str = load_prompt("service_flow/prompts/base_service_agent.md")
    service_prompt_str = load_prompt("service_flow/prompts/service_agent.md")
    full_prompt_str = base_prompt_str + "\n\n" + service_prompt_str

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", full_prompt_str),
            ("user", "{input}"),
            ("ai", "{agent_scratchpad}"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)

    agent_chain = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    memory = build_memory(f"{session_id}:service")
    
    agent_executor = AgentExecutor(
        agent=agent_chain, 
        tools=tools, 
        verbose=verbose, 
        memory=memory,
        handle_parsing_errors=True
    )

    return agent_executor