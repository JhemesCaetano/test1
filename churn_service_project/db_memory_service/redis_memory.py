from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from .config import REDIS_URL


def build_memory(session_id: str):
    """
    Cria uma memória de conversação com buffer que usa o Redis como backend.
    """
    # 1. Cria uma conexão com o histórico de mensagens no Redis para uma session_id específica.
    # Cada conversa (session_id) terá sua própria chave no Redis.
    message_history = RedisChatMessageHistory(
        url=REDIS_URL, session_id=session_id
    )

    # 2. Cria o objeto de memória da LangChain.
    # Ele usa o histórico do Redis para armazenar e recuperar as mensagens.
    # O 'k=10' significa que ele manterá as últimas 10 trocas de mensagens na memória ativa.
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", 
        chat_memory=message_history, 
        return_messages=True, 
        k=10
    )
    
    return memory