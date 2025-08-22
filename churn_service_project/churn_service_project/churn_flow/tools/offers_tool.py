"""
Tool que busca ofertas de retenção na API Mock de ofertas.
"""
import requests
import os
from common.session_data_tool import get_session_data

# URL da API de ofertas, lida a partir das variáveis de ambiente
OFFERS_API_URL = os.getenv("OFFERS_API_URL", "http://localhost:9000")

def get_churn_offers(session_id: str) -> dict:
    """
    Busca na API de ofertas as promoções de retenção disponíveis para o cliente,
    com base nos detalhes do cliente salvos na sessão.
    """
    print(f"--- Ferramenta get_churn_offers: Buscando ofertas para session_id: {session_id} ---")
    
    # Busca os detalhes do cliente (plano, etc.) que o ServiceAgent salvou no Redis
    session_data = get_session_data(session_id)
    customer_details = session_data.get("customer_details")

    if not customer_details:
        print("!!! Erro na ferramenta get_churn_offers: Detalhes do cliente não encontrados.")
        return {"error": "Detalhes do cliente não encontrados na sessão.", "ofertas": []}

    try:
        url = f"{OFFERS_API_URL}/offers/{session_id}"
        print(f"--- Consultando a API de ofertas em: {url} ---")
        
        # A API Mock espera os detalhes do cliente no corpo da requisição
        response = requests.post(url, json=customer_details)
        response.raise_for_status()
        
        offers_data = response.json()
        print(f"--- Ofertas recebidas da API: {offers_data} ---")
        return offers_data

    except requests.exceptions.RequestException as e:
        error_message = f"Erro ao comunicar com a API de ofertas: {e}"
        print(f"!!! {error_message}")
        return {"error": error_message, "ofertas": []}