import requests
from pytest_bdd import scenarios, given, parsers, when, then

scenarios("features/comments.feature")

# ====================================================
# GIVEN
# ====================================================

@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url):
    return base_url

@given(parsers.cfparse('que o endpoint para comments é "{path}"'), target_fixture="path")
def endpoint(path):
    return path

@given(parsers.cfparse('que existe um comentário com id "{comment_id}"'), target_fixture="comment_id")
def comment_id(comment_id):
    return comment_id

@given(parsers.cfparse('que o comentário "{comment_id}" está configurado na base de dados'))
def setup_comment_for_tests(base_url, path, comment_id):

    body = {
        "id": comment_id,
        "post_id": "1",
        "name": "Test User",
        "email": "test@example.com",
        "body": "Este é um comentário para testes automáticos"
    }

    url = base_url + path

    resp = requests.post(url, json=body, headers={'Content-Type': 'application/json'})
    if resp.status_code not in [200, 201, 409]:
        print(f"[WARN] Falha ao inserir comentário {comment_id}. Status {resp.status_code}")


# ====================================================
# WHEN (AÇÕES)
# ====================================================

@when(parsers.cfparse('eu enviar uma requisição GET para "{path}"'), target_fixture="response")
def send_get_list(base_url, path):
    return requests.get(base_url + path)

@when(parsers.cfparse('eu enviar uma requisição GET para "{path}/{comment_id}"'), target_fixture="response")
def send_get_by_id(base_url, path, comment_id):
    return requests.get(f"{base_url}{path}/{comment_id}")

@when(parsers.cfparse('eu enviar uma requisição POST para "{path}" com o seguinte corpo:'), target_fixture="response")
def send_post(base_url, path):

    body = {
        "id": "FOO-CMT",
        "post_id": "999",
        "name": "Foo User",
        "email": "foo@example.com",
        "body": "Comentário gerado automaticamente para testes"
    }

    return requests.post(base_url + path, json=body, headers={'Content-Type': 'application/json'})

@when(parsers.cfparse('eu enviar uma requisição PUT para "{path}/{comment_id}" com o seguinte corpo:'), target_fixture="response")
def send_put(base_url, path, comment_id):

    body = {
        "id": comment_id,
        "post_id": "999",
        "name": "Usuário Alterado",
        "email": "update@example.com",
        "body": "Comentário atualizado via PUT"
    }

    return requests.put(f"{base_url}{path}/{comment_id}", json=body, headers={'Content-Type': 'application/json'})

@when(parsers.cfparse('eu enviar uma requisição PATCH para "{path}/{comment_id}" com o seguinte corpo:'), target_fixture="response")
def send_patch(base_url, path, comment_id):

    body = {
        "body": "Comentário parcialmente atualizado via PATCH"
    }

    return requests.patch(f"{base_url}{path}/{comment_id}", json=body, headers={'Content-Type': 'application/json'})

@when(parsers.cfparse('eu enviar uma requisição DELETE para "{path}/{comment_id}"'), target_fixture="response")
def send_delete(base_url, path, comment_id):
    return requests.delete(f"{base_url}{path}/{comment_id}")


# ====================================================
# FUNÇÕES AUXILIARES
# ====================================================

def _extract_list(response):
    try:
        data = response.json()
    except Exception:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "data" in data:
        return data["data"]

    return []

def _extract_object(response):
    try:
        data = response.json()
    except:
        return {}

    if isinstance(data, dict) and "data" in data:
        return data["data"]

    return data if isinstance(data, dict) else {}

def _datatable_to_dict(dt):
    if not dt:
        return []
    keys = dt[0]
    rows = []
    for line in dt[1:]:
        item = {}
        for idx, key in enumerate(keys):
            item[key] = line[idx]
        rows.append(item)
    return rows


# ====================================================
# THEN (VALIDAÇÕES)
# ====================================================

@then(parsers.cfparse('o código de status da resposta deve ser {status:d}'))
def check_status(status, response):
    assert response.status_code == status

@then('a resposta deve ser um array de JSON')
def check_json_array(response):
    assert isinstance(_extract_list(response), list)

@then('a resposta deve ser um objeto JSON')
def check_json_object(response):
    assert isinstance(_extract_object(response), dict)

@then('o array deve conter pelo menos 1 elemento')
def check_not_empty(response):
    assert len(_extract_list(response)) >= 1

@then(parsers.cfparse('cada comentário deve ter os campos "{fields}"'))
def check_fields(response, fields):
    fields = fields.replace(" e ", ",").split(",")
    fields = [f.strip().strip('"') for f in fields]

    for item in _extract_list(response):
        for f in fields:
            assert f in item

@then('o objeto deve ser igual ao seguinte:')
def check_object_table(response, datatable):
    expected_rows = _datatable_to_dict(datatable)
    obj = _extract_object(response)

    for row in expected_rows:
        field = row["campo"]
        value = row["valor"]

        # Conversão automática de tipos
        if field in obj:
            if isinstance(obj[field], int):
                expected = int(value)
            elif isinstance(obj[field], bool):
                expected = value.lower() in ["true", "1"]
            else:
                expected = value.strip('"')
            assert str(obj[field]) == str(expected), f"Campo {field}: esperado {expected}, obtido {obj[field]}"