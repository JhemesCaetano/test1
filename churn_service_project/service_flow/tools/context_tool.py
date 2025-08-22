"""
Tool para manipulação de contexto do ServiceAgent
via microserviço db_memory_service.
"""
import requests
# CORREÇÃO FINAL: Import absoluto a partir da raiz do projeto
from service_flow.config import DB_MEMORY_URL

def set_context_owner(owner: str, session_id: str = "default") -> str:
    # ... (o resto do código não muda)
    url = f"{DB_MEMORY_URL}/set_context"
    payload = {"session_id": session_id, "owner": owner}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return f"Contexto definido como {owner}"
    else:
        return f"Erro ao definir contexto: {response.text}"

def get_context_owner(session_id: str = "default") -> str:
    url = f"{DB_MEMORY_URL}/get_context/{session_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("owner")
    else:
        return f"Erro ao obter contexto: {response.text}"