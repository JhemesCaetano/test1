from fastapi import FastAPI, HTTPException
import requests
import os
import json
from common.session_data_tool import get_session_data, set_session_data
from service_flow.agents.service_agent import build_service_agent
from service_flow.tools.customer_tool import get_customer_details

CHURN_URL = os.getenv("CHURN_URL", "http://localhost:8001")
app = FastAPI()

@app.post("/service/{session_id}")
async def process_service(session_id: str):
    print(f"--- ENDPOINT /service/{session_id} ATINGIDO ---")

    # 1. Busca os dados da sessão (incluindo a mensagem) do Redis
    session_data = get_session_data(session_id)
    if not session_data or "mensagem" not in session_data:
        raise HTTPException(status_code=404, detail=f"Nenhuma mensagem encontrada no Redis para a sessão {session_id}")
    
    msg = session_data["mensagem"]
    print(f"--- Mensagem recuperada do Redis: '{msg}' ---")

    customer_details = get_customer_details(session_id)
    if "error" not in customer_details:
        session_data["customer_details"] = customer_details
        set_session_data(session_id, session_data) # Atualiza o Redis com os dados do cliente

    context_msg = f"Dados do cliente: {customer_details}. Mensagem do cliente: {msg}"
    service_agent = build_service_agent(session_id=session_id)
    agent_input = {"input": context_msg}
    resposta_agente = service_agent.invoke(agent_input)
    output_str = resposta_agente.get("output", "[]")

    try:
        output_data = json.loads(output_str)
        result = output_data[0] if isinstance(output_data, list) and output_data else {}
    except (json.JSONDecodeError, TypeError):
        result = {}

    if result.get("action") == "Cancelar":
        print(f"--- ServiceAgent detectou cancelamento. Transferindo para Churn Flow ---")
        # A lógica de transferência agora também usa o Redis
        # (A mensagem já está lá, então apenas disparamos o serviço)
        trigger_url = f"{CHURN_URL}/churn/{session_id}"
        response = requests.post(trigger_url)
        response.raise_for_status()
        return response.json()

    return {"response": output_str}