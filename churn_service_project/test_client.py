import requests
import json
import time

# URL do seu orquestrador local
ORCHESTRATOR_URL = "http://localhost:8080/chat"

def enviar_mensagem(session_id: str, mensagem: str):
    """Função para enviar uma mensagem para o chatbot e imprimir a resposta."""
    payload = {
        "session_id": session_id,
        "mensagem": mensagem
    }
    
    print(f"\n>>>> ENVIANDO PARA O AGENTE:")
    print(f"     Sessão: {session_id}")
    print(f"     Mensagem: '{mensagem}'")
    
    try:
        response = requests.post(ORCHESTRATOR_URL, json=payload)
        response.raise_for_status()
        
        print(f"\n<<<< RESPOSTA DO AGENTE:")
        # Imprime a resposta formatada
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"\n!!!! ERRO: Não foi possível conectar ao orquestrador: {e}")

if __name__ == "__main__":
    print("--- CENÁRIO 1: ATENDIMENTO GERAL ---")
    SESSION_ID = "conversa-teste-001"
    enviar_mensagem(SESSION_ID, "Olá, gostaria de saber qual o meu plano atual.")