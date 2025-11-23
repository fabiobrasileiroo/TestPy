import requests
from pytest_bdd import scenarios, given, parsers, when, then

scenarios("features/products.feature")

@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url: str) -> str:
    return base_url

@given(parsers.cfparse('que o endpoint para listar produtos é "{path}"'), target_fixture="path")
def endpoint(path: str) -> str:
    return path

@given(parsers.cfparse('que existe um produto com id "{id}"'),target_fixture="id")
def get_by_id(id:str) -> str:
   return id    

# 1. Listar todos os produtos

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'), target_fixture="response")   
def send_get_request(base_url:str, path: str):
    url = base_url + path
    resp = requests.get(url)
    return resp

# 2. Listar produto por ID

@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}/{id}"'), target_fixture="response")
def send_get_request_with_id(base_url:str, path: str, id: str):
    url = base_url + path + '/' + id
    resp = requests.get(url)
    return resp

# 3. Criar produto
@when(parsers.cfparse('eu enviar uma requisição `POST` para "{path}" com o seguinte corpo:'), target_fixture="response")
def send_post_request(base_url: str, path: str):
    body = {
        "title": "Foo title",
        "description": "Foo desc",
        "brand": "Foo Brand",
        "category": "Fooooooo",
        "price": 19.2,
        "rating": 2.5,
        "stock": 13
    }
    url = base_url + path
    resp = requests.post(url, json=body)
    return resp

# 4. Atualizar produto
@when(parsers.cfparse('eu enviar uma requisição `PUT` para "{path}/{id}" com o seguinte corpo:'), target_fixture="response")
def send_put_request(base_url: str, path: str, id: str):
    body = {
        "title": "Footitle",
        "description": "Foodesc",
        "brand": "FooBrand",
        "category": "Fooooooo",
        "price": 19.2,
        "rating": 2.5,
        "stock": 13
    }
    url = base_url + path + '/' + id
    resp = requests.put(url, json=body)
    return resp

# 5. Atualizar parcialmente produto
@when(parsers.cfparse('eu enviar uma requisição `PATCH` para "{path}/{id}" com o seguinte corpo:'), target_fixture="response")
def send_patch_request(base_url: str, path: str, id: str):
    body = {
        "price": 25.5,
        "stock": 20
    }
    url = base_url + path + '/' + id
    resp = requests.patch(url, json=body)
    return resp

# 6. Deletar produto
@when(parsers.cfparse('eu enviar uma requisição `DELETE` para "{path}/{id}"'), target_fixture="response")
def send_delete_request(base_url: str, path: str, id: str):
    url = base_url + path + '/' + id
    resp = requests.delete(url)
    return resp

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
def check_status_code_response(status_code: int, response):
    assert response.status_code == status_code

@then(parsers.cfparse('o código de status deve ser {status_code:d}'))
def check_status_code_alt(status_code: int, response):
    assert response.status_code == status_code

@then('o objeto deve ser igual ao seguinte:')
def check_object_equals_table(response, datatable):
    data = _extract_object_from_response(response)
    rows = _datatable_to_dict(datatable)
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        # Tenta converter para int/float/bool se possível
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

@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
    # print_response_body(response)
    data = _extract_list_from_response(response)
    assert isinstance(data, list)

@then('o array deve conter pelo menos 1 produto')
def check_array_not_empty(response):
    data = _extract_list_from_response(response)
    print("Array length:", len(data))
    assert len(data) >= 1

@then(parsers.cfparse('cada produto deve ter os campos "{fields}"'))
def check_product_fields(response, fields):
    fields_clean = fields.replace(' e ', ',')
    expected_fields = [f.strip().strip('"') for f in fields_clean.split(',') if f.strip()]
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    for product in data:
        for f in expected_fields:
            assert f in product

@then('a resposta deve ser um objeto `JSON`')
def check_json_object(response):
    data = _extract_object_from_response(response)
    assert isinstance(data, dict)

@then('a resposta dessa requisição deve ser um objeto `JSON`')
def check_json_object_alt(response):
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
    rows = _datatable_to_dict(datatable)
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        if isinstance(actual_value, bool):
            expected_bool = valor.lower() in ['true', '1', 'yes']
            assert actual_value == expected_bool, f"Campo {campo}: esperado {expected_bool}, obtido {actual_value}"
        elif isinstance(actual_value, int):
            expected_int = int(valor)
            assert actual_value == expected_int, f"Campo {campo}: esperado {expected_int}, obtido {actual_value}"
        elif isinstance(actual_value, float):
            expected_float = float(valor)
            assert actual_value == expected_float, f"Campo {campo}: esperado {expected_float}, obtido {actual_value}"
        else:
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

@then('a resposta deve conter o seguinte produto com um array de objetos com os seguintes valores:')
def check_response_contains_product(response, datatable):
    data = _extract_list_from_response(response)
    assert isinstance(data, list) and data
    product = data[0]  # Supondo o primeiro
    rows = _datatable_to_dict(datatable)
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = product.get(campo)
        if isinstance(actual_value, bool):
            expected_bool = valor.lower() in ['true', '1', 'yes']
            assert actual_value == expected_bool, f"Campo {campo}: esperado {expected_bool}, obtido {actual_value}"
        elif isinstance(actual_value, int):
            expected_int = int(valor)
            assert actual_value == expected_int, f"Campo {campo}: esperado {expected_int}, obtido {actual_value}"
        elif isinstance(actual_value, float):
            expected_float = float(valor)
            assert actual_value == expected_float, f"Campo {campo}: esperado {expected_float}, obtido {actual_value}"
        else:
            expected_str = valor.strip('"')
            assert str(actual_value) == expected_str, f"Campo {campo}: esperado '{expected_str}', obtido '{actual_value}'"

@then('a resposta deve ser um objeto com os seguinte valores:')
def check_object_values_typo(response, datatable):
    data = _extract_object_from_response(response)
    rows = _datatable_to_dict(datatable)
    for row in rows:
        campo = row['campo']
        valor = row['valor']
        actual_value = data.get(campo)
        expected_str = valor.strip('"')
        assert str(actual_value) == expected_str

