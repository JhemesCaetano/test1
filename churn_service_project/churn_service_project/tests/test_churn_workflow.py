# tests/test_churn_workflow.py

import pytest
from churn_flow.workflow.graph import route_action

# Usamos @pytest.mark.parametrize para testar múltiplos cenários com uma única função
@pytest.mark.parametrize("action_input, expected_node", [
    ("Ofereça Oferta1", "executor"),
    ("Insista Oferta1", "executor"),
    ("Contrate Oferta2", "executor"),
    ("Cancelamento", "executor"),
    ("Dúvidas Oferta1", "executor"),
])
def test_route_action_para_executor(action_input, expected_node):
    """
    Verifica se todas as ações de negociação levam ao nó 'executor'.
    """
    # Prepara um estado de entrada simulado
    state = {"agent_response": {"action": action_input}}
    
    # Executa a função de roteamento
    proximo_no = route_action(state)
    
    # Verifica se o resultado é o esperado
    assert proximo_no == expected_node

def test_route_action_para_retornar_ao_servico():
    """
    Verifica se a ação 'Esclarecer' leva corretamente ao nó 'return_to_service'.
    """
    state = {"agent_response": {"action": "Esclarecer"}}
    proximo_no = route_action(state)
    assert proximo_no == "return_to_service"

def test_route_action_para_transferir_especialista():
    """
    Verifica se a ação 'Transferir Especialista' leva ao nó 'specialist_transfer'.
    """
    state = {"agent_response": {"action": "Transferir Especialista"}}
    proximo_no = route_action(state)
    assert proximo_no == "specialist_transfer"