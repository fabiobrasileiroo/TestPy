import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../jose-cities/features/cities.feature")

# -----------------
# GIVEN
# -----------------

@given(parsers.cfparse('que a url base da API é "{base_url}"'), target_fixture="base_url")
def base_url(base_url):
    return base_url

@given(parsers.cfparse('existe um id de cidade "{city_id}"'), target_fixture="city_id")
def city_id(city_id):
    return city_id


# -----------------
# WHEN
# -----------------

@when(parsers.cfparse('eu fizer uma requisição GET para "{path}"'), target_fixture="response")
def send_get(base_url, path):
    url = base_url + path
    resp = requests.get(url)
    print("URL:", url)
    print("Response:", resp.text)
    return resp


# -----------------
# THEN
# -----------------

@then(parsers.cfparse('o código de status da resposta deve ser {status:d}'))
def check_status(response, status):
    assert response.status_code == status


@then(parsers.cfparse('o JSON deve conter "{field}"'))
def check_json_field(response, field):
    body = response.json()
    assert field in body or field in body.get("data", {})


@then(parsers.cfparse('cada feature deve ter os campos "{fields}"'))
def check_feature_fields(response, fields):
    body = response.json()
    features = body.get("features", [])

    assert isinstance(features, list), "features deve ser uma lista"

    expected = [f.strip() for f in fields.split(",")]

    for feat in features:
        for f in expected:
            assert f in feat, f"Campo {f} não encontrado"


@then(parsers.cfparse('dentro de data as propriedades devem ter "{fields}"'))
def check_properties_fields(response, fields):
    body = response.json()
    props = body["data"]["properties"]
    expected = [f.strip() for f in fields.split(",")]

    for f in expected:
        assert f in props, f"Propriedade {f} não encontrada"
