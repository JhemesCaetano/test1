# Arquivo: common/config.py

import os

# Carrega a URL do Redis a partir das variáveis de ambiente do contêiner
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")