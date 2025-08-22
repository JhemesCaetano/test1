import requests
import os

# A URL da API de clientes será lida da variável de ambiente do contêiner
CUSTOMER_API_URL = os.getenv("CUSTOMER_API_URL", "http://localhost:9001")

def get_customer_details(session_id: str) -> dict:
    """
    Busca os detalhes do cliente, incluindo seu plano atual,
    usando a session_id como identificador.
    """
    try:
        url = f"{CUSTOMER_API_URL}/customer/{session_id}"
        print(f"ServiceAgent: Consultando API de clientes em: {url}")
        response = requests.get(url)
        if response.status_code == 404:
            return {"error": "Cliente não encontrado."}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Usamos str(e) para converter o erro em uma string legível
        print(f"ERRO ao acessar a API de clientes: {e}")
        return {"error": f"Erro ao comunicar com o sistema de clientes: {str(e)}"}