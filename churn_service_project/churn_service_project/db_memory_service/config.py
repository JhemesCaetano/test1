import os

# URL do Redis (pode ser substituída por outro backend depois)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
