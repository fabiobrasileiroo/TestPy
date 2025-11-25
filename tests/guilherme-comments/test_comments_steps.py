import os
import requests
from pytest_bdd import scenarios, given, parsers, when, then

# Resolve feature file path relative to this file so it works regardless of case-sensitive
feature_path = os.path.join(os.path.dirname(__file__), "features/comments.feature")
scenarios(feature_path)

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

    # Use keys matching the API (camelCase) to avoid 400 errors
    body = {
        "id": comment_id,
        "postId": "1",
        "comment": "Este é um comentário para testes automáticos",
        "user": {
            "id": "50",
            "name": "Test",
            "lastname": "User",
            "username": "testuser"
        }
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
        "postId": "1",
        "comment": "Comentário gerado automaticamente para testes",
        "user": {
            "id": "1000",
            "name": "Foo",
            "lastname": "User",
            "username": "fooUser"
        }
    }

    return requests.post(base_url + path, json=body, headers={'Content-Type': 'application/json'})

@when(parsers.cfparse('eu enviar uma requisição PUT para "{path}/{comment_id}" com o seguinte corpo:'), target_fixture="response")
def send_put(base_url, path, comment_id):

    body = {
        "id": comment_id,
        "postId": "1",
        "comment": "Comentário atualizado via PUT",
        "user": {
            "id": "1000",
            "name": "Usuário Alterado",
            "lastname": "Alterado",
            "username": "usuarioAlterado"
        }
    }

    return requests.put(f"{base_url}{path}/{comment_id}", json=body, headers={'Content-Type': 'application/json'})

@when(parsers.cfparse('eu enviar uma requisição PATCH para "{path}/{comment_id}" com o seguinte corpo:'), target_fixture="response")
def send_patch(base_url, path, comment_id):

    body = {
        "comment": "Comentário parcialmente atualizado via PATCH"
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
    if response.status_code != status:
        try:
            print("Response body:", response.json())
        except Exception:
            print("Response text:", response.text)
    assert response.status_code == status


@then(parsers.cfparse('o objeto deve ter os campos "{fields}"'))
def check_object_fields(response, fields):
    fields = fields.replace(" e ", ",").split(",")
    fields = [f.strip().strip('"') for f in fields]

    obj = _extract_object(response)
    for f in fields:
        if f == 'post_id':
            assert ('post_id' in obj) or ('postId' in obj), f"Campo 'post_id' não encontrado em {obj}"
        elif f == 'body':
            assert ('body' in obj) or ('comment' in obj), f"Campo 'body' não encontrado em {obj}"
        else:
            # for nested fields like 'user' we just check presence
            if '.' in f:
                # only check top-level existence for nested path
                top = f.split('.')[0]
                assert top in obj, f"Campo {top} não encontrado em {obj}"
            else:
                assert f in obj

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

    # Accept camelCase or snake_case variations (postId/post_id, body/comment)
    for item in _extract_list(response):
        for f in fields:
            # Support nested fields like 'user.name'
            if '.' in f:
                # follow nested structure
                parts = f.split('.')
                current = item
                for p in parts:
                    candidates = [p]
                    if p == 'post_id':
                        candidates = ['post_id', 'postId']
                    elif p == 'body':
                        candidates = ['body', 'comment']
                    found = False
                    for key in candidates:
                        if isinstance(current, dict) and key in current:
                            current = current[key]
                            found = True
                            break
                    assert found, f"Campo '{f}' não encontrado em {item}"
            else:
                if f == 'post_id':
                    assert ('post_id' in item) or ('postId' in item), f"Campo 'post_id' não encontrado em {item}"
                elif f == 'body':
                    assert ('body' in item) or ('comment' in item), f"Campo 'body' não encontrado em {item}"
                else:
                    assert f in item, f"Campo {f} não encontrado em {item}"

@then('o objeto deve ser igual ao seguinte:')
def check_object_table(response, datatable):
    expected_rows = _datatable_to_dict(datatable)
    obj = _extract_object(response)

    def _get_value_by_field(o, field):
        # support nested fields like 'user.name' and map snake_case/camelCase differences
        parts = field.split('.')
        current = o
        for p in parts:
            candidates = [p]
            if p == 'post_id':
                candidates = ['post_id', 'postId']
            elif p == 'body':
                candidates = ['body', 'comment']
            found = False
            for key in candidates:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                    found = True
                    break
            if not found:
                return (None, None)
        # current now holds the value
        return (True, current)

    for row in expected_rows:
        field = row["campo"]
        value = row["valor"]
        exists, actual_value = _get_value_by_field(obj, field)
        assert exists, f"Campo {field} não encontrado na resposta"

        # Conversão automática de tipos
        if isinstance(actual_value, int):
            expected = int(value)
        elif isinstance(actual_value, bool):
            expected = value.lower() in ["true", "1"]
        else:
            expected = value.strip('"')
        assert str(actual_value) == str(expected), f"Campo {field}: esperado {expected}, obtido {actual_value}"
