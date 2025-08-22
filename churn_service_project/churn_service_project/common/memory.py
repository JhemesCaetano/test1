# Arquivo: common/memory.py

from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
# Importa a URL do nosso novo config comum
from .config import REDIS_URL

def build_memory(session_id: str):
    """
    Cria uma memória de conversação com buffer que usa o Redis como backend.
    """
    message_history = RedisChatMessageHistory(
        url=REDIS_URL, session_id=session_id
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", 
        chat_memory=message_history, 
        return_messages=True, 
        k=10 # Mantém as últimas 10 trocas de mensagens na memória
    )
    
    return memory