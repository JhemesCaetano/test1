from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI(
    title="Mock Offers API",
    description="API Falsa que retorna ofertas de retenção com base no plano do cliente.",
    version="1.0.0"
)

# Banco de dados falso de ofertas, organizado por plano
MOCK_OFFERS_DB = {
    "Fibra Home 1G": [
        {"id": "Oferta1A", "descricao": "Mantenha seu plano Fibra Home 1G com 15% de desconto por 6 meses.", "valor": 118.99},
        {"id": "Oferta1B", "descricao": "Faça o downgrade para Fibra Gamer 500M e pague menos.", "valor": 119.99}
    ],
    "Fibra Gamer 500M": [
        {"id": "Oferta2A", "descricao": "Adicione um Ponto Extra de Wi-Fi gratuito por 1 ano.", "valor": 119.99}
    ],
    "Fibra Full 2G": [
        {"id": "OfertaVIP", "descricao": "Como cliente VIP, oferecemos 25% de desconto vitalício no seu plano.", "valor": 187.49}
    ]
    # Note que o "Plano Antigo 100M" não tem ofertas cadastradas
}

class CustomerDetails(BaseModel):
    name: str
    plan: str
    plan_value: float

@app.post("/offers/{session_id}")
def get_mock_offers(session_id: str, customer: CustomerDetails):
    """
    Retorna ofertas com base no plano atual do cliente.
    """
    print(f"--- MOCK OFFERS API: Recebida requisição para session_id: {session_id} ---")
    print(f"--- MOCK OFFERS API: Detalhes do cliente recebidos: {customer} ---")
    
    customer_plan = customer.plan
    
    # Busca ofertas para o plano específico do cliente
    ofertas_para_plano = MOCK_OFFERS_DB.get(customer_plan, [])
    
    if ofertas_para_plano:
        print(f"--- MOCK OFFERS API: {len(ofertas_para_plano)} oferta(s) encontrada(s) para o plano '{customer_plan}'. ---")
    else:
        print(f"--- MOCK OFFERS API: Nenhuma oferta encontrada para o plano '{customer_plan}'. ---")
        
    return {
        "session_id": session_id,
        "ofertas": ofertas_para_plano,
        "message": "Ofertas recuperadas com sucesso da API MOCK."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)