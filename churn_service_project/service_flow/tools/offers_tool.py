"""
Tool de ofertas genéricas (não financeiras).
Este é opcional no fluxo de service.
"""

def obter_ofertas_servico(session_id: str = "default") -> dict:
    """
    Retorna possíveis benefícios/ofertas para clientes em atendimento geral.
    """
    ofertas = [
        {
            "id": "ServicoPlus",
            "descricao": "Atendimento prioritário no suporte técnico",
            "valor": "Sem custo adicional"
        },
        {
            "id": "AssistenciaRemota",
            "descricao": "Assistência remota grátis por 1 mês",
            "valor": "Benefício temporário"
        }
    ]

    return {
        "session_id": session_id,
        "ofertas": ofertas,
        "message": "Ofertas de atendimento recuperadas com sucesso"
    }
