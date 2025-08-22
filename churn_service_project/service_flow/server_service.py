from fastapi import FastAPI, Request
import requests
import os

from service_flow.agents.service_agent import build_service_agent
from service_flow.tools.customer_tool import get_customer_details
from common.session_data_tool import set_session_data

CHURN_URL = os.getenv("CHURN_URL", "http://localhost:8001/churn")

app = FastAPI()

@app.post("/service")
async def process_service(request: Request):
    data = await request.json()
    msg = data.get("mensagem", "")
    session_id = data.get("session_id", "default")
    
    # Adicionando um print para depuração, para garantir que o session_id está correto
    print(f"--- Service Flow recebendo dados: session_id='{session_id}', mensagem='{msg}' ---")

    customer_details = get_customer_details(session_id)
    
    if "error" not in customer_details:
        print(f"ServiceFlow: Salvando detalhes do cliente {customer_details} no Redis.")
        set_session_data(session_id, {"customer_details": customer_details})

    context_msg = f"Dados do cliente: {customer_details}. Mensagem do cliente: {msg}"

    service_agent = build_service_agent(session_id=session_id)
    
    # --- CORREÇÃO PRINCIPAL: Usando .invoke() em vez de .run() ---
    # O método invoke é o padrão moderno e espera um dicionário.
    agent_input = {"input": context_msg}
    resposta_agente = service_agent.invoke(agent_input)
    # A resposta do invoke é um dicionário, extraímos o output.
    output_dict = resposta_agente.get("output", [{}])[0]

    # A ação agora está dentro do dicionário de saída
    result = output_dict if isinstance(output_dict, dict) else {}

    if result.get("action") == "Cancelar":
        print(f"--- ServiceAgent detectou cancelamento. Transferindo para Churn Flow ---")
        try:
            churn_payload = {"mensagem": msg, "session_id": session_id}
            response = requests.post(CHURN_URL, json=churn_payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro ao comunicar com Churn Flow: {e}"}

    return {"response": resposta_agente.get("output")}