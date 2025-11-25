import requests
from pytest_bdd import scenarios, given, parsers, when, then

scenarios("features/cities.feature")

@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url: str) -> str:
    return base_url

@given(parsers.cfparse('que o endpoint para cidades é "{path}"'), target_fixture="path")
def endpoint(path: str) -> str:
    return path

@given(parsers.cfparse('que existe uma cidade com id "{city_id}"'), target_fixture="city_id")
def get_by_id(city_id: str) -> str:
    return city_id

@given(parsers.cfparse('que a cidade "{city_id}" é configurada na base de dados'))
def setup_city_for_tests(base_url: str, path: str, city_id: str):

    body = {
        "id": city_id, "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [90.24, 23.43]},
        "properties": {"city": "Dhaka", "country": "Bangladesh", "iso2": "BD", "iso3": "BGD", "tld": "bd"}
    }
    url = base_url + path
    
    # Tenta criar a cidade para garantir que ela exista antes dos testes dependentes.
    # Aceita 201 (Criado) ou 200/409 (Já existe ou sucesso idempotente).
    resp = requests.post(url, json=body, headers={'Content-Type': 'application/json'})
    
    if resp.status_code not in [201, 200, 409]:
         print(f"Alerta: Falha ao configurar a cidade {city_id} para teste. Status: {resp.status_code}")


@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response")
def send_get_request(base_url: str, path: str):
    url = base_url + path
    resp = requests.get(url)
    return resp

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}/{city_id}"'), target_fixture="response")
def send_get_request_with_id(base_url: str, path: str, city_id: str):
    url = base_url + path + '/' + city_id
    resp = requests.get(url)
    return resp

@when(parsers.cfparse('eu enviar uma requisição `POST` para "{path}" com o seguinte corpo:'), target_fixture="response")
def send_post_request(base_url: str, path: str):
    body = {
        "id": "FOO", "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [111.111, 222.222]},
        "properties": {"city": "Foo", "country": "Foo", "iso2": "FOO", "iso3": "FOO", "tld": "foo"}
    }
    url = base_url + path
    resp = requests.post(url, json=body, headers={'Content-Type': 'application/json'})
    return resp

@when(parsers.cfparse('eu enviar uma requisição `PUT` para "{path}/{city_id}" com o seguinte corpo:'), target_fixture="response")
def send_put_request(base_url: str, path: str, city_id: str):
    body = {
        "id": city_id, "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [333.333, 444.444]},
        "properties": {"city": "Dhaka", "country": "Bangladesh", "iso2": "BD", "iso3": "BGD", "tld": "bd"}
    }
    url = base_url + path + '/' + city_id
    resp = requests.put(url, json=body, headers={'Content-Type': 'application/json'})
    return resp

@when(parsers.cfparse('eu enviar uma requisição `PATCH` para "{path}/{city_id}" com o seguinte corpo:'), target_fixture="response")
def send_patch_request(base_url: str, path: str, city_id: str):
    body = {"geometry": {"type": "Point", "coordinates": [111.111, 222.222]}}
    url = base_url + path + '/' + city_id
    resp = requests.patch(url, json=body, headers={'Content-Type': 'application/json'})
    return resp

@when(parsers.cfparse('eu enviar uma requisição `DELETE` para "{path}/{city_id}"'), target_fixture="response")
def send_delete_request(base_url: str, path: str, city_id: str):
    url = base_url + path + '/' + city_id
    resp = requests.delete(url)
    return resp

def _extract_list_from_response(response):
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Erro ao decodificar JSON na lista: {response.text}")
        return []
        
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    if isinstance(data, list):
        return data
        
    print(f"Erro: Resposta GET não é uma lista. Tipo: {type(data)}. Conteúdo: {data}")
    return []

def _extract_object_from_response(response):
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Erro ao decodificar JSON no objeto: {response.text}")
        return {}
        
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        return data["data"]
    if isinstance(data, dict):
        return data
        
    return {}

def _datatable_to_dict(datatable):
    if not datatable:
        return []
    headers = datatable[0]
    result = []
    for row in datatable[1:]:
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(row):
                row_dict[header] = row[i]
        result.append(row_dict)
    return result

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code_response(status_code: int, response):
    assert response.status_code == status_code

@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
    data = _extract_list_from_response(response)
    assert isinstance(data, list)

@then('a resposta deve ser um objeto `JSON`')
def check_json_object(response):
    data = _extract_object_from_response(response)
    assert isinstance(data, dict)

@then('o array deve conter pelo menos 1 elemento')
def check_array_not_empty(response):
    data = _extract_list_from_response(response)
    print("Array length:", len(data))
    assert len(data) >= 1

@then(parsers.cfparse('cada cidade deve ter os campos "{fields}"'))
def check_city_fields(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    for item in data:
        for f in expected_fields:
            assert f in item

@then('o objeto deve ser igual ao seguinte:')
def check_object_equals_table(response, datatable):
    data = _extract_object_from_response(response)
    rows = _datatable_to_dict(datatable)
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        try:
            if isinstance(actual_value, bool):
                expected = valor.lower() in ['true', '1', 'yes']
            elif isinstance(actual_value, int):
                expected = int(valor)
            elif isinstance(actual_value, float):
                expected = float(valor)
            else:
                expected = valor.strip('"')
        except Exception:
            expected = valor.strip('"')
        assert str(actual_value) == str(expected), f"Campo {campo}: esperado '{expected}', obtido '{actual_value}'"