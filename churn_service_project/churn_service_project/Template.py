# === 1. IMPORTS ===
# Importações necessárias para construir o agente com LangChain e OpenAI.
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from app.common.config import OPENAI_API_KEY, DB_MEMORY_URL # Supondo uma pasta 'common' para config
from app.common.utils import load_prompt # Supondo uma pasta 'common' para utils
from app.common.memory import build_memory # Supondo uma pasta 'common' para memória

# Importe as funções das ferramentas específicas deste agente.
from .tools.sua_ferramenta_especifica import sua_funcao_da_ferramenta_1
from .tools.outra_ferramenta_especifica import sua_funcao_da_ferramenta_2

# === 2. DEFINIÇÃO DAS FERRAMENTAS ===
# Cada agente tem um conjunto de ferramentas que definem suas capacidades.
def get_agent_tools(session_id: str):
    """
    Monta a lista de ferramentas disponíveis para o agente.
    Parâmetros específicos podem ser passados para as ferramentas usando lambdas.
    """
    tools = [
        Tool(
            name="NomeDaFerramenta1",
            func=sua_funcao_da_ferramenta_1,
            description="Descrição clara e objetiva do que esta ferramenta faz. O LLM usará isso para decidir quando usá-la."
        ),
        Tool(
            name="NomeDaFerramenta2",
            # Exemplo de como passar um parâmetro (session_id) para a função da ferramenta
            func=lambda: sua_funcao_da_ferramenta_2(session_id=session_id),
            description="Descrição da segunda ferramenta."
        ),
        # Adicione quantas ferramentas forem necessárias
    ]
    return tools

# === 3. FUNÇÃO PRINCIPAL DE CONSTRUÇÃO (BUILDER) ===
# Esta função centraliza a criação e configuração do agente.
def build_generic_agent(session_id: str, verbose: bool = True):
    """
    Cria e configura um Agente Genérico com LLM, memória e ferramentas.

    Args:
        session_id (str): O identificador único da conversa.
        verbose (bool): Se True, o agente imprimirá seus pensamentos no console.

    Returns:
        AgentExecutor: O agente LangChain pronto para ser executado.
    """
    print(f"--- Construindo Agente Genérico para a sessão: {session_id} ---")
    
    # --- a. Configuração do LLM ---
    # Define o modelo de linguagem que será o cérebro do agente.
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0, # Baixa temperatura para respostas mais determinísticas e consistentes
        openai_api_key=OPENAI_API_KEY
    )

    # --- b. Configuração da Memória ---
    # Conecta o agente ao histórico da conversa no Redis.
    # O nome do agente é adicionado ao session_id para criar um histórico isolado.
    memory = build_memory(f"{session_id}:generic_agent")

    # --- c. Carregamento dos Prompts ---
    # Carrega as instruções que definem a personalidade e as regras do agente.
    base_prompt = load_prompt("app/prompts/base_agent.md") # Prompt base com regras gerais
    agent_specific_prompt = load_prompt("app/agents/generic_agent/prompts/generic_agent_prompt.md") # Prompt específico
    
    system_message = base_prompt + "\n\n" + agent_specific_prompt

    # --- d. Montagem das Ferramentas ---
    tools = get_agent_tools(session_id)

    # --- e. Inicialização do Agente ---
    # Junta todas as peças: LLM, ferramentas, memória e prompts.
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, # Tipo de agente bom para conversas com ferramentas
        memory=memory,
        verbose=verbose,
        agent_kwargs={
            "system_message": system_message
        },
        handle_parsing_errors=True # Ajuda a lidar com saídas mal formatadas do LLM
    )

    return agent