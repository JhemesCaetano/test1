"""
Tool de ofertas de retenção (financeiras).
Pode ser expandido para buscar em banco de dados ou API externa.
"""

def obter_ofertas_rotatividade(session_id: str = "default") -> dict:
    """
    Retorna ofertas disponíveis para retenção de clientes.
    Neste exemplo, são ofertas mockadas.
    """
    ofertas = [
        {
            "id": "Oferta1",
            "descricao": "20% de desconto nos próximos 3 meses",
            "valor": "Plano reduzido temporário"
        },
        {
            "id": "Oferta2",
            "descricao": "Upgrade gratuito para velocidade maior por 2 meses",
            "valor": "Benefício promocional"
        }
    ]

    return {
        "session_id": session_id,
        "ofertas": ofertas,
        "message": "Ofertas recuperadas com sucesso"
    }
