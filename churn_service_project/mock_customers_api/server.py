from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(
    title="Mock Customer API",
    description="API Falsa para simular um banco de dados de clientes.",
    version="1.0.0"
)

# Banco de dados falso de clientes. Use a session_id dos seus testes como chave.
# Adicione quantos clientes de teste precisar.
MOCK_CUSTOMER_DB = {
    "conversa-teste-001": {"name": "João Silva", "plan": "Fibra Home 1G", "plan_value": 139.99},
    "conversa-python-002": {"name": "Maria Oliveira", "plan": "Fibra Gamer 500M", "plan_value": 119.99},
    "cliente-sem-oferta": {"name": "Carlos Pereira", "plan": "Plano Antigo 100M", "plan_value": 89.99},
    "cliente-vip-123": {"name": "Ana Costa (VIP)", "plan": "Fibra Full 2G", "plan_value": 249.99}
}

@app.get("/customer/{session_id}")
def get_customer_details(session_id: str):
    """
    Retorna os detalhes de um cliente com base na sua session_id.
    """
    print(f"--- MOCK CUSTOMER API: Recebida requisição para session_id: {session_id} ---")
    
    if session_id in MOCK_CUSTOMER_DB:
        print(f"--- MOCK CUSTOMER API: Cliente encontrado. Retornando dados. ---")
        return MOCK_CUSTOMER_DB[session_id]
    
    print(f"--- MOCK CUSTOMER API: Cliente NÃO encontrado. Retornando 404. ---")
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)