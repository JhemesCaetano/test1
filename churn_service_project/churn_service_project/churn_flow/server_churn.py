from fastapi import FastAPI, HTTPException
from common.session_data_tool import get_session_data
from churn_flow.workflow.graph import app as churn_workflow_app

app = FastAPI()

@app.post("/churn/{session_id}")
async def process_churn(session_id: str):
    """
    Endpoint que é disparado e inicia o workflow de churn.
    """
    print(f"--- ENDPOINT /churn/{session_id} ATINGIDO ---")
    
    # 1. Busca os dados da sessão (mensagem) do Redis
    session_data = get_session_data(session_id)
    if not session_data or "mensagem" not in session_data:
        raise HTTPException(status_code=404, detail=f"Nenhuma mensagem encontrada no Redis para a sessão {session_id}")

    inputs = {
        "session_id": session_id,
        "mensagem": session_data["mensagem"]
    }

    print(f"--- CHURN FLOW INICIADO PARA SESSÃO: {inputs['session_id']} ---")
    
    final_state = churn_workflow_app.invoke(inputs)
    
    response_data = final_state.get("final_response", {"error": "Ocorreu um erro no fluxo de churn."})
    
    return {"response": response_data}