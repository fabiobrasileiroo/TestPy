import json
import requests
from pytest_bdd import scenarios, given, when, then, parsers

# from app.config import BASE_URL


scenarios("features/songs.feature")


# Contexto
# ========
@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url") # target_fixture o que ele faz é definir a nome da fixture que será usada nos outros passos
def base_url(base_url):
    return base_url



@given(parsers.cfparse('que o endpoint para listar músicas é "{path}"'), target_fixture="path")
def endpoint(path):
    return path


# Cenários
# ========

# Listar todas as músicas

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response")
def send_get_request(base_url, path: str):
    url = base_url + path
    resp = requests.get(url)
    return resp


def _extract_list_from_response(response):
    data = response.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data


def _print_response_body(response):
    try:
        body = response.json()
        pretty = json.dumps(body, indent=2, ensure_ascii=False)
        print("Response JSON body:\n" + pretty)
    except Exception:
        print("Response text body:\n" + (response.text or "<empty>"))


@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
    _print_response_body(response)
    print("Response status code:", response.status_code == status_code)
    assert response.status_code == status_code


@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
    _print_response_body(response)
    data = _extract_list_from_response(response)
    assert isinstance(data, list)


@then('o array deve conter pelo menos 1 música')
def check_array_not_empty(response):
    _print_response_body(response)
    data = _extract_list_from_response(response)
    assert len(data) >= 1


@then(parsers.cfparse('cada música deve ter os campos "{fields}"'))
def check_song_fields(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    _print_response_body(response)
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    for song in data:
        for f in expected_fields:
            assert f in song

