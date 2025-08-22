from fastapi import FastAPI, Request
# Importa o 'app' compilado do nosso novo workflow de churn
from churn_flow.workflow.graph import app as churn_workflow_app

app = FastAPI()

@app.post("/churn")
async def process_churn(request: Request):
    """
    Endpoint que recebe a chamada do ServiceAgent e inicia o workflow de churn.
    """
    data = await request.json()
    
    # O estado inicial é o payload recebido do ServiceAgent
    inputs = {
        "session_id": data.get("session_id", "default"),
        "mensagem": data.get("mensagem", "")
    }

    print(f"---CHURN FLOW INICIADO PARA SESSÃO: {inputs['session_id']}---")
    
    # Invoca o workflow de LangGraph com o estado inicial
    final_state = churn_workflow_app.invoke(inputs)
    
    # A resposta final estará na chave 'final_response' do estado retornado pelo grafo
    response_data = final_state.get("final_response", {"error": "Ocorreu um erro no fluxo de churn."})
    
    return {"response": response_data}