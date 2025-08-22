import requests
import json
import re

ORCHESTRATOR_URL = "http://localhost:8080/chat"

def clean_json_string(s):
    """Remove a marcação de código JSON e outros caracteres de escape."""
    # Remove ```json ... ```
    match = re.search(r'```json\s*([\s\S]*?)\s*```', s)
    if match:
        s = match.group(1)
    # Remove escapes de nova linha e aspas extras
    s = s.replace('\\n', '').replace('\\"', '"')
    return s

def enviar_mensagem(session_id: str, mensagem: str):
    """Envia uma mensagem para o chatbot e imprime a resposta formatada."""
    payload = {"session_id": session_id, "mensagem": mensagem}
    print("\n>>>> ENVIANDO...")
    try:
        response = requests.post(ORCHESTRATOR_URL, json=payload)
        response.raise_for_status()
        
        resposta_json = response.json()
        print("\n<<<< RESPOSTA DO AGENTE:")
        
        try:
            # Pega a resposta interna, que é uma string
            inner_response_str = resposta_json.get("resposta", {}).get("response", "{}")
            
            # Limpa a string JSON antes de tentar decodificar
            cleaned_str = clean_json_string(inner_response_str)
            
            inner_response_json = json.loads(cleaned_str)
            
            if isinstance(inner_response_json, list) and inner_response_json:
                data = inner_response_json[0]
            elif isinstance(inner_response_json, dict):
                 data = inner_response_json
            else:
                data = {}

            agent_output = data.get('output', 'Não foi possível extrair a mensagem do agente.')
            print(f"\n      -> MENSAGEM: \"{agent_output}\"\n")
        except Exception as e:
            print(f"--- Não foi possível analisar a resposta como JSON, mostrando resposta bruta ---")
            print(json.dumps(resposta_json, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"\n!!!! ERRO: {e}")

if __name__ == "__main__":
    print("===================================================================")
    print("========= INICIANDO TESTE INTERATIVO DO CHATBOT =========")
    print("===================================================================")
    session_id = input("Digite um ID para a sessão (ex: conversa-teste-001): ") or "conversa-teste-001"
    print(f"\nIniciando chat com a sessão '{session_id}'. Digite 'sair' para terminar.")
    print("-------------------------------------------------------------------")
    while True:
        mensagem_cliente = input("\nVOCÊ (Cliente): ")
        if mensagem_cliente.lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando o teste.")
            break
        if not mensagem_cliente:
            continue
        enviar_mensagem(session_id, mensagem_cliente)