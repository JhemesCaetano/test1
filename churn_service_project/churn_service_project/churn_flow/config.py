import os

# Chave da API da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "CHANGE_ME")

# URL do microserviço de memória
DB_MEMORY_URL = os.getenv("DB_MEMORY_URL", "http://localhost:8000")

# URL do Redis para a memória da conversa
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
