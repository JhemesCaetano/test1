# tests/test_customer_tool.py

from service_flow.tools.customer_tool import get_customer_details
import requests

# A fixture 'mocker' é fornecida pela biblioteca pytest-mock
def test_get_customer_details_sucesso(mocker):
    """
    Testa o cenário feliz: a API de clientes retorna os dados com sucesso (HTTP 200).
    """
    # 1. Prepara a simulação (Mock)
    # Cria um objeto que imita a resposta da biblioteca 'requests'
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    expected_data = {"name": "João Silva", "plan": "Fibra Home 1G"}
    mock_response.json.return_value = expected_data
    
    # Instrui o mocker a substituir a função 'requests.get' pela nossa simulação
    mocker.patch('requests.get', return_value=mock_response)
    
    # 2. Executa a função que queremos testar
    resultado = get_customer_details("cliente-123")
    
    # 3. Verifica se o resultado é o esperado
    assert resultado == expected_data

def test_get_customer_details_cliente_nao_encontrado(mocker):
    """
    Testa o cenário onde o cliente não é encontrado (HTTP 404).
    """
    # 1. Prepara a simulação para um erro 404
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    
    mocker.patch('requests.get', return_value=mock_response)
    
    # 2. Executa a função
    resultado = get_customer_details("cliente-inexistente")
    
    # 3. Verifica se a função tratou o erro 404 corretamente
    assert resultado == {"error": "Cliente não encontrado."}

def test_get_customer_details_falha_api(mocker):
    """
    Testa o cenário de uma falha de conexão com a API.
    """
    # 1. Simula uma exceção de rede
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Erro de conexão"))
    
    # 2. Executa a função
    resultado = get_customer_details("qualquer-cliente")
    
    # 3. Verifica se a função tratou a exceção genérica
    assert "error" in resultado
    assert "Erro ao comunicar com o sistema de clientes" in resultado["error"]