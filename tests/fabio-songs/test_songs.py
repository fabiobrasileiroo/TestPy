import requests
from pytest_bdd import scenarios, given, when, then, parsers
# import pytest

scenarios("features/songs.feature")

# Contexto
# ========
@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url: str) -> str:
    return base_url

# E
@given(parsers.cfparse('que o endpoint para listar músicas é "{path}"'), target_fixture="path")
def endpoint(path: str) -> str:
    return path

# vem do 2.
@given(parsers.cfparse('que existe uma música com id "{id}"'),target_fixture="id")
def get_by_id(id:str) -> str:
   return id 


# Cenários
# ========

# 1.Listar todas as músicas

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response")
def send_get_request(base_url:str, path: str):
    url = base_url + path
    resp = requests.get(url)
    return resp


# 2. Listar música por ID

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}/{id}"'), target_fixture="response")
def send_get_request_with_id(base_url:str, path: str, id: str):
    url = base_url + path + '/' + id
    resp = requests.get(url)
    return resp


# 3. Atualizar música

@when(parsers.cfparse('eu enviar uma requisição `PUT` para "{path}/{id}" com o seguinte corpo:'), target_fixture="response")
def send_put_request(base_url: str, path: str, id: str):
    # Corpo fixo baseado no arquivo de recursos
    # TODO: Encontrar uma maneira melhor de acessar a docstring no pytest-bdd 8.x
    body = {
        "name": "New Espresso",
        "artists": "New Artist",
        "isExplicit": False,
        "durationMs": 180000,
        "albumName": "New espresso",
        "albumReleaseDate": "2025-01-01"
    }
    url = base_url + path + '/' + id
    resp = requests.put(url, json=body)
    return resp

# 4. Criar música

@when(parsers.cfparse('eu enviar uma requisição `POST` para "{path}" com o seguinte corpo:'), target_fixture="response")
def send_post_request(base_url: str, path: str):
    # Corpo fixo baseado no arquivo de recursos
    # TODO: Encontrar uma maneira melhor de acessar a docstring no pytest-bdd 8.x
    body = {
        "name": "foooName",
        "artists": "fooArtist",
        "isExplicit": True,
        "durationMs": 175459,
        "albumName": "FooAlbum",
        "albumReleaseDate": "2024-04-12"
    }
    url = base_url + path
    resp = requests.post(url, json=body)
    return resp

# 5. Deletar música

@when(parsers.cfparse('eu enviar uma requisição `DELETE` para "{path}/{id}"'), target_fixture="response")
def send_delete_request(base_url: str, path: str, id: str):
    url = base_url + path + '/' + id
    resp = requests.delete(url)
    return resp


#===================
# Funções auxiliares
def _extract_list_from_response(response):
    data = response.json()
    print('isinstance? ', isinstance(data, dict))
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data


def _extract_object_from_response(response):
    """Extrai objeto da resposta, considerando wrapper 'data'"""
    data = response.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        return data["data"]
    return data


def _datatable_to_dict(datatable):
    """Converte datatable (lista de listas) para lista de dicts"""
    if not datatable:
        return []
    
    # Primeira linha são os headers
    headers = datatable[0]
    result = []
    
    # Demais linhas são os dados
    for row in datatable[1:]:
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(row):
                row_dict[header] = row[i]
        result.append(row_dict)
    
    return result


# Em seguida, passos de verificação (Then)
# ====================================================

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(status_code: int, response):
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


@then('a resposta deve ser um objeto `JSON`')
def check_json_object(response):
    data = _extract_object_from_response(response)
    assert isinstance(data, dict)


@then(parsers.cfparse('o objeto deve ter os campos "{fields}"'))
def check_object_fields(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    data = _extract_object_from_response(response)
    for f in expected_fields:
        assert f in data


@then(parsers.cfparse('o objeto deve os campos "{fields}"'))
def check_object_fields_typo(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    data = _extract_object_from_response(response)
    for f in expected_fields:
        assert f in data


@then('a resposta deve ser um objeto com os seguintes valores:')
def check_object_values(response, datatable):
    data = _extract_object_from_response(response)
    # Converter tabela para lista de dicionários
    rows = _datatable_to_dict(datatable)
    
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        
        # Comparar com base no tipo de actual_value
        if isinstance(actual_value, bool):
            expected_bool = valor.lower() in ['true', '1', 'yes']
            assert actual_value == expected_bool, f"Campo {campo}: esperado {expected_bool}, obtido {actual_value}"
        elif isinstance(actual_value, int):
            expected_int = int(valor)
            assert actual_value == expected_int, f"Campo {campo}: esperado {expected_int}, obtido {actual_value}"
        else:
            # Comparação de string (remover aspas se presentes)
            expected_str = valor.strip('"')
            assert str(actual_value) == expected_str, f"Campo {campo}: esperado '{expected_str}', obtido '{actual_value}'"


@then('a resposta deve ser um objeto com os seguinte valor:')
def check_object_value(response, datatable):
    data = _extract_object_from_response(response)
    rows = _datatable_to_dict(datatable)
    
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        expected_str = valor.strip('"')
        assert str(actual_value) == expected_str


@then('a resposta deve conter a seguinte música com um array de objetos com os seguintes valores:')
def check_response_contains_song(response, datatable):
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    song = data[0]  #  Supondo o primeiro
    
    rows = _datatable_to_dict(datatable)
    
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = song.get(campo)
        
        # Comparar com base no tipo de actual_value
        if isinstance(actual_value, bool):
            expected_bool = valor.lower() in ['true', '1', 'yes']
            assert actual_value == expected_bool, f"Campo {campo}: esperado {expected_bool}, obtido {actual_value}"
        elif isinstance(actual_value, int):
            expected_int = int(valor)
            assert actual_value == expected_int, f"Campo {campo}: esperado {expected_int}, obtido {actual_value}"
        else:
            # Comparação de string (remover aspas se presentes)
            expected_str = valor.strip('"')
            assert str(actual_value) == expected_str, f"Campo {campo}: esperado '{expected_str}', obtido '{actual_value}'"



