import requests
import os

DB_MEMORY_URL = os.getenv("DB_MEMORY_URL", "http://localhost:8000")

def set_session_data(session_id: str, data: dict) -> dict:
    """Salva dados da ocorrência (ex: detalhes do cliente) no Redis."""
    url = f"{DB_MEMORY_URL}/set_session_data"
    payload = {"session_id": session_id, "data": data}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_session_data(session_id: str) -> dict:
    """Obtém dados da ocorrência do Redis."""
    url = f"{DB_MEMORY_URL}/get_session_data/{session_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}