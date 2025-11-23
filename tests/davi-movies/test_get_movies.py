import requests
import json
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/movies_get.feature")

# Step: Dado o endpoint
@given(parsers.cfparse('o endpoint: "{path}"'))
def endpoint(path: str) -> str:
    return path

# Função auxiliar para extrair dados
def extract_datas(response):
    data = response.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data

# Step: Quando realizar a requisição GET
@when(parsers.cfparse('realizar a requisição GET no: "{path}"'),
      target_fixture="response")
def request_api(path: str):
    response = requests.get(path)
    return response

# Step: Então o código de status da resposta deve ser X
@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
    assert response.status_code == status_code

# Step: Cada filme deve ter os campos
@then(parsers.cfparse('cada filme deve ter os campos "{fields}"'))
def check_movie_labels(response, fields):
    # separa os campos por vírgula
    expected_labels = [f.strip().strip('"') for f in fields.split(',') if f.strip()]
    data = extract_datas(response)
    assert isinstance(data, list) and data
    for movie in data:
        for f in expected_labels:
            assert f in movie
