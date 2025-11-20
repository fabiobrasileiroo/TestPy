import requests
from pytest_bdd import scenarios, given, when, then, parsers
# from utils.print_teste import print_response_body

# from app.config import BASE_URL


scenarios("features/songs.feature")


# Contexto
# ========
@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url: str):
    return base_url



@given(parsers.cfparse('que o endpoint para listar músicas é "{path}"'), target_fixture="path")
def endpoint(path: str):
    return path


# Cenários
# ========

# 1.Listar todas as músicas

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response")
def send_get_request(base_url:str, path: str):
    url = base_url + path
    resp = requests.get(url)
    return resp


def _extract_list_from_response(response):
    data = response.json()
    print('isinstance? ', isinstance(data, dict))
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
    # print_response_body(response)
    print("Response status code:", response.status_code == status_code)
    assert response.status_code == status_code


@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
    # print_response_body(response)
    data = _extract_list_from_response(response)
    assert isinstance(data, list)


@then('o array deve conter pelo menos 1 música')
def check_array_not_empty(response):
    # print_response_body(response)
    data = _extract_list_from_response(response)
    assert len(data) >= 1


@then(parsers.cfparse('cada música deve ter os campos "{fields}"'))
def check_song_fields(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    print('expected_fields:', expected_fields)
    # print_response_body(response)
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    for song in data:
        for f in expected_fields:
            print('aqui:', f, song)
            assert f in song


# 2. Listar música por ID

@given(parsers.cfparse('que existe uma música com id "{id}"'),target_fixture="id")
def get_by_id(id:str):
   return id 

# @when(parsers.cfparse('eu enviar uma requisição `GET` para "{path_with_id}"'),target_fixture="path_with_id")
# def get_path_with_id(path_with_id: str):
#     return path_with_id

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response_by_id")
def send_get_request_with_id(base_url:str, path: str, id: str):
    url = base_url + path + '/' + id
    resp = requests.get(url)
    return resp

@then(parsers.cfparse('o código de status da respota deve ser {status_code}'))
def check_status_code(status_code:str,response_by_id):
    assert response_by_id.status_code == 200


