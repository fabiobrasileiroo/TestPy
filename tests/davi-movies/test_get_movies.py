import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/movies.feature")

@given(parsers.cfparse('Endpoint dos filmes:"{path}"'))
def endpoint(path:str) -> str:
    return path

def extract_datas(respose):
    data = respose.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data

@when(parsers.cfparse('Enviar uma requisição `GET` para "{path}"'))
def request_api(path:str) -> str:
    url = path
    response = requests.get(url)
    return response

@then(parsers.cfparse('O código de status da resposta deve ser {status_code:d}'))
def check_status_code(response,status_code):
     assert response.status_code == status_code


@then(parsers.cfparse('O array não pode estar zerado'))
def check_null_array(response):
    data = extract_datas(response)
    assert isinstance(data, list)
    assert len(data) != 0

@then(parsers.cfparse('Cada filme deve ter os campos "{fields}"'))
def check_movie_labels(respose,labels):
    labels_clean = labels.replace(' e ', ',')
    expected_labels = [f.strip().strip('"') for f in labels_clean.split(',') if f.strip()]
    print('expected_fields:', expected_labels)
    data = extract_datas(respose)
    assert isinstance(data, list) and data
    for song in data:
        for f in expected_labels:
            print('aqui:', f, song)
            assert f in song